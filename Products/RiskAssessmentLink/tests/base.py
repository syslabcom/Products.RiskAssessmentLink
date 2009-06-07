from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

ztc.installProduct('CMFLinkChecker')
ztc.installProduct('RiskAssessmentLink')
ztc.installProduct('ZCatalog')

ptc.setupPloneSite(products=['RiskAssessmentLink', 'CMFLinkChecker'])

class RiskAssessmentLinkTestCase(ptc.PloneTestCase):
    pass
    
class RiskAssessmentLinkFunctionalTestCase(ptc.FunctionalTestCase):
    pass