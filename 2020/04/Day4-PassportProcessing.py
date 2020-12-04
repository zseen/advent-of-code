import unittest
import re
from typing import List

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"

PASSPORT_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}
COUNTRY_ID_FIELD = "cid"


def getInput():
    inputList = [[]]

    with open(INPUT_FILE, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            if line == "\n":
                inputList.append([])
            else:
                line = line.strip("\n")
                lineSplit = re.split('-|: | ', line)
                inputList[-1].extend(lineSplit)

    fieldToDataAllPassports = getFieldToData(inputList)
    return fieldToDataAllPassports

def getFieldToData(passportDataList):
    fieldToDataList = []
    for passport in passportDataList:
        passportFieldToDataCollection = dict()
        for entry in passport:
            entry = entry.split(':')
            passportFieldToDataCollection[entry[0]] = entry[1]
        fieldToDataList.append(passportFieldToDataCollection)
    return fieldToDataList

def isPassportValid(passport: dict):
    passportFields = set(passport.keys())
    if passportFields == set(PASSPORT_FIELDS):
        return True
    return PASSPORT_FIELDS - passportFields == {COUNTRY_ID_FIELD}

def getValidPassportsNum(passports: List):
    validPassportCounter = 0
    for passport in passports:
        if isPassportValid(passport):
            validPassportCounter += 1
    return validPassportCounter




l = getInput()
c = getValidPassportsNum(l)
print(c)
