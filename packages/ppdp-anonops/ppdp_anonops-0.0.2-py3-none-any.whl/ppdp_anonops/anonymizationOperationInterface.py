import abc
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log.exporter.xes import factory as xes_exporter

from p_privacy_metadata.privacyExtension import privacyExtension


class AnonymizationOperationInterface(metaclass=abc.ABCMeta):
    def __init__(self):
        pass
        #    self.xesLogPath = xesLogPath
        #    self.xesLog = xes_importer.apply(xesLogPath)

        # @classmethod
        # def __subclasshook__(cls, subclass):
        #     return (hasattr(subclass, 'Process') and callable(subclass.Process))

        # @abc.abstractmethod
        # def Process(self, path: str, parameter):
        #     """Perform the anonymization operation on th xes log"""
        #     raise NotImplementedError

        # def ExportLog(self, xesExportLogPath):
        #    xes_exporter.export_log(self.xesLog, xesExportLogPath)

    def AddExtension(self, xesLog, anonOp, level, target):
        # adding privacy extension here....
        prefix = 'privacy:'
        uri = 'paper_version_uri/privacy.xesext'

        privacy = privacyExtension(xesLog, prefix, uri)

        #privacy.set_anonymizer('substitution', 'event', 'concept:name')
        privacy.set_anonymizer(anonOp, level, target)
        # End of adding extension

        return xesLog

    def getEventAttributes(self, xes_log):
        event_attribs = []
        for case_index, case in enumerate(xes_log):
            for event_index, event in enumerate(case):
                for key in event.keys():
                    if key not in event_attribs:
                        event_attribs.append(key)
        return event_attribs

    def _getEventAttributeValues(self, xesLog, attribute):
        values = []

        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if(attribute in event.keys()):
                    values.append(event[attribute])

        return values

    def _getCaseAttributeValues(self, xesLog, attribute):
        return [case[attribute] for case_index, case in enumerate(xesLog)]

    def _getEventAttributesTuples(self, xesLog, clusterRelevantAttributes):
        tuples = []

        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                t = tuple((event[attribute] if attribute in event.keys() else 0) for attribute in clusterRelevantAttributes)
                if (t not in tuples):
                    tuples.append(t)

        return tuples
