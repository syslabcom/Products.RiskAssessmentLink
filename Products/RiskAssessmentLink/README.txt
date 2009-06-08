Introduction
============

This content type can be used to link to an external resources on Risk Assessment. Several fields offer the possibility to enter meta-information about these resources.

Boilerplate
===========

First, we must perform some setup. We use the testbrowser that is shipped
with Five, as this provides proper Zope 2 integration. Most of the 
documentation, though, is in the underlying zope.testbrower package.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> self.portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in. We will
do this using the default user from PloneTestCase:

    >>> from Products.PloneTestCase.setup import portal_owner, default_password

    >>> browser.open(portal_url)

We have the login portlet, so let's use that.

    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.

We then test that we are still on the portal front page:

    >>> browser.url == portal_url
    True

And we ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True



Adding a Risk Assessment Link
=============================

We add a Risk Assessment Link and make sure the id is set correctly.
    >>> _ = self.folder.invokeFactory(type_name='RiskAssessmentLink', id='myralink')
    >>> myralink = self.folder.myralink
    >>> myralink.getId()
	'myralink'

For good measure, we also set a title and test for it.	
	>>> myralink.setTitle('My Risk Assessment Link')
	>>> myralink.Title()
	'My Risk Assessment Link'

