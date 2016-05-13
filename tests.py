''' CROPS test runner '''

import unittest
import sys
import argparse

def run_unittests(udir):
    ''' Execute Unit Tests '''
    tests = unittest.TestLoader().discover('tests/functional/'+udir)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    return result.wasSuccessful()

def run_functional_tests(fdir):
    ''' Execute Functional Tests '''
    tests = unittest.TestLoader().discover('tests/functional/'+fdir)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    return result.wasSuccessful()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--functionaldir", "-f", default="",
                        help="Directory of functional tests")
    parser.add_argument("--unitdir", "-u", default="",
                        help="Directory of functional tests")

    args = parser.parse_args()

    print "#" * 70
    print "Test Runner: Unit tests"
    print "#" * 70
    unit_results = run_unittests(args.unitdir)

    print "#" * 70
    print "Test Runner: Functional tests"
    print "#" * 70
    functional_results = run_functional_tests(args.functionaldir)

    if unit_results and functional_results:
        sys.exit(0)
    else:
        sys.exit(1)
