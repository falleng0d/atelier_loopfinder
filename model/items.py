from __future__ import annotations

import csv
from typing import List, TextIO, Callable

from pydantic import BaseModel

class Item(BaseModel):
	Name: str
	Type: List[str]
	Recipe: List[str]
	Effects: List[str] = []

class Model(BaseModel):
	items: List[Item]

def ryza_csv_load_strategy(file: TextIO) -> Model:
	"""
	Load data from a csv file.
	Recipe = ["Ingredient 1", "Ingredient 2", "Ingredient 3", "Ingredient 4"]
	Type = ["Category 1", "Category 2", "Category 3", "Category 4", "Add Category 1",
	"Add Category 2"]
	Effects = ["SQ+1", "SQ+2", "ES+1", "ES+2", "ES+3"]
	"""
	type_columns = ["Category 1", "Category 2", "Category 3", "Category 4",
	                "Add Category 1", "Add Category 2"]
	recipe_columns = ["Ingredient 1", "Ingredient 2", "Ingredient 3", "Ingredient 4"]
	effects_columns = ["SQ+1", "SQ+2", "ES+1", "ES+2", "ES+3"]
	effects_values = ["Synth Quantity +1", "Synth Quantity +2", "Effect Spread +1",
	                  "Effect Spread +2", "Effect Spread +3"]
	effect_from_column_name = lambda x: effects_values[effects_columns.index(x)]
	model = Model(items=[])

	reader = csv.DictReader(file, delimiter=',', quotechar='"')
	for row in reader:
		if "Include" in row and row["Include"] != "X":
			continue
		item = Item(
			Name=row['Item'],
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

def ryza_2_csv_load_strategy(file: TextIO) -> Model:
	"""
	Load data from a csv file. (ryza_2_recipes.csv)
	Recipe = ["Ingredient 1", "Ingredient 2", "Ingredient 3", "Ingredient 4"]
	Type = ["Category 1", "Category 2", "Category 3", "Category 4", "Add Category 1",
	"Add Category 2"]
	Effects = ["ES", "SQ", "EV"]
	"""
	type_columns = ["Category 1", "Category 2", "Category 3", "Category 4",
	                "Add Category 1", "Add Category 2"] # "Add Category 3", "Add Category 4"
	recipe_column_prefix = "Ingredient"
	effects_abrev_expanded = {
		"SQ": "Synth Quantity",
		"ES": "Effect Spread",
		"EV": "EV"
	}
	effect_label_of = lambda col, val: f"{effects_abrev_expanded[col]} +{val}"
	model = Model(items=[])

	reader = csv.DictReader(file, delimiter=',', quotechar='"')
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
		for column in row.keys():
			if column.startswith(recipe_column_prefix) and row[column] != "":
				item.Recipe.append(row[column])
		for column in effects_abrev_expanded.keys():
			value = row[column]
			if column in row and value != "":
				item.Effects.append(effect_label_of(column, value))
		model.items.append(item)

	return model

def load_csv_data(file: str, strategy: Callable[[TextIO], Model]) -> Model:
	"""
	Load data from a csv file using a strategy.
	"""
	with open(file, newline='') as csvfile:
		model = strategy(csvfile)
	return model

if __name__ == "__main__":
	materials = load_csv_data("./../assets/ryza_materials.csv", ryza_csv_load_strategy)
	recipes = load_csv_data("./../assets/ryza_recipes.csv", ryza_csv_load_strategy)
	print(recipes)
