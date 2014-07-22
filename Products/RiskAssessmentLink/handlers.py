from Products.RiskAssessmentLink.content.interfaces import IRiskAssessmentLink
from Products.CMFCore.utils import getToolByName

def print_events(event):
    print "print_events:" , event


def link_edited(obj, event):
    riskfactors = obj.getRiskfactors()
    # remove 'independent' entry if other values were selected
    if len(riskfactors)>1 and '0' in riskfactors:
        riskfactors = [x for x in riskfactors if x!='0']
        obj.setRiskfactors(riskfactors)
    nace = obj.getNace()
    if len(nace)>1 and '0' in nace:
        nace = [x for x in nace if x!='0']
        obj.setNace(nace)
    if '0' in riskfactors and '0' in nace:
        obj.setCategoryIndependent(True)
    else:
        obj.setCategoryIndependent(False)
    setattr(obj, 'original_url_path', obj.absolute_url_path())


    def getMyProvider(self):
        pm = getToolByName(self, 'portal_membership')
        hf = pm.getHomeFolder()
        try:
            name = pm.getAuthenticatedMember().getUserId()
        except:
            name = pm.getAuthenticatedMember().getUserName()
        f = pm.getMembersFolder()
        path = "/".join( f.getPhysicalPath() ) + '/' + name
        res = self.portal_catalog(portal_type='Provider', path=path)
        return len(res) > 0 and res[0].getObject() or None

    provider = getMyProvider(obj)
    # if we find a provider and there is none set already, we set the default one. otherwise don't touch
    if provider and not obj.getRemoteProvider():
        obj.setRemoteProvider(provider.UID())

    obj.reindexObject()


def link_edit_begun(obj, event):
    if not len(obj.getNace()):
        obj.setNace(['0'])
    if not len(obj.getRiskfactors()):
        obj.setRiskfactors(['0'])