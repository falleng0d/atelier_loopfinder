from __future__ import annotations

from typing import List

import yaml
import csv
from pydantic import BaseModel

class Item(BaseModel):
    Name: str
    Type: List[str]
    Recipe: List[str]
    Effects: List[str] = []


class Model(BaseModel):
    items: List[Item]

def load_yaml_data(file: str) -> Model:
    with open(file) as f:
        data = Model.parse_obj(yaml.safe_load(f))
    return data

def load_csv_data(file: str) -> Model:
    """
    Load data from a csv file.
    Recipe = ["Ingredient 1", "Ingredient 2", "Ingredient 3", "Ingredient 4"]
    Type = ["Category 1", "Category 2", "Category 3", "Category 4", "Add Category 1", "Add Category 2"]
    Effects = ["SQ+1", "SQ+2", "ES+1", "ES+2", "ES+3"]
    """
    type_columns = ["Category 1", "Category 2", "Category 3", "Category 4", "Add Category 1","Add Category 2"]
    recipe_columns = ["Ingredient 1", "Ingredient 2", "Ingredient 3", "Ingredient 4"]
    effects_columns = ["SQ+1", "SQ+2", "ES+1", "ES+2", "ES+3"]
    effects_values = ["Synth Quantity +1", "Synth Quantity +2", "Effect Spread +1", "Effect Spread +2", "Effect Spread +3"]
    effect_from_column_name = lambda x: effects_values[effects_columns.index(x)]
    model = Model(items=[])
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if "Include" in row and row["Include"] != "X":
                continue
            item = Item(
                Name=row['Name'],
                Type=[],
                Recipe=[])
            for column in type_columns:
                if column in row and row[column] != "":
                    item.Type.append(row[column])
            for column in recipe_columns:
                if column in row and row[column] != "":
                    item.Recipe.append(row[column])
            for column in effects_columns:
                if column in row and row[column] != "":
                    item.Effects.append(effect_from_column_name(column))
            model.items.append(item)
    return model

if __name__ == "__main__":
    materials = load_csv_data("./../assets/ryza_materials.csv")
    recipes = load_csv_data("./../assets/ryza_recipes.csv")
    print(recipes)
