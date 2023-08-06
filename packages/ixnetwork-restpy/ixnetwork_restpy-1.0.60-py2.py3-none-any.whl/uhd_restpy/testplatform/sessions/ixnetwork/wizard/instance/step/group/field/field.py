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


class Field(Base):
    """
    The Field class encapsulates a list of field resources that are managed by the user.
    A list of resources can be retrieved from the server using the Field.find() method.
    The list can be managed by using the Field.add() and Field.remove() methods.
    """

    __slots__ = ()
    _SDM_NAME = 'field'
    _SDM_ATT_MAP = {
        'Caption': 'caption',
        'Errors': 'errors',
        'LabelHint': 'labelHint',
        'NodeId': 'nodeId',
        'NotifyOnChange': 'notifyOnChange',
        'Readonly': 'readonly',
        'TableHint': 'tableHint',
        'Type': 'type',
        'Value': 'value',
        'ValueHint': 'valueHint',
        'Visible': 'visible',
    }

    def __init__(self, parent):
        super(Field, self).__init__(parent)

    @property
    def Caption(self):
        """
        Returns
        -------
        - str: name of wizard field
        """
        return self._get_attribute(self._SDM_ATT_MAP['Caption'])
    @Caption.setter
    def Caption(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Caption'], value)

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
    def NotifyOnChange(self):
        """
        Returns
        -------
        - bool: When set the scripts 'update' method will be called on value change
        """
        return self._get_attribute(self._SDM_ATT_MAP['NotifyOnChange'])
    @NotifyOnChange.setter
    def NotifyOnChange(self, value):
        self._set_attribute(self._SDM_ATT_MAP['NotifyOnChange'], value)

    @property
    def Readonly(self):
        """
        Returns
        -------
        - bool: indicates if the field can be modified or not
        """
        return self._get_attribute(self._SDM_ATT_MAP['Readonly'])
    @Readonly.setter
    def Readonly(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Readonly'], value)

    @property
    def TableHint(self):
        """
        Returns
        -------
        - str: result from last wizard run
        """
        return self._get_attribute(self._SDM_ATT_MAP['TableHint'])
    @TableHint.setter
    def TableHint(self, value):
        self._set_attribute(self._SDM_ATT_MAP['TableHint'], value)

    @property
    def Type(self):
        """
        Returns
        -------
        - str(kBool | kEnumValue | kFloat | kInteger | kMultivalue | kString | kTable): 
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['Type']))

    @property
    def Value(self):
        """
        Returns
        -------
        - str: value of wizard field
        """
        return self._get_attribute(self._SDM_ATT_MAP['Value'])
    @Value.setter
    def Value(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Value'], value)

    @property
    def ValueHint(self):
        """
        Returns
        -------
        - str: JSON formatted string, e.g. { min: 1, max: 100}, { mvPattern: [singleValue], { supportedEnums: [ {value: foo1, caption: Foo1 } ] } }
        """
        return self._get_attribute(self._SDM_ATT_MAP['ValueHint'])
    @ValueHint.setter
    def ValueHint(self, value):
        self._set_attribute(self._SDM_ATT_MAP['ValueHint'], value)

    @property
    def Visible(self):
        """
        Returns
        -------
        - bool: field is hidden if false, shown if true
        """
        return self._get_attribute(self._SDM_ATT_MAP['Visible'])
    @Visible.setter
    def Visible(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Visible'], value)

    def update(self, Caption=None, Errors=None, LabelHint=None, NodeId=None, NotifyOnChange=None, Readonly=None, TableHint=None, Value=None, ValueHint=None, Visible=None):
        """Updates field resource on the server.

        This method has some named parameters with a type: obj (Multivalue).
        The Multivalue class has documentation that details the possible values for those named parameters.

        Args
        ----
        - Caption (str): name of wizard field
        - Errors (str): JSON formatted list of errors, should only be set through wizard framework
        - LabelHint (str): JSON formatted string used for placing labelon image, should only be set through wizard framework
        - NodeId (str): 
        - NotifyOnChange (bool): When set the scripts 'update' method will be called on value change
        - Readonly (bool): indicates if the field can be modified or not
        - TableHint (str): result from last wizard run
        - Value (str): value of wizard field
        - ValueHint (str): JSON formatted string, e.g. { min: 1, max: 100}, { mvPattern: [singleValue], { supportedEnums: [ {value: foo1, caption: Foo1 } ] } }
        - Visible (bool): field is hidden if false, shown if true

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

    def add(self, Caption=None, Errors=None, LabelHint=None, NodeId=None, NotifyOnChange=None, Readonly=None, TableHint=None, Value=None, ValueHint=None, Visible=None):
        """Adds a new field resource on the server and adds it to the container.

        Args
        ----
        - Caption (str): name of wizard field
        - Errors (str): JSON formatted list of errors, should only be set through wizard framework
        - LabelHint (str): JSON formatted string used for placing labelon image, should only be set through wizard framework
        - NodeId (str): 
        - NotifyOnChange (bool): When set the scripts 'update' method will be called on value change
        - Readonly (bool): indicates if the field can be modified or not
        - TableHint (str): result from last wizard run
        - Value (str): value of wizard field
        - ValueHint (str): JSON formatted string, e.g. { min: 1, max: 100}, { mvPattern: [singleValue], { supportedEnums: [ {value: foo1, caption: Foo1 } ] } }
        - Visible (bool): field is hidden if false, shown if true

        Returns
        -------
        - self: This instance with all currently retrieved field resources using find and the newly added field resources available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._create(self._map_locals(self._SDM_ATT_MAP, locals()))

    def remove(self):
        """Deletes all the contained field resources in this instance from the server.

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        self._delete()

    def find(self, Caption=None, Errors=None, LabelHint=None, NodeId=None, NotifyOnChange=None, Readonly=None, TableHint=None, Value=None, ValueHint=None, Visible=None):
        """Finds and retrieves field resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve field resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all field resources from the server.

        Args
        ----
        - Caption (str): name of wizard field
        - Errors (str): JSON formatted list of errors, should only be set through wizard framework
        - LabelHint (str): JSON formatted string used for placing labelon image, should only be set through wizard framework
        - NodeId (str): 
        - NotifyOnChange (bool): When set the scripts 'update' method will be called on value change
        - Readonly (bool): indicates if the field can be modified or not
        - TableHint (str): result from last wizard run
        - Value (str): value of wizard field
        - ValueHint (str): JSON formatted string, e.g. { min: 1, max: 100}, { mvPattern: [singleValue], { supportedEnums: [ {value: foo1, caption: Foo1 } ] } }
        - Visible (bool): field is hidden if false, shown if true

        Returns
        -------
        - self: This instance with matching field resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of field data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the field resources from the server available through an iterator or index

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def get_device_ids(self, PortNames=None, Type=None):
        """Base class infrastructure that gets a list of field device ids encapsulated by this object.

        Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

        Args
        ----
        - PortNames (str): optional regex of port names
        - Type (str): optional regex of type

        Returns
        -------
        - list(int): A list of device ids that meets the regex criteria provided in the method parameters

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._get_ngpf_device_ids(locals())
