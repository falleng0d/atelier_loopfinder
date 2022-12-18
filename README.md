# Atelier Loopfinder 

Python cli tool to find crafting loops in atelier games

Currently only supports Atelier Ryza: Ever Darkness & the Secret Hideout

I will keep adding support for more games as I play them

## Usage
```bash
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  loops   Find all loops of size {--size}
  search  Find all items that matches
  uses    Find all items that uses {--item-name} as ingredient
```


## Examples

### Find all loops of size 3 starting from item "Flour"
```bash
> python .\main.py loops --size=3 "Flour"  
```
```
Found 2 loops of size 3
- Flour[Flour] -> [Flour]Poison Cube
    then Poison Cube[(Gas)] -> [(Gas)]Bug Net
        Effects:
                Poison Cube: [Synth Quantity +1, Synth Quantity +2]

- Flour[Flour] -> [Flour]Delicious Bait
    then Delicious Bait[(Fruit)] -> [(Fruit)]Mixing Oil
```

### Find all loops of size 3 starting from item "Natural Cloth"

Note the use of --simplified-output to not show the matching type/recipe requirements
```bash
> python .\main.py loops --size=3 --simplified-output "Natural Cloth"
```
```
Found 5 loops of size 3
Natural Cloth -> Glass Flower -> Alchemy Fibers
Natural Cloth -> Puni Leather -> Beastial Air
Natural Cloth -> Green Supplement -> Alchemy Fibers
Natural Cloth -> Zettel -> Alchemy Fibers
```

### Find all items that uses "Natural Cloth" as ingredient
```bash
> python .\main.py uses --item-name "Natural Cloth"
```
```
Found 17 items that uses Natural Cloth as ingredient
Glass Flower
Forest Bell
Plant Seed
Puni Leather
Radiant Plate
Skuller Coat
Frost Armor
Fairy Cloak
Grass Beans
Green Supplement
Zettel
Alchemy Fibers
Kurken Sweats
Noble Tunic
Leather Protector
Chain Vest
Border Scale
```

### Find all items that matches "cloth"
```bash
> python .\main.py search "cloth"
```
```
Found 2 items named cloth

  Name:         Cloth
  Types:        (Cloth)
  Recipe:       (Thread), (Animal Product), (Supplement)

  Name:         Natural Cloth
  Types:        (Cloth), (Plant)
  Recipe:       Alchemy Fibers, Plant Essence, (Plant), (Animal Product)
```
