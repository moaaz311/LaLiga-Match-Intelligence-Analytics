# Data Dictionary: SpainLeague Analytical Data Warehouse

## Overview
The `SpainLeague` database follows a Star Schema architecture optimized for high-performance sports analytics, business intelligence reporting in Power BI, and interactive HTML UI rendering.

---

## 1. Dimension Tables

### `Teams` (Club Dimension)
Primary dimension storing metadata and visual identity for all 20 LaLiga clubs.

| Column Name | Data Type | Constraints | Description | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `team_id` | `VARCHAR(50)` | Primary Key | Unique team identifier from API | `"86"` |
| `abbrev` | `VARCHAR(10)` | Unique | Standard 3-letter club abbreviation | `"RMA"`, `"FCB"`, `"ATM"` |
| `name` | `VARCHAR(100)` | | Full official club name | `"Real Madrid"` |
| `display_name` | `VARCHAR(100)` | | Display friendly club name | `"Real Madrid"` |
| `short_name` | `VARCHAR(50)` | | Short club moniker | `"Real Madrid"` |
| `location` | `VARCHAR(100)` | | Home city / region | `"Madrid"` |
| `color` | `VARCHAR(20)` | | Primary brand hex color for UI styling | `"#FFFFFF"`, `"#004D98"` |
| `logo` | `VARCHAR(500)` | | CDN image URL for official club crest | `https://a.espncdn.com/...` |

---

### `Dim_Players` (Player Dimension)
Consolidated player dimension derived from multi-category league leaderboards and enriched via ESPN and TheSportsDB APIs.

| Column Name | Data Type | Constraints | Description | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `player_id` | `VARCHAR(50)` | Primary Key | Unique player identifier | `"231050"` |
| `name` | `VARCHAR(150)` | | Full player name | `"Kylian Mbappé"`, `"Robert Lewandowski"` |
| `team` | `VARCHAR(10)` | Foreign Key -> `Teams(abbrev)` | Club abbreviation the player represents | `"RMA"`, `"FCB"` |
| `position` | `VARCHAR(20)` | | Playing position | `"Forward"`, `"Midfielder"`, `"Defender"`, `"Goalkeeper"` |
| `Player_Image_URL` | `VARCHAR(500)` | | Verified high-resolution headshot URL (NULL for initials fallback) | `https://www.thesportsdb.com/images/...` |

---

## 2. Fact Tables

### `Fact_Matches` (Match Results & Fixtures)
Stores all 380 scheduled and completed fixtures for the LaLiga 2026/2027 season.

| Column Name | Data Type | Constraints | Description | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `game_id` | `VARCHAR(50)` | Primary Key | Unique match fixture identifier | `"705891"` |
| `season` | `BIGINT` | | League season year | `2026` |
| `stage` | `VARCHAR(50)` | | Competition stage | `"league"` |
| `date` | `DATE` | Indexed | Match calendar date | `2026-10-24` |
| `starts_at` | `VARCHAR(50)` | | Match start timestamp (ISO) | `2026-10-24T19:00:00Z` |
| `status` | `VARCHAR(20)` | | Match state | `"final"`, `"scheduled"`, `"in_progress"` |
| `status_detail`| `VARCHAR(50)` | | Additional match context | `"FT"`, `"Postponed"` |
| `result` | `VARCHAR(10)` | | Match outcome code | `"H"`, `"A"`, `"D"` |
| `neutral_site` | `BIT` | | Whether match was played at neutral venue | `0` (False) |
| `venue` | `VARCHAR(150)` | | Stadium name | `"Santiago Bernabéu"` |
| `city` | `VARCHAR(100)` | | Host city | `"Madrid"` |
| `attendance` | `FLOAT` | | Recorded match attendance | `78450` |
| `Home_Team_ID` | `VARCHAR(50)` | Foreign Key -> `Teams(team_id)` | Home team ID | `"86"` |
| `Home_Abbreviation` | `VARCHAR(10)` | | Home team 3-letter code | `"RMA"` |
| `Home_Team` | `VARCHAR(100)` | | Home team display name | `"Real Madrid"` |
| `Home_Score` | `BIGINT` | | Home team goals scored | `2` |
| `Away_Team_ID` | `VARCHAR(50)` | Foreign Key -> `Teams(team_id)` | Away team ID | `"83"` |
| `Away_Abbreviation` | `VARCHAR(10)` | | Away team 3-letter code | `"FCB"` |
| `Away_Team` | `VARCHAR(100)` | | Away team display name | `"Barcelona"` |
| `Away_Score` | `BIGINT` | | Away team goals scored | `1` |

---

### `Fact_Player_Leaders` (Player Statistical Leaderboards)
Top-100 player leaderboards across 10 distinct statistical disciplines.

| Column Name | Data Type | Constraints | Description | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `rank` | `BIGINT` | | Ranking position within stat category | `1`, `2`, `3` |
| `player_id` | `VARCHAR(50)` | Foreign Key -> `Dim_Players(player_id)` | Unique player ID | `"231050"` |
| `name` | `VARCHAR(150)` | | Player name | `"Vinicius Junior"` |
| `position` | `VARCHAR(20)` | | Primary tactical position | `"Forward"` |
| `team` | `VARCHAR(10)` | Foreign Key -> `Teams(abbrev)` | Club abbreviation | `"RMA"` |
| `games` | `BIGINT` | | Total appearances | `28` |
| `minutes` | `BIGINT` | | Total minutes played on pitch | `2340` |
| `value` | `FLOAT` | | Raw aggregate metric value | `18.0` (goals), `11.0` (assists) |
| `per90` | `FLOAT` | | Normalized rate per 90 minutes played | `0.69`, `0.42` |
| `stat` | `VARCHAR(50)` | Indexed | Metric category name | `"goals"`, `"assists"`, `"xg"`, `"shots"`, `"clean_sheets"` |

---

### `Fact_Standings` (League Table & Progression)
Current league championship standings, point tallies, and recent form indicators.

| Column Name | Data Type | Description | Sample Value |
| :--- | :--- | :--- | :--- |
| `rank` | `BIGINT` | Current league table rank (1 to 20) | `1` |
| `team_id` | `VARCHAR(50)` | Foreign Key to `Teams(team_id)` | `"86"` |
| `abbrev` | `VARCHAR(10)` | Club abbreviation | `"RMA"` |
| `display_name` | `VARCHAR(100)` | Club display name | `"Real Madrid"` |
| `played` | `BIGINT` | Total matches contested | `28` |
| `wins` | `BIGINT` | Total victories | `20` |
| `draws` | `BIGINT` | Total draws | `5` |
| `losses` | `BIGINT` | Total defeats | `3` |
| `goals_for` | `BIGINT` | Goals scored | `62` |
| `goals_against`| `BIGINT` | Goals conceded | `22` |
| `goal_diff` | `BIGINT` | Goal difference (`goals_for - goals_against`) | `+40` |
| `points` | `BIGINT` | Total league points (`wins * 3 + draws`) | `65` |
| `deductions` | `BIGINT` | Regulatory point deductions | `0` |
| `form` | `VARCHAR(50)` | Five-match rolling form string | `"W-W-D-W-L"` |

---

### `Fact_Team_Stats` (Team Performance & Efficiency)
Aggregated team-level tactical and performance metrics across attack, defense, and discipline.

| Column Name | Data Type | Description | Sample Value |
| :--- | :--- | :--- | :--- |
| `team_id` | `VARCHAR(50)` | Foreign Key to `Teams(team_id)` | `"86"` |
| `abbrev` | `VARCHAR(10)` | Club abbreviation | `"RMA"` |
| `display_name` | `VARCHAR(100)` | Club display name | `"Real Madrid"` |
| `games` | `BIGINT` | Total matches analyzed | `28` |
| `goals_for` | `FLOAT` | Total goals scored | `62.0` |
| `goals_against`| `FLOAT` | Total goals conceded | `22.0` |
| `xg_for` | `FLOAT` | Total Expected Goals generated | `58.4` |
| `xg_against` | `FLOAT` | Total Expected Goals conceded | `24.1` |
| `shots_for` | `FLOAT` | Total shots attempted | `412.0` |
| `shots_against`| `FLOAT` | Total shots conceded | `280.0` |
| `shots_on_target_for` | `FLOAT` | Shots on target attempted | `175.0` |
| `shots_on_target_against` | `FLOAT` | Shots on target conceded | `98.0` |
| `possession_pct` | `FLOAT` | Average ball possession percentage | `59.4` |
| `pass_accuracy_pct` | `FLOAT` | Team passing completion rate | `87.8` |
| `passes` | `BIGINT` | Total passes attempted | `16420` |
| `corners` | `FLOAT` | Total corner kicks earned | `168.0` |
| `fouls` | `FLOAT` | Total fouls committed | `295.0` |
| `yellow_cards` | `FLOAT` | Total yellow cards received | `48.0` |
| `red_cards_total` | `BIGINT` | Total red cards received | `2` |
| `tackles` | `FLOAT` | Total defensive tackles won | `445.0` |
| `interceptions` | `FLOAT` | Total passing interceptions made | `228.0` |
| `clean_sheets` | `BIGINT` | Total matches without conceding a goal | `13` |
| `failed_to_score` | `BIGINT` | Total matches failing to score | `3` |

---

### `Fact_Ratings` (Elo Strength Index)
Relative team strength evaluation computed via the Elo rating algorithm.

| Column Name | Data Type | Description | Sample Value |
| :--- | :--- | :--- | :--- |
| `rank` | `BIGINT` | Global Elo strength rank | `1` |
| `team_id` | `VARCHAR(50)` | Foreign Key to `Teams(team_id)` | `"86"` |
| `abbrev` | `VARCHAR(10)` | Club abbreviation | `"RMA"` |
| `name` | `VARCHAR(100)` | Club name | `"Real Madrid"` |
| `elo` | `FLOAT` | Computed Elo rating score | `1985.4` |
| `last_game` | `DATE` | Date of match for rating calibration | `2026-10-24` |

