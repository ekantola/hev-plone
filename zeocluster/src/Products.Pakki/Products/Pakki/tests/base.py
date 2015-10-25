from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_pakki_policy():
    """Set up additional products required for the Pakki site policy.

    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """

    # Load the ZCML configuration for the Products.Pakki package.
    fiveconfigure.debug_mode = True
    import Products.Pakki
    zcml.load_config('configure.zcml', Products.Pakki)
    fiveconfigure.debug_mode = False

    # We need to tell the testing frameworkj that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML.

    ztc.installPackage('Products.Pakki')
    ztc.installPackage('Products.PakkiLayout')

# The order here is important: We first call the (deferred) function
# whidh installs the products we nede for the Pakki package. Then,
# we let PloneTestCase set up this product on installation.
setup_pakki_policy()
ptc.setupPloneSite(products=['Products.Pakki'])

class PakkiTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code here.
    """
