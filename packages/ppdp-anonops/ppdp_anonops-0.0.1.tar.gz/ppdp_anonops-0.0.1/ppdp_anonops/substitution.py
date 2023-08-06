from .anonymizationOperationInterface import AnonymizationOperationInterface
import random


class Substitution(AnonymizationOperationInterface):

    def __init__(self):
        super(Substitution, self).__init__()

    def SubstituteEventAttributeValue(self, xesLog, targetAttribute, sensitiveAttributeValues):
        insensitiveAttributes = []
        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if (targetAttribute in event.keys() and event[targetAttribute] not in insensitiveAttributes and event[targetAttribute] not in sensitiveAttributeValues):
                    insensitiveAttributes.append(event[targetAttribute])

        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if (targetAttribute in event.keys() and event[targetAttribute] in sensitiveAttributeValues):
                    event[targetAttribute] = insensitiveAttributes[random.randint(0, len(insensitiveAttributes) - 1)]

        return self.AddExtension(xesLog, 'sub', 'event', targetAttribute)
