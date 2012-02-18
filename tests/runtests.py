import unittest
import os, sys

REGRESSION_TEST_DIRNAME='regressiontests'
REGRESSION_TEST_DIR = os.path.join(os.path.dirname(__file__), REGRESSION_TEST_DIRNAME)

sys.path.insert(0,'../src/')


def load_suite_tests():
    suites = []
    for dirpath, dirnames, filenames in os.walk(REGRESSION_TEST_DIR):
        for f in filenames:
            basename, ext = os.path.splitext(f)
            if (ext == '.py'): # and (f != '__init__.py'):
                modname = "%s.%s" % ('.'.join(dirpath.split('/')), basename)
                package = __import__(modname, globals(), locals(), [], -1)
                mod = sys.modules[modname]
                if hasattr(mod, 'suite'):
                    suites.append(mod.suite())

    return suites


if __name__ == '__main__':
    suites = load_suite_tests()
    suite = unittest.TestSuite(suites)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
