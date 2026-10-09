"""Single source of truth for month mapping shared across app features."""

# Climate data and question lookups use this Perth-area guide consistently.
SEASON_BY_MONTH = {
    1: "Birak",
    2: "Bunuru",
    3: "Bunuru",
    4: "Djeran",
    5: "Djeran",
    6: "Makuru",
    7: "Makuru",
    8: "Djilba",
    9: "Djilba",
    10: "Kambarang",
    11: "Kambarang",
    12: "Birak",
}


def season_for_month(month):
    """Return the Perth-area season guide for a calendar month."""
    return SEASON_BY_MONTH[month]
