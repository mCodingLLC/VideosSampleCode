from io import StringIO

from debugme import (
    load_recipes,
    load_ingredient_locations,
    choose_recipes,
    get_grocery_items,
)


def test_load_recipes(monkeypatch):
    recipe_str = r"""
    [
        {
            "name": "spaghetti bolognese",
            "ingredients": [
                {"name": "ground beef", "quantity": "1 lb"}
            ]
        }
    ]
    """
    expected = [
        {
            "name": "spaghetti bolognese",
            "ingredients": [
                {"name": "ground beef", "quantity": "1 lb"},
            ],
        }
    ]
    monkeypatch.setattr("builtins.open", lambda _: StringIO(recipe_str))
    actual = load_recipes(...)
    assert actual == expected


def test_load_ingredient_locations(monkeypatch):
    ingredients_str = r"""
    [
        {"name": "avocado", "where": "produce"}
    ]
    """
    expected = {"avocado": "produce"}
    monkeypatch.setattr("builtins.open", lambda _: StringIO(ingredients_str))
    actual = load_ingredient_locations(...)
    assert actual == expected


def test_choose_recipes(monkeypatch):
    recipes = [
        {
            "name": "just beef",
            "ingredients": [
                {"name": "ground beef", "quantity": "1 lb"},
            ],
        },
        {
            "name": "just cheese",
            "ingredients": [
                {"name": "cheese", "quantity": "1 lb"},
            ],
        },
    ]
    monkeypatch.setattr("builtins.input", lambda _: "0,0,1")
    expected = [recipes[0], recipes[0], recipes[1]]
    actual = choose_recipes(recipes)
    assert actual == expected


def test_get_grocery_items():
    recipes = [
        {
            "name": "just beef",
            "ingredients": [
                {"name": "ground beef", "quantity": "1 lb"},
            ],
        },
        {
            "name": "just cheese",
            "ingredients": [
                {"name": "cheese", "quantity": "2 lb"},
            ],
        },
    ]
    ingredients_locs = {
        "ground beef": "meat",
        "cheese": "dairy",
    }
    expected = [
        {"name": "ground beef", "quantity": "1 lb", "where": "meat"},
        {"name": "cheese", "quantity": "2 lb", "where": "dairy"},
    ]
    actual = get_grocery_items(ingredients_locs, recipes)
    assert actual == expected


# more tests!
