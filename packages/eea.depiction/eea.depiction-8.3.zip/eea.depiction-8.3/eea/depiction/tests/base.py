""" Base for tests
"""

import eea.depiction
import eea.rdfmarshaller
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from Zope2.App import zcml

P_VIDEO = True
try:
    import p4a.video
except ImportError:
    P_VIDEO = False


@onsetup
def setup_depiction():
    """ Setup
    """
    fiveconfigure.debug_mode = True

    if P_VIDEO:
        zcml.load_config('test.zcml', p4a.video)

    zcml.load_config('overrides.zcml', eea.depiction)
    zcml.load_config('configure.zcml', eea.depiction)
    zcml.load_config('configure.zcml', eea.rdfmarshaller)

    fiveconfigure.debug_mode = False

    if P_VIDEO:
        PloneTestCase.installPackage('p4a.video')


setup_depiction()
PloneTestCase.setupPloneSite(extension_profiles=(
    'eea.depiction:default',))


class DepictionTestCase(PloneTestCase.FunctionalTestCase):
    """ Depiction Test Case
    """
    pass


class DepictionFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    """ Depiction Functional Test Case
    """
    pass
