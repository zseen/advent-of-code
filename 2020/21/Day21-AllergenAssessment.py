import unittest
from typing import List, Set, Dict
from collections import OrderedDict

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"

AllergenToIngredientType = Dict[str, List[str]]


class Food:
    def __init__(self, ingredients: List[str], allergens: List[str]):
        self.ingredients: List[str] = ingredients
        self.allergens: List[str] = allergens


class AllergenSourceIdentifier:
    def __init__(self, foods: List[Food]):
        self._foods: List[Food] = foods
        self._allergenToPossibleSourceIngredients: AllergenToIngredientType = self._findPossibleSourcesForAllergens()
        self._ingredientToFrequency: Dict[str, int] = dict()

    def countIngredientsOccurrencesNotContainingAllergens(self) -> int:
        self._countIngredientsOccurrencesInFoods()
        allIngredientsPossiblyContainingAllergens: List[List[str]] = list(self._allergenToPossibleSourceIngredients.values())

        ingredientsNotContainingAllerensFrequencyCount = 0
        for ingredient, frequency in self._ingredientToFrequency.items():
            if all(ingredient not in ingredients for ingredients in allIngredientsPossiblyContainingAllergens):
                ingredientsNotContainingAllerensFrequencyCount += frequency
        return ingredientsNotContainingAllerensFrequencyCount

    def getCanonicalDangerousIngredientList(self) -> str:
        allergenToIngredientSortedByAllergen: OrderedDict[str, List[str]] = OrderedDict(sorted(self._allergenToPossibleSourceIngredients.items()))
        ingredientsSortedByAllergens: List[List[str]] = list(allergenToIngredientSortedByAllergen.values())
        if not all(len(ingredient) == 1 for ingredient in ingredientsSortedByAllergens):
            raise ValueError("Allergen seems to be mapped to ingredient incorrectly.")
        return ",".join(ingredient[0] for ingredient in ingredientsSortedByAllergens)

    def determineAllergensToIngredientsExclusively(self) -> None:
        ingredientsSurelyContainingAllergen: Set[str] = set()
        while len(ingredientsSurelyContainingAllergen) != len(self._allergenToPossibleSourceIngredients):
            for allergen, ingredients in self._allergenToPossibleSourceIngredients.items():
                if len(ingredients) == 1 and ingredients[0] not in ingredientsSurelyContainingAllergen:
                    ingredientsSurelyContainingAllergen.add(ingredients[0])
                    self._removeIdentifiedIngredientFromOtherAllergenSources(ingredients[0])
                elif len(ingredients) == 0:
                    raise ValueError("Allergen seems to have no possible source.")

    def _findPossibleSourcesForAllergens(self) -> AllergenToIngredientType:
        allergenToPossibleSourceIngredients: AllergenToIngredientType = dict()
        for food in self._foods:
            for allergen in food.allergens:
                if allergen in allergenToPossibleSourceIngredients:
                    allergenToPossibleSourceIngredients[allergen] = list(
                        set(food.ingredients).intersection(set(allergenToPossibleSourceIngredients[allergen])))
                else:
                    allergenToPossibleSourceIngredients[allergen] = food.ingredients
        return allergenToPossibleSourceIngredients

    def _countIngredientsOccurrencesInFoods(self) -> None:
        ingredientToFrequency: Dict[str, int] = {}
        for food in self._foods:
            for ingredient in food.ingredients:
                if ingredient in ingredientToFrequency:
                    ingredientToFrequency[ingredient] += 1
                else:
                    ingredientToFrequency[ingredient] = 1
        self._ingredientToFrequency = ingredientToFrequency

    def _removeIdentifiedIngredientFromOtherAllergenSources(self, identifiedAllergenSourceIngredient: str) -> None:
        for allergen, ingredients in self._allergenToPossibleSourceIngredients.items():
            if len(ingredients) != 1 and identifiedAllergenSourceIngredient in ingredients:
                ingredients.remove(identifiedAllergenSourceIngredient)


def getInput(inputFile: str):
    foods = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            chunks = line.split("(")
            if len(chunks) != 2:
                raise ValueError("Unexpected line format after splitting.")
            ingredients = chunks[0].strip(" ").split(" ")
            allergensRawData = chunks[1].strip(")").split(" ")
            allergens = [allergen.strip(",") for allergen in allergensRawData[1:]]

            foods.append(Food(ingredients, allergens))
    return foods


def main():
    foods = getInput(INPUT_FILE)
    allergenSourceIdentifier = AllergenSourceIdentifier(foods)
    print(allergenSourceIdentifier.countIngredientsOccurrencesNotContainingAllergens())  # 2020
    allergenSourceIdentifier.determineAllergensToIngredientsExclusively()
    print(allergenSourceIdentifier.getCanonicalDangerousIngredientList())  # bcdgf,xhrdsl,vndrb,dhbxtb,lbnmsr,scxxn,bvcrrfbr,xcgtv


class AllergenSourceIdentifierTester(unittest.TestCase):
    def setUp(self) -> None:
        self.foods = getInput(TEST_INPUT_FILE)
        self.allergenSourceIdentifier = AllergenSourceIdentifier(self.foods)

    def test_countIngredientsOccurrencesNotContainingAllergens_correctSumReturned(self):
        self.assertEqual(self.allergenSourceIdentifier.countIngredientsOccurrencesNotContainingAllergens(), 5)

    def test_createCanonicalDangerousIngredientList_correctValueReturned(self):
        self.allergenSourceIdentifier.determineAllergensToIngredientsExclusively()
        self.assertEqual(self.allergenSourceIdentifier.getCanonicalDangerousIngredientList(), "mxmxvkd,sqjhc,fvjkl")


if __name__ == '__main__':
    #main()
    unittest.main()
