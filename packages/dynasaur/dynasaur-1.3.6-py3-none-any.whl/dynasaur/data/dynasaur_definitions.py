import time
import json

from ..utils.constants import LOGConstants, DefFileConstants, UnitsConstants, DefinitionConstants, \
    ObjectConstantsForData, JsonConstants, LoggerERROR, LoggerWARNING, PluginsParamDictDef
from ..utils.constants import LoggerReadDynasaurDefinitionFile as LD
from ..data.def_file_validator import TestDefinitionJSON


class Units(object):
    def __init__(self):
        self._time = 1.0  # in seconds
        self._length = 1.0  # in meters
        self._weight = 1.0  # in kilogram
        self.grav_const = 9.81

    def set_time(self, _time):
        self._time = _time

    def set_length(self, length):
        self._length = length

    def set_weight(self, weight):
        self._weight = weight

    def second(self):
        return self._time

    def meter(self):
        return self._length

    def kilogram(self):
        return self._weight


class DefintionObject(object):
    def __init__(self, oid):
        """
        Init function / constructor
        :param oid:
        :return:
        """
        self._oid = oid
        self._parts = {}
        self._elements = {}

    def set_parts(self, part):
        self._parts = part

    def add_part(self, pid):
        self._parts[pid] = pid

    def add_element(self, eid):
        self._elements[eid] = eid

    def get_parts(self):
        return sorted(self._parts)

    def get_element(self):
        return sorted(self._elements)


class DynasaurDefinitions:
    # create the object container
    def __init__(self, logger):
        """
        constructor

        :param logger:
        :return:
        """
        self._title = ''
        self._objects = {}
        self.logger = logger
        self._logger = self.logger
        self._info = []

        # set all class members
        self._cross_sections = {}
        self._node = {}
        self._disbout = {}
        self._part_disbout = {}
        self._contact = {}
        self._discrete = {}
        self._element = {}
        self._seatbelt = {}
        self._energy_part = {}
        self._energy_global = {}
        self._abstat = {}
        self._riskfunction = {DefFileConstants.FUNC_CRITERIA: {},
                              DefFileConstants.FUNC_DATA_VISUALIZATION: {}}

        self._criteria = {}
        self._data_vis = {}
        self._units = Units()

    def get_param_dict_from_command(self, command):
        """
        :param command:
        :return dictionary on the command
        """
        if 'visualization' in command:
            d = command
            d[PluginsParamDictDef.DYNASAUR_JSON] = self.get_data_vis(command['visualization'])
            return d

        elif 'criteria' in command:
            d = command
            d[PluginsParamDictDef.DYNASAUR_JSON] = self.get_criteria(command['criteria'])
            return d
        else:
            print("[ERROR] Command not in command list")
            return

    def get_units(self):
        """
        get units

        :param:
        :return units:
        """
        return self._units

    def get_criteria(self, key):
        """
        get criteria

        :param key:
        :return criteria:
        """
        if key not in self._criteria.keys() or len(self._criteria) == 0:
            self._logger.emit(LOGConstants.ERROR[0], LoggerERROR.print_statements[6] + "\"" + key + "\"")
            exit("Exiting, check your def file")
            return
        return self._criteria[key]

    def get_data_vis(self, key):
        """
        get code

        :param:
        :return code:
        """
        if key not in self._data_vis.keys() or len(self._data_vis) == 0:
            self._logger.emit(LOGConstants.ERROR[0], LoggerERROR.print_statements[7] + "\"" + key + "\"")
            exit("Exiting, check your def file")
        return self._data_vis[key]

    def get_ids_from_name(self, name, data_container, plugin_name):
        """
        get ids from given name

        :param name:
        :param data_container:
        :param plugin_name:
        :return dict(name):
        """
        d = {}
        if data_container == "nodout":
            d = self._node
        elif data_container == "rcforc":
            d = self._contact
        elif data_container == "deforc":
            d = self._discrete
        elif data_container == "elout":
            d = self._element
        elif data_container == "secforc":
            d = self._cross_sections
        elif data_container == "sbtout":
            d = self._seatbelt
        elif data_container == "matsum":
            d = self._energy_part
        elif data_container == "glstat":
            d = self._energy_global
        elif data_container == "disbout":
            d = self._disbout
        elif data_container == "disbout_part":
            d = self._part_disbout
        elif data_container == "abstat":
            d = self._abstat

        if name not in d.keys() or len(d) == 0:
            self._logger.emit(LOGConstants.ERROR[0],
                              "In " + plugin_name + LoggerERROR.print_statements[5] + "\"" + name + "\"")
            time.sleep(.5)
            exit("Exiting, check your def file")

            return

        return d[name]

    def get_defined_objects_containing_parts(self, part_ids):
        """
        get defined object containing parts

        :param part_ids:
        :return list_defined_objects:
        """
        list_defined_objects = []
        for tmp_object_name in sorted(self._objects):
            tmp_part_ids = list(self._objects[tmp_object_name].get_parts())
            intersection = [val for val in tmp_part_ids if val in part_ids]
            if len(intersection) != 0:
                list_defined_objects.append(tmp_object_name)

        if len(list_defined_objects) == 0:
            list_defined_objects.append("")

        return list_defined_objects

    def get_defined_objects_containing_all_parts(self, part_ids):
        """
        get defined object

        :param part_ids:
        :return list_defined_objects:
        """
        list_defined_objects = []
        for tmp_object_name in sorted(self._objects):
            tmp_part_ids = list(self._objects[tmp_object_name].get_parts())
            intersection = [val for val in tmp_part_ids if val in part_ids]
            if len(tmp_part_ids) == len(intersection):
                list_defined_objects.append(tmp_object_name)

        if len(list_defined_objects) == 0:
            list_defined_objects.append("")

        return list_defined_objects

    def define_dynasaur_everything(self, part_ids):
        """
        define dynasaur everything
        :param part_ids:  list of part_ids
        :return:
        """

        # create an Everything object
        name = "Dynasaur Everything"
        self._objects[name] = DefintionObject(name)

        # only store ids not the entire dict would cause side effects
        self._objects[name].set_parts(part_ids)

    def get_all_data_types_from_json(self, d, ls):
        """
        get all data types

        :param d:
        :param ls:
        :return d[TYPE]:
        """

        for key in d.keys():
            if key is None:
                continue
            if isinstance(d[key], dict):
                data_type = self.get_all_data_types_from_json(d[key], ls)
                if data_type is not None and data_type not in ls:
                    if isinstance(data_type, list):
                        for type_ in data_type:
                            ls.append(type_)
                    else:
                        ls.append(data_type)
            elif JsonConstants.TYPE in d.keys():
                return d[JsonConstants.TYPE]

    def get_required_datatypes(self, plugin_name):
        """
        get required datatype

        :param plugin_name:
        :return ls:
        """
        ls = []
        if DefinitionConstants.CRITERIA == plugin_name:
            self.get_all_data_types_from_json(self._criteria, ls)
        elif DefinitionConstants.DATA_VIS == plugin_name:
            self.get_all_data_types_from_json(self._data_vis, ls)
        else:
            assert False
        return ls

    def get_parts_by_object_containing_part_ids(self, tmp_object, part_ids):
        """
        get parts by object containing part ids

        :param tmp_object:
        :param part_ids:
        :return parts by object:
        """
        return [val for val in part_ids if val in self._objects[tmp_object].get_parts()]

    def get_info(self):
        """
        get info

        :param:
        :return info:
        """
        return self._info

    def _set_contact(self, json_object):
        """
        set contact object type

        :param json_object:
        :return:
        """
        name = json_object[JsonConstants.NAME]

        if JsonConstants.ID in json_object:
            self._contact[name] = json_object[JsonConstants.ID]

        if JsonConstants.ID_RANGE in json_object:
            self._contact[name] = [str(i) + json_object[JsonConstants.ID_RANGE][0][-1]
                                   for i in range(int(json_object[JsonConstants.ID_RANGE][0][:-1]),
                                                  int(json_object[JsonConstants.ID_RANGE][-1][:-1]) + 1)]

    def _set_datacontainer_defintion(self, json_object, def_container):
        name = json_object[JsonConstants.NAME]

        if JsonConstants.ID in json_object:
            def_container[name] = json_object[JsonConstants.ID]

        if JsonConstants.ID_RANGE in json_object:
            def_container[name] = [i for i in range(json_object[JsonConstants.ID_RANGE][0],
                                                    json_object[JsonConstants.ID_RANGE][-1] + 1)]

        if JsonConstants.PART_ID in json_object:
            def_container[name] = json_object[JsonConstants.PART_ID]



    def __set_object(self, json_object):
        """
        set object

        :param json_object:
        :return:
        """
        name = json_object[JsonConstants.NAME]
        self._objects[name] = DefintionObject(name)
        if JsonConstants.ID in json_object:
            for part in json_object[JsonConstants.ID]:
                self._objects[name].add_part(part)

        if JsonConstants.ID_RANGE in json_object:
            for i in range(json_object[JsonConstants.ID_RANGE][0], json_object[JsonConstants.ID_RANGE][-1]):
                self._objects[name].add_part(i)

        # TODO: Check if we need elem?
        elif "elem" in json_object:
            for elem in json_object["elem"]:
                self._objects[name].add_element(elem)

        elif "elem_range" in json_object:
            for i in range(json_object["elem_range"][0], json_object["elem_range"][1]):
                self._objects[name].add_element(i)

    def _parse_objects(self, json_objects):
        """
        parse json objects and call setter

        :param json_object:
        :return:
        """
        for json_object in json_objects[DefinitionConstants.OBJECTS]:

            if json_object[JsonConstants.TYPE] == ObjectConstantsForData.ELEMENTOBJECT:
                self.__set_object(json_object)
            elif json_object[JsonConstants.TYPE] == ObjectConstantsForData.NODE:
                self._set_datacontainer_defintion(json_object, self._node)
            elif json_object[JsonConstants.TYPE] == ObjectConstantsForData.AIRBAG:
                self._set_datacontainer_defintion(json_object, self._abstat)
            elif json_object[JsonConstants.TYPE] == ObjectConstantsForData.DISBOUT:
                self._set_datacontainer_defintion(json_object, self._disbout)
            elif json_object[JsonConstants.TYPE] == ObjectConstantsForData.ELEMENT:
                self._set_datacontainer_defintion(json_object, self._element)
            elif json_object[JsonConstants.TYPE] == ObjectConstantsForData.CONTACT:
                self._set_contact(json_object)
            elif json_object[JsonConstants.TYPE] == ObjectConstantsForData.DISCRETE:
                self._set_datacontainer_defintion(json_object, self._discrete)
            elif json_object[JsonConstants.TYPE] == ObjectConstantsForData.SEAT_BELT:
                self._set_datacontainer_defintion(json_object, self._seatbelt)
            elif json_object[JsonConstants.TYPE] == ObjectConstantsForData.CROSS_SECTION:
                self._set_datacontainer_defintion(json_object, self._cross_sections)
            elif json_object[JsonConstants.TYPE] == ObjectConstantsForData.ENERGY_PART:
                self._set_datacontainer_defintion(json_object, self._energy_part)
            elif json_object[JsonConstants.TYPE] == ObjectConstantsForData.ENERGY_GLOBAL:
                self._set_datacontainer_defintion(json_object, self._energy_global)
            elif json_object[JsonConstants.TYPE] == ObjectConstantsForData.DISBOUT_PART:
                self._set_datacontainer_defintion(json_object, self._part_disbout)
            else:
                self._logger.emit(LOGConstants.WARNING[0],
                                  json_object[JsonConstants.TYPE] + LoggerWARNING.print_statements[1])

    def _set_unit(self, json_object):
        """
        set unit object

        :param json_object:
        :return:
        """
        for key_name in json_object[DefinitionConstants.UNIT]:
            if key_name == UnitsConstants.TIME:
                if json_object[DefinitionConstants.UNIT][key_name] == UnitsConstants.SECOND:
                    self._units.set_time(UnitsConstants.ONE)
                elif json_object[DefinitionConstants.UNIT][key_name] == UnitsConstants.MILLISECOND:
                    self._units.set_time(UnitsConstants.THOUSAND)
            elif key_name == UnitsConstants.LENGTH:
                if json_object[DefinitionConstants.UNIT][key_name] == UnitsConstants.METER:
                    self._units.set_length(UnitsConstants.ONE)
                elif json_object[DefinitionConstants.UNIT][key_name] == UnitsConstants.MILLIMETER:
                    self._units.set_length(UnitsConstants.THOUSAND)
            elif key_name == UnitsConstants.WEIGHT:
                if json_object[DefinitionConstants.UNIT][key_name] == UnitsConstants.KILOGRAM:
                    self._units.set_weight(UnitsConstants.ONE)
                elif json_object[DefinitionConstants.UNIT][key_name] == UnitsConstants.TON:
                    self._units.set_weight(UnitsConstants.WEIGHT_DEFAULT)

    def _set_criteria(self, json_object):
        """
        set criteria object

        :param json_object:
        :return:
        """
        for criteria in json_object[DefinitionConstants.CRITERIA]:
            body_part = criteria[JsonConstants.PART_OF]
            self._criteria[body_part + "_" + criteria[JsonConstants.NAME]] = criteria

    def _set_diagram_visualisation(self, json_object):
        """
        set data visualisation object

        :param json_object:
        :return:
        """
        for definition in json_object[DefinitionConstants.DATA_VIS]:
            body_part = definition[JsonConstants.PART_OF]
            self._data_vis[body_part + "_" + definition[JsonConstants.NAME]] = definition

    def _set_info(self):
        """
        set info in data visualisation

        :param:
        :return:
        """
        info = []
        for key in self._data_vis.keys():
            if JsonConstants.INFO in self._data_vis[key].keys():
                if len(self._data_vis[key][JsonConstants.INFO].split(":")) == 3:
                    info.append(self._data_vis[key][JsonConstants.INFO])
                elif len(self._data_vis[key][JsonConstants.INFO].split(":")) == 2:
                    self._data_vis[key][JsonConstants.INFO].append(":")
                    info.append(self._data_vis[key][JsonConstants.INFO])
                elif len(self._data_vis[key][JsonConstants.INFO].split(":")) > 3:
                    self._data_vis[key][JsonConstants.INFO] = "::"
                    info.append(self._data_vis[key][JsonConstants.INFO])
                else:
                    self._data_vis[key][JsonConstants.INFO].append(":")
                    info.append(self._data_vis[key][JsonConstants.INFO])
            else:
                info.append(None)
        self._info = info

    def read_def(self, fn):
        """
        read definition file

        :param fn:
        :return:
        """
        self._logger.emit(LOGConstants.READ_DYNASAUR_DEF[0], LD.READ % fn)
        if fn is None:
            exit("No definition file")
        with open(fn) as fd:
            try:
                json_objects = json.load(fd)
            except ValueError as e:
                self._logger.emit(LOGConstants.ERROR[0], LoggerERROR.print_statements[4] % e)
                exit("Exiting - Invalid JSON file")  # Because Mutant, if GUI "exit()" comment
                return

        # TestDefinitionJSON.test_def_json(json_objects, self._logger)

        for j_object in json_objects:
            if DefinitionConstants.TITLE in j_object:
                self._title = j_object[DefinitionConstants.TITLE]
            elif DefinitionConstants.UNIT in j_object:
                self._set_unit(j_object)
            elif DefinitionConstants.CRITERIA in j_object:
                self._set_criteria(j_object)
            elif DefinitionConstants.DATA_VIS in j_object:
                self._set_diagram_visualisation(j_object)
                self._set_info()
            elif DefinitionConstants.OBJECTS in j_object:
                self._parse_objects(json_objects)
            else:
                self._logger.emit(LOGConstants.ERROR[0], "json object not understood:" + str(j_object))
                return

        self._logger.emit(LOGConstants.READ_DYNASAUR_DEF[0], LD.DONE)

