CREATE DATABASE SpainLeague;



USE SpainLeague;
SELECT 'Teams' AS tbl, COUNT(*) AS n FROM Teams
UNION ALL SELECT 'Fact_Matches', COUNT(*) FROM Fact_Matches          -- up to 380
UNION ALL SELECT 'Fact_Standings', COUNT(*) FROM Fact_Standings      -- 20
UNION ALL SELECT 'Fact_Team_Stats', COUNT(*) FROM Fact_Team_Stats    -- 20
UNION ALL SELECT 'Fact_Ratings', COUNT(*) FROM Fact_Ratings
UNION ALL SELECT 'Fact_Player_Leaders', COUNT(*) FROM Fact_Player_Leaders
UNION ALL SELECT 'Dim_Players', COUNT(*) FROM Dim_Players;

SELECT TOP 5 Home_Team, Home_Score, Away_Team, Away_Score, [date]
FROM Fact_Matches ORDER BY [date] DESC;