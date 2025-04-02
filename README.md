# feynman


# query intent algo

Let’s mix it up! I’ll give you three different algorithms, each with a name, a short description, and how they’d handle a sequence of numbers like `1, 1, 2, 3, 1, 2, 2, 4` to predict the next intent. These will riff off the intent-deduction vibe but with distinct flavors—no code, just the logic, since you’re after the approach.

---

### 1. Momentum Rider
- **Description**: Sticks to the most recent streak, only shifting if the streak breaks or weakens.
- **How It Works**: Scans the end of the sequence for a run of repeats (like `2, 2`). If the last number matches the streak, it rides that; if not, it picks the last number as a new start.
- **On `1, 1, 2, 3, 1, 2, 2, 4`**: Sees `2, 2` as a streak, but `4` breaks it. No new streak with `4` yet, so it picks `4` (last number).
- **Output**: `4`

---

### 2. Majority Rules
- **Description**: Counts all numbers and picks the one with the highest total frequency, ignoring recency.
- **How It Works**: Tallies each number’s appearances across the whole sequence and goes with the winner (ties broken by the last occurrence).
- **On `1, 1, 2, 3, 1, 2, 2, 4`**: Counts: `1` = 3, `2` = 3, `3` = 1, `4` = 1. Tie between `1` and `2`, but `2` is later, so it wins.
- **Output**: `2`

---

### 3. Weighted Flow
- **Description**: Balances recency and frequency by giving more weight to later numbers, then picks the highest score.
- **How It Works**: Assigns weights (e.g., position-based: 1st = 1, 2nd = 2, ..., 8th = 8) to each number, sums the weights per value, and takes the max.
- **On `1, 1, 2, 3, 1, 2, 2, 4`**: Weights: `1 (1), 1 (2), 2 (3), 3 (4), 1 (5), 2 (6), 2 (7), 4 (8)`. Scores: `1` = 1+2+5 = 8, `2` = 3+6+7 = 16, `3` = 4, `4` = 8. `2` wins.
- **Output**: `2`

---

### Quick Take
- **Momentum Rider**: Loves the latest vibe (`4`), like the toy code’s “stick to the flow.”
- **Majority Rules**: Goes for the crowd favorite (`2`), ignoring when things happened.
- **Weighted Flow**: Blends past and present, favoring recent heavy hitters (`2`).


