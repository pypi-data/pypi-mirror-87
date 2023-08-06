from unittest import TestCase
import os
from ppdp_anonops import Suppression
from pm4py.objects.log.importer.xes import factory as xes_importer


class TestSuppression(TestCase):
    def getTestXesLog(self):
        xesPath = os.path.join(os.path.dirname(__file__), 'resources', 'running_example.xes')
        return xes_importer.apply(xesPath)

    def test_suppressEvent(self):
        log = self.getTestXesLog()

        s = Suppression()

        no_traces = len(log)
        no_events = sum([len(trace) for trace in log])
        self.assertEqual(no_traces, 6)
        self.assertEqual(no_events, 42)

        log = s.SuppressEvent(log, "concept:name", "reinitiate request")  # concept:name is activity

        no_traces = len(log)
        no_events = sum([len(trace) for trace in log])
        self.assertEqual(no_traces, 6)
        self.assertEqual(no_events, 39)

    def test_suppressEventAttribute(self):
        log = self.getTestXesLog()

        s = Suppression()

        matchAttribute = "concept:name"
        matchAttributeValue = "reinitiate request"
        supressedAttribute = "org:resource"

        no_traces = len(log)
        no_events = sum([len(trace) for trace in log])
        counter = 0

        for case_index, case in enumerate(log):
            for event_index, event in enumerate(case):
                if (event[matchAttribute] == matchAttributeValue):
                    if(event[supressedAttribute] == None):
                        counter += 1

        self.assertEqual(no_traces, 6)
        self.assertEqual(no_events, 42)
        self.assertEqual(counter, 0)

        # Supress resource if activity matches 'reinitiate request'
        log = s.SuppressEventAttribute(log, supressedAttribute, matchAttribute, matchAttributeValue)

        no_traces = len(log)
        no_events = sum([len(trace) for trace in log])
        counter = 0

        for case_index, case in enumerate(log):
            for event_index, event in enumerate(case):
                if (event[matchAttribute] == matchAttributeValue):
                    if(event[supressedAttribute] == None):
                        counter += 1

        self.assertEqual(no_traces, 6)
        self.assertEqual(no_events, 42)
        self.assertEqual(counter, 3)

    def test_suppressCaseByTraceLength(self):
        log = self.getTestXesLog()

        s = Suppression()

        no_traces = len(log)
        no_events = sum([len(trace) for trace in log])
        self.assertEqual(no_traces, 6)
        self.assertEqual(no_events, 42)

        log = s.SuppressCaseByTraceLength(log, 5)

        no_traces = len(log)
        no_events = sum([len(trace) for trace in log])
        self.assertEqual(no_traces, 4)
        self.assertEqual(no_events, 20)
