# AI Interaction Log

Project: Noongar Seasons weather app  
Purpose: Record AI assistance, how suggestions were evaluated, and which changes were retained. The students reviewed the output and remain responsible for the submitted code and report.

## Interaction 1 — Resolve app launch error

**Date:** During project development  
**AI tool:** OpenAI Codex in VS Code / Codex desktop  
**Task:** Fix a `SyntaxError` in `Moduals/Question_Modual.py` caused by unresolved Git merge-conflict markers so `main.py` could launch.  
**AI contribution:** Helped remove the invalid conflict-marker text and repair the affected module.  
**Evaluation and use:** The user ran `main.py` and reported that the app opened. The repaired module was retained.

## Interaction 2 — Improve season pages and graphs

**Date:** During project development  
**AI tool:** OpenAI Codex in VS Code / Codex desktop  
**Task:** Show a graph, seasonal description, and nature information on each season page; improve graph readability and page layout; add more season, wildlife, and meteorological detail; and use subtle seasonal page colours.  
**AI contribution:** Helped refine the season-page interface, content, and graph assets in response to the user's feedback.  
**Evaluation and use:** The user reviewed the pages and requested further changes to image size, graph quality, and content. The interface was refined through that feedback.

## Interaction 3 — Add Country acknowledgement and overview

**Date:** During project development  
**AI tool:** OpenAI Codex in VS Code / Codex desktop  
**Task:** Add an acknowledgement of Country to the home page and an overview of the Noongar seasons with the supplied image on the wheel page.  
**AI contribution:** Helped add the requested content and image to the app pages.  
**Evaluation and use:** The user reviewed the result and continued giving design feedback.

## Interaction 4 — Read and summarize weather CSV data

**Date:** During project development  
**AI tool:** OpenAI Codex in VS Code / Codex desktop  
**Task:** Improve the app using the supplied weather files and assignment brief.  
**AI contribution:** Added `Moduals/ClimateData.py` to read daily rainfall and maximum-temperature CSV files, validate readings, join observations by date, and calculate monthly and annual summaries. Added a climate-data page in `main.py`.  
**Evaluation and use:** The CSV calculations were checked with 11 automated tests in the `automated tests` folder. The user can run them with `python3 -m unittest discover -s "automated tests" -v` from the project folder.

## Interaction 5 — GitHub Copilot graph request in VS Code

**Date:** 9 October 2026  
**AI tool:** GitHub Copilot Chat in VS Code  
**Session title:** “Graph integration and design updates”  
**Session reference:** `d1689f68-cd0e-472b-aaeb-9cfbd04cbfbb`  
**Task / prompt visible in the session:** The user asked Copilot to create matching graphs for all six Noongar seasons and remake the supplied graph; the prompt also had `1.csv` attached. The saved chat preview truncates the rest of the prompt, so this log records its visible meaning rather than inventing the missing words.  
**Copilot response / outcome:** The session showed Copilot beginning to install Matplotlib, then displaying a message that the monthly credit limit had been reached. The session was marked failed; no completed graph implementation is visible in this chat.  
**Evaluation and use:** This Copilot attempt is recorded as an incomplete attempt, not as a successful code contribution. Its output was not treated as verified or incorporated on the basis of this failed session. The user should review any other Copilot sessions or code edits separately before claiming them as contributions.

## Reflection

The AI tools were used to suggest and implement code and interface changes, but tool output was not assumed to be correct automatically. The weather-data calculations were checked with automated tests, and the app was reviewed after changes. Copilot's graph session did not complete, so its failure is documented rather than presented as a successful result. The students should verify sources, confirm that cultural descriptions are appropriate for the places discussed, and be prepared to explain the submitted code.
