from .anonymizationOperationInterface import AnonymizationOperationInterface
from copy import deepcopy
import random
from datetime import timedelta


class Addition(AnonymizationOperationInterface):
    """WARNING / TODO: Currently the value-matching for the matching attribute takes only the last event in the trace into consideration!"""
    # Possibly set up a lambda based filter, user can enter a python lambda that will be evaluated

    def __init__(self):
        super(Addition, self).__init__()

    def AddEventAtRandomPlaceInTrace(self, xesLog, eventTemplate, matchAttribute=None, matchAttributeValue=None, matchOperation=None, doNotUseRandomlyGeneratedTimestamp=False):
        return self.AddEventAtPositionX(xesLog, eventTemplate, matchAttribute, matchAttributeValue, matchOperation, doNotUseRandomlyGeneratedTimestamp, -1)

    def AddEventFirstInTrace(self, xesLog, eventTemplate, matchAttribute=None, matchAttributeValue=None, matchOperation=None, doNotUseRandomlyGeneratedTimestamp=False):
        return self.AddEventAtPositionX(xesLog, eventTemplate, matchAttribute, matchAttributeValue, matchOperation, doNotUseRandomlyGeneratedTimestamp, 0)

    def AddEventLastInTrace(self, xesLog, eventTemplate, matchAttribute=None, matchAttributeValue=None, matchOperation=None, doNotUseRandomlyGeneratedTimestamp=False):
        return self.AddEventAtPositionX(xesLog, eventTemplate, matchAttribute, matchAttributeValue, matchOperation, doNotUseRandomlyGeneratedTimestamp, -2)

    def AddEventAtPositionX(self, xesLog, eventTemplate, matchAttribute=None, matchAttributeValue=None, matchOperation=None, doNotUseRandomlyGeneratedTimestamp=False, position=-1):
        for case_index, case in enumerate(xesLog):
            newEvent = self.__getEvent(eventTemplate)
            traceLength = len(case)
            lastEvent = case[traceLength - 1]

            # Either no attribute match is required or the lastEvent is a match
            isMatch = (matchAttribute in ('', None) and matchAttributeValue in ('', None)) or matchOperation is None or matchOperation(case, matchAttribute, matchAttributeValue)

            if(isMatch):
                newPos = position

                if(position == -1):
                    newPos = random.randint(0, traceLength)
                elif(position == -2):
                    newPos = traceLength

                if (not doNotUseRandomlyGeneratedTimestamp):
                    newEvent["time:timestamp"] = self.__getRandomFittingTimestamp(case, newPos)

                case.insert(newPos, newEvent)

        self.AddExtension(xesLog, "add", "case", "trace")
        return xesLog

    def __getEvent(self, eventTemplate):
        newEvent = {}
        for attribute in eventTemplate:
            newEvent[attribute['Name']] = attribute['Value']
        return newEvent

    def __getRandomFittingTimestamp(self, events, newIndex):
        traceLength = len(events)

        # Randomly generate timestamp fitting the event into the trace
        if (newIndex == 0):
            minTime = events[0]["time:timestamp"] - timedelta(seconds=random.randint(1, 3600))
            maxTime = events[0]["time:timestamp"]
        elif (newIndex == traceLength - 1):
            minTime = events[traceLength - 2]["time:timestamp"]
            maxTime = events[traceLength - 1]["time:timestamp"]
        elif (newIndex == traceLength):  # Event appended at the end
            minTime = events[traceLength - 1]["time:timestamp"]
            maxTime = minTime + timedelta(seconds=random.randint(1, 3600))
        else:
            minTime = events[newIndex - 1]["time:timestamp"]
            maxTime = events[newIndex]["time:timestamp"]

        secDelta = random.randint(0, (maxTime - minTime).total_seconds())
        return minTime + timedelta(seconds=secDelta)
