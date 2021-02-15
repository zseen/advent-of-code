import unittest
from typing import List, Set, Dict

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"



def getInput(inputFile: str):
    foods = []

    allAllergens = set()
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            #chunks = line.split("(")
            #print(chunks)
            #ingredients = chunks[0].strip(" ").split(" ")
            #print(ingredients)
            foods.append(line)

            #allergens = [allergen.strip(",") for allergen in chunks[1].strip(")").split(" ")[1:]]
            #allAllergens.update(set([allergen for allergen in allergens]))

    return foods

def findPotentialIngredientsToAllergens(foods: List[str]):
    allergenToPotentialIngredients = dict()
    for food in foods:
        chunks = food.split("(")
        ingredients = chunks[0].strip(" ").split(" ")
        allergens = [allergen.strip(",") for allergen in chunks[1].strip(")").split(" ")[1:]]
        if len(allergens) == 1:
            allergenToPotentialIngredients[allergens[0]] = set(ingredients)


    return allergenToPotentialIngredients

def eliminate(allergenToPotentialIngredients, foods):
    allAllergens = allergenToPotentialIngredients.keys()
    allAllergensLength = len(allAllergens)
    sureMatch = dict()
    print(allergenToPotentialIngredients)

    while True:
        for food in foods:
            chunks = food.split("(")
            ingredients = chunks[0].strip(" ").split(" ")
            allergens = [allergen.strip(",") for allergen in chunks[1].strip(")").split(" ")[1:]]
            if len(allergens) > 1:
                for allergen in allergens:
                    if allergen not in sureMatch:
                        ingredientsForAllergen: Set = allergenToPotentialIngredients[allergen]
                        commonItems = set(ingredients).intersection(ingredientsForAllergen)
                        if len(commonItems) == 1:
                            sureMatch[allergen] = list(commonItems)[0]
                            for x, ing in allergenToPotentialIngredients.items():
                                if commonItems[0] in ing:
                                    ingredients.remove(commonItems[0])
                            del allergenToPotentialIngredients[allergen]
            allergenWithSingleIngredient = []
            for allerg, ings in allergenToPotentialIngredients.items():
                if len(ings) == 1:
                    sureMatch[allerg] = list(ings)[0]
                    allergenWithSingleIngredient.append(allerg)
            for item in allergenWithSingleIngredient:
                del allergenToPotentialIngredients[item]

            if len(sureMatch) == allAllergensLength:
                return sureMatch


def getIngredientFrequency(foods):
    ingredientToFrequency = dict()
    for food in foods:
        chunks = food.split("(")
        ingredients = chunks[0].strip(" ").split(" ")
        for ingredient in ingredients:
            if ingredient in ingredientToFrequency:
                ingredientToFrequency[ingredient] += 1
            else:
                ingredientToFrequency[ingredient] = 1

    return ingredientToFrequency


def getAllergenlessIngredientsFrequencies(ingredientToFrequency, allergenToIngredient):
    ingredientsContainingAllergen = set([value for key, value in allergenToIngredient.items()])

    allFrequencies = 0
    for ingredient, frequency in ingredientToFrequency.items():
        if ingredient not in ingredientsContainingAllergen:
            allFrequencies += frequency

    return allFrequencies









foods = getInput(INPUT_FILE)

allPot = findPotentialIngredientsToAllergens(foods)
#print(allPot)

sure = eliminate(allPot, foods)
#print(sure)

ingredientsToFrequencies = getIngredientFrequency(foods)

finalRes = getAllergenlessIngredientsFrequencies(ingredientsToFrequencies, sure)
print(finalRes)