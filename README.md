# Noongar Seasons — Perth Weather App

A Tkinter learning app about the six Noongar seasons, Perth weather, and seasonal nature. Month ranges are approximate and describe one regional guide, not all Noongar Country.

## Install and run
Main.py can be run from Powershell,Terminal or Visual Studio Code
or
From this folder, create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

In VS Code, select `.venv/bin/python` as the interpreter. Keep `Data/` and `modules/` beside `main.py`.

## Project layout

- `main.py` starts the app and routes between features. `modules/` contains the
  season, question, climate, source, and security screens, plus climate-data
  parsing and calculations.
- `Data/` contains the climate CSVs and images used by the app.
- `tests/` contains the automated climate-data tests.
- `docs/` contains the written report, project notes, and source references.

## Use

- Select a season on the wheel to view its notes, image, and climate graph.
- Use the questions area for seasonal information and the council region lookup.
- Choose **Explore 2024 climate data** for summaries calculated from the supplied CSV files.
- Open **Sources** in the app for references.

## Tests

From the project folder, run:

```bash
python -m unittest discover -s tests -v
```

The 11 tests cover CSV loading, date and value validation, missing readings, and climate calculations.

## Data and project files

`Data/1.csv` contains 2024 Perth Metro daily rainfall; `Data/2.csv` contains daily maximum temperatures (BOM station 009225). The climate page calculates summaries from these files. Season-page graphs are supplied in `Data/Graphs/`, and nature images are in `Data/Season Visuals/`.

Sources: [Bureau of Meteorology Climate Data Online](https://www.bom.gov.au/climate/data/) · [DPIRD Noongar Six Seasons fact sheet](https://marinewaters.fish.wa.gov.au/resource/fact-sheet-the-noongar-six-seasons/).

- [Architecture diagram](docs/ARCHITECTURE.md)
- [Deployment](docs/DEPLOYMENT.md)
- [AI interaction log](docs/AI-LOG.md)
- [Written report](docs/Written%20report.md)

Source PDFs and supporting images are in `docs/references/`.

This is a local desktop app, not a hosted service or installer. Check image and data reuse terms before redistribution.
