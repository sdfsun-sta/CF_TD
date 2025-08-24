# CF_TD

This repository contains configuration and validation utilities for a tower defence prototype.  
Game balance values are stored in CSV files so that they can be tweaked without code changes.  
`data_loader.py` demonstrates how to load and validate weapon data according to the design rules.

## Data files
- `data/Weapon.csv` – weapon parameters with schema checks.
- `data/Enemy.csv` – basic enemy stats.
- `data/Tactical.csv` – tactical ability configuration.
- `data/WaveRecipe.csv` – wave composition examples.

## Running validation
```
python - <<'PY'
from pathlib import Path
from data_loader import load_weapons
print(load_weapons(Path('data/Weapon.csv')))
PY
```

## Tests
```
pytest
```
