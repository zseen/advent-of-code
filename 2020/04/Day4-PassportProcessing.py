import unittest
import re
from typing import List

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"

PASSPORT_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}
PASSPORT_FIELDS_TO_ACCEPTABLE_VALUES = {"byr": '[1][9][2-9][0-9]|[2][0][0][1-2]', "iyr": '[2][0][1][0-9]|[2][0][2][0]',
                                        "eyr": '[2][0][2][0-9]|[2][0][3][0]',
                                        "hgt": '[1][5-8][0-9][c][m]|[1][9][0-3][c][m]|[5][9][i][n]|[6][0-9][i][n]|[7][0-6][i][n]',
                                        "hcl": '[#][0-9a-f]{6}', "ecl": '(amb)|(blu)|(brn)|(gry)|(grn)|(hzl)|(oth)',
                                        "pid": '[0-9]{9}', "cid": '\s|.'}


P_F_T_A_V =  {"byr": (1920, 2002), "iyr": (2010, 2020),
            "eyr": (2020, 2030),
            "hgt": [(150, 193), (59, 76)],
            "hcl": ["#", 0, 9, "a", "f"],
            "ecl": ["amb", "blu","brn", "gry","grn","hzl","oth"],
            "pid": (0, 9), "cid": [True]}
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
            passportFieldToDataCollection[str(entry[0])] = str(entry[1])
        fieldToDataList.append(passportFieldToDataCollection)
    return fieldToDataList


def isPassportValidInitialCheck(passport: dict):
    passportFields = set(passport.keys())
    if passportFields == set(PASSPORT_FIELDS):
        return True
    return PASSPORT_FIELDS - passportFields == {COUNTRY_ID_FIELD}


def isDataInFieldAcceptable(field, data):
    pattern = PASSPORT_FIELDS_TO_ACCEPTABLE_VALUES[field]
    match = re.match(pattern, data)
    return match is not None






def isPassportValid(passport: dict):
    for field, data in passport.items():
        # print(field, data)
        if not isDataInFieldAcceptable(field, data):
            return False
    return True


def getValidPassportsNum(passports: List):
    validPassportCounter = 0
    for passport in passports:
        #print("passport:", passport)
        if isPassportValidInitialCheck(passport) and isPassportValid(passport):
            validPassportCounter += 1
    return validPassportCounter

#-------------------------

def isDataInFieldAcceptableAlternative(field, data):

    # P_F_T_A_V =  {"byr": (1920, 2002), "iyr": (2010, 2020),
    #             "eyr": (2020, 2030),
    #             "hgt": [(150, 193), (59, 76)],
    #             "hcl": ["#", 0, 9, "a", "f"],
    #             "ecl": ["amb", "blu","brn", "gry","grn","hzl","oth"],
    #             "pid": (0, 9), "cid": [None, True]}
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
        if data[-1] == "m" or data[-1] =="n":
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

def getValidPassportsNumALTERNAIVE(passports: List):
    validPassportCounter = 0
    for passport in passports:
        #print("passport:", passport)
        if isPassportValidInitialCheck(passport) and isPassportValidAlt(passport):
            validPassportCounter += 1
    return validPassportCounter

def isPassportValidAlt(passport: dict):
    for field, data in passport.items():
        # print(field, data)
        if not isDataInFieldAcceptableAlternative(field, data):
            return False
    return True



# byr: [1][9][2-9][0-9]|[2][0][0][1-2]
# iyr: [2][0][1][0-9]|[2][0][2][0]
# eyr: [2][0][2][0-9]|[2][0][3][0]
# hgt: [1][5-8][0-9][c][m]|[1][9][0-3][c][m]|[5][9][i][n]|[6][0-9][i][n]|[7][0-6][i][n]
# hcl: [#][0-9a-f]{6}
# ecl: (amb)|(blu)|(brn)|(gry)|(grn)|(hzl)|(oth)
# pid: [0-9]{9}



l = getInput()
# print(l)
c = getValidPassportsNum(l)  # 112 is too high
print(c)

v = getValidPassportsNumALTERNAIVE(l)  # 111 is correct
print(v)
