from unittest import TestCase
import os
from ppdp_anonops import Substitution
from pm4py.objects.log.importer.xes import factory as xes_importer


class TestSubstitution(TestCase):
    def getTestXesLog(self):
        xesPath = os.path.join(os.path.dirname(__file__), 'resources', 'running_example.xes')
        return xes_importer.apply(xesPath)

    def test_substituteResources(self):
        log = self.getTestXesLog()

        s = Substitution()

        frequency = {"Sean": 0, "Sara": 0}
        for case_index, case in enumerate(log):
            for event_index, event in enumerate(case):
                if event["org:resource"] in frequency.keys():
                    frequency[event["org:resource"]] += 1

        self.assertGreater(frequency["Sean"], 0)
        self.assertGreater(frequency["Sara"], 0)

        log = s.SubstituteEventAttributeValue(log, "org:resource", ["Sean", "Sara"])

        frequency = {"Sean": 0, "Sara": 0}
        for case_index, case in enumerate(log):
            for event_index, event in enumerate(case):
                if event["org:resource"] in frequency.keys():
                    frequency[event["org:resource"]] += 1

        self.assertEqual(frequency["Sean"], 0)
        self.assertEqual(frequency["Sara"], 0)
