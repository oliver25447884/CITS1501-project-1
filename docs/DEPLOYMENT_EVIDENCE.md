# Local Deployment Evidence

## Deployment type

This is a local Python/Tkinter desktop app. It is not a hosted website or a packaged installer. The project must be run with its source files and `Data/` assets available in the project folder.

## Environment recorded

- Operating system: macOS
- Python: 3.14.7, from the project's `.venv`
- App entry point: `main.py`
- Automated tests: `tests/test_climate_data.py`

## Checks recorded on 9 October 2026

- `main.py` and its app modules passed a Python syntax parse.
- Import check passed: `import main` completed successfully.
- Automated climate-data checks passed: **11 tests, OK**.

Test command used from the project root:

```bash
python3 -m unittest discover -s tests -v
```

The 11 tests cover the supplied 2024 files, leap-year date coverage, monthly and annual calculations, missing readings, invalid dates and values, required data coverage, and season mapping.

## GUI launch evidence still to capture

A launch attempt from the Codex command environment exited with code 134 before an app window appeared. That does not establish a successful GUI launch in the user's VS Code session, so this file does not claim that the window was visually verified.

For final evidence, open this project folder in VS Code, select its `.venv` Python interpreter, then run:

```bash
.venv/bin/python main.py
```

Capture a screenshot showing the app window open. If it opens, include that screenshot with this file or in the written report. If it does not, record the complete terminal error and resolve it before claiming the GUI has been deployed successfully.

## Reproducing the local setup

From the project root, install the listed dependencies if the environment has not already been prepared:

```bash
python3 -m pip install -r requirements.txt
```

Then start the app with `.venv/bin/python main.py` after activating or selecting the project's environment. Keep `Data/` and `modules/` beside `main.py`; the app loads its local code and assets from those folders.
