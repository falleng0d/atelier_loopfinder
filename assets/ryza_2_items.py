import csv
import pandas as pd

# CSV Columns:
# name
# Type
# fire
# wind
# ice
# lightning
# elementvalue
# Category 1
# category/1/slug
# category/1/name
# category/2/slug
# category/2/name
# category/3/slug
# category/3/name
# ingredient_set/0/ing
# ingredient_set/1/ing
# ingredient_set/2/ing
# ingredient_set/3/ing
# ingredient_set/4/ing
# ingredient_set/5/ing
# ingredient_set/6/ing
# ingredient_set/7/ing
# ingredient_set/8/ing
# ingredient_set/9/ing
# ingredient_set/10/ing
# ingredient_set/11/ing
# ingredient_set/12/ing
# ingredient_set/13/ing
# ingredient_set/14/ing
# ingredient_set/15/ing
# ingredient_set/16/ing
# ingredient_set/17/ing
# ingredient_set/18/ing
# ingredient_set/19/ing
# ingredient_set/20/ing
# ingredient_set/21/ing
# ingredient_set/22/ing
# ingredient_set/23/ing

def merge_ingredient_columns(filename: str) -> None:
	new_rows = []
	with open(filename, newline='') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
		for row in reader:
			new_row = {"Name": row["name"], "Type": row["Type"]}
			# merge ingredient_set/n/ing
			# first find the unique ingredient_set/n/ing values
			ingredient_values = set()
			for column in row.keys():
				if column.startswith("ingredient_set/") and column.endswith("/ing"):
					if row[column] != "":
						ingredient_values.add(row[column])
					# Adds new columns Ingredient 1, Ingredient 2, etc.
					# for each unique ingredient_set/n/ing value
					for i, ingredient in enumerate(ingredient_values):
						new_row[f"Ingredient {i+1}"] = ingredient
			new_rows.append(new_row)
	# write the new file
	df = pd.DataFrame(new_rows)
	filename_without_extension = filename.split(".")[0]
	df.to_csv(filename_without_extension + "_conv.csv", index=False, header=True)

if __name__ == "__main__":
	merge_ingredient_columns("ryza_2_items.csv")
