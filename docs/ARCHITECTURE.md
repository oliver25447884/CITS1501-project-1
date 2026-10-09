# Application Architecture

```mermaid
flowchart LR
    User[User] --> Main[main.py\nTkinter app and navigation]

    Main --> Security[security_module.py\nstartup and login]
    Main --> Questions[question_module.py\nquestions and region lookup]
    Main --> ClimatePage[climate_page.py\nclimate report screen]
    Main --> Sources[source_module.py\nreferences window]
    Main --> Wheel[season_wheel.py\ninteractive season wheel and details]
    Main --> Climate[climate_data.py\nCSV loading and calculations]
    Calendar[season_calendar.py\nshared month-to-season mapping]

    Climate --> Rain[Data/1.csv\ndaily rainfall]
    Climate --> Temp[Data/2.csv\ndaily maximum temperature]
    Climate --> Calendar
    Questions --> Calendar
    Wheel --> Calendar
    Climate --> Summaries[Monthly and annual summaries]
    Summaries --> Main

    Wheel --> Nature[Data/Season Visuals/\nseason nature images]
    Wheel --> Graphs[Data/Graphs/\nseason climate graphs]
    Wheel --> SeasonStats[Season-specific summary content]

    Tests[tests/test_climate_data.py] -. checks .-> Climate
```

## How the pieces work together

- `main.py` creates the Tkinter window, starts the app, and routes navigation between feature modules.
- `security_module.py` supplies the startup and login screens.
- `question_module.py` provides question-and-answer content, answer widgets, and the council-to-region lookup.
- `climate_page.py` presents the monthly analysis computed by `climate_data.py`.
- `source_module.py` displays the source list used by the app.
- `season_wheel.py` draws the interactive season wheel and builds the season detail pages. It loads charts from `Data/Graphs/` and nature images from `Data/Season Visuals/`.
- `season_calendar.py` provides the shared month-to-season mapping used by the climate calculations, question lookup, and season pages.
- `climate_data.py` reads rainfall and maximum-temperature observations from `Data/1.csv` and `Data/2.csv`, validates dates and values, joins readings by date, and calculates summaries for the climate page.
- `tests/test_climate_data.py` checks the climate data reader and its calculations.
