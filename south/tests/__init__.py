
import unittest
import os
import sys
from functools import wraps
from django.conf import settings
from south.hacks import hacks

# Add the tests directory so fakeapp is on sys.path
test_root = os.path.dirname(__file__)
sys.path.append(test_root)

# Note: the individual test files are imported below this.

class Monkeypatcher(unittest.TestCase):

    """
    Base test class for tests that play with the INSTALLED_APPS setting at runtime.
    """

    def create_fake_app(self, name):
        
        class Fake:
            pass
        
        fake = Fake()
        fake.__name__ = name
        try:
            fake.migrations = __import__(name + ".migrations", {}, {}, ['migrations'])
        except ImportError:
            pass
        return fake


    def setUp(self):
        """
        Changes the Django environment so we can run tests against our test apps.
        """
        if getattr(self, 'installed_apps', None):
            hacks.set_installed_apps(self.installed_apps)
    
    
    def tearDown(self):
        """
        Undoes what setUp did.
        """
        if getattr(self, 'installed_apps', None):
            hacks.reset_installed_apps()

# Make sure skipUnless is available.
try:
    # skipUnless added in Python 2.7;
    from unittest import skipUnless
except ImportError:
    try: 
        # django.utils.unittest added in Django 1.3;
        from django.utils.unittest import skipUnless
    except ImportError:
        def skipUnless(condition, message):
            def decorator(testfunc):
                @wraps(testfunc)
                def wrapper(self):
                    if condition:
                        # Apply method
                        testfunc(self)
                    else:
                        # The skip exceptions are not available either...
                        print "Skipping", testfunc.__name__,"--", message
                return wrapper
            return decorator


# Try importing all tests if asked for (then we can run 'em)
try:
    skiptest = settings.SKIP_SOUTH_TESTS
except:
    skiptest = True

if not skiptest:
    from south.tests.db import *
    from south.tests.db_mysql import *
    from south.tests.logic import *
    from south.tests.autodetection import *
    from south.tests.logger import *
    from south.tests.inspector import *
    from south.tests.freezer import *
