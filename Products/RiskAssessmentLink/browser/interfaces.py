from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface, Attribute
from plone.portlets.interfaces import IPortletManager

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer.
    """

class IVocabularyHelper(Interface):
    """Interface that holds verious methods for working with vocaularies"""

    def getDisplayListFor(vocabularyName=''):
        """ Return DisplayList for given vocabulary"""


    def getSubjectList():
        """Return a display list of Subject entries"""

class ISynchronizer(Interface):
    """ Interface for synchronization functionality """
