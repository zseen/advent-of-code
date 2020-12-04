import unittest
import re
from typing import List

INPUT_FILE = "input.txt"
TEST_INPUT_FILE_ONE = "test_input_1.txt"
TEST_INPUT_FILE_TWO = "test_input_2.txt"

PASSPORT_FIELDS_TO_ACCEPTABLE_REGEX_VALUES = {"byr": '[1][9][2-9][0-9]|[2][0][0][1-2]',
                                              "iyr": '[2][0][1][0-9]|[2][0][2][0]',
                                              "eyr": '[2][0][2][0-9]|[2][0][3][0]',
                                              "hgt": '[1][5-8][0-9][c][m]|[1][9][0-3][c][m]|[5][9][i][n]|[6][0-9][i][n]|[7][0-6][i][n]',
                                              "hcl": '[#][0-9a-f]{6}',
                                              "ecl": '(amb)|(blu)|(brn)|(gry)|(grn)|(hzl)|(oth)',
                                              "pid": '[0-9]{9}$', "cid": '\s|.'}

COUNTRY_ID_FIELD = "cid"


def getInput(inputFile):
    dataForAllPassports = [[]]

    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            if line == "\n":
                dataForAllPassports.append([])
            else:
                line = line.strip("\n")
                lineSplit = re.split(' ', line)
                dataForAllPassports[-1].extend(lineSplit)

    allPassportsWithFieldToData: List = getAllPassportsWithFieldToData(dataForAllPassports)
    return allPassportsWithFieldToData


def createPassportWithFieldToData(rawPassport: List):
    passportAllFieldsToData = dict()
    for entry in rawPassport:
        entry = entry.split(':')
        passportAllFieldsToData[str(entry[0])] = str(entry[1])
    return passportAllFieldsToData


def getAllPassportsWithFieldToData(rawPassportsCollection: List):
    allPassportsWithFieldToData: List = []
    for rawPassport in rawPassportsCollection:
        allPassportsWithFieldToData.append(createPassportWithFieldToData(rawPassport))
    return allPassportsWithFieldToData


def isPassportFormatValid(passport: dict):
    passportFields = set(passport.keys())
    allPassportFields = set(PASSPORT_FIELDS_TO_ACCEPTABLE_REGEX_VALUES.keys())
    if passportFields == allPassportFields:
        return True
    return allPassportFields - passportFields == {COUNTRY_ID_FIELD}


def isPassportValid(passport: dict):
    if not isPassportFormatValid(passport):
        return False

    for field, data in passport.items():
        if not isDataInFieldAcceptable(data, field):
            return False
    return True


def isDataInFieldAcceptable(data, field) -> bool:
    pattern = PASSPORT_FIELDS_TO_ACCEPTABLE_REGEX_VALUES[field]
    match = re.match(pattern, data)
    # match is either an object or None, the "is not None" part is only there to express that a boolean is returned in both cases (match found or not)
    return match is not None


def getValidPassportsCount(passports: List, validatingFunc):
    validPassportCounter = 0
    for passport in passports:
        if validatingFunc(passport):
            validPassportCounter += 1
    return validPassportCounter


# This function below will be deleted, just wanted to show this abomination
def isDataInFieldAcceptableAlternative(field, data):
    if field == "byr":
        dataInt = int(data)
        if 1920 <= dataInt <= 2002:
            return True
    elif field == "iyr":
        dataInt = int(data)
        if 2010 <= dataInt <= 2020:
            return True
    elif field == "eyr":
        dataInt = int(data)
        if 2020 <= dataInt <= 2030:
            return True
    elif field == "hgt":
        if data[-1] == "m" or data[-1] == "n":
            if data[-1] == "m":
                if 150 <= int(data[0:len(data) - 2]) <= 193:
                    return True
            if data[-1] == "n":
                if 59 <= int(data[0:len(data) - 2]) <= 76:
                    return True
        return False
    elif field == "hcl":
        if len(data) != 7:
            return False
        if data[0] != "#":
            return False
        poss = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
        for char in data[1:]:
            if char not in poss:
                return False
        return True
    elif field == "ecl":
        return data in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
    elif field == "pid":
        if len(data) != 9:
            return False
        for char in data:
            if not char.isdigit():
                return False
        return True
    elif field == "cid":
        return True

    return False


def main():
    passports = getInput(INPUT_FILE)
    print(getValidPassportsCount(passports, isPassportFormatValid))  # 233
    print(getValidPassportsCount(passports, isPassportValid))  # 111


class ValidPassportCounterTest(unittest.TestCase):
    def test_getValidPassportsCount_onlyFormatRequirementChecked_correctNumOfValidPassportsReturned(self):
        passports = getInput(TEST_INPUT_FILE_ONE)
        self.assertEqual(2, getValidPassportsCount(passports, isPassportFormatValid))

    def test_getValidPassportsCount_dataInFieldsChecked_correctNumOfValidPassportsReturned(self):
        passports = getInput(TEST_INPUT_FILE_TWO)
        self.assertEqual(4, getValidPassportsCount(passports, isPassportValid))


if __name__ == '__main__':
    # main()
    unittest.main()
