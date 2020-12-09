import unittest
import re
from typing import List
import itertools

INPUT_FILE = "input.txt"
TEST_INPUT_FILE_ONE = "test_input_part_1.txt"
TEST_INPUT_FILE_TWO = "test_input_part_2.txt"

PASSPORT_FIELDS_TO_VALID_REGEX_VALUES = {"byr": '19[2-9][0-9]|200[0-2]',
                                              "iyr": '201[0-9]|2020',
                                              "eyr": '202[0-9]|2030',
                                              "hgt": '1[5-8][0-9]cm|19[0-3]cm|59in|6[0-9]in|7[0-6]in',
                                              "hcl": '#[0-9a-f]{6}',
                                              "ecl": 'amb|blu|brn|gry|grn|hzl|oth',
                                              "pid": '[0-9]{9}', "cid": '.*'}

COUNTRY_ID_FIELD = "cid"


def getInput(inputFile):
    with open(inputFile, "r") as inputFile:
        allDataForRawPassports = inputFile.read()
        allDataForRawPassports = allDataForRawPassports.split("\n\n")

        allRawPassports = []
        for rawPassports in allDataForRawPassports:
            rawPassports = rawPassports.split()
            allRawPassports.append(rawPassports)

        return getAllPassportsWithFieldToData(allRawPassports)



def createPassportDict(rawPassport: List):
    passportDict = dict()
    for entry in rawPassport:
        entry = entry.split(':')
        passportDict[entry[0]] = entry[1]
    return passportDict


def getAllPassportsWithFieldToData(rawPassportsCollection: List):
    return [createPassportDict(rawPassport) for rawPassport in
                     rawPassportsCollection]


def isPassportFormatValid(passport: dict):
    passportFields = set(passport.keys())
    allPossiblePassportFields = set(PASSPORT_FIELDS_TO_VALID_REGEX_VALUES.keys())
    return (allPossiblePassportFields - {COUNTRY_ID_FIELD}).issubset(passportFields)


def isPassportValid(passport: dict):
    if not isPassportFormatValid(passport):
        return False

    for field, data in passport.items():
        if not isDataInFieldValid(data, field):
            return False
    return True


def isDataInFieldValid(data, field) -> bool:
    pattern = PASSPORT_FIELDS_TO_VALID_REGEX_VALUES[field]
    match = re.fullmatch(pattern, data)
    return match is not None


def getValidPassportsCount(passports: List, validatingFunc: callable):
    return sum(map(lambda passport: validatingFunc(passport), passports))


def main():
    passports = getInput(INPUT_FILE)
    print(getValidPassportsCount(passports, isPassportFormatValid))  # 233
    print(getValidPassportsCount(passports, isPassportValid))  # 111


class ValidPassportCounterTest(unittest.TestCase):
    def test_getValidPassportsCount_onlyFormatRequirementChecked_correctNumValidPassportsReturned(self):
        passports = getInput(TEST_INPUT_FILE_ONE)
        self.assertEqual(2, getValidPassportsCount(passports, isPassportFormatValid))

    def test_getValidPassportsCount_dataInFieldsChecked_correctNumValidPassportsReturned(self):
        passports = getInput(TEST_INPUT_FILE_TWO)
        self.assertEqual(4, getValidPassportsCount(passports, isPassportValid))


if __name__ == '__main__':
    # main()
    unittest.main()
