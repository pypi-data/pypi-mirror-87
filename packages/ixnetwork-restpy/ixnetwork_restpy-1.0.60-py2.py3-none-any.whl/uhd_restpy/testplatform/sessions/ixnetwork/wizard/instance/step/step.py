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


class Step(Base):
    """
    The Step class encapsulates a list of step resources that are managed by the user.
    A list of resources can be retrieved from the server using the Step.find() method.
    The list can be managed by using the Step.add() and Step.remove() methods.
    """

    __slots__ = ()
    _SDM_NAME = 'step'
    _SDM_ATT_MAP = {
        'Caption': 'caption',
        'Description': 'description',
        'Errors': 'errors',
        'ImageFilename': 'imageFilename',
        'ImageToggleEnabled': 'imageToggleEnabled',
        'ImageToggleState': 'imageToggleState',
        'LabelHint': 'labelHint',
        'NodeId': 'nodeId',
        'Readonly': 'readonly',
        'RegionHint': 'regionHint',
        'Visible': 'visible',
    }

    def __init__(self, parent):
        super(Step, self).__init__(parent)

    @property
    def Group(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.wizard.instance.step.group.group.Group): An instance of the Group class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.wizard.instance.step.group.group import Group
        return Group(self)

    @property
    def Caption(self):
        """
        Returns
        -------
        - str: Name of wizard step
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
        - str: description of wizard step
        """
        return self._get_attribute(self._SDM_ATT_MAP['Description'])
    @Description.setter
    def Description(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Description'], value)

    @property
    def Errors(self):
        """
        Returns
        -------
        - str: JSON formatted list of errors, should only be set through wizard framework
        """
        return self._get_attribute(self._SDM_ATT_MAP['Errors'])
    @Errors.setter
    def Errors(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Errors'], value)

    @property
    def ImageFilename(self):
        """
        Returns
        -------
        - str: 
        """
        return self._get_attribute(self._SDM_ATT_MAP['ImageFilename'])
    @ImageFilename.setter
    def ImageFilename(self, value):
        self._set_attribute(self._SDM_ATT_MAP['ImageFilename'], value)

    @property
    def ImageToggleEnabled(self):
        """
        Returns
        -------
        - bool: 
        """
        return self._get_attribute(self._SDM_ATT_MAP['ImageToggleEnabled'])
    @ImageToggleEnabled.setter
    def ImageToggleEnabled(self, value):
        self._set_attribute(self._SDM_ATT_MAP['ImageToggleEnabled'], value)

    @property
    def ImageToggleState(self):
        """
        Returns
        -------
        - bool: 
        """
        return self._get_attribute(self._SDM_ATT_MAP['ImageToggleState'])
    @ImageToggleState.setter
    def ImageToggleState(self, value):
        self._set_attribute(self._SDM_ATT_MAP['ImageToggleState'], value)

    @property
    def LabelHint(self):
        """
        Returns
        -------
        - str: JSON formatted string used for placing labelon image, should only be set through wizard framework
        """
        return self._get_attribute(self._SDM_ATT_MAP['LabelHint'])
    @LabelHint.setter
    def LabelHint(self, value):
        self._set_attribute(self._SDM_ATT_MAP['LabelHint'], value)

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
    def Readonly(self):
        """
        Returns
        -------
        - bool: 
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
        - str: JSON formatted string used for placing labelon image, should only be set through wizard framework
        """
        return self._get_attribute(self._SDM_ATT_MAP['RegionHint'])
    @RegionHint.setter
    def RegionHint(self, value):
        self._set_attribute(self._SDM_ATT_MAP['RegionHint'], value)

    @property
    def Visible(self):
        """
        Returns
        -------
        - bool: step is hidden if false, shown if true
        """
        return self._get_attribute(self._SDM_ATT_MAP['Visible'])
    @Visible.setter
    def Visible(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Visible'], value)

    def update(self, Caption=None, Description=None, Errors=None, ImageFilename=None, ImageToggleEnabled=None, ImageToggleState=None, LabelHint=None, NodeId=None, Readonly=None, RegionHint=None, Visible=None):
        """Updates step resource on the server.

        Args
        ----
        - Caption (str): Name of wizard step
        - Description (str): description of wizard step
        - Errors (str): JSON formatted list of errors, should only be set through wizard framework
        - ImageFilename (str): 
        - ImageToggleEnabled (bool): 
        - ImageToggleState (bool): 
        - LabelHint (str): JSON formatted string used for placing labelon image, should only be set through wizard framework
        - NodeId (str): 
        - Readonly (bool): 
        - RegionHint (str): JSON formatted string used for placing labelon image, should only be set through wizard framework
        - Visible (bool): step is hidden if false, shown if true

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

    def add(self, Caption=None, Description=None, Errors=None, ImageFilename=None, ImageToggleEnabled=None, ImageToggleState=None, LabelHint=None, NodeId=None, Readonly=None, RegionHint=None, Visible=None):
        """Adds a new step resource on the server and adds it to the container.

        Args
        ----
        - Caption (str): Name of wizard step
        - Description (str): description of wizard step
        - Errors (str): JSON formatted list of errors, should only be set through wizard framework
        - ImageFilename (str): 
        - ImageToggleEnabled (bool): 
        - ImageToggleState (bool): 
        - LabelHint (str): JSON formatted string used for placing labelon image, should only be set through wizard framework
        - NodeId (str): 
        - Readonly (bool): 
        - RegionHint (str): JSON formatted string used for placing labelon image, should only be set through wizard framework
        - Visible (bool): step is hidden if false, shown if true

        Returns
        -------
        - self: This instance with all currently retrieved step resources using find and the newly added step resources available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._create(self._map_locals(self._SDM_ATT_MAP, locals()))

    def remove(self):
        """Deletes all the contained step resources in this instance from the server.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        self._delete()

    def find(self, Caption=None, Description=None, Errors=None, ImageFilename=None, ImageToggleEnabled=None, ImageToggleState=None, LabelHint=None, NodeId=None, Readonly=None, RegionHint=None, Visible=None):
        """Finds and retrieves step resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve step resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all step resources from the server.

        Args
        ----
        - Caption (str): Name of wizard step
        - Description (str): description of wizard step
        - Errors (str): JSON formatted list of errors, should only be set through wizard framework
        - ImageFilename (str): 
        - ImageToggleEnabled (bool): 
        - ImageToggleState (bool): 
        - LabelHint (str): JSON formatted string used for placing labelon image, should only be set through wizard framework
        - NodeId (str): 
        - Readonly (bool): 
        - RegionHint (str): JSON formatted string used for placing labelon image, should only be set through wizard framework
        - Visible (bool): step is hidden if false, shown if true

        Returns
        -------
        - self: This instance with matching step resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of step data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the step resources from the server available through an iterator or index

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)
