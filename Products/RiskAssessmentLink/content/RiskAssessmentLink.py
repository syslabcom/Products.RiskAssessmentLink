# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from plone.indexer.decorator import indexer
from collective.dynatree.atwidget import DynatreeWidget

try:
    from Products.LinguaPlone.public import *
except ImportError:
    HAS_LINGUAPLONE = False
else:
    HAS_LINGUAPLONE = True

from zope.interface import implements
import interfaces
#from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
from Products.RiskAssessmentLink.config import *

from Products.ATCountryWidget.Widget import CountryWidget, MultiCountryWidget
from Products.VocabularyPickerWidget.VocabularyPickerWidget import VocabularyPickerWidget
from Products.DataGridField.DataGridField import DataGridField
from Products.DataGridField.DataGridWidget import DataGridWidget
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.RiskAssessmentLink.config import *
from Products.Archetypes.Widget import SelectionWidget
from Products.Archetypes.utils import DisplayList
from Products.RiskAssessmentLink import RAMessageFactory as _
from Products.CMFPlone import PloneMessageFactory as _plone_message_factory
from Products.LinguaPlone.browser.vocabularies import AllContentLanguageVocabularyFactory

from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFCore.utils import getToolByName
from zope.i18n import translate

from zope.component import getUtility
from gfb.policy.interfaces import IVocabularyUtility

schema = Schema((

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            label=_plone_message_factory(u'Title'),
        ),
        required=True,
        schemata="default",
        searchable=True,
        accessor="Title",
    ),
    TextField(
        name='description',
        widget=TextAreaWidget(
            label=_(u'ra_description_label', default=u'Short description (3-8 lines)'),
            description=_(u'ra_description_description', default=u'Please enter a short descriptive text')
        ),
        required=True,
        schemata="default",
        searchable=True,
        accessor="Description",
    ),
    StringField(
        name='remoteUrl',
        languageIndependent=True,
        widget=StringField._properties['widget'](
            macro="urlwidget",
            rows=60,
            label=_(u'ra_remoteUrl_label', default=u'URL'),
            description=_(u'ra_remoteUrl_description', default=u"The web address of the remote information."),
        ),
        required=True,
        searchable=False,
    ),
    DateTimeField(
        name='dateOfEditing',
        languageIndependent=True,
        required=True,
        widget=CalendarWidget(
            label=_(u'ra_dateOfEditing_label', default=u"Date of last editing"),
            description=_(u'ra_dateOfEditing_description', default=u"Enter the date when the action guideline was last updated."),
            show_hm=False,
            format='%Y/%m',
        ),
    ),
    LinesField(
        name='contents',
        languageIndependent=True,
        widget=MultiSelectionWidget(
            label=_(u'ra_contents_label', default=u"Procedural guidelines contain..."),
            description=_(u'ra_contents_description', "Check where applicable"),
            rows=5,
            format="checkbox",
        ),
        vocabulary=NamedVocabulary("""RiskAssessmentContents"""),
        enforceVocabulary=True,
        schemata="default",
        multiValued=True,
    ),
    TextField(
        name='remarks',
        languageIndependent=True,
        schemata="default",
        widget=RichWidget(
            rows=5,
            label=_(u'ra_remarks_label', default=u'Remarks'),
            description=_(u'ra_remarks_description', default=u'Here you can add an in-depth comment'),
        ),
        default_output_type="text/html",
        default_content_type="text/html",
        required=True,
        searchable=True,
    ),
    DataGridField(
        name='additionalKeywords',
        languageIndependent=True,
        widget=DataGridWidget(
            label=_(u'ra_additionalKeywords_label', default=u'Addtional keywords'),
            description=_(u'ra_additionalKeywords_description', default=u'Here you can add additional keywords'),
            auto_insert=True,
        ),
        schemata="default",
        columns=("Keywords",),
        allow_empty_rows=False,
        searchable=True,
    ),
    LinesField(
        name='nace',
        required=True,
        languageIndependent=True,
        multiValued=True,
        vocabulary=NamedVocabulary("NACE"),
        widget=DynatreeWidget(
            selectMode=2,
            label=_(u'ra_nace_label', default=u"Sector (NACE Code)"),
            description=_(u'ra_nace_description', default='Pick one or more entries'),
#            quicksearch_help_text=_(u'ra_nace_quicksearch_help_text', default="You can use the Add button to select sectors by browsing the vocabulary. Or you can type in a term or parts of it in the quicksearch field and then click on an item in the results list."),
        ),
        schemata='Sector',
    ),
    LinesField(
        name='riskfactors',
        required=True,
        widget=DynatreeWidget(
            label=_(u'ra_riskfactors_label', default=u"Risk factors"),
            description=_(u'ra_riskfactors_description', default=u''),
            selectMode=2,
#            quicksearch_help_text=_(u'ra_riskfactors_quicksearch_help_text', default="You can use the Add button to select risk factors by browsing the vocabulary. Or you can type in a term or parts of it in the quicksearch field and then click on an item in the results list."),
        ),
        languageIndependent=True,
        schemata="Riskfactors",
        multiValued=True,
        vocabulary=NamedVocabulary("""RiskFactors"""),
    ),
#    LinesField(
#        name='occupation',
#        languageIndependent=True,
#        widget=VocabularyPickerWidget(
#            label="Occupation",
#            vocabulary='ISCO',
#            description="Select one or more entries",
#            level=2,
#            label_msgid='RiskAssessmentLink_label_occupation',
#            description_msgid='RiskAssessmentLink_help_occupation',
#            i18n_domain='RiskAssessmentLink',
#        ),
#        enforceVocabulary=False,
#        schemata="Occupation",
#        multiValued=True,
#    ),
    LinesField(
        name='medium',
        languageIndependent=True,
        widget=MultiSelectionWidget(
            label=_(u'ra_medium_label', default=u"Available as..."),
            description=_(u'ra_medium_description', default="Pick the type of the medium"),
            format="checkbox",
            rows=4,
        ),
        schemata="Other",
        multiValued=True,
        vocabulary='getMediumVocabulary',
    ),
    StringField(
        name='type_methodology',
        languageIndependent=True,
        widget=MultiSelectionWidget(
            label=_(u"ra_type_methodology_label", default=u'Type / methodology'),
            description=_(u'ra_type_methodology_description', default=u''),
            format="checkbox",
         ),
         vocabulary='getType_methodologyVocabulary',
         schemata="Other",
         multiValued=True,
    ),
    StringField(
        name='price',
        languageIndependent=True,
        widget=StringField._properties['widget'](
            label=_(u'ra_price_label', default="Price"),
            description=_(u'ra_price_description', default=u'Please leave blank if free of charge.'),
            rows=10,
        ),
        schemata="Other",
    ),
    BooleanField(
        name='free_for_members',
        languageIndependent=True,
        widget=BooleanField._properties['widget'](
            label=_(u'ra_free_for_members_label', default=u'Free for members'),
            description=_(u'ra_free_for_members_description', default=u''),
        ),
        schemata="Other",
    ),
    BooleanField(
        name='sme',
        languageIndependent=True,
        widget=BooleanField._properties['widget'](
            label=_(u'ra_sme_label', default=u"Recommended for small companies"),
            description=_(u'ra_sme_description', default=u""),
        ),
        schemata="Other",
    ),
    LinesField(
        name='country',
        enforceVocabulary=False,
        languageIndependent=True,
        multiValued=True,
        widget=MultiCountryWidget(
            label=_(u'ra_countries_label', default=u"Countries"),
            description=_(u'ra_countries_description', default=u'Select one or more countries appropriate for this content'),
            provideNullValue=1,
            nullValueTitle="Select...",
        ),
        schemata='Other',
    ),
    LinesField(
        name='remoteLanguage',
        languageIndependent=True,
        widget=MultiSelectionWidget(
            label=_(u'ra_remoteLanguage_label', default=u"Available in..."),
            description=_(u'ra_remoteLanguage_deswcription', u"The language of the linked contents"),
            rows=5,
        ),
        enforceVocabulary=True,
        schemata="Other",
        multiValued=True,
        vocabulary='getFilteredLanguages',
    ),
    ReferenceField(
        name='remoteProvider',
        languageIndependent=True,
        widget=ReferenceWidget(
            label=_(u'ra_remoteProvider_label', default=u'Provider of this information'),
            description=_(u'ra_remoteProvider_description', default=u''),
            condition="python:object.REQUEST.get('mode', '')=='search' or object.portal_membership.getAuthenticatedMember().allowed(object, ['Manager'])",
        ),
        allowed_types=('Provider',),
        relationship="provider_of",
        multiValued=True,
    ),
    BooleanField(
        name='categoryIndependent',
        languageIndependent=True,
        widget=BooleanField._properties['widget'](
            visible=dict(edit='invisible', view='invisible'),
            label=_(u'ra_categoryIndependent_label', default=u'Category independent'),
            description=_(u'ra_categoryIndependent_description', 
                default=u'Tick here to limit your search to general and introductory Risk Assessment Links.'),
        ),
    ),
),
)


RiskAssessmentLink_schema = BaseSchema.copy() + \
    ATContentTypeSchema.copy() + \
    schema.copy()

finalizeATCTSchema(RiskAssessmentLink_schema)

unwantedFields = ('rights', 'subject', 'contributors', 'allowDiscussion', 'location',
    'creators', 'effectiveDate', 'expirationDate', 'creation_date', 'modification_date',
    'relatedItems', 'excludeFromNav', 'language')

for name in unwantedFields:
    RiskAssessmentLink_schema[name].widget.visible['edit'] = 'invisible'
    RiskAssessmentLink_schema.changeSchemataForField(name, 'Other')



class RiskAssessmentLink(BaseContent, ATCTContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IRiskAssessmentLink)

    meta_type = 'RiskAssessmentLink'
    _at_rename_after_creation = True

    schema = RiskAssessmentLink_schema


    def _validProviders(self):
        # switch: if the current user has Manager rights, show ALL Provider objects,
        # else filter to those that are assigned to at least one data object (RiskAssessmentLink)
        pc = getToolByName(self, 'portal_catalog')
        if self.portal_membership.getAuthenticatedMember().allowed(self, ['Manager']):
            provRes = pc(portal_type='Provider')
        else:
            rc = getToolByName(self, 'reference_catalog')
            res = rc(relationship='provider_of')
            uids = set()
            for r in res:
                uids.add(r.targetUID)
            
            provRes = pc(UID = list(uids))
        return provRes

    security.declarePublic('getProviderVocabulary')
    def getProviderVocabulary(self):
        """
        """
        provRes = self._validProviders()
        plt = getToolByName(self, 'portal_languages')
        lang = plt.getPreferredLanguage()
        pvt = getToolByName(self, 'portal_vocabularies')
        VOCAB = pvt.get('provider_category')
        results = dict()
        if VOCAB:
            DL =VOCAB.getDisplayList(self)
            cats = DL.keys()
            for catId, catName in DL.items():
                results[catId] = (catName, dict())
            for res in provRes:
                if res.Language != lang:
                    try:
                        ob = res.getObject()
                    except:
                        # stale catalog entry
                        continue
                    ob = ob.getTranslation(lang) or ob
                    title = ob.Title()
                else:
                    title = res.Title
                if res.getProvider_category in cats:
                    results[res.getProvider_category][1][res.UID] = (title, None)
        else:
            for res in provRes:
                results[res.UID] = (res.Title, None)
        return results


    security.declarePublic('getProviderQuicksearch')
    def getProviderQuicksearch(self):
        """ return a DisplayList of all providers """
        provRes = self._validProviders()
        DL = DisplayList()
        for r in provRes:
            DL.add(r.UID, r.Title)
        return DL

    security.declarePublic('getTermByKey')
    def getTermByKey(self, key):
        """ Return the Term by key based on a cached dict
        """
        return ""

    security.declarePublic('getContentsVocabulary')
    def getContentsVocabulary(self):
        """
        """
        return self._Vocabulary('RiskAssessmentContents')

    security.declarePublic('getRiskFactorsVocabulary')
    def getRiskFactorsVocabulary(self):
        """
        """
        return self._Vocabulary('RiskFactors')

    security.declarePublic('getNACEVocabulary')
    def getNACEVocabulary(self):
        """
        """
        return self._Vocabulary('NACE')

    def _Vocabulary(self, vocab_name):
        pv = getToolByName(self, 'portal_vocabularies')
        VOCAB = getattr(pv, vocab_name, None)
        if VOCAB:
            return VOCAB.getDisplayList(VOCAB)
        else:
            return DisplayList()

    def getMediumVocabulary(self):
        """ return the Values for the medium field """
        return self._Vocabulary('RiskassessmentMedia')

    def getType_methodologyVocabulary(self):
        """ return the Values for the Type / Methodology field """
        return self._Vocabulary('RiskassessmentTypeMethodology')

    def getFilteredLanguages(self):
        """ return the languages supported in the site """
        ppt = getToolByName(self, 'portal_properties')
        sps = ppt.site_properties
        plt = getToolByName(self, 'portal_languages')
        REMOTE_LANGUAGES = sps.getProperty('REMOTE_LANGUAGES', None)

        if REMOTE_LANGUAGES:
            L = list()
            vocab = AllContentLanguageVocabularyFactory(self)
            for lang in REMOTE_LANGUAGES:
                if lang in vocab:
                    L.append((lang, vocab.getTerm(lang).title))
        else:      
            L = plt.listSupportedLanguages()
        L.sort()
        return DisplayList(L)

    def getRemoteProviderUID(self):
        """ return the UID of the provider, stored via reference. Used for indexing.
            Intelligent enough to return correct language version
        """
        lang = self.Language()
        uid = list()
        providers = self.getRemoteProvider()
        for provider in providers:
            uid.append(provider.UID())
            if provider.Language()!=lang:
                trans = provider.getTranslation(lang)
                if trans:
                    uid.append(trans.UID())

        return uid



registerType(RiskAssessmentLink, PROJECTNAME)
# end of class RiskAssessmentLink

