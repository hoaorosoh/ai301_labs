-- loading unique teams
INSERT INTO teams (current_name)
SELECT DISTINCT COALESCE(f.current, raw_names.team_name) AS actual_current_name
FROM (
    SELECT home_team AS team_name FROM results
    UNION
    SELECT away_team FROM results
    UNION
    SELECT team FROM goalscorers
    UNION
    SELECT current FROM former_names
) AS raw_names
LEFT JOIN former_names f 
    ON raw_names.team_name = f.former
WHERE COALESCE(f.current, raw_names.team_name) IS NOT NULL;

-- loading matches
INSERT INTO matches (date, city, country, tournament, home_team_id, away_team_id, home_score, away_score, winner_id, neutral)
WITH NameToID AS (
    -- Get current names
    SELECT current_name AS search_name, team_id FROM teams
    UNION
    -- Get former names and link them to the current team_id
    SELECT f.former AS search_name, t.team_id 
    FROM former_names f
    JOIN teams t ON f.current = t.current_name
)
SELECT 
    r.date, 
    r.city, 
    r.country, 
    r.tournament, 
    th.team_id AS home_team_id, 
    ta.team_id AS away_team_id, 
    r.home_score, 
    r.away_score, 
    CASE 
        WHEN r.home_score > r.away_score THEN th.team_id
        WHEN r.away_score > r.home_score THEN ta.team_id
        ELSE NULL 
    END AS winner_id,
    r.neutral
FROM results r
JOIN NameToID th ON r.home_team = th.search_name
JOIN NameToID ta ON r.away_team = ta.search_name;


INSERT INTO goals (match_id, team_id, scorer, minute, own_goal, penalty)
WITH NameToID AS (
    -- Get current names
    SELECT current_name AS search_name, team_id FROM teams
    UNION
    -- Get former names and link them to the current team_id
    SELECT f.former AS search_name, t.team_id 
    FROM former_names f
    JOIN teams t ON f.current = t.current_name
)
SELECT 
    m.match_id,
    tg.team_id,
    g.scorer,
    g.minute,
    g.own_goal,
    g.penalty
FROM goalscorers g
-- Swap home team string for ID
JOIN NameToID th ON g.home_team = th.search_name
-- Swap away team string for ID
JOIN NameToID ta ON g.away_team = ta.search_name
-- Triangulate the match_id using the date and team IDs
JOIN matches m ON g.date = m.date AND m.home_team_id = th.team_id AND m.away_team_id = ta.team_id
-- Swap the scoring team string for ID
JOIN NameToID tg ON g.team = tg.search_name;