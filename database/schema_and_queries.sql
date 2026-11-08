-- =====================================================================
-- LaLiga Match Intelligence & Analytics Platform
-- Database Creation, Schema DDL, Constraints & Analytical Queries
-- Target Engine: Microsoft SQL Server (2016+)
-- =====================================================================

USE master;
GO

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'SpainLeague')
BEGIN
    CREATE DATABASE SpainLeague;
END
GO

USE SpainLeague;
GO

-- =====================================================================
-- 1. DIMENSION TABLES
-- =====================================================================

-- Dim_Teams: 20 LaLiga clubs
IF OBJECT_ID('dbo.Teams', 'U') IS NOT NULL
BEGIN
    -- Ensure primary key constraint exists
    IF NOT EXISTS (SELECT * FROM sys.key_constraints WHERE name = 'PK_Teams_team_id')
    BEGIN
        ALTER TABLE dbo.Teams ALTER COLUMN team_id VARCHAR(50) NOT NULL;
        ALTER TABLE dbo.Teams ADD CONSTRAINT PK_Teams_team_id PRIMARY KEY CLUSTERED (team_id);
    END
END
GO

-- Dim_Players: 294 Unique Players extracted from league leaderboards
IF OBJECT_ID('dbo.Dim_Players', 'U') IS NOT NULL
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.key_constraints WHERE name = 'PK_Dim_Players_player_id')
    BEGIN
        ALTER TABLE dbo.Dim_Players ALTER COLUMN player_id VARCHAR(50) NOT NULL;
        ALTER TABLE dbo.Dim_Players ADD CONSTRAINT PK_Dim_Players_player_id PRIMARY KEY CLUSTERED (player_id);
    END
END
GO

-- =====================================================================
-- 2. FACT TABLES
-- =====================================================================

-- Fact_Matches: 380 full-season match fixtures & results
IF OBJECT_ID('dbo.Fact_Matches', 'U') IS NOT NULL
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.key_constraints WHERE name = 'PK_Fact_Matches_game_id')
    BEGIN
        ALTER TABLE dbo.Fact_Matches ALTER COLUMN game_id VARCHAR(50) NOT NULL;
        ALTER TABLE dbo.Fact_Matches ADD CONSTRAINT PK_Fact_Matches_game_id PRIMARY KEY CLUSTERED (game_id);
    END
    
    -- Helpful Indexes
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Fact_Matches_date')
        CREATE NONCLUSTERED INDEX IX_Fact_Matches_date ON dbo.Fact_Matches([date]);
        
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Fact_Matches_Home_Team_ID')
        CREATE NONCLUSTERED INDEX IX_Fact_Matches_Home_Team_ID ON dbo.Fact_Matches(Home_Team_ID);
        
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Fact_Matches_Away_Team_ID')
        CREATE NONCLUSTERED INDEX IX_Fact_Matches_Away_Team_ID ON dbo.Fact_Matches(Away_Team_ID);
END
GO

-- Fact_Player_Leaders: 776 metric records across 10 statistical categories
IF OBJECT_ID('dbo.Fact_Player_Leaders', 'U') IS NOT NULL
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Fact_Player_Leaders_stat')
        CREATE NONCLUSTERED INDEX IX_Fact_Player_Leaders_stat ON dbo.Fact_Player_Leaders(stat, [value] DESC);
        
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Fact_Player_Leaders_player_id')
        CREATE NONCLUSTERED INDEX IX_Fact_Player_Leaders_player_id ON dbo.Fact_Player_Leaders(player_id);
END
GO

-- Fact_Standings: Official League Standings Table (20 Clubs)
IF OBJECT_ID('dbo.Fact_Standings', 'U') IS NOT NULL
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Fact_Standings_rank')
        CREATE NONCLUSTERED INDEX IX_Fact_Standings_rank ON dbo.Fact_Standings([rank] ASC);
END
GO

-- Fact_Team_Stats: Deep Team-Level Advanced Metrics (20 Clubs)
IF OBJECT_ID('dbo.Fact_Team_Stats', 'U') IS NOT NULL
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Fact_Team_Stats_team_id')
        CREATE NONCLUSTERED INDEX IX_Fact_Team_Stats_team_id ON dbo.Fact_Team_Stats(team_id);
END
GO

-- Fact_Ratings: Club Elo Strength Ratings
IF OBJECT_ID('dbo.Fact_Ratings', 'U') IS NOT NULL
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Fact_Ratings_elo')
        CREATE NONCLUSTERED INDEX IX_Fact_Ratings_elo ON dbo.Fact_Ratings(elo DESC);
END
GO


-- =====================================================================
-- 3. ANALYTICAL QUERIES & VERIFICATION
-- =====================================================================

-- Table Record Counts Verification
SELECT 'Teams' AS [Table_Name], COUNT(*) AS [Record_Count] FROM dbo.Teams
UNION ALL SELECT 'Dim_Players', COUNT(*) FROM dbo.Dim_Players
UNION ALL SELECT 'Fact_Matches', COUNT(*) FROM dbo.Fact_Matches
UNION ALL SELECT 'Fact_Player_Leaders', COUNT(*) FROM dbo.Fact_Player_Leaders
UNION ALL SELECT 'Fact_Ratings', COUNT(*) FROM dbo.Fact_Ratings
UNION ALL SELECT 'Fact_Standings', COUNT(*) FROM dbo.Fact_Standings
UNION ALL SELECT 'Fact_Team_Stats', COUNT(*) FROM dbo.Fact_Team_Stats;
GO

-- Top 10 Scorers with per-90 Efficiency and Team Details
SELECT TOP 10
    pl.[rank] AS [Rank],
    pl.name AS [Player_Name],
    p.position AS [Position],
    t.display_name AS [Club],
    pl.games AS [Matches_Played],
    pl.minutes AS [Minutes_Played],
    pl.[value] AS [Goals_Scored],
    pl.per90 AS [Goals_Per_90],
    p.Player_Image_URL AS [Photo_URL]
FROM dbo.Fact_Player_Leaders pl
INNER JOIN dbo.Dim_Players p ON pl.player_id = p.player_id
LEFT JOIN dbo.Teams t ON p.team = t.abbrev
WHERE pl.stat = 'goals'
ORDER BY pl.[value] DESC, pl.per90 DESC;
GO

-- Expected Goals (xG) vs Actual Goals Overperformance Analysis
WITH Goals AS (
    SELECT player_id, name, team, [value] AS actual_goals, per90 AS goals_per90
    FROM dbo.Fact_Player_Leaders
    WHERE stat = 'goals'
),
XG AS (
    SELECT player_id, [value] AS expected_goals, per90 AS xg_per90
    FROM dbo.Fact_Player_Leaders
    WHERE stat = 'xg'
)
SELECT TOP 15
    g.name AS [Player_Name],
    g.team AS [Team],
    g.actual_goals AS [Actual_Goals],
    ROUND(x.expected_goals, 2) AS [Expected_Goals_xG],
    ROUND(g.actual_goals - x.expected_goals, 2) AS [xG_Overperformance],
    ROUND(g.goals_per90, 2) AS [Goals_Per_90],
    ROUND(x.xg_per90, 2) AS [xG_Per_90]
FROM Goals g
INNER JOIN XG x ON g.player_id = x.player_id
ORDER BY [xG_Overperformance] DESC;
GO

-- League Standings Summary & Goal Difference
SELECT 
    [rank] AS [Pos],
    display_name AS [Club],
    played AS [P],
    wins AS [W],
    draws AS [D],
    losses AS [L],
    goals_for AS [GF],
    goals_against AS [GA],
    goal_diff AS [GD],
    points AS [PTS],
    [form] AS [Recent_Form]
FROM dbo.Fact_Standings
ORDER BY [rank] ASC;
GO

-- Team Offensive and Defensive Efficiency
SELECT 
    ts.display_name AS [Club],
    ts.games AS [Games],
    ROUND(ts.goals_for, 2) AS [Total_Goals_For],
    ROUND(ts.goals_against, 2) AS [Total_Goals_Against],
    ROUND(ts.goals_for / NULLIF(ts.games, 0), 2) AS [Scoring_Avg_Per_Game],
    ROUND(ts.goals_against / NULLIF(ts.games, 0), 2) AS [Conceded_Avg_Per_Game],
    ROUND(ts.possession_pct, 1) AS [Avg_Possession_Pct],
    ROUND(ts.pass_accuracy_pct, 1) AS [Pass_Accuracy_Pct],
    ts.clean_sheets AS [Clean_Sheets]
FROM dbo.Fact_Team_Stats ts
ORDER BY [Scoring_Avg_Per_Game] DESC;
GO

-- Home vs Away League Wide Win Percentages
SELECT 
    COUNT(*) AS [Total_Matches_Played],
    SUM(CASE WHEN Home_Score > Away_Score THEN 1 ELSE 0 END) AS [Home_Wins],
    SUM(CASE WHEN Away_Score > Home_Score THEN 1 ELSE 0 END) AS [Away_Wins],
    SUM(CASE WHEN Home_Score = Away_Score THEN 1 ELSE 0 END) AS [Draws],
    ROUND(100.0 * SUM(CASE WHEN Home_Score > Away_Score THEN 1 ELSE 0 END) / COUNT(*), 1) AS [Home_Win_Pct],
    ROUND(100.0 * SUM(CASE WHEN Away_Score > Home_Score THEN 1 ELSE 0 END) / COUNT(*), 1) AS [Away_Win_Pct],
    ROUND(100.0 * SUM(CASE WHEN Home_Score = Away_Score THEN 1 ELSE 0 END) / COUNT(*), 1) AS [Draw_Pct],
    SUM(Home_Score + Away_Score) AS [Total_Goals],
    ROUND(1.0 * SUM(Home_Score + Away_Score) / COUNT(*), 2) AS [Avg_Goals_Per_Match]
FROM dbo.Fact_Matches
WHERE status = 'final';
GO

