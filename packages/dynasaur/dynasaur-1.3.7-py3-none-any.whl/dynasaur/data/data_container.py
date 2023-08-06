from ..data.ls_dyna import DEForc, Elout, EloutObject, Glstat, Matsum, Nodout, RCForc, SBTout, Secforc, Disbout, PartDisbout, Abstat
from ..utils.constants import ObjectConstantsForData


class DataContainer:
    """
    class DataContainer
    store objects types
    """
    _elout = None
    _elout_object = None
    _secforc = None
    _rcforc = None
    _deforc = None
    _nodout = None
    _volume = None
    _sbtout = None
    _matsum = None
    _glstat = None
    _disbout = None
    _part_disbout = None
    _abstat = None

    @staticmethod
    def get_data(name):
        """
        :param: name

        :return: Object on the given name
        """
        if name == ObjectConstantsForData.ELEMENT:
            return DataContainer._elout
        if name == ObjectConstantsForData.ELEMENTOBJECT:
            return DataContainer._elout_object
        elif name == ObjectConstantsForData.CROSS_SECTION:
            return DataContainer._secforc
        elif name == ObjectConstantsForData.DISCRETE:
            return DataContainer._deforc
        elif name == ObjectConstantsForData.NODE:
            return DataContainer._nodout
        elif name == ObjectConstantsForData.SEAT_BELT:
            return DataContainer._sbtout
        elif name == ObjectConstantsForData.CONTACT:
            return DataContainer._rcforc
        elif name == ObjectConstantsForData.ENERGY_PART:
            return DataContainer._matsum
        elif name == ObjectConstantsForData.ENERGY_GLOBAL:
            return DataContainer._glstat
        elif name == ObjectConstantsForData.DISBOUT:
            return DataContainer._disbout
        elif name == ObjectConstantsForData.DISBOUT_PART:
            return DataContainer._part_disbout
        elif name == ObjectConstantsForData.AIRBAG:
            return DataContainer._abstat
        return

    @staticmethod
    def init_all_data_sources(binout, logger, dynasaur_def, volume_path):
        """
        init all data sources
        :param: binout
        :param: logger
        :param: dynasaur definition
        :param: binout path/directory

        :return:
        """
        DataContainer._secforc = Secforc(binout, logger, dynasaur_def)
        DataContainer._elout = Elout(binout, logger, dynasaur_def)
        DataContainer._elout_object = EloutObject(binout, logger, dynasaur_def, volume_path=volume_path)
        DataContainer._nodout = Nodout(binout, logger, dynasaur_def)
        DataContainer._deforc = DEForc(binout, logger, dynasaur_def)
        DataContainer._disbout = Disbout(binout, logger, dynasaur_def)
        DataContainer._part_disbout = PartDisbout(binout, logger, dynasaur_def)
        DataContainer._rcforc = RCForc(binout, logger, dynasaur_def)
        DataContainer._sbtout = SBTout(binout, logger, dynasaur_def)
        DataContainer._matsum = Matsum(binout, logger, dynasaur_def)
        DataContainer._glstat = Glstat(binout, logger, dynasaur_def)
        DataContainer._abstat = Abstat(binout, logger, dynasaur_def)

    @staticmethod
    def init_data_source_nodout(madymo, logger, dynasaur_def):
        """
        Init nodout data source

        :param: madymo
        :param: logger
        :param: dynasaur definitions

        :return:
        """
        DataContainer._nodout = Nodout(madymo, logger, dynasaur_def, code_type=CodeType.MADYMO)

