from unittest.result import TestResult
from pyPhases.test.BaseTest import TestCase
from typing import Iterable
import unittest
from unittest.loader import TestLoader
from unittest.suite import TestSuite


class TestRun(unittest.TestCase):
    phaseTests: Iterable[TestCase] = []

    def testAll(self):
        pass

    def countTestCases(self):
        return len(self.phaseTests)

    def run(self, result=None):
        testSuite = TestSuite()
        loader = TestLoader()

        for testCase in self.phaseTests:
            tests = loader.loadTestsFromTestCase(testCase)
            testSuite.addTests(tests)
        return testSuite.run(result)
