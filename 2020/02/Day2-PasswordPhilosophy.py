import unittest

INPUT_FILE = "input.txt"

class PasswordPolicy:
    def __init__(self, frequencyMin, frequencyMax, char, password):
        self.frequencyMin = frequencyMin
        self.frequencyMax = frequencyMax
        self.char = char
        self.password = password


def getInput():
    passwords = []
    with open(INPUT_FILE, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            minFreq = ""
            maxFreq = ""
            pwChar = ""
            password = ""
            i = 0

            while line[i].isdigit():
                minFreq += str(line[i])
                i += 1
            while not line[i].isdigit():
                i += 1
            while line[i].isdigit():
                maxFreq += str(line[i])
                i += 1
            while not line[i].isalpha():
                i += 1
            if line[i].isalpha():
                pwChar = line[i]
                i += 1
            while not line[i].isalpha():
                i += 1
            while i < len(line) and line[i].isalpha():
                password += line[i]
                i += 1
            passwordPolicy = PasswordPolicy(int(minFreq), int(maxFreq), pwChar, password)
            passwords.append(passwordPolicy)
    return passwords


def getValidPasswordsCount(allPasswordPolicies):
    validPasswordsCount = 0
    for pwpolicy in allPasswordPolicies:
        if isPasswordValid(pwpolicy):
            validPasswordsCount += 1
    return validPasswordsCount

def isPasswordValid(passwordPolicy: PasswordPolicy):
    desiredCharCount = 0
    for character in passwordPolicy.password:
        if character == passwordPolicy.char:
            desiredCharCount += 1

    return passwordPolicy.frequencyMin <= desiredCharCount <= passwordPolicy.frequencyMax

def main():
    allPasswordPolicies = getInput()
    print(getValidPasswordsCount(allPasswordPolicies)) # 636


class PasswordPolicyTester(unittest.TestCase):
    def test_getValidPasswordCount_validnAndInvalidGiven_twoValidsFound(self):
        # [1-3 a: abcde, 1-3 b: cdefg, 2-9 c: ccccccccc]
        pwp1 = PasswordPolicy(1, 3, "a", "abcde")
        pwp2 = PasswordPolicy(1, 3, "b", "cdefg")
        pwp3 = PasswordPolicy(2, 9, "c", "ccccccccc")
        allPwPolicies = [pwp1, pwp2, pwp3]
        self.assertEqual(2, getValidPasswordsCount(allPwPolicies))

if __name__ == '__main__':
    main()
    #unittest.main()
