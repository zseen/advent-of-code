import unittest
import re

INPUT_FILE = "input.txt"


class PasswordPolicy:
    def __init__(self, firstNum, secondNum, char, password):
        self.firstNum = firstNum
        self.secondNum = secondNum
        self.char = char
        self.password = password


def getPasswordPolicies():
    passwordPolicies = []
    with open(INPUT_FILE, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip()
            lineSplit = re.split('-|: | |\n', line)
            firstNum = lineSplit[0]
            secondNum = lineSplit[1]
            pwChar = lineSplit[2]
            password = lineSplit[3]
            passwordPolicy = PasswordPolicy(int(firstNum), int(secondNum), pwChar, password)
            passwordPolicies.append(passwordPolicy)

    return passwordPolicies


def getValidPasswordsCount(allPasswordPolicies, validatorFunc):
    validPasswordPoliciesCount = 0
    for passwordPolicy in allPasswordPolicies:
        if validatorFunc(passwordPolicy):
            validPasswordPoliciesCount += 1
    return validPasswordPoliciesCount


def isPasswordValid(passwordPolicy: PasswordPolicy):
    desiredCharCount = passwordPolicy.password.count(passwordPolicy.char)
    return passwordPolicy.firstNum <= desiredCharCount <= passwordPolicy.secondNum


# ----------------------------------------------------------------------------------------------------------------------
def isPasswordValidPos(passwordPolicy: PasswordPolicy):
    firstPositionChar = passwordPolicy.password[passwordPolicy.firstNum - 1]
    secondPositionChar = passwordPolicy.password[passwordPolicy.secondNum - 1]

    if firstPositionChar == secondPositionChar:
        return False

    return (firstPositionChar == passwordPolicy.char or secondPositionChar == passwordPolicy.char)


def main():
    allPasswordPolicies = getPasswordPolicies()
    print(getValidPasswordsCount(allPasswordPolicies, isPasswordValid))  # 636
    print(getValidPasswordsCount(allPasswordPolicies, isPasswordValidPos))  # 588


class PasswordPolicyTester(unittest.TestCase):
    def test_getValidPasswordCount_validnAndInvalidGiven_twoValidsFound(self):
        # [1-3 a: abcde, 1-3 b: cdefg, 2-9 c: ccccccccc]
        pwp1 = PasswordPolicy(1, 3, "a", "abcde")
        pwp2 = PasswordPolicy(1, 3, "b", "cdefg")
        pwp3 = PasswordPolicy(2, 9, "c", "ccccccccc")
        allPwPolicies = [pwp1, pwp2, pwp3]
        self.assertEqual(2, getValidPasswordsCount(allPwPolicies, isPasswordValid))

    def test_getValidPasswordCountPos_valindAndInvalidGiven_oneValidFound(self):
        # [1-3 a: abcde, 1-3 b: cdefg, 2-9 c: ccccccccc]
        pwp1 = PasswordPolicy(1, 3, "a", "abcde")
        pwp2 = PasswordPolicy(1, 3, "b", "cdefg")
        pwp3 = PasswordPolicy(2, 9, "c", "ccccccccc")
        allPwPolicies = [pwp1, pwp2, pwp3]
        self.assertEqual(1, getValidPasswordsCount(allPwPolicies, isPasswordValidPos))


if __name__ == '__main__':
    # main()
    unittest.main()
