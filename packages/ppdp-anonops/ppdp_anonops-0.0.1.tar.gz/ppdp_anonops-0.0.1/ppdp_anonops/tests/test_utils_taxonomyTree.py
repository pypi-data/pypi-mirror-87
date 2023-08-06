from unittest import TestCase
import os
from ppdp_anonops.utils import *
import logging
import sys


class Test_Utils_TaxonomyTree(TestCase):
    def __generateTestTree(self):
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

        return tax

    def __getTreeJson(self):
        return '[{"text":"Klinik","icon":true,"data":false,"children":[{"id":"j1_3","text":"Buchhaltung","icon":true,"data":false,"children":[],"type":"default"},{"id":"j1_2","text":"IT","icon":true,"data":false,"children":[{"id":"j1_5","text":"R&D","icon":true,"data":false,"children":[],"type":"default"},{"id":"j1_4","text":"Support","icon":true,"data":false,"children":[],"type":"default"}],"type":"default"}],"type":"default"}]'

    def test_01_CreateTree(self):
        tax = self.__generateTestTree()
        self.assertEqual(len(tax.RootNode.Children), 3)

    def test_02_SearchTree(self):
        tax = self.__generateTestTree()
        self.assertFalse(True, 'IMPLEMENT SEARCH OPERATIONS!')
        pass

    def test_03_ImportTree(self):
        tree = TaxonomyTree.CreateFromJSON(self.__getTreeJson(), "text", "children")

        node = tree.GetNodeByName("R&D")
        self.assertIsNotNone(node, "R&D node not found")
        self.assertEqual(node.GetNodePath(), "ROOT/Klinik/IT/R&D")

        node = tree.GetNodeByName("IT")
        self.assertIsNotNone(node, "IT node not found")
        self.assertEqual(node.GetNodePath(), "ROOT/Klinik/IT")
        self.assertEqual(len(node.Children), 2)

    def test_04_TreeAsDictByLevel(self):
        tax = self.__generateTestTree()

        # All nodes below level 2 get generalized to level 2 names
        dict = tax.GetGeneralizedDict_NodeNameToDepthXParentalName(2)
        for n in ['Surgeon', 'Anesthesist', 'Caretaker', 'Surgery', 'Internist', 'Pharmacist', 'Diagnostic']:
            self.assertTrue(n in dict.keys() and dict[n] == 'Hospital')
        for n in ['Bookkeeping', 'IT', 'Consulting', 'Support']:
            self.assertTrue(n in dict.keys() and dict[n] == 'Insurance')

        # All nodes below level 3 get generalized to level 3 names
        dict = tax.GetGeneralizedDict_NodeNameToDepthXParentalName(3)
        for n in ['Surgeon', 'Anesthesist']:
            self.assertTrue(n in dict.keys() and dict[n] == 'Surgery')
        for n in ['Caretaker', 'Internist', 'Pharmacist']:
            self.assertTrue(n in dict.keys() and dict[n] == 'Diagnostic')

        # As there are nodes on depth 4, but no nodes below them, the result should be empty
        dict = tax.GetGeneralizedDict_NodeNameToDepthXParentalName(4)
        self.assertEqual(len(dict.keys()), 0)
        pass

    def test_05_TreeAsDictLeafPath(self):
        tax = self.__generateTestTree()

        # All nodes below level 2 get generalized to level 2 names
        dict = tax.GetPathDict_NodeNamesUntilLeaf()

        self.assertTrue('Healthcare' in dict.keys())
        self.assertTrue('Hospital' in dict.keys())
        self.assertTrue('Bookkeeping' in dict.keys())
        self.assertTrue('Sean' in dict.keys())

        self.assertTrue(len(dict['Healthcare']) == 1 and dict['Healthcare'][-1] == 'Healthcare' and dict['Healthcare'][0] == 'Healthcare')
        self.assertTrue(len(dict['Hospital']) == 2 and dict['Hospital'][-1] == 'Hospital' and dict['Hospital'][0] == 'Healthcare')
        self.assertTrue(len(dict['Bookkeeping']) == 3 and dict['Bookkeeping'][-1] == 'Bookkeeping' and dict['Bookkeeping'][0] == 'Healthcare')
        self.assertTrue(len(dict['Sean']) == 4 and dict['Sean'][-1] == 'Sean' and dict['Sean'][0] == 'Healthcare')

        pass
