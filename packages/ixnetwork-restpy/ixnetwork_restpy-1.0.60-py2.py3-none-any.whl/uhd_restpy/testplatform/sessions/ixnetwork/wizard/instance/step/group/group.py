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


class Group(Base):
    """
    The Group class encapsulates a list of group resources that are managed by the user.
    A list of resources can be retrieved from the server using the Group.find() method.
    The list can be managed by using the Group.add() and Group.remove() methods.
    """

    __slots__ = ()
    _SDM_NAME = 'group'
    _SDM_ATT_MAP = {
        'Alignment': 'alignment',
        'Caption': 'caption',
        'Description': 'description',
        'NodeId': 'nodeId',
        'PortAssignmentCategories': 'portAssignmentCategories',
        'Readonly': 'readonly',
        'RegionHint': 'regionHint',
        'Type': 'type',
        'Visible': 'visible',
    }

    def __init__(self, parent):
        super(Group, self).__init__(parent)

    @property
    def AssignedPort(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.wizard.instance.step.group.assignedport.assignedport.AssignedPort): An instance of the AssignedPort class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.wizard.instance.step.group.assignedport.assignedport import AssignedPort
        return AssignedPort(self)

    @property
    def AvailablePort(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.wizard.instance.step.group.availableport.availableport.AvailablePort): An instance of the AvailablePort class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.wizard.instance.step.group.availableport.availableport import AvailablePort
        return AvailablePort(self)

    @property
    def Field(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.wizard.instance.step.group.field.field.Field): An instance of the Field class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.wizard.instance.step.group.field.field import Field
        return Field(self)

    @property
    def Alignment(self):
        """
        Returns
        -------
        - str(center | fullwidth | left | right): 
        """
        return self._get_attribute(self._SDM_ATT_MAP['Alignment'])
    @Alignment.setter
    def Alignment(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Alignment'], value)

    @property
    def Caption(self):
        """
        Returns
        -------
        - str: Name of wizard group
        """
        return self._get_attribute(self._SDM_ATT_MAP['Caption'])
    @Caption.setter
    def Caption(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Caption'], value)

    @property
    def Description(self):
        """
        Returns
        -------
        - str: Description of wizard group
        """
        return self._get_attribute(self._SDM_ATT_MAP['Description'])
    @Description.setter
    def Description(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Description'], value)

    @property
    def NodeId(self):
        """
        Returns
        -------
        - str: 
        """
        return self._get_attribute(self._SDM_ATT_MAP['NodeId'])
    @NodeId.setter
    def NodeId(self, value):
        self._set_attribute(self._SDM_ATT_MAP['NodeId'], value)

    @property
    def PortAssignmentCategories(self):
        """
        Returns
        -------
        - list(str): 
        """
        return self._get_attribute(self._SDM_ATT_MAP['PortAssignmentCategories'])
    @PortAssignmentCategories.setter
    def PortAssignmentCategories(self, value):
        self._set_attribute(self._SDM_ATT_MAP['PortAssignmentCategories'], value)

    @property
    def Readonly(self):
        """
        Returns
        -------
        - bool: indicates if the group and all its fields can be modified or not
        """
        return self._get_attribute(self._SDM_ATT_MAP['Readonly'])
    @Readonly.setter
    def Readonly(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Readonly'], value)

    @property
    def RegionHint(self):
        """
        Returns
        -------
        - str: JSON formatted string used for placing region on image, should only be set through wizard framework
        """
        return self._get_attribute(self._SDM_ATT_MAP['RegionHint'])
    @RegionHint.setter
    def RegionHint(self, value):
        self._set_attribute(self._SDM_ATT_MAP['RegionHint'], value)

    @property
    def Type(self):
        """
        Returns
        -------
        - str(normal | portAssignment): 
        """
        return self._get_attribute(self._SDM_ATT_MAP['Type'])
    @Type.setter
    def Type(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Type'], value)

    @property
    def Visible(self):
        """
        Returns
        -------
        - bool: group and its fields are hidden if false, shown if true
        """
        return self._get_attribute(self._SDM_ATT_MAP['Visible'])
    @Visible.setter
    def Visible(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Visible'], value)

    def update(self, Alignment=None, Caption=None, Description=None, NodeId=None, PortAssignmentCategories=None, Readonly=None, RegionHint=None, Type=None, Visible=None):
        """Updates group resource on the server.

        Args
        ----
        - Alignment (str(center | fullwidth | left | right)): 
        - Caption (str): Name of wizard group
        - Description (str): Description of wizard group
        - NodeId (str): 
        - PortAssignmentCategories (list(str)): 
        - Readonly (bool): indicates if the group and all its fields can be modified or not
        - RegionHint (str): JSON formatted string used for placing region on image, should only be set through wizard framework
        - Type (str(normal | portAssignment)): 
        - Visible (bool): group and its fields are hidden if false, shown if true

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

    def add(self, Alignment=None, Caption=None, Description=None, NodeId=None, PortAssignmentCategories=None, Readonly=None, RegionHint=None, Type=None, Visible=None):
        """Adds a new group resource on the server and adds it to the container.

        Args
        ----
        - Alignment (str(center | fullwidth | left | right)): 
        - Caption (str): Name of wizard group
        - Description (str): Description of wizard group
        - NodeId (str): 
        - PortAssignmentCategories (list(str)): 
        - Readonly (bool): indicates if the group and all its fields can be modified or not
        - RegionHint (str): JSON formatted string used for placing region on image, should only be set through wizard framework
        - Type (str(normal | portAssignment)): 
        - Visible (bool): group and its fields are hidden if false, shown if true

        Returns
        -------
        - self: This instance with all currently retrieved group resources using find and the newly added group resources available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._create(self._map_locals(self._SDM_ATT_MAP, locals()))

    def remove(self):
        """Deletes all the contained group resources in this instance from the server.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        self._delete()

    def find(self, Alignment=None, Caption=None, Description=None, NodeId=None, PortAssignmentCategories=None, Readonly=None, RegionHint=None, Type=None, Visible=None):
        """Finds and retrieves group resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve group resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all group resources from the server.

        Args
        ----
        - Alignment (str(center | fullwidth | left | right)): 
        - Caption (str): Name of wizard group
        - Description (str): Description of wizard group
        - NodeId (str): 
        - PortAssignmentCategories (list(str)): 
        - Readonly (bool): indicates if the group and all its fields can be modified or not
        - RegionHint (str): JSON formatted string used for placing region on image, should only be set through wizard framework
        - Type (str(normal | portAssignment)): 
        - Visible (bool): group and its fields are hidden if false, shown if true

        Returns
        -------
        - self: This instance with matching group resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of group data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the group resources from the server available through an iterator or index

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)
