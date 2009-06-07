import logging
logger = logging.getLogger('Products.RiskAssessmentLink')
# import lms retrievers if we have Linkchecker installed
try:
    import lmsretrievers
except:
    logger.info('Not importing LMS Retrievers. CMFLinkchecker not present?')