#!/usr/bin/env python

import os
import sys
import unittest

REGRESSION_TEST_DIRNAME = 'regressiontests'
REGRESSION_TEST_DIR = REGRESSION_TEST_DIRNAME

sys.path.insert(0, '../src/')


def load_suite_tests(only=None):
    only_module, only_test_case = None, None
    if only:
        args = only.split(".")
        only_module, only_test_case, only_function = args[0], (args[1:] and args[1] or None), (args[2:] and args[2] or None)
    suites = []
    for dirpath, dirnames, filenames in os.walk(REGRESSION_TEST_DIR):
        for f in filenames:
            basename, ext = os.path.splitext(f)
            if (ext == '.py') and (not only_module or (only_module == basename)):
                modname = "%s.%s" % ('.'.join(dirpath.split('/')), basename)
                package = __import__(modname, globals(), locals(), [], 0)
                mod = sys.modules[modname]
                if hasattr(mod, 'suite'):
                    suite = mod.suite()
                    if only_test_case:
                        suite._tests = [t for t in suite._tests if t.__class__.__name__ == only_test_case]
                        if only_function:
                            suite._tests = [t for t in suite._tests if t._testMethodName == only_function]
                    suites.append(suite)
    return suites


if __name__ == '__main__':
    # Doctests.
    import doctest
    doctest_response = doctest.testfile("../src/colbert/daterange.py")

    only = None
    if len(sys.argv) > 1:
        only = sys.argv[1]
    suites = load_suite_tests(only=only)
    suite = unittest.TestSuite(suites)
    unittest_response = unittest.TextTestRunner(verbosity=2).run(suite)

    sys.exit(bool(doctest_response.failed or unittest_response.errors))
