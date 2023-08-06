import functools

import numpy as np

from ..utils.constants import LOGConstants, TestConstants, JsonConstants
import copy

class BinoutData(object):

    def __init__(self, binout, logger, dynasaur_definitions, name):
        """
        Initialization/constructor

        :param: binout
        :param: logger
        :param: dynasaur definition
        :param: name (binout name)

        :return:
        """

        self._binout = binout
        self._logger = logger
        self._dynasaur_definitions = dynasaur_definitions
        self._name = name
        self._time = None
        self._time_interp = None
        self._data = {}
        self._ids = None

        self._defined_types = []
        self._set_defined_types(self._dynasaur_definitions)
        self._clean_defined_types()
        self._check_for_id_in_binout()

    def get_time(self):
        """
        :return: time array
        """
        return self._time

    def get_interpolated_time(self):
        """
        :return: interpolated time array
        """
        return self._time_interp

    def get_channels_ids_object_name(self, object_name, plugin_name):
        """
        :return: time array
        """
        return self._dynasaur_definitions.get_ids_from_name(object_name, self._name, plugin_name)

    def get_ids(self):
        """
        :return: ids as numpy  int array
        """
        return self._ids.astype(np.uint32)

    def _interp_time(self, time_):
        """
        inteprolate time to decimal values
        :param time_:
        :return: inteprolated time vector
        """

        if self._dynasaur_definitions.get_units().second() == 1000:  # means ms
            end_time_ = np.round(time_[-1] - time_[0])  # assumed ms
            assert (time_[0] < 0.02)
        elif self._dynasaur_definitions.get_units().second() == 1:  # means s
            end_time_ = np.round(time_[-1] - time_[0], 3)
            # TODO: make assert even if the condition satisfied
            # assert (time_[0] < 0.00001)
        else:
            assert False

        # check if the time_diff is already constant:
        # https://stackoverflow.com/questions/3844801/check-if-all-elements-in-a-list-are-identical
        # https://numpy.org/doc/stable/reference/generated/numpy.allclose.html
        time_diff = np.diff(time_)
        if (np.allclose(time_diff, np.tile([time_diff[0]], len(time_diff)))):
            return time_

        time_interp = np.linspace(time_[0], end_time_, len(time_))
        return time_interp

    def _read_data_types(self, elem_name=None):
        """
        :param elem_name:

        initialized data types
        """
        data = {}
        args_ = [self._name, elem_name] if elem_name is not None else [self._name]

        array = []
        insert_indices = np.array([], dtype=int)
        ind = np.array([], dtype=int)

        # check if type_data has to be extended due to deleted elements
        args_temp = args_ + [self.ids_name]
        ids = self._binout.read(*args_temp)

        len_indices = 0

        # check if elements have been destroyed
        if isinstance(ids[0], tuple):
            for i in range(0, ids.shape[0]):
                logic_intersection = np.in1d(ids[0], ids[i])
                array.append(np.where(np.logical_not(logic_intersection)))
                indices = np.where(np.logical_not(logic_intersection))
                if indices[0].size != 0:
                    insert_indices = np.append(insert_indices, indices[0] + len(ids[0]) * i - np.arange(len_indices,
                                                                                                        len_indices + len(
                                                                                                            indices[
                                                                                                                0])))
                    ind = np.append(ind, indices[0] + len(ids[0]) * i)
                    len_indices += len(indices[0])

        available_channels = [value for value in self.__class__.DATA_CHANNEL_TYPES if
                              value in self._binout.read(*args_)]

        for key in available_channels:
            args_temp = args_ + [key]
            type_data = self._binout.read(*args_temp)

            if type_data.shape[0] == 0:
                continue

            # check if all ids "survived"
            if len(type_data.shape) == 1:
                if not isinstance(type_data[0], tuple):  # case if only one data point available
                    type_data = type_data[:self._time_interp.shape[0]].reshape(-1, 1)
            else:
                type_data = type_data[:self._time_interp.shape[0], :]

            if len(insert_indices) != 0:  # Deleted elements should only be possible for elements
                assert (self._name == "elout")
                flatted_data_array = list(sum(type_data, ()))

                zeros = np.zeros(len(insert_indices))
                a = np.insert(flatted_data_array, insert_indices, zeros).reshape((-1, 1)),

                # shape: [time]:[element id, part id, integration point]:[lambda1, lambda2, lambda3]
                #       TODO
                # e.g.: 7 time steps, 3 parts, each part 2 elements with 2 integration points, 3 eigenvalues
                # e.g.: results in shape of (7, 12, 3)
                # data_tensor = a.reshape(time_step_size, int(a.shape[0] / time_step_size), w_stress.shape[1])
                type_data = np.reshape(a[0], (self._time_interp.shape[0], -1))

            # type_data = np.reshape(type_data, (time_interp.shape[0], -1))
            data_interp = np.zeros(shape=(self._time_interp.shape[0], type_data.shape[1]))
            for i in range(type_data.shape[1]):
                data_interp[:, i] = np.interp(self._time_interp,
                                              self._time[:self._time_interp.shape[0]], type_data[:, i])
            data[key] = data_interp

        self._data = {**self._data, **data}

    def __init_data__(self, elem_name=None):
        """
        initialized
        :param elem_name:  only necessary for LS-dyna elout data
        """
        if elem_name is not None:
            self._time = self._binout.read(self._name, elem_name, 'time').flatten()
            self._time_interp = self._interp_time(self._time)
            self._ids = np.array(self._binout.read(self._name, elem_name, self.__class__.ids_name)[0])
            self._read_data_types(elem_name=elem_name)
        else:
            self._time = self._binout.read(self._name, 'time').flatten()
            self._time_interp = self._interp_time(self._time)
            # TODO: Check if data is not there index out of range -> resulting crash
            self._ids = np.array(self._binout.read(self._name, self.__class__.ids_name))
            self._read_data_types()

        assert (len(self._ids.shape) == 1)

    def _set_defined_types(self, dynasaur_definitions):
        """
        set defined types
        :param dynasaur definitions
        """
        for def_key in dynasaur_definitions.__dict__:
            if def_key == "_criteria":
                for key in dynasaur_definitions.__dict__[def_key].keys():
                    self._get_data_from_json(dynasaur_definitions.__dict__[def_key][key])
            if def_key == "_data_vis":
                for key in dynasaur_definitions.__dict__[def_key].keys():
                    self._get_data_from_json(dynasaur_definitions.__dict__[def_key][key]["x"])
                    self._get_data_from_json(dynasaur_definitions.__dict__[def_key][key]["y"])

    def _get_data_from_json(self, json_object):
        """
        recursive function
        inner part of the json object can be :
            * value
            * strain_stress
            * array
        """
        if 'function' in json_object.keys():  # expected name and params
            parameter_def = json_object['function']['param']
            for key in parameter_def.keys():
                if type(parameter_def[key]) is dict:  # step into recursion
                    self._get_data_from_json(parameter_def[key])


        else:  # data to obtain
            if "value" in json_object.keys():
                return
            elif "strain_stress" in json_object.keys():
                return
            elif "array" in json_object.keys():
                self._defined_types.append(json_object['array'])
                return
            else:
                print(json_object)
                assert False

    def _clean_defined_types(self):
        """
        clean defined types
        :param:
        """
        _list_temp = []
        for array_temp in self._defined_types:
            for type in array_temp:
                type = type.replace("(", "")
                type = type.replace(")", "")
                first_type = type.split(",")[0]
                second_type = type.split(",")[1]
                second_type = second_type.replace(" ", "")
                if first_type == "0" and second_type != "0":
                    if second_type in self.DATA_CHANNEL_TYPES:
                        _list_temp.append(second_type)
                elif first_type != "0" and second_type == '0':
                    if first_type in self.DATA_CHANNEL_TYPES:
                        _list_temp.append(first_type)
                else:
                    if first_type in self.DATA_CHANNEL_TYPES:
                        _list_temp.append(first_type)
                    if second_type in self.DATA_CHANNEL_TYPES:
                        _list_temp.append(second_type)
        self._defined_types = set(_list_temp)

    def read_binout_data(self):
        """
        :return: reading success (True when data was read in, False when no data available)
        """
        # data already read
        if self._ids is not None:
            return True

        # i.e.  no rcforc in binout
        if self._name not in self._binout.read():
            self._logger.emit(LOGConstants.ERROR[0], "no " + self._name + " data in binout")
            return False

        # data read
        self._logger.emit(LOGConstants.READ_BINOUT[0], 'read ' + self._name + ' data ...')

        elements = self._binout.read(self._name)
        elem_name = None
        if self._name == "elout":
            elem_name = "beam"
            elements = self._binout.read(self._name, elem_name)

        # check if required data is available (defined in SBTout.__DATA_CHANNEL_TYPES__)
        if not self._check_negative_intersection(elements):
            return False

        self.__init_data__(elem_name)
        self._logger.emit(LOGConstants.READ_BINOUT[0], "done reading " + self._name + "!")

        return True

    def _check_for_id_in_binout(self):
        """
        check if defined id is in binout
        :return:
        """
        return_function = [None]
        if self._name == "secforc":
            return_function = self._check_id_in_binout("_cross_sections")
        elif self._name == "nodout":
            return_function = self._check_id_in_binout("_node")
        elif self._name == "rcforc":
            return_function = self._check_id_in_binout("_contact")
        elif self._name == "deforc":
            return_function = self._check_id_in_binout("_discrete")
        elif self._name == "elout":
            return_function = self._check_id_in_binout("_element")
        elif self._name == "sbtout":
            return_function = self._check_id_in_binout("_seatbelt")
        elif self._name == "matsum":
            return_function = self._check_id_in_binout("_energy_part")
        elif self._name == "disbout":
            return_function = self._check_id_in_binout("_disbout")
        elif self._name == "disbout_part":
            return_function = self._check_id_in_binout("_disbout_part")
        elif self._name == "glstat":
            return_function = self._check_id_in_binout("_energy_global")
        elif self._name == "abstat":
            return_function = self._check_id_in_binout("_abstat")
        if not return_function[0]:
            self._logger.emit(LOGConstants.WARNING[0], "Not valid ID: " + return_function[1] +
                              ". Plese check your def file!")

    def _check_id_in_binout(self, binout_name):
        """
        :param: binout name

        :return: True or False
        """
        # TODO: Maybe check if the key is 0(null)
        if binout_name == "_energy_global":
            return True, "temp"
        ids_list = []
        dyn_def_key = getattr(self._dynasaur_definitions, binout_name)
        if len(dyn_def_key) == 0:
            return True, "temp"
        if self._name == "elout":
            return True, "temp"
            # keys = self._binout.read(self._name)
            # ids_list = np.concatenate([self._binout.read(self._name, elem_name, "ids")[0] if elem_name != "solid" else
            #                           self._binout.read(self._name, elem_name, "ids") for elem_name in keys])
        else:
            ids_list = self._binout.read(self._name, "ids")

        for sec in dyn_def_key:
            temp_list = list(
                map(functools.partial(BinoutData.map_help_function, binout_name, ids_list), dyn_def_key[sec]))

            if len(temp_list) == 0:
                return False, sec
            dyn_def_key[sec] = [tmp for tmp in temp_list if tmp != None].copy()
        return True, "temp"

    @staticmethod
    def map_help_function(binout_name, ids_list, id_):
        """

        :param binout_name:
        :param ids_list:
        :param id_:
        :return:
        """
        if binout_name == TestConstants.CONTACT:
            master_slave = id_[-1]
            id_for_loop = int(id_[:-1])

            if id_for_loop in ids_list:
                return str(id_for_loop) + master_slave
        elif id_ in ids_list:
            return id_

    def _check_negative_intersection(self, elements):
        """
        :param: elements

        :return: True or False
        """
        # only necessary functions
        negative_intersection = [val for val in self._defined_types if val not in elements]
        if len(negative_intersection) != 0:
            self._logger.emit(LOGConstants.WARNING[0], "binout keys: " + " ".join(elements))
            self._logger.emit(LOGConstants.WARNING[0],
                              "Your definition file tries to access the following undefined keys : " + " ".join(negative_intersection))
        return True

    def get_data_of_defined_json(self, json_object, data_offsets):
        """
        :param: json object
        :param: data offsets

        :return: data array between data offset and date delta t
        """
        ids = self.get_channels_ids_object_name(json_object[JsonConstants.ID_UPPER_CASE], self._name)

        if len(ids) == 0:
            if "ID" in json_object:
                self._logger.emit(LOGConstants.ERROR[0],
                                  "Missing ID in the input data with identifier: " + json_object["ID"])

            return

        data_offset = 0
        data_delta_t = -1
        for (t, offset, delta_t) in data_offsets:
            if t == json_object["type"]:
                data_offset = offset
                data_delta_t = delta_t

        array_definition = json_object[JsonConstants.ARRAY]
        if array_definition[0].split(',')[0].strip(' (') == "all":
            converted_tuples = [(index, array_definition[0].split(',')[1].strip(' )')) for index, id_ in
                                enumerate(ids)]
        else:
            # processing data array
            converted_tuples = [(int(tuple_string.split(',')[0].strip(' (')), tuple_string.split(',')[1].strip(' )'))
                                for tuple_string
                                in array_definition]

        data_array = None
        for tpl in converted_tuples:
            d = copy.copy(self.get_measurement_channel(id_=ids[tpl[0]], channel_name=tpl[1]))
            if len(d) == 0:
                return None
            if tpl[1] == "time":
                d -= d[data_offset, 0]
            data_array = d[data_offset:data_delta_t] if data_array is None else np.append(data_array,
                                                                                          d[data_offset:data_delta_t],
                                                                                          axis=1)

        return data_array

    def get_measurement_channel(self, id_, channel_name):
        """
        returns the interpolated channel,
        Aim: Constant time interval
        :param id:
        :param channel_name:
        :return:
        """
        if channel_name == 'time':
            return self._time_interp.reshape(-1, 1)
        if np.issubdtype(self._ids.dtype, np.number):
            data_index = np.where(int(id_) == self._ids)[0]
        else:  # madymo case ... ids are not numeric
            data_index = np.where(id_ == self._ids)[0]

        if len(data_index) == 0:
            self._logger.emit(LOGConstants.ERROR[0], 'ID ' + str(id_) + ' not in binout')
            exit()

        self._logger.emit(LOGConstants.DATA_PLUGIN[0], 'read id ' + str(id_) + ' from channel name: ' + channel_name)
        assert (len(data_index) >= 1)

        if channel_name not in self._data.keys():
            self._logger.emit(LOGConstants.ERROR[0], str(id_) + ' has no data with the identifier : ' + channel_name)
            return []

        d = self._data[channel_name][:, data_index]

        return d.reshape(-1, len(data_index))
