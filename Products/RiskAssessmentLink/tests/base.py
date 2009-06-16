from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
import gocept.linkchecker

from Products.Five import fiveconfigure, zcml
from Products.PloneTestCase import layer

SiteLayer = layer.PloneSite

class RALinkLayer(SiteLayer):
    @classmethod
    def setUp(cls):
        ztc.installProduct('ATVocabularyManager')
        ztc.installProduct('RiskAssessmentLink')
        ztc.installProduct('ZCatalog')
        fiveconfigure.debug_mode = True

        import gocept.linkchecker
        zcml.load_config('configure.zcml', gocept.linkchecker)
        fiveconfigure.debug_mode = False

        ptc.setupPloneSite(products=['RiskAssessmentLink', 'ATVocabularyManager'])
        ztc.installPackage('gocept.linkchecker')
        SiteLayer.setUp()


class RiskAssessmentLinkTestCase(ptc.PloneTestCase):
    layer = RALinkLayer
    pass

class RiskAssessmentLinkFunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """
    layer = RALinkLayer

    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def _setup(self):
        ptc.FunctionalTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()


    def afterSetUp(self):
        roles = ('Member', 'Contributor')
        self.portal.portal_membership.addMember('contributor',
                                                'secret',
                                                roles, [])
