from unittest import TestCase
import os
from ppdp_anonops import Generalization
from ppdp_anonops.utils import TaxonomyTree, TaxonomyTreeNode
from pm4py.objects.log.importer.xes import factory as xes_importer


class TestGeneralization(TestCase):
    def getTestXesLog(self):
        xesPath = os.path.join(os.path.dirname(__file__), 'resources', 'running_example.xes')
        return xes_importer.apply(xesPath)

    def test_01_generalizationTime(self):
        log = self.getTestXesLog()
        s = Generalization()

        no_events = sum([len(trace) for trace in log])

        log = s.GeneralizeEventTimeAttribute(log, "time:timestamp", "seconds")
        self.assertEqual(self.getTime(log, "time:timestamp", "seconds"), 0)

        log = s.GeneralizeEventTimeAttribute(log, "time:timestamp", "minutes")
        self.assertEqual(self.getTime(log, "time:timestamp", "minutes"), 0)

        log = s.GeneralizeEventTimeAttribute(log, "time:timestamp", "hours")
        self.assertEqual(self.getTime(log, "time:timestamp", "hours"), 0)

        log = s.GeneralizeEventTimeAttribute(log, "time:timestamp", "days")
        self.assertEqual(self.getTime(log, "time:timestamp", "days"), 0)

        log = s.GeneralizeEventTimeAttribute(log, "time:timestamp", "months")
        self.assertEqual(self.getTime(log, "time:timestamp", "months"), no_events)  # no_events as default value for days is 1 and not 0 (0 is an ivalid day-of-month)

    def test_02_generalizationResourceTaxonomy(self):
        self.Fail("Test is not redesigned to count depth from leafnode => TODO: Restructure")
        tax = TaxonomyTree()
        n_healthcare = tax.AddNode("Healthcare")

        n_hospital = n_healthcare.AddChildNode("Hospital")
        n_surgery = n_hospital.AddChildNode("Surgery")
        n_surgery.AddChildNode("Surgeon")
        n_surgery.AddChildNode("Anesthesist")
        n_surgery.AddChildNode("Caretaker")
        n_diagnostic = n_hospital.AddChildNode("Diagnostic")
        n_diagnostic.AddChildNode("Internist")
        n_diagnostic.AddChildNode("Pharmacist")
        n_diagnostic.AddChildNode("Caretaker")

        n_insurance = n_healthcare.AddChildNode("Insurance")
        n_insurance.AddChildNode("Bookkeeping")
        n_it = n_insurance.AddChildNode("IT")
        n_insurance.AddChildNode("Consulting")
        n_support = n_insurance.AddChildNode("Support")
        n_it.AddChildNode("Ellen")
        n_it.AddChildNode("Mike")
        n_it.AddChildNode("Pete")
        n_support.AddChildNode("Sara")
        n_support.AddChildNode("Sean")
        n_support.AddChildNode("Sue")

        n_aerospace = tax.AddNode("Aerospace")
        n_it = tax.AddNode("IT")

        log = self.getTestXesLog()
        s = Generalization()

        bCountIT = 0
        bCountSupport = 0
        for case_index, case in enumerate(log):
            for event_index, event in enumerate(case):
                if event["org:resource"] in ["Ellen", "Mike", "Pete"]:
                    bCountIT += 1
                elif event["org:resource"] in ["Sara", "Sean", "Sue"]:
                    bCountSupport += 1

        log = s.GeneralizeEventAttributeByTaxonomyTreeDepth(log, "org:resource", tax, 3)

        aCountIT = 0
        aCountSupport = 0
        for case_index, case in enumerate(log):
            for event_index, event in enumerate(case):
                if event["org:resource"] == "IT":
                    aCountIT += 1
                elif event["org:resource"] == "Support":
                    aCountSupport += 1

        self.assertEqual(aCountIT, bCountIT, "Before and After count of resources expected does not match")
        self.assertEqual(aCountSupport, bCountSupport, "Before and After count of resources expected does not match")

        # Test again with higher level of generalization
        log = self.getTestXesLog()
        s = Generalization()
        log = s.GeneralizeEventAttributeByTaxonomyTreeDepth(log, "org:resource", tax, 2)

        aCountInsurance = 0
        for case_index, case in enumerate(log):
            for event_index, event in enumerate(case):
                if event["org:resource"] == "Insurance":
                    aCountInsurance += 1

        self.assertEqual(aCountIT + aCountSupport, aCountInsurance, "Before and After count of resources expected does not match")

    def getTime(self, xesLog, dateTimeAttribute, generalizationLevel):
        ret = 0

        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if(generalizationLevel == "seconds"):
                    ret += event[dateTimeAttribute].microsecond

                if(generalizationLevel == "minutes"):
                    ret += event[dateTimeAttribute].second

                if(generalizationLevel == "hours"):
                    ret += event[dateTimeAttribute].minute

                if(generalizationLevel == "days"):
                    ret += event[dateTimeAttribute].hour

                if(generalizationLevel == "months"):
                    ret += event[dateTimeAttribute].day

                if(generalizationLevel == "years"):
                    ret += event[dateTimeAttribute].month
        return ret
