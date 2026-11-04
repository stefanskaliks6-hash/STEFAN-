# URBS 250 – Lecture 6-2 homework: Group 7, Office Mid-Rise

Stefan Skaliks Aparicio is in **Group 7: Office Mid-Rise** (lecture 6-2, slide 12).

## Deliverables
| File | What it is |
|---|---|
| `Group7_Office_MidRise_Summary.pptx` | The summary deck: slide 1 cover sheet (type + members), slide 2 summary table (Average / Min / Max), slides 3–16 one example slide per member |
| `Group7_Data_Calculator.xlsx` | Type each member's numbers into the *Submissions* sheet; the *Summary* sheet computes Average / Min / Max automatically |
| `data/group7_submissions.json` | Single source of the team's numbers, used to rebuild the deck |

## Filling in the team's numbers
1. Collect each member's property homework values (Montréal assessment roll): lot size (m²), lot value, building value, property total, GFA (m²), previous assessment, plus optional floors and year built.
2. Either type them into the Excel calculator and copy the Summary values into slide 2, **or** put them in `data/group7_submissions.json` and rebuild:
   ```bash
   npm install && node build_deck.js && python3 build_calculator.py
   ```
3. On slide 1, keep only the members present today (or set `"presenting": [...]` in the JSON).
4. Paste each member's property photo into the frame on their slide.
