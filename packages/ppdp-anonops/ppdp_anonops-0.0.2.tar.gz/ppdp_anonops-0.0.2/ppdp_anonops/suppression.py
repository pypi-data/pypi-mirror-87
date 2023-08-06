from .anonymizationOperationInterface import AnonymizationOperationInterface
from pm4py.objects.log.importer.xes import factory as xes_importer_factory
import hashlib


class Suppression(AnonymizationOperationInterface):
    """Replace a """

    def __init__(self):
        super(Suppression, self).__init__()

    def SuppressEvent(self, xesLog, matchAttribute, matchAttributeValue):
        for t_idx, trace in enumerate(xesLog):
            # filter out all the events with matching attribute values - matchAttribute "concept:name" at event level typically represents the performed activity
            trace[:] = [event for event in trace if (matchAttribute not in event.keys() or event[matchAttribute] != matchAttributeValue)]
        return self.AddExtension(xesLog, 'sup', 'event', 'event')

    def SuppressCaseByTraceLength(self, xesLog, maxLength):
        # Filter for cases with acceptable length
        xesLog[:] = [trace for trace in xesLog if len(trace) <= maxLength]
        return self.AddExtension(xesLog, 'sup', 'case', 'case')

    def SuppressEventAttribute(self, xesLog, suppressedAttribute, matchAttribute=None, matchAttributeValue=None):
        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                isMatch = (matchAttribute is None and matchAttributeValue is None) or (matchAttribute in event.keys() and event[matchAttribute] == matchAttributeValue)

                if (isMatch):
                    # Only supress resource if activity value is a match
                    event[suppressedAttribute] = None
        return self.AddExtension(xesLog, 'sup', 'event', suppressedAttribute)

    def SuppressCase(self, xesLog, matchAttribute, matchAttributeValue):
        # filter out all the cases with matching attribute values
        xesLog[:] = [case for case in xesLog if (matchAttribute not in case.attributes.keys() or case.attributes[matchAttribute] != matchAttributeValue)]

        return self.AddExtension(xesLog, 'sup', 'case', 'case')

    def SuppressCaseAttribute(self, xesLog, suppressedAttribute, matchAttribute=None, matchAttributeValue=None):
        for case_index, case in enumerate(xesLog):
            isMatch = (matchAttribute is None and matchAttributeValue is None) or (matchAttribute in case.attributes.keys() and case.attributes[matchAttribute] == matchAttributeValue)

            if (isMatch):
                # Only supress resource if activity value is a match
                case.attributes[suppressedAttribute] = None
        return self.AddExtension(xesLog, 'sup', 'case', suppressedAttribute)
