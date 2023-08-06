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


class Ospfv3Router(Base):
    """Ospfv3 Device level Configuration
    The Ospfv3Router class encapsulates a list of ospfv3Router resources that are managed by the user.
    A list of resources can be retrieved from the server using the Ospfv3Router.find() method.
    The list can be managed by using the Ospfv3Router.add() and Ospfv3Router.remove() methods.
    """

    __slots__ = ()
    _SDM_NAME = 'ospfv3Router'
    _SDM_ATT_MAP = {
        'Active': 'active',
        'BBit': 'bBit',
        'Count': 'count',
        'DescriptiveName': 'descriptiveName',
        'DisableAutoGenerateLinkLsa': 'disableAutoGenerateLinkLsa',
        'DisableAutoGenerateRouterLsa': 'disableAutoGenerateRouterLsa',
        'DiscardLearnedLsa': 'discardLearnedLsa',
        'EBit': 'eBit',
        'EnableGracefulRestartHelperMode': 'enableGracefulRestartHelperMode',
        'EnableStrictLsaChecking': 'enableStrictLsaChecking',
        'EnableSupportReasonSwReloadUpgrade': 'enableSupportReasonSwReloadUpgrade',
        'EnableSupportReasonSwRestart': 'enableSupportReasonSwRestart',
        'EnableSupportReasonSwitchToRedundantControlProcessor': 'enableSupportReasonSwitchToRedundantControlProcessor',
        'EnableSupportReasonUnknown': 'enableSupportReasonUnknown',
        'Errors': 'errors',
        'LocalRouterId': 'localRouterId',
        'LsaRefreshTime': 'lsaRefreshTime',
        'LsaRetransmitTime': 'lsaRetransmitTime',
        'MaxNumLsaPerSecond': 'maxNumLsaPerSecond',
        'Name': 'name',
        'SessionInfo': 'sessionInfo',
        'SessionStatus': 'sessionStatus',
        'StateCounts': 'stateCounts',
        'Status': 'status',
    }

    def __init__(self, parent):
        super(Ospfv3Router, self).__init__(parent)

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
    def BBit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Router-LSA B-Bit
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['BBit']))

    @property
    def Count(self):
        """
        Returns
        -------
        - number: Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Count'])

    @property
    def DescriptiveName(self):
        """
        Returns
        -------
        - str: Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offers more context
        """
        return self._get_attribute(self._SDM_ATT_MAP['DescriptiveName'])

    @property
    def DisableAutoGenerateLinkLsa(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Support graceful restart helper mode when restart reason is unknown and unplanned.
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['DisableAutoGenerateLinkLsa']))

    @property
    def DisableAutoGenerateRouterLsa(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Support graceful restart helper mode when restart reason is unknown and unplanned.
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['DisableAutoGenerateRouterLsa']))

    @property
    def DiscardLearnedLsa(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Discard Learned LSAs
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['DiscardLearnedLsa']))

    @property
    def EBit(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Router-LSA E-Bit
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['EBit']))

    @property
    def EnableGracefulRestartHelperMode(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Enable Graceful Restart helper Mode,if enabled Discard Learned LSAs should be disabled in order to learn the LSAs
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['EnableGracefulRestartHelperMode']))

    @property
    def EnableStrictLsaChecking(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Terminate graceful restart when an LSA has changed
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['EnableStrictLsaChecking']))

    @property
    def EnableSupportReasonSwReloadUpgrade(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Support graceful restart helper mode when restart reason is Software Reload or Upgrade.
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['EnableSupportReasonSwReloadUpgrade']))

    @property
    def EnableSupportReasonSwRestart(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Support graceful restart helper mode when restart reason is Ospfv3 software restart.
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['EnableSupportReasonSwRestart']))

    @property
    def EnableSupportReasonSwitchToRedundantControlProcessor(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Support graceful restart helper mode when restart reason is unplanned switchover.
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['EnableSupportReasonSwitchToRedundantControlProcessor']))

    @property
    def EnableSupportReasonUnknown(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Support graceful restart helper mode when restart reason is unknown and unplanned.
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['EnableSupportReasonUnknown']))

    @property
    def Errors(self):
        """
        Returns
        -------
        - list(dict(arg1:str[None | /api/v1/sessions/1/ixnetwork//.../*],arg2:list[str])): A list of errors that have occurred
        """
        return self._get_attribute(self._SDM_ATT_MAP['Errors'])

    @property
    def LocalRouterId(self):
        """
        Returns
        -------
        - list(str): Router ID
        """
        return self._get_attribute(self._SDM_ATT_MAP['LocalRouterId'])

    @property
    def LsaRefreshTime(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): LSA Refresh time (s)
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['LsaRefreshTime']))

    @property
    def LsaRetransmitTime(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): LSA Retransmit time(s)
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['LsaRetransmitTime']))

    @property
    def MaxNumLsaPerSecond(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Inter Flood LSUpdate burst gap (ms)
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['MaxNumLsaPerSecond']))

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
    def SessionInfo(self):
        """
        Returns
        -------
        - list(str[noIfaceUp | up]): Logs additional information about the session Information
        """
        return self._get_attribute(self._SDM_ATT_MAP['SessionInfo'])

    @property
    def SessionStatus(self):
        """
        Returns
        -------
        - list(str[down | notStarted | up]): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
        """
        return self._get_attribute(self._SDM_ATT_MAP['SessionStatus'])

    @property
    def StateCounts(self):
        """
        Returns
        -------
        - dict(total:number,notStarted:number,down:number,up:number): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
        """
        return self._get_attribute(self._SDM_ATT_MAP['StateCounts'])

    @property
    def Status(self):
        """
        Returns
        -------
        - str(configured | error | mixed | notStarted | started | starting | stopping): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Status'])

    def update(self, Name=None):
        """Updates ospfv3Router resource on the server.

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

    def add(self, Name=None):
        """Adds a new ospfv3Router resource on the server and adds it to the container.

        Args
        ----
        - Name (str): Name of NGPF element, guaranteed to be unique in Scenario

        Returns
        -------
        - self: This instance with all currently retrieved ospfv3Router resources using find and the newly added ospfv3Router resources available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._create(self._map_locals(self._SDM_ATT_MAP, locals()))

    def remove(self):
        """Deletes all the contained ospfv3Router resources in this instance from the server.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        self._delete()

    def find(self, Count=None, DescriptiveName=None, Errors=None, LocalRouterId=None, Name=None, SessionInfo=None, SessionStatus=None, StateCounts=None, Status=None):
        """Finds and retrieves ospfv3Router resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve ospfv3Router resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all ospfv3Router resources from the server.

        Args
        ----
        - Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.
        - DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offers more context
        - Errors (list(dict(arg1:str[None | /api/v1/sessions/1/ixnetwork//.../*],arg2:list[str]))): A list of errors that have occurred
        - LocalRouterId (list(str)): Router ID
        - Name (str): Name of NGPF element, guaranteed to be unique in Scenario
        - SessionInfo (list(str[noIfaceUp | up])): Logs additional information about the session Information
        - SessionStatus (list(str[down | notStarted | up])): Current state of protocol session: Not Started - session negotiation not started, the session is not active yet. Down - actively trying to bring up a protocol session, but negotiation is didn't successfully complete (yet). Up - session came up successfully.
        - StateCounts (dict(total:number,notStarted:number,down:number,up:number)): A list of values that indicates the total number of sessions, the number of sessions not started, the number of sessions down and the number of sessions that are up
        - Status (str(configured | error | mixed | notStarted | started | starting | stopping)): Running status of associated network element. Once in Started state, protocol sessions will begin to negotiate.

        Returns
        -------
        - self: This instance with matching ospfv3Router resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of ospfv3Router data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the ospfv3Router resources from the server available through an iterator or index

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def get_device_ids(self, PortNames=None, Active=None, BBit=None, DisableAutoGenerateLinkLsa=None, DisableAutoGenerateRouterLsa=None, DiscardLearnedLsa=None, EBit=None, EnableGracefulRestartHelperMode=None, EnableStrictLsaChecking=None, EnableSupportReasonSwReloadUpgrade=None, EnableSupportReasonSwRestart=None, EnableSupportReasonSwitchToRedundantControlProcessor=None, EnableSupportReasonUnknown=None, LsaRefreshTime=None, LsaRetransmitTime=None, MaxNumLsaPerSecond=None):
        """Base class infrastructure that gets a list of ospfv3Router device ids encapsulated by this object.

        Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

        Args
        ----
        - PortNames (str): optional regex of port names
        - Active (str): optional regex of active
        - BBit (str): optional regex of bBit
        - DisableAutoGenerateLinkLsa (str): optional regex of disableAutoGenerateLinkLsa
        - DisableAutoGenerateRouterLsa (str): optional regex of disableAutoGenerateRouterLsa
        - DiscardLearnedLsa (str): optional regex of discardLearnedLsa
        - EBit (str): optional regex of eBit
        - EnableGracefulRestartHelperMode (str): optional regex of enableGracefulRestartHelperMode
        - EnableStrictLsaChecking (str): optional regex of enableStrictLsaChecking
        - EnableSupportReasonSwReloadUpgrade (str): optional regex of enableSupportReasonSwReloadUpgrade
        - EnableSupportReasonSwRestart (str): optional regex of enableSupportReasonSwRestart
        - EnableSupportReasonSwitchToRedundantControlProcessor (str): optional regex of enableSupportReasonSwitchToRedundantControlProcessor
        - EnableSupportReasonUnknown (str): optional regex of enableSupportReasonUnknown
        - LsaRefreshTime (str): optional regex of lsaRefreshTime
        - LsaRetransmitTime (str): optional regex of lsaRetransmitTime
        - MaxNumLsaPerSecond (str): optional regex of maxNumLsaPerSecond

        Returns
        -------
        - list(int): A list of device ids that meets the regex criteria provided in the method parameters

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._get_ngpf_device_ids(locals())

    def Ospfv3StartRouter(self, *args, **kwargs):
        """Executes the ospfv3StartRouter operation on the server.

        Start OSPFv3 Router

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        ospfv3StartRouter(SessionIndices=list)
        --------------------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        ospfv3StartRouter(SessionIndices=string)
        ----------------------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('ospfv3StartRouter', payload=payload, response_object=None)

    def Ospfv3StopRouter(self, *args, **kwargs):
        """Executes the ospfv3StopRouter operation on the server.

        Stop OSPFv3 Router

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        ospfv3StopRouter(SessionIndices=list)
        -------------------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        ospfv3StopRouter(SessionIndices=string)
        ---------------------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('ospfv3StopRouter', payload=payload, response_object=None)

    def RestartDown(self, *args, **kwargs):
        """Executes the restartDown operation on the server.

        Stop and start interfaces and sessions that are in Down state.

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        restartDown(SessionIndices=list)
        --------------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        restartDown(SessionIndices=string)
        ----------------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('restartDown', payload=payload, response_object=None)

    def Start(self, *args, **kwargs):
        """Executes the start operation on the server.

        Start selected protocols.

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        start(SessionIndices=list)
        --------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        start(SessionIndices=string)
        ----------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('start', payload=payload, response_object=None)

    def Stop(self, *args, **kwargs):
        """Executes the stop operation on the server.

        Stop selected protocols.

        The IxNetwork model allows for multiple method Signatures with the same name while python does not.

        stop(SessionIndices=list)
        -------------------------
        - SessionIndices (list(number)): This parameter requires an array of session numbers 0 1 2 3

        stop(SessionIndices=string)
        ---------------------------
        - SessionIndices (str): This parameter requires a string of session numbers 1-4;6;7-12

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        payload = { "Arg1": self }
        for i in range(len(args)): payload['Arg%s' % (i + 2)] = args[i]
        for item in kwargs.items(): payload[item[0]] = item[1]
        return self._execute('stop', payload=payload, response_object=None)
