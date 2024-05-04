# Helltaker AI27

## Overview

The **helltaker_ia02** project contains various utilities for managing Helltaker grids, along with examples.

## Level Structure

Each level is defined in a simple `.txt` file with the following format:
- First line: title
- Second line: maximum number of moves
- Subsequent lines: level description

Characters used to define elements within the grid:
- `H`: Hero
- `D`: Demoness
- `#`: Wall
- ` ` : Empty space
- `B`: Block
- `K`: Key
- `L`: Lock
- `M`: Mob (skeleton)
- `S`: Spikes
- `T`: Safe trap
- `U`: Unsafe trap
- `O`: Block on spike
- `P`: Block on safe trap
- `Q`: Block on unsafe trap

### Example

```
Level 1
23
     ###
  ### H#
 #  M  #
 # M M #
#  ####
# B  B #
# B B  D#
#########
```

## Utilities

The Python3 package `helltaker_utils` includes functions to read these files and check the plans.

### `grid_from_file(filename: str, voc: dict = {})`

This function reads a file and converts it into a Helltaker grid.

**Arguments:**
- `filename`: File containing the grid description
- `voc`: Optional argument to convert each grid cell to your own vocabulary

**Returns:**
- A dictionary containing:
   - The game grid as a list of lists of characters
   - Number of rows `m`
   - Number of columns `n`
   - Grid title
   - Maximum number of moves `max_steps`

### `check_plan(plan: str)`

This function checks whether your plan is valid.

- **Argument**: A plan in the form of a string
- **Returns**: `True` if the plan is valid, `False` otherwise

## Implementation Models

We've implemented models in STRIPS, ASPPLAN, and SATPLAN as part of this project.

