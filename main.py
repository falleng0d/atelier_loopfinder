from dataclasses import dataclass
from typing import List, TypeVar

import click

import model

all_items = model.load_data("items.yaml").items

# A loop is a special kind of sequence where the last item uses the first item


T = TypeVar("T")

def last(array: List[T]) -> T:
    return array[len(array) - 1]


@dataclass
class UsesRelation:
    item: model.Item
    ingredient: model.Item
    MatchingIngredientRequirement: str
    MatchingIngredientType: str

def item_uses_ingredient(item: model.Item, ingredient: model.Item) -> UsesRelation:
    """
    Given an item and an ingredient, check if the item uses the ingredient as an ingredient.
    If the item uses the ingredient, return the UsesRelation.
    """
    if ingredient.Name in item.Recipe:
        return UsesRelation(item, ingredient, ingredient.Name, ingredient.Name)
    for t in ingredient.Type:
        for i in item.Recipe:
            if i in t:
                return UsesRelation(item, ingredient, t, i)
    raise ValueError(f"{item.Name} does not use {ingredient.Name}")

def explain_relation(item_a: model.Item, item_b: model.Item) -> str:
    """
    Given a list of items, explain how {item_a} is related to {item_b}.
    """

    # Check if {item_a} and {item_b} are used to craft each other
    try:
        relation_a = item_uses_ingredient(item_b, item_a)
        relation_b = item_uses_ingredient(item_a, item_b)
        return f"{relation_a.ingredient.Name}({relation_a.MatchingIngredientRequirement}) <-> {relation_b.ingredient.Name}({relation_b.MatchingIngredientRequirement})"

        # relation_a = item_uses_ingredient(item_b, item_a)
        # relation_b = item_uses_ingredient(item_a, item_b)
        # explanation = f"{relation_a.ingredient.Name}" \
        #               f"[{relation_a.MatchingIngredientRequirement}] -> " \
        #               f"[{relation_a.MatchingIngredientType}]" \
        #               f"{relation_a.item.Name}\n"
        # explanation += f"{relation_b.ingredient.Name}" \
        #                f"[{relation_b.MatchingIngredientRequirement}] -> " \
        #                f"[{relation_b.MatchingIngredientType}]" \
        #                f"{relation_b.item.Name}\n"
        # return explanation
    except ValueError:
        pass

    # Check if {item_a} is used to craft {item_b}
    try:
        relation = item_uses_ingredient(item_b, item_a)
        return f"{relation.ingredient.Name}[{relation.MatchingIngredientRequirement}] -> [{relation.MatchingIngredientType}]{relation.item.Name}"
    except ValueError:
        pass

    # Check if {item_b} is used to craft {item_a}
    try:
        relation = item_uses_ingredient(item_a, item_b)
        return f"{relation.ingredient.Name}[{relation.MatchingIngredientRequirement}] <- [{relation.MatchingIngredientType}]{relation.item.Name}"
    except ValueError:
        pass

    return "No relation"

def explain_loop(loop: List[model.Item]) -> str:
    """
    Given a loop, explain how each sequential pair of items in the loop is related.
    """

    # For each pair {item_a} and {item_b}, with b coming after a. Check if {item_a} and {item_b} are used to craft each other.
    explanation = "- "
    for i in range(len(loop) - 1):
        item_a = loop[i]
        item_b = loop[i + 1]
        try:
            relation_a = item_uses_ingredient(item_b, item_a)
            arrow = ' -> '
            if explanation != "- ":
                explanation += click.style('\n    then ', fg='blue')
            explanation += f"{relation_a.ingredient.Name}" \
                           f"{click.style(f'[{relation_a.MatchingIngredientRequirement}]', fg='magenta')}" \
                           f"{click.style(arrow, fg='blue')}" \
                           f"{click.style(f'[{relation_a.MatchingIngredientType}]', fg='magenta')}" \
                           f"{relation_a.item.Name}"
        except ValueError:
            pass

    return f"{explanation}\n"

def explain_loop_simplified(loop: List[model.Item]) -> str:
    """
    Given a loop, explain how each sequential pair of items in the loop is related.
    """

    # For each pair {item_a} and {item_b}, with b coming after a. Check if {item_a} and {item_b} are used to craft each other.
    explanation = ""
    for i in range(len(loop)):
        item = loop[i]
        explanation += f"{item.Name}"
        if i < len(loop) - 1:
            explanation += click.style(' -> ', fg='blue')

    return explanation

def find_item_named(name: str, items: List[model.Item]) -> model.Item:
    """Given a list of items, find the item with the given name"""
    for item in items:
        if item.Name == name:
            return item
    raise ValueError(f"Item not found: {name}")

def find_is_used_as_ingredient_of(item: model.Item, items: List[model.Item]) -> List[model.Item]:
    """
    Given a list of items, find all items that uses {item} as ingredient.
    For an item to be considered a match, it must have {item} in its Recipe list or any of its types.
    """
    matches = []
    for i in items:
        if item == i:
            continue
        if item.Name in i.Recipe:
            matches.append(i)
            continue
        for t in item.Type:
            if t in i.Recipe:
                matches.append(i)
    return matches

def find_ingredients_of(item: model.Item, items: List[model.Item]) -> List[model.Item]:
    """
    Given a list of items, find all items that are used to craft {item}.
    For an item to be considered a match, it must have {item} in its Recipe list or any of its types.
    """
    matches = []
    for i in items:
        if i.Name in item.Recipe:
            matches.append(i)
            continue
        for t in item.Recipe:
            if t in i.Type:
                matches.append(i)
    return matches

def find_bidireactional_related_items(item: model.Item, items: List[model.Item]) -> List[model.Item]:
    """
    Given a list of items, find all items that are related to {item} in both directions.

    A bidirectional relationship between items is when both items can be crafted from each other

    Returns a list of items that are related to {item} in both directions.
    """
    bi_related_items: List[model.Item] = []

    # Items that use {item} as ingredient
    items_using_item = find_is_used_as_ingredient_of(item=item, items=items)

    # Check if any of the {items_using_item} can be used to craft {item} back
    for i in items_using_item:
        try:
            item_uses_ingredient(item=item, ingredient=i)
            bi_related_items.append(i)
        except ValueError:
            pass

    return bi_related_items

def find_bidireactional_related_pairs(item: model.Item, items: List[model.Item]) -> List[List[model.Item]]:
    """
    Given a list of items, find all items that are related to {item} in both directions.

    A bidirectional relationship between items is when both items can be crafted from each other

    Returns a list of pairs of items that are related to each other in both directions.
    """
    bi_related_sequences: List[List[model.Item]] = []

    # Items that use {item} as ingredient
    items_using_item = find_is_used_as_ingredient_of(item=item, items=items)

    # Check if any of the {items_using_item} can be used to craft {item} back
    for i in items_using_item:
        try:
            item_uses_ingredient(item=item, ingredient=i)
            bi_related_sequences.append([item, i])
        except ValueError:
            pass

    return bi_related_sequences

def compare_sequences(seq_a: List[model.Item], seq_b: List[model.Item]) -> bool:
    """
    Given two sequences, check if they are the same.
    """
    if len(seq_a) != len(seq_b):
        return False
    for i in range(len(seq_a)):
        if seq_a[i] != seq_b[i]:
            return False
    return True

def find_looping_sequences(sequence: List[model.Item],
                           sequence_size: int,
                           possible_ending_items: List[model.Item],
                           remaining_items: List[model.Item]) -> List[List[model.Item]]:
    current_size = len(sequence)

    if current_size == 0:
        sequences = []
        for starting_item in remaining_items:
            next_remaining_items = [item for item in remaining_items if
                                    item != starting_item]
            # The starting_item uses the ending_item as ingredient
            _possible_ending_items = find_ingredients_of(starting_item, next_remaining_items)
            if len(_possible_ending_items) == 0:
                continue
            sequences.extend(find_looping_sequences([starting_item], sequence_size,
                                          _possible_ending_items, next_remaining_items))
        return sequences

    current_item = last(sequence)
    possible_next_items = find_is_used_as_ingredient_of(current_item, remaining_items)

    # the next item can be any possible_next_items
    if current_size < sequence_size - 1:
        sequences = []
        for candidate in possible_next_items:
            next_sequence = [*sequence, candidate]
            next_remaining_items = [item for item in remaining_items if
                                    item != candidate]
            sequences.extend(
                find_looping_sequences(next_sequence, sequence_size, possible_ending_items, next_remaining_items))

        return sequences

    # the next item must be in the possible_ending_items
    if current_size == sequence_size - 1:
        sequences = []
        for candidate in possible_next_items:
            if candidate in possible_ending_items:
                sequences.append([*sequence, candidate])
        return sequences

    return []


def find_bidirectional_related_pairs(items: List[model.Item]) -> List[List[model.Item]]:
    """
    Given a list of items, find all bidirectional pairs (loops).
    """
    pairs: List[List[model.Item]] = []
    for item in items:
        bi_related_items = find_bidireactional_related_items(item, items)
        pairs.extend([[item, related_item] for related_item in bi_related_items])
    return pairs


@click.command(name="uses",
               help="Find all items that uses {--item-name} as ingredient")
@click.option("--item-name", "-i", prompt_required=True, help="The item to search for")
def cmd_find_recipe_matches(item_name: str) -> None:
    item = find_item_named(item_name, all_items)
    matches = find_is_used_as_ingredient_of(item, all_items)
    click.echo(f"Found {len(matches)} items that uses {item_name} as ingredient")

    for match in matches:
        click.echo(match.Name)

@click.command(name="loops",
               help="Find all loops of size 1 that start with {--item-name}")
@click.option("--item-name", "-i", prompt_required=True, help="The item to search for")
def cmd_find_loops(item_name: str) -> None:
    item = find_item_named(item_name, all_items)
    loops = find_bidireactional_related_pairs(item, all_items)
    click.echo(f"Found {len(loops)} loops that start with {item_name}")

    # explain the loop by comparing each item to the next item with explain_relation
    for loop in loops:
        click.echo(f"{explain_relation(loop[0], loop[1])}")

@click.command(name="loops:all",
               help="Find all loops of size 1")
def cmd_find_all_loops() -> None:
    loops = find_bidirectional_related_pairs(all_items)
    click.echo(f"Found {len(loops)} loops")

    # explain the loop by comparing each item to the next item with explain_relation
    for loop in loops:
        click.echo(f"{explain_relation(loop[0], loop[1])}")

@click.command(name="loops:all-of-size",
                help="Find all loops of size {--size}")
@click.option("--size", "-s", prompt_required=True, help="The size of the loops to search for", default=2)
def cmd_find_all_loops_of_size(size: int) -> None:
    loops = find_looping_sequences([], size, [], all_items)
    click.echo(f"Found {len(loops)} loops of size {size}")

    # explain the loop by comparing each item to the next item with explain_relation
    for loop in loops:
        click.echo(f"{explain_loop(loop)}")


@click.group()
def cli() -> None:
    pass


cli.add_command(cmd_find_recipe_matches)
cli.add_command(cmd_find_loops)
cli.add_command(cmd_find_all_loops)
cli.add_command(cmd_find_all_loops_of_size)

if __name__ == "__main__":
    cli()

