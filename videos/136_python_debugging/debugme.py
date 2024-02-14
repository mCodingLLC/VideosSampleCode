import itertools
import json


def load_recipes(filename):
    with open(filename) as f_in:
        return json.load(f_in)


def load_ingredient_locations(filename):
    with open(filename) as f_in:
        ingredients = json.load(f_in)
    return {item["name"]: item["where"] for item in ingredients}


def verify_ingredients_exist(recipes, ingredients):
    for recipe in recipes:
        for ingr in recipe["ingredients"]:
            if ingr["name"] not in ingredients:
                raise ValueError(
                    f"Recipe {recipe['name']} referred to unknown ingredient: {ingr['name']}"
                )


def choose_recipes(recipes):
    for idx, recipe in enumerate(recipes):
        print(f"{idx}: {recipe['name']}")
    while True:
        selection = input("What are you shopping for? ")
        try:
            choices = [int(item.strip()) for item in selection.split(",") if item]
            if not all(0 <= choice < len(recipes) for choice in choices):
                raise ValueError
            return [recipes[choice] for choice in choices]
        except ValueError:
            print("Invalid selection. Please try again.")


def get_grocery_items(all_ingredient_locs, recipes):
    grocery_items = []
    for recipe in recipes:
        ingredients = recipe["ingredients"]
        items = [
            {
                "name": ingr["name"],
                "quantity": ingr["quantity"],
                "where": all_ingredient_locs[ingr["name"]],
            }
            for ingr in ingredients
        ]
        grocery_items.extend(items)
    return grocery_items


def combine_like_items(grocery_items):
    def name_key(item):
        return item["name"]

    items = sorted(grocery_items, key=name_key)
    new_items = []
    for name, like_items in itertools.groupby(items, name_key):
        like_items = list(like_items)
        combined_item = {
            "name": name,
            "quantity": " + ".join(item["quantity"] for item in like_items),
            "where": like_items[0]["where"],
        }
        new_items.append(combined_item)
    return new_items


def print_grocery_items_by_location(grocery_items):
    def where_key(x):
        return x["where"]

    def where_then_name_key(x):
        return x["where"], x["name"]

    grocery_items = sorted(grocery_items, key=where_then_name_key)
    groups = itertools.groupby(grocery_items, key=where_key)

    for where, items in groups:
        print(f"===== {where} =====")
        for item in items:
            print(f"{item['name']}, {item['quantity']}")
        print()


def main():
    all_recipes = load_recipes("recipes.json")
    all_ingredient_locs = load_ingredient_locations("ingredients.json")
    verify_ingredients_exist(all_recipes, all_ingredient_locs)
    chosen_recipes = choose_recipes(all_recipes)
    grocery_items = get_grocery_items(all_ingredient_locs, chosen_recipes)
    grocery_items = combine_like_items(grocery_items)

    print("Here's your grocery list:")
    print_grocery_items_by_location(grocery_items)


if __name__ == "__main__":
    main()
