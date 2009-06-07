from interfaces import IVocabularyHelper
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from Products.CMFPlone import utils
from Products.Five import BrowserView
from Products.Archetypes.utils import DisplayList


class VocabularyHelper(BrowserView):
    implements(IVocabularyHelper)


    def getDisplayListFor(self, vocabularyName=''):
        """See interface"""
        pv = getToolByName(self, 'portal_vocabularies')
        VOCAB = getattr(pv, vocabularyName, None)
        if not VOCAB:
            return DisplayList()
        DL = VOCAB.getDisplayList(self)
        return DL

    def getSubjectList(self):
        """See interface"""
        pc = getToolByName(self, 'portal_catalog')
        vals = pc.uniqueValuesFor('Subject')
        result = DisplayList()
        for v in vals:
            result.add(v,v)
        return result