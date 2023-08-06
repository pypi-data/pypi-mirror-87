from unittest import TestCase
import os
from ppdp_anonops import Cryptography
from pm4py.objects.log.importer.xes import factory as xes_importer


class TestCryptography(TestCase):
    def getTestXesLog(self):
        xesPath = os.path.join(os.path.dirname(__file__), 'resources', 'running_example.xes')
        return xes_importer.apply(xesPath)

    def test_01_hashEvent(self):
        log = self.getTestXesLog()

        s = Cryptography()

        targetAttribute = "org:resource"
        #matchAttributeValue = "Ellen"

        frequency = []
        for case_index, case in enumerate(log):
            for event_index, event in enumerate(case):
                if event[targetAttribute] not in frequency:
                    frequency.append(event[targetAttribute])

        log = s.HashEventAttribute(log, targetAttribute)

        frequencyNew = []
        for case_index, case in enumerate(log):
            for event_index, event in enumerate(case):
                if event[targetAttribute] not in frequencyNew:
                    frequencyNew.append(event[targetAttribute])

        self.assertEqual(len(frequency), 6)
        self.assertEqual(len(frequencyNew), 6)

    def test_02_hashEventWithMatch(self):
        log = self.getTestXesLog()

        s = Cryptography()

        targetAttribute = "org:resource"
        matchAttribute = "concept:name"
        matchAttributeValue = "register request"

        frequency = []
        for case_index, case in enumerate(log):
            for event_index, event in enumerate(case):
                if event["org:resource"] not in frequency:
                    frequency.append(event["org:resource"])

        log = s.HashEventAttribute(log, targetAttribute, matchAttribute, matchAttributeValue)

        frequencyNew = []
        for case_index, case in enumerate(log):
            for event_index, event in enumerate(case):
                if event["org:resource"] not in frequencyNew:
                    frequencyNew.append(event["org:resource"])

        self.assertEqual(len(frequency), 6)
        self.assertEqual(len(frequencyNew), 9)

    def test_03_encryptEvent(self):
        log = self.getTestXesLog()

        s = Cryptography()

        targetAttribute = "org:resource"
        #matchAttributeValue = "Ellen"

        frequency = []
        for case_index, case in enumerate(log):
            for event_index, event in enumerate(case):
                if event["org:resource"] not in frequency:
                    frequency.append(event["org:resource"])

        log = s.EncryptEventAttribute(log, targetAttribute)

        frequencyNew = []
        for case_index, case in enumerate(log):
            for event_index, event in enumerate(case):
                if event["org:resource"] not in frequencyNew:
                    frequencyNew.append(event["org:resource"])

        self.assertEqual(len(frequency), 6)
        self.assertEqual(len(frequencyNew), 6)

    def test_04_encryptEventWithMatch(self):
        log = self.getTestXesLog()

        s = Cryptography()

        targetAttribute = "org:resource"
        matchAttribute = "concept:name"
        matchAttributeValue = "register request"

        frequency = []
        for case_index, case in enumerate(log):
            for event_index, event in enumerate(case):
                if event["org:resource"] not in frequency:
                    frequency.append(event["org:resource"])

        log = s.EncryptEventAttribute(log, targetAttribute, matchAttribute, matchAttributeValue)

        frequencyNew = []
        for case_index, case in enumerate(log):
            for event_index, event in enumerate(case):
                if event["org:resource"] not in frequencyNew:
                    frequencyNew.append(event["org:resource"])

        self.assertEqual(len(frequency), 6)
        self.assertEqual(len(frequencyNew), 9)
