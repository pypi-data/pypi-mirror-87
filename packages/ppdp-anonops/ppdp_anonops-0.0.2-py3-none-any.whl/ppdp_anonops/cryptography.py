from .anonymizationOperationInterface import AnonymizationOperationInterface
from pm4py.objects.log.importer.xes import factory as xes_importer_factory
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from base64 import b64encode

import time


class Cryptography(AnonymizationOperationInterface):
    """Extract text from a PDF."""

    def __init__(self):
        super(Cryptography, self).__init__()
        self.cryptoKey = b'Sixteen byte key'
        self.cryptoIV = b'I am IV for AES!'
        self.cryptoSalt = "a.9_Oq1S*23xLgB"

    def HashEventAttribute(self, xesLog, targetedAttribute, matchAttribute=None, matchAttributeValue=None,  hashAlgo='ripemd160'):
        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                # Only hash if value is a match or no mathcing is required
                isMatch = matchAttribute in (None, '') or (matchAttribute in event.keys() and event[matchAttribute] == matchAttributeValue)

                if(isMatch and targetedAttribute in event.keys()):
                    # Only supress resource if activity value is a match
                    h = hashlib.new(hashAlgo)
                    h.update((self.cryptoSalt + str(event[targetedAttribute])).encode('utf-8'))
                    event[targetedAttribute] = h.hexdigest()

        return self.AddExtension(xesLog, 'cry', 'event', targetedAttribute)

    def EncryptEventAttribute(self, xesLog, targetedAttribute, matchAttribute=None, matchAttributeValue=None):
        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                # Only crypt if value is a match or no mathcing is required
                isMatch = matchAttribute in (None, '') or (matchAttribute in event.keys() and event[matchAttribute] == matchAttributeValue)

                if(isMatch and targetedAttribute in event.keys()):
                    cipher = AES.new(self.cryptoKey, AES.MODE_CBC, iv=self.cryptoIV)
                    event[targetedAttribute] = cipher.encrypt(pad(str(event[targetedAttribute]).encode('utf-8'), AES.block_size)).hex()

        return self.AddExtension(xesLog, 'cry', 'event', targetedAttribute)

    def HashCaseAttribute(self, xesLog, targetedAttribute, matchAttribute=None, matchAttributeValue=None, hashAlgo='ripemd160'):
        h = hashlib.new(hashAlgo)

        for case_index, case in enumerate(xesLog):
            # Only hash if value is a match or no mathcing is required
            isMatch = matchAttribute in (None, '') or (matchAttribute in case.attributes.keys() and case.attributes[matchAttribute] == matchAttributeValue)

            if(isMatch and targetedAttribute in case.attributes.keys()):
                h.update((self.cryptoSalt + str(case.attributes[targetedAttribute])).encode('utf-8'))
                case.attributes[targetedAttribute] = h.hexdigest()

        return self.AddExtension(xesLog, 'cry', 'case', targetedAttribute)

    def EncryptCaseAttribute(self, xesLog, targetedAttribute, matchAttribute=None, matchAttributeValue=None):
        for case_index, case in enumerate(xesLog):
            # Only crypt if value is a match or no mathcing is required
            isMatch = matchAttribute in (None, '') or (matchAttribute in case.attributes.keys() and case.attributes[matchAttribute] == matchAttributeValue)

            if(isMatch and targetedAttribute in case.attributes.keys()):
                cipher = AES.new(self.cryptoKey, AES.MODE_CBC, iv=self.cryptoIV)
                case.attributes[targetedAttribute] = cipher.encrypt(pad(str(case.attributes[targetedAttribute]).encode('utf-8'), AES.block_size)).hex()

        return self.AddExtension(xesLog, 'cry', 'case', targetedAttribute)
