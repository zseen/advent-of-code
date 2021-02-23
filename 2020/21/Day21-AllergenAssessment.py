import unittest
from typing import List, Set, Dict

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"



def getInput(inputFile: str):
    foods = []

    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            chunks = line.split("(")
            ingredients = chunks[0].strip(" ").split(" ")
            allergens = [allergen.strip(",") for allergen in chunks[1].strip(")").split(" ")[1:]]
            foods.append((ingredients, allergens))
    return foods



def findPossibleSourcesForAllergens(foods: List):
    allergenToPossibleSourceIngredients: Dict[str, List[str]] = dict()
    for food in foods:
        for allergen in food[1]:
            if allergen in allergenToPossibleSourceIngredients:
                allergenToPossibleSourceIngredients[allergen] = [ingredient for ingredient in food[0] if ingredient in allergenToPossibleSourceIngredients[allergen]]
            else:
                allergenToPossibleSourceIngredients[allergen] = [ingredient for ingredient in food[0]]
    return allergenToPossibleSourceIngredients

def countIngredientsOccurrencesInFoods(foods: List):
    occurrences = {}
    for food in foods:
        for ingredient in food[0]:
            if ingredient in occurrences:
                occurrences[ingredient] += 1
            else:
                occurrences[ingredient] = 1
    return occurrences


def countIngredientsOccurrencesNotContainingAllergens(ingredientToFrequencies: Dict, allergenToPossibleSourceIngredients: Dict):
    count = 0
    for ingredient, frequency in ingredientToFrequencies.items():
        if all(ingredient not in v for v in allergenToPossibleSourceIngredients.values()):
            count += frequency
    return count


def getAllergenToSourceIngredient(allergenToPossibleSourceIngredients):
    ingredientsSurelyContainingAllergen = set()
    while any(len(a) > 1 for a in allergenToPossibleSourceIngredients.values()):
        for allergen, ingredient in allergenToPossibleSourceIngredients.items():
            if len(ingredient) == 1 and ingredient[0] not in ingredientsSurelyContainingAllergen:
                ingredientsSurelyContainingAllergen.add(ingredient[0])
            elif len(ingredient) > 1:
                for i in ingredientsSurelyContainingAllergen:
                    if i in ingredient:
                        allergenToPossibleSourceIngredients[allergen].remove(i)
    return allergenToPossibleSourceIngredients


foods = getInput(INPUT_FILE)
allergenToPossibleIngredients = findPossibleSourcesForAllergens(foods)
ingredientToFrequencies = countIngredientsOccurrencesInFoods(foods)

print(getAllergenToSourceIngredient(allergenToPossibleIngredients))
print(countIngredientsOccurrencesNotContainingAllergens(ingredientToFrequencies, allergenToPossibleIngredients))

#
#
# print(allergens)
# print(occurrences)