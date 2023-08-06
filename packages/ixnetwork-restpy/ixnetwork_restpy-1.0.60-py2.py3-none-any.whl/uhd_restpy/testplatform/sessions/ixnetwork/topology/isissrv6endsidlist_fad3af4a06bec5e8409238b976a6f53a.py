# MIT LICENSE
#
# Copyright 1997 - 2020 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE. 
from uhd_restpy.base import Base
from uhd_restpy.files import Files


class IsisSRv6EndSIDList(Base):
    """ISIS SRv6 End SID
    The IsisSRv6EndSIDList class encapsulates a required isisSRv6EndSIDList resource which will be retrieved from the server every time the property is accessed.
    """

    __slots__ = ()
    _SDM_NAME = 'isisSRv6EndSIDList'
    _SDM_ATT_MAP = {
        'Active': 'active',
        'AdvertiseCustomSubTLV': 'advertiseCustomSubTLV',
        'Count': 'count',
        'CustomSubTlv': 'customSubTlv',
        'DescriptiveName': 'descriptiveName',
        'EndPointFunction': 'endPointFunction',
        'Flags': 'flags',
        'LocatorName': 'locatorName',
        'Name': 'name',
        'Sid': 'sid',
        'SidName': 'sidName',
    }

    def __init__(self, parent):
        super(IsisSRv6EndSIDList, self).__init__(parent)

    @property
    def Active(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Activate/Deactivate Configuration
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['Active']))

    @property
    def AdvertiseCustomSubTLV(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Advertise Custom Sub-TLV
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['AdvertiseCustomSubTLV']))

    @property
    def Count(self):
        """
        Returns
        -------
        - number: Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Count'])

    @property
    def CustomSubTlv(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Custom Sub-TLV
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['CustomSubTlv']))

    @property
    def DescriptiveName(self):
        """
        Returns
        -------
        - str: Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offers more context
        """
        return self._get_attribute(self._SDM_ATT_MAP['DescriptiveName'])

    @property
    def EndPointFunction(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): End-Point Function
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['EndPointFunction']))

    @property
    def Flags(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Flags
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['Flags']))

    @property
    def LocatorName(self):
        """
        Returns
        -------
        - list(str): Locator Name
        """
        return self._get_attribute(self._SDM_ATT_MAP['LocatorName'])

    @property
    def Name(self):
        """
        Returns
        -------
        - str: Name of NGPF element, guaranteed to be unique in Scenario
        """
        return self._get_attribute(self._SDM_ATT_MAP['Name'])
    @Name.setter
    def Name(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Name'], value)

    @property
    def Sid(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): SID
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['Sid']))

    @property
    def SidName(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): SID Name
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['SidName']))

    def update(self, Name=None):
        """Updates isisSRv6EndSIDList resource on the server.

        This method has some named parameters with a type: obj (Multivalue).
        The Multivalue class has documentation that details the possible values for those named parameters.

        Args
        ----
        - Name (str): Name of NGPF element, guaranteed to be unique in Scenario

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

    def get_device_ids(self, PortNames=None, Active=None, AdvertiseCustomSubTLV=None, CustomSubTlv=None, EndPointFunction=None, Flags=None, Sid=None, SidName=None):
        """Base class infrastructure that gets a list of isisSRv6EndSIDList device ids encapsulated by this object.

        Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

        Args
        ----
        - PortNames (str): optional regex of port names
        - Active (str): optional regex of active
        - AdvertiseCustomSubTLV (str): optional regex of advertiseCustomSubTLV
        - CustomSubTlv (str): optional regex of customSubTlv
        - EndPointFunction (str): optional regex of endPointFunction
        - Flags (str): optional regex of flags
        - Sid (str): optional regex of sid
        - SidName (str): optional regex of sidName

        Returns
        -------
        - list(int): A list of device ids that meets the regex criteria provided in the method parameters

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._get_ngpf_device_ids(locals())
