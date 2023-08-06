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


class Template(Base):
    """
    The Template class encapsulates a list of template resources that are managed by the system.
    A list of resources can be retrieved from the server using the Template.find() method.
    """

    __slots__ = ()
    _SDM_NAME = 'template'
    _SDM_ATT_MAP = {
        'Caption': 'caption',
        'Category': 'category',
        'Description': 'description',
        'Overviewimage': 'overviewimage',
        'Overviewsections': 'overviewsections',
        'Scriptfile': 'scriptfile',
    }

    def __init__(self, parent):
        super(Template, self).__init__(parent)

    @property
    def Saved(self):
        """
        Returns
        -------
        - obj(uhd_restpy.testplatform.sessions.ixnetwork.wizard.template.saved.saved.Saved): An instance of the Saved class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from uhd_restpy.testplatform.sessions.ixnetwork.wizard.template.saved.saved import Saved
        return Saved(self)

    @property
    def Caption(self):
        """
        Returns
        -------
        - str: short, user-friendly name of the wizard
        """
        return self._get_attribute(self._SDM_ATT_MAP['Caption'])

    @property
    def Category(self):
        """
        Returns
        -------
        - str: category the wizard belongs to
        """
        return self._get_attribute(self._SDM_ATT_MAP['Category'])

    @property
    def Description(self):
        """
        Returns
        -------
        - str: 
        """
        return self._get_attribute(self._SDM_ATT_MAP['Description'])

    @property
    def Overviewimage(self):
        """
        Returns
        -------
        - str: path to overview image
        """
        return self._get_attribute(self._SDM_ATT_MAP['Overviewimage'])

    @property
    def Overviewsections(self):
        """
        Returns
        -------
        - list(dict(arg1:str,arg2:str)): 
        """
        return self._get_attribute(self._SDM_ATT_MAP['Overviewsections'])

    @property
    def Scriptfile(self):
        """
        Returns
        -------
        - str: path to wizard script
        """
        return self._get_attribute(self._SDM_ATT_MAP['Scriptfile'])

    def find(self, Caption=None, Category=None, Description=None, Overviewimage=None, Overviewsections=None, Scriptfile=None):
        """Finds and retrieves template resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve template resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all template resources from the server.

        Args
        ----
        - Caption (str): short, user-friendly name of the wizard
        - Category (str): category the wizard belongs to
        - Description (str): 
        - Overviewimage (str): path to overview image
        - Overviewsections (list(dict(arg1:str,arg2:str))): 
        - Scriptfile (str): path to wizard script

        Returns
        -------
        - self: This instance with matching template resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of template data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the template resources from the server available through an iterator or index

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)
