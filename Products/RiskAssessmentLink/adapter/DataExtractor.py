from slc.synchronizer import interfaces
from Products.RiskAssessmentLink.content.interfaces import IRiskAssessmentLink
from zope import interface
from zope import component

REMOVE_FIELDS = ['riskfactors', 
                 'categoryIndependent', 
                 'additionalKeywords', 
                 'remarks', 
                 'medium', 
                 'price', 
                 'sme'
                ]
REWRITE_FIELDS = {'contents' : 'ra_contents'}

class DataExtractor(object):
    """ 
    """
    interface.implements(interfaces.IDataExtractor)
    component.adapts(IRiskAssessmentLink)


    def __init__(self, context):
        self.context = context

    def portal_type(self):
        return 'RALink'

    def data(self):
        data = dict()
        fields = self.context.Schema().fields()
        for field in fields:
            fname = field.getName()

            if fname in REMOVE_FIELDS:
                continue
            if fname in REWRITE_FIELDS.keys():
                fname = REWRITE_FIELDS[fname]

            ftype = field.getType()
            if ftype == 'Products.Archetypes.Field.ReferenceField':
                data[fname] = field.getRaw(self.context)
            else:
                value = field.getAccessor(self.context)()
                if value is None:
                    value = "[[None]]"
                data[fname] = value

        return data

