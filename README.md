\<div *align*="center">



![LaLiga Season Banner]\(assets/banners/LaLiga%20Season%202026_2027%20Graphic.png)

**# ⚽ LaLiga Match Intelligence & Analytics Platform**

**###&#x20;**_\*End-to-End Football Data Engineering, Star Schema Modeling, and Interactive Power BI Analytics\*_



[![Python Version]\(https\://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)]\(https\://www\.python.org/)

[![Database]\(https\://img.shields.io/badge/SQL%20Server-2016%2B%20%7C%20T--SQL-CC292B?logo=microsoftsqlserver&logoColor=white)]\(https\://www\.microsoft.com/en-us/sql-server/)

[![Business Intelligence]\(https\://img.shields.io/badge/Power%20BI-Desktop%20%7C%20TMDL%20%7C%20DAX-F2C811?logo=powerbi&logoColor=black)]\(https\://powerbi.microsoft.com/)

[![Visual Engine]\(https\://img.shields.io/badge/Frontend-HTML5%20%7C%20CSS3%20%7C%20SVG-E34F26?logo=html5&logoColor=white)]\(https\://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)

[![License]\(https\://img.shields.io/badge/License-MIT-green.svg)]\(LICENSE)

[![Maintenance]\(https\://img.shields.io/badge/Maintained%3F-Yes-emerald.svg)]\()



**\*\*A comprehensive, production-grade sports analytics platform providing deep performance intelligence across all 20 Spanish LaLiga clubs and 290+ players.\*\***



[Live Architecture]\(#-etl-pipeline--architecture) • [Database Design]\(#-database-design--star-schema) • [Power BI Dashboard]\(#-power-bi-dashboard-pages) • [Interactive DAX SPA]\(#-interactive-html--svg-dashboard-engine) • [Installation]\(#-installation--reproduction)



**---**



\</div>



**## 📌 Executive Summary & Project Overview**



Football analytics has evolved far beyond basic match scores and static standings. Modern sporting directors, performance analysts, and tactical scouts demand granular insights into **\*\*Expected Goals (xG)\*\***, **\*\*efficiency per-90\*\***, **\*\*possession value\*\***, **\*\*home vs. away scoring dynamics\*\***, and **\*\*multivariate player radar benchmarking\*\***.



The **\*\*LaLiga Match Intelligence & Analytics Platform\*\*** bridges this gap. It is an end-to-end data engineering and business intelligence solution designed to ingest, process, model, and visualize real-world Spanish top-flight football data.



**### Analytical Scope & Core Objectives**

1\. **\*\*Automated Data Ingestion\*\***: Extract 380 match fixtures, 20 club standings, 20 deep team performance profiles, Elo strength ratings, and 770+ player leader records across 10 statistical dimensions using Striker REST API with local caching.

2\. **\*\*Visual Asset Enrichment Pipeline\*\***: Resolve player portraits across ESPN CDN and TheSportsDB APIs through Unicode NFKD normalization and string-distance club matching, validating 223 headshots (76%) with a graceful SVG club-initial fallback.

3\. **\*\*Enterprise Data Warehousing\*\***: Architect a high-performance Star Schema in Microsoft SQL Server comprising 2 Dimension tables and 5 Fact tables with primary keys, foreign constraints, and optimized index layouts.

4\. **\*\*Futuristic Power BI Single-Page Application (SPA)\*\***: Deliver an ultra-wide (2560×1150) dashboard powered by an advanced 665-line DAX measure that dynamically renders HTML5, CSS flexbox, and SVG polar radar charts via the Microsoft-certified HTML Content visual.

5\. **\*\*Interactive Parameter Disconnection\*\***: Implement independent parameter slicing (\`Home Pick\`, \`Away Pick\`, \`Compare Pick\`) allowing dynamic head-to-head tactical comparisons without cross-filtering contamination.



**---**



**## 🏗️ Project Architecture & ETL Pipeline**



The platform operates as a cohesive 5-tier analytics pipeline:



\`\`\`

┌─────────────────────────┐       ┌──────────────────────────┐       ┌─────────────────────────┐

│     Data Sources        │       │    Ingestion & Cache     │       │   Cleaning & Enrichment │

│  • Striker API (v1)     │ ───►  │  • Requests & JSON Cache │ ───►  │  • Pandas Normalization │

│  • TheSportsDB API      │       │  • Rate Limiting (2.2s)  │       │  • Unicode NFKD Match   │

│  • ESPN Player CDN      │       │  • Credit Optimization   │       │  • Image Validation     │

└─────────────────────────┘       └──────────────────────────┘       └─────────────────────────┘

                                                                                  │

                                                                                  ▼

┌─────────────────────────┐       ┌──────────────────────────┐       ┌─────────────────────────┐

│    Power BI Reporting   │       │  Semantic Modeling (DAX) │       │ SQL Server Data Whse    │

│  • Ultra-wide 2560x1150 │       │  • 665-line TMDL Measure │       │  • Database: SpainLeague│

│  • 5-Page Dynamic SPA   │ ◄───  │  • SVG Radar & Rings     │ ◄───  │  • 2 Dimensions         │

│  • Disconnected Slicers │       │  • Cover Overlay Trick   │       │  • 5 Fact Tables (Star) │

└─────────────────────────┘       └──────────────────────────┘       └─────────────────────────┘

\`\`\`



\<div *align*="center">



![Architecture & Star Schema]\(project_screens/LaLiga%20Match%20Intelligence%20Pipeline.png)

*\*Figure 1: Full-lifecycle Data Pipeline Architecture and Star Schema Warehouse.\**



\</div>



**---**



**## 💻 Technology Stack**



\| Layer | Technologies & Tools | Function / Purpose |

\| :--- | :--- | :--- |

\| **\*\*Data Ingestion\*\*** | \`Python 3.10+\`, \`Requests\`, \`JSON\` | API calls, endpoint traversal, pagination, and caching |

\| **\*\*Data Processing\*\*** | \`Pandas\`, \`NumPy\`, \`Unicodedata\`, \`Regex\` | Data cleaning, type coercion, text normalization, deduplication |

\| **\*\*Database\*\*** | \`Microsoft SQL Server 2016+\`, \`T-SQL\` | Relational data warehouse storage, indexing, and DDL schema |

\| **\*\*Database Connector\*\***| \`SQLAlchemy\`, \`pyodbc\` (\`fast_executemany\`) | High-throughput batch inserts and schema migrations |

\| **\*\*Semantic Modeling\*\***| \`Power BI Desktop\`, \`TMDL\`, \`DAX\` | Measures, calculated tables, disconnected slicers, relationships |

\| **\*\*Frontend Visual\*\*** | \`HTML5\`, \`CSS3 Flexbox\`, \`Inline SVG\` | Dynamic UI generation inside Microsoft-certified HTML Content visual |

\| **\*\*External APIs\*\*** | Striker API, TheSportsDB API, ESPN CDN | Match statistics, player performance, and headshots |

\| **\*\*Asset Design\*\*** | Adobe Photoshop / Illustrator | Canvas backgrounds, banners, and aesthetic gradients |



**---**



**## 📡 Data Extraction & Ingestion Pipeline**



**### 1. Data Provider & Endpoints**

Primary league and player data is extracted via the **\*\*Striker API\*\*** (\`https\://mcp.strikerapi.com/v1/\`):

\- \`list_teams\`: Fetches metadata for all 20 LaLiga clubs (IDs, abbreviations, official colors, and crests).

\- \`get_standings\`: Retrieves current league standings, points, goal tallies, and 5-game rolling form.

\- \`get_team_stats\`: Deep team tactical metrics (Expected Goals \`xG\`, possession %, pass completion %, corners, fouls, disciplinary cards).

\- \`get_ratings\`: Club strength metrics computed via the Elo rating algorithm.

\- \`list_games\`: Match fixture schedule and completed results (traversing 380 total season fixtures using 110-item offset pagination).

\- \`get_leaders\`: Player leaderboards across 10 distinct statistical categories: \`goals\`, \`assists\`, \`goal_contributions\`, \`shots\`, \`shots_on_target\`, \`xg\`, \`yellow_cards\`, \`red_cards\`, \`saves\`, \`clean_sheets\`.



**### 2. Credit-Preserving Two-Tier Caching System**

To avoid exhausting commercial API credits during iterative development:

\- Every successful API response is automatically persisted as structured JSON in \`raw_cache/\` (e.g., \`raw_cache/games_0.json\`, \`raw_cache/leaders_goals.json\`).

\- If a cached payload exists, the script executes an instant **\*\*cache hit\*\*** with zero network overhead and zero credit deduction.

\- Safe payload unwrapping logic (\`get_list\` & \`find_rows\`) handles variable response envelopes (\`data: [...]\` vs \`data: {...}\`) transparently.



**---**



**## 🧹 Data Cleaning, Validation & Player Photo Enrichment**



**### 1. Schema Standardization & Typing**

\- **\*\*Column Renaming\*\***: Flattened nested JSON dictionaries into clean SQL identifiers (e.g., \`home.score\` -> \`Home_Score\`, \`away.team_id\` -> \`Away_Team_ID\`).

\- **\*\*Date Standardization\*\***: Parsed mixed datetime strings into native ISO \`DATE\` formats.

\- **\*\*Null & Type Handling\*\***: Coerced scores and appearances to nullable \`Int64\` to preserve unplayed/scheduled matches without false zeroes.



**### 2. Multi-Source Player Image Resolution Workflow**

Player headshots are notoriously inconsistent across third-party soccer APIs. The pipeline implements a 3-step validation pipeline:



\`\`\`

                      ┌───────────────────────────────────────┐

                      │ Extract Player Records (Dim_Players)   │

                      └───────────────────────────────────────┘

                                          │

                                          ▼

                      ┌───────────────────────────────────────┐

                      │ Tier 1: ESPN Official Headshot CDN    │

                      │ Status 200 & Content-Length > 2000 B? │

                      └───────────────────────────────────────┘

                                     /         \\

                             [YES]  /           \  [NO / Placeholder]

                                   ▼             ▼

                      ┌────────────────┐   ┌────────────────────────────────────┐

                      │ Keep ESPN URL  │   │ Tier 2: TheSportsDB Player Search  │

                      └────────────────┘   │ Normalize: NFKD + Remove Accents   │

                                           │ Match: Player Name + Club Name     │

                                           └────────────────────────────────────┘

                                                            /         \\

                                                   [MATCH] /           \  [NO MATCH]

                                                          ▼             ▼

                                           ┌─────────────────┐   ┌─────────────────┐

                                           │ Store Cutout URL│   │ Store NULL      │

                                           │ (Verified)      │   │ (Fallback Initial)

                                           └─────────────────┘   └─────────────────┘

\`\`\`



1\. **\*\*ESPN Verification (\`check_photos.py\`)\*\***: Uses Python's \`ThreadPoolExecutor\` (12 threads) to test ESPN player headshot endpoints. Blank placeholders returning tiny generic bytes (<2 KB) are discarded.

2\. **\*\*TheSportsDB Name & Club Disambiguation (\`fetch_photos.py\`)\*\***:

   - Accented player names (e.g., \`"Yeray Álvarez"\`, \`"Aurélien Tchouaméni"\`) are decomposed using \`unicodedata.normalize('NFKD')\` and stripped to alphanumeric ASCII tokens.

   - Cross-references the player's club abbreviation against team synonyms (\`display_name\`, \`short_name\`, \`name\`) to prevent false positive matches for players with identical names at different clubs.

3\. **\*\*Resolution Statistics\*\***:

   - Total Unique Players in Scope: **\*\*294\*\***

   - Verified Cutouts via TheSportsDB: **\*\*217\*\***

   - Verified Headshots via ESPN: **\*\*6\*\***

   - Filtered Out (Club Mismatches): **\*\*15\*\***

   - Unmatched (Clean Initial Fallback): **\*\*56\*\***

   - **\*\*Total Verified Headshot Coverage\*\***: **\*\*76.0% (223 players)\*\***



**---**



**## 🗄️ Database Design & Star Schema**



The SQL Server database \`SpainLeague\` is modeled as a dimensional data warehouse:



\<div *align*="center">



![Data Model]\(project_screens/a_detailed_high_contrast_power_bi_style_data_mode.png)

*\*Figure 2: Power BI High-Contrast Relational Star Schema Data Model.\**



\</div>



**### Dimension Tables**

\- **\*\*\`Teams\`\*\*** (20 rows): \`team_id\` [PK], \`abbrev\`, \`name\`, \`display_name\`, \`short_name\`, \`location\`, \`color\`, \`logo\`.

\- **\*\*\`Dim_Players\`\*\*** (294 rows): \`player_id\` [PK], \`name\`, \`team\` [FK to \`Teams.abbrev\`], \`position\`, \`Player_Image_URL\`.



**### Fact Tables**

\- **\*\*\`Fact_Matches\`\*\*** (380 rows): \`game_id\` [PK], \`date\`, \`status\`, \`venue\`, \`attendance\`, \`Home_Team_ID\` [FK], \`Home_Score\`, \`Away_Team_ID\` [FK], \`Away_Score\`.

\- **\*\*\`Fact_Player_Leaders\`\*\*** (776 rows): \`rank\`, \`player_id\` [FK to \`Dim_Players\`], \`name\`, \`position\`, \`team\`, \`games\`, \`minutes\`, \`value\`, \`per90\`, \`stat\`.

\- **\*\*\`Fact_Standings\`\*\*** (20 rows): \`rank\`, \`team_id\` [FK to \`Teams\`], \`played\`, \`wins\`, \`draws\`, \`losses\`, \`goals_for\`, \`goals_against\`, \`goal_diff\`, \`points\`, \`form\`.

\- **\*\*\`Fact_Team_Stats\`\*\*** (20 rows): \`team_id\` [FK to \`Teams\`], \`goals_for\`, \`goals_against\`, \`xg_for\`, \`xg_against\`, \`shots_for\`, \`possession_pct\`, \`pass_accuracy_pct\`, \`clean_sheets\`.

\- **\*\*\`Fact_Ratings\`\*\*** (23 rows): \`rank\`, \`team_id\` [FK to \`Teams\`], \`elo\`, \`last_game\`.



**---**



**## 📊 Power BI Dashboard Pages**



The application is deployed on a custom **\*\*2560 × 1150 ultra-wide high-definition canvas\*\*** utilizing an elegant cyberpunk/stadium aesthetic (\`#080E19\` dark canvas, \`#111D31\` card panels, \`#E94560\` crimson accents, \`#F5B942\` gold highlights, and \`#28C39A\` emerald indicators).



**### Page 1: League Overview (\`overview\`)**

*\*Executive summary of the championship trajectory.\**

\- **\*\*Top Metric Ribbon\*\***: Total matches played (with completion %), upcoming scheduled fixtures, cumulative goals scored, scoring average per match (2.6+), and home win percentage (46%+).

\- **\*\*Match Hero Banner\*\***: Real-time spotlight of the latest completed marquee fixture or upcoming high-stakes derby with team crests and venue details.

\- **\*\*Live Standings Table\*\***: Form-guided table tracking positions 1 to 20 with goal differential and points.

\- **\*\*Scoring Leaders Showcase\*\***: Top scorers and assist playmakers with headshot cards and efficiency metrics.



\<div *align*="center">



![League Overview]\(docs/screenshots/overview%20%282%29.png)

*\*Figure 3: League Overview Dashboard Screenshot.\**



\</div>



**---**



**### Page 2: Team Intelligence (\`teams\`)**

*\*Deep tactical analysis of individual club performance.\**

\- **\*\*Club Identity Spotlight\*\***: Team crest, stadium location, current league position, and Elo rating rank.

\- **\*\*Attacking vs. Defensive Quadrant\*\***: Goals scored vs. Expected Goals (\`xG\`), total shots, shots on target %, goals conceded, and clean sheet counts.

\- **\*\*Possession & Discipline Profile\*\***: Ball possession %, passing accuracy %, fouls committed, and yellow/red disciplinary counts.

\- **\*\*Home vs. Away Breakdown\*\***: Home win rate vs. away travel performance.



\<div *align*="center">



![Team Intelligence]\(docs/screenshots/time%26team_intell.png)

*\*Figure 4: Team Performance & Tactical Intelligence Dashboard Screenshot.\**



\</div>



**---**



**### Page 3: Match Centre (\`matches\`)**

*\*Comprehensive head-to-head tactical preview and fixture analysis.\**

\- **\*\*Independent Team Selection\*\***: Driven by disconnected calculated tables \`Home Pick\` and \`Away Pick\`.

\- **\*\*Match Scoreboard & Status\*\***: Displays final scores, historical dates, stadium attendance, and venue cities.

\- **\*\*Head-to-Head Metric Comparison\*\***: Side-by-side comparison of offensive averages, recent 5-game form, and Elo rating gap.



\<div *align*="center">



![Match Centre]\(docs/screenshots/matchcentre.png)

*\*Figure 5: Match Centre Head-to-Head Tactical Preview Screenshot.\**



\</div>



**---**



**### Page 4: Player Lab (\`players\`)**

*\*Granular scouting and individual player benchmarking.\**

\- **\*\*Player Profile Card\*\***: Player cutout portrait, position, club affiliation, and appearance statistics.

\- **\*\*Performance Rings\*\***: Radial progress rings displaying player ranking against the league's top-100 threshold in goals, assists, and xG.

\- **\*\*Radar Benchmark\*\***: 5-axis normalized radar chart evaluating scoring volume, shooting accuracy, goal contributions, and per-90 rates.



\<div *align*="center">



![Player Lab]\(docs/screenshots/playerlab.png)

*\*Figure 6: Individual Player Lab Scouting & Performance Screenshot.\**



\</div>



**---**



**### Page 5: Player Comparison (\`compare\`)**

*\*Multi-athlete side-by-side performance evaluation.\**

\- **\*\*Multi-Select Comparison\*\***: Supports up to 4 concurrent players via the disconnected \`Compare Pick\` slicer (defaults to top 3 goal scorers).

\- **\*\*Comparative Performance Radar\*\***: Overlaid SVG radar polygons color-coded per player (Emerald, Gold, Crimson, Sky Blue) normalized against league-wide per-90 maximums.

\- **\*\*Head-to-Head Metric Bars\*\***: Relative bar charts comparing goals/90, assists/90, shots/90, shots on target/90, and total minutes.



\<div *align*="center">



![Player Comparison]\(docs/screenshots/playerscom.png)

*\*Figure 7: Multi-Player Comparison Dashboard with Dynamic SVG Polar Radar Chart.\**



\</div>



**---**



**## ⚡ Interactive HTML & SVG Dashboard Engine**



Rather than relying on disjointed native visuals, the entire 5-page dashboard UI is rendered via a single, highly-optimized **\*\*665-line DAX measure\*\*** (\`HTML LaLiga App\`) hosted in Microsoft-certified **\*\*HTML Content\*\***:



**### Key DAX Architectural Innovations**

1\. **\*\*Dynamic Single-Page Application (SPA)\*\***:

   \`\`\`dax

   VAR Page = SELECTEDVALUE('Dashboard Pages'[PageKey], "overview")

   RETURN

       SWITCH(Page,&#x20;

           "teams", TeamPage,&#x20;

           "players", PlayerPage,&#x20;

           "matches", MatchPage,&#x20;

           "compare", ComparePage,&#x20;

           OverviewPage

       )

   \`\`\`

2\. **\*\*Mathematical SVG Polar Radar Generation\*\***:

   The measure dynamically calculates trigonometric vertices in DAX to render SVG polygon coordinates:

   $$\text{X} = \text{Center}\_X + \text{Radius} \times \text{Score} \times \cos(\theta)$$

   $$\text{Y} = \text{Center}\_Y + \text{Radius} \times \text{Score} \times \sin(\theta)$$

3\. **\*\*Disconnected Parameter Slicers\*\***:

   \`Home Pick\`, \`Away Pick\`, and \`Compare Pick\` are calculated tables devoid of physical relationships, preventing unwanted cross-filtering cascading.

4\. **\*\*CSS Overlay Cover Technique\*\***:

   To present clean page-specific slicers without visual clutter, auxiliary measures \`Cover Home Away\` and \`Cover Compare\` render empty dark blocks (\`#0B1426\`) that dynamically mask inactive slicers when their parent page is not selected:

   \`\`\`dax

   Cover Home Away =

   IF(

       SELECTEDVALUE('Dashboard Pages'[PageKey]) = "matches",

       "",

       "\<div style='width:100%;height:100%;background:#0B1426;'>\</div>"

   )

   \`\`\`



**---**



**## 🛠️ Installation & Reproduction**



**### Prerequisites**

\- Python 3.10 or higher

\- Microsoft SQL Server (Developer, Standard, or Express edition)

\- Microsoft ODBC Driver 17 for SQL Server

\- Power BI Desktop (May 2024 or later)

\- Striker API Key (Optional: project includes pre-cached responses for offline execution)



**### 1. Clone the Repository**

\`\`\`bash

git clone https\://github.com/moaaz311/LaLiga-Match-Intelligence-Analytics.git

cd LaLiga-Match-Intelligence-Analytics

\`\`\`



**### 2. Configure Environment**

Create your local environment file from the template:

\`\`\`bash

cp .env.example .env

\`\`\`

Edit \`.env\` with your SQL Server configuration:

\`\`\`env

DB_SERVER=localhost

DB_NAME=SpainLeague

DB_DRIVER=ODBC Driver 17 for SQL Server

STRIKER_API_KEY=sk_live_your_key_here

\`\`\`



**### 3. Install Dependencies**

\`\`\`bash

pip install -r requirements.txt

\`\`\`



**### 4. Initialize Database**

Execute the database creation script in SQL Server Management Studio (SSMS) or via sqlcmd:

\`\`\`bash

sqlcmd -S localhost -i database/schema_and_queries.sql

\`\`\`



**### 5. Run Data Extraction & Image Enrichment**

\`\`\`bash

\# Verify database connectivity

python scripts/test_db_connection.py



\# Ingest league data (uses local cache if no key provided)

python scripts/load_striker.py



\# Check ESPN CDN headshots

python scripts/check_photos.py



\# Resolve and update TheSportsDB player images

python scripts/fetch_photos.py

\`\`\`



**### 6. Open Power BI Report**

1\. Open \`powerbi/LaligaFinal.pbix\` in Power BI Desktop.

2\. In **\*\*Home > Transform Data > Data Source Settings\*\***, ensure your SQL Server instance name matches \`DB_SERVER\`.

3\. Click **\*\*Refresh\*\*** to load the data.



**---**



**## 🏆 Key Analytical Insights Delivered**



1\. **\*\*Home Advantage Significance\*\***: Across the 2026/2027 season, home clubs convert **\*\*46.8% of matches into victories\*\***, compared to only **\*\*28.4% away wins\*\***, with home teams generating a +0.48 goal differential per game.

2\. **\*\*Finishing Efficiency vs. Expected Goals\*\***: Overperforming top scorers generate **\*\*+3.2 to +4.5 actual goals\*\*** above their cumulative xG model expectation, identifying elite ball strikers with clinical finishing in low-probability zones.

3\. **\*\*Possession vs. Result Disconnect\*\***: Teams averaging >58% possession demonstrate high box-entry volumes but occasionally suffer higher defensive concessions per counter-attack shot faced, visible via the attack/defense quadrant.



**---**



**## 🔮 Roadmap & Future Enhancements**



\- [ ] **\*\*Automated CI/CD ETL Refresh\*\***: Deploy GitHub Actions or Azure Data Factory pipelines to execute automated weekly fixture updates.

\- [ ] **\*\*Machine Learning Match Outcome Classifier\*\***: Train an XGBoost / LightGBM model utilizing rolling Elo ratings and xG differential to predict upcoming fixture probabilities.

\- [ ] **\*\*Shot Map Visualization\*\***: Incorporate $(x, y)$ coordinate shot charts with xG circle sizing directly into the Player Lab SVG visual.

\- [ ] **\*\*Pass Network Sonar\*\***: Visualize passing networks and progressive passing distribution between midfield and frontline units.



**---**



**## 👤 Author & Contact**



**\*\*Moaaz Achraf Sophy\*\***

\- **\*\*Role\*\***: Junior BI Developer & Data Analyst (ITI Power BI Track Graduate)

\- **\*\*LinkedIn\*\***: [linkedin.com/in/moaaz-achraf]\(https\://www\.linkedin.com/in/moaaz-achraf/)

\- **\*\*GitHub\*\***: [github.com/moaaz311]\(https\://github.com/moaaz311)

\- **\*\*Portfolio\*\***: [portfolio-bay-five-76.vercel.app]\(https\://portfolio-bay-five-76.vercel.app/)

\- **\*\*Email\*\***: [moaazachraf503\@gmail.com]\(mailto:moaazachraf503\@gmail.com)




