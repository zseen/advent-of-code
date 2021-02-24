import unittest
from typing import List, Set, Dict

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
        allIngredients: List[List[str]] = list(self._allergenToPossibleSourceIngredients.values())
        return sum(frequency for ingredient, frequency in self._ingredientToFrequency.items() if
                   all(ingredient not in ingredients for ingredients in allIngredients))

    def createCanonicalDangerousIngredientList(self) -> str:
        allergenToIngredientSortedByAllergen: AllergenToIngredientType = dict(sorted(self._allergenToPossibleSourceIngredients.items()))
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
                elif len(ingredients) > 1:
                    self._removeIdentifiedIngredientsFromPossibleAllergenSources(allergen, ingredientsSurelyContainingAllergen, ingredients)
                elif len(ingredients) == 0:
                    raise ValueError("Allergen seems to have no possible source.")

    def getAllergenToIngredient(self) -> AllergenToIngredientType:
        return self._allergenToPossibleSourceIngredients

    def _findPossibleSourcesForAllergens(self) -> AllergenToIngredientType:
        allergenToPossibleSourceIngredients: AllergenToIngredientType = dict()
        for food in self._foods:
            for allergen in food.allergens:
                if allergen in allergenToPossibleSourceIngredients:
                    allergenToPossibleSourceIngredients[allergen] = [ingredient for ingredient in food.ingredients if
                                                                     ingredient in allergenToPossibleSourceIngredients[allergen]]
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

    def _removeIdentifiedIngredientsFromPossibleAllergenSources(self, allergen: str, ingredientsSurelyContainingAllergen: Set[str],
                                                                possibleSourceIngredients: List[str]) -> None:
        for ingredientSurelyContainingAllergen in ingredientsSurelyContainingAllergen:
            if ingredientSurelyContainingAllergen in possibleSourceIngredients:
                self._allergenToPossibleSourceIngredients[allergen].remove(ingredientSurelyContainingAllergen)


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
            allergens = [allergen.strip(",") for allergen in chunks[1].strip(")").split(" ")[1:]]
            foods.append(Food(ingredients, allergens))
    return foods


def main():
    foods = getInput(INPUT_FILE)
    allergenSourceIdentifier = AllergenSourceIdentifier(foods)
    print(allergenSourceIdentifier.countIngredientsOccurrencesNotContainingAllergens())  # 2020
    allergenSourceIdentifier.determineAllergensToIngredientsExclusively()
    print(allergenSourceIdentifier.createCanonicalDangerousIngredientList())  # bcdgf,xhrdsl,vndrb,dhbxtb,lbnmsr,scxxn,bvcrrfbr,xcgtv


class AllergenSourceIdentifierTester(unittest.TestCase):
    def setUp(self) -> None:
        self.foods = getInput(TEST_INPUT_FILE)
        self.allergenSourceIdentifier = AllergenSourceIdentifier(self.foods)

    def test_countIngredientsOccurrencesNotContainingAllergens_correctSumReturned(self):
        self.assertEqual(self.allergenSourceIdentifier.countIngredientsOccurrencesNotContainingAllergens(), 5)

    def test_createCanonicalDangerousIngredientList_correctValueReturned(self):
        self.allergenSourceIdentifier.determineAllergensToIngredientsExclusively()
        self.assertEqual(self.allergenSourceIdentifier.createCanonicalDangerousIngredientList(), "mxmxvkd,sqjhc,fvjkl")


if __name__ == '__main__':
    # main()
    unittest.main()
