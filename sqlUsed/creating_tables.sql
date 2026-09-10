-- 1. Teams Table (Base table)
CREATE TABLE teams (
    team_id INT PRIMARY KEY AUTO_INCREMENT,
    current_name VARCHAR(255) NOT NULL
);

-- 2. Team Name Changes (Maps to former_names)
-- 1:N relationship with Teams
CREATE TABLE team_name_changes (
    change_id INT PRIMARY KEY AUTO_INCREMENT,
    team_id INT NOT NULL,
    current_name VARCHAR(255),
    former_name VARCHAR(255),
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

-- 3. Matches (Maps to results)
-- N:1 relationships with Teams for home, away, and winner
CREATE TABLE matches (
    match_id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE,
    city VARCHAR(255),
    country VARCHAR(255),
    tournament VARCHAR(255),
    home_team_id INT NOT NULL,
    away_team_id INT NOT NULL,
    home_score INT,
    away_score INT,
    winner_id INT,
    neutral INT, -- Included from the results schema screenshot
    FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (winner_id) REFERENCES teams(team_id)
);

-- 4. Goals (Maps to goalscorers)
-- N:1 relationships with Matches ("were in") and Teams ("by team")
CREATE TABLE goals (
    goal_id INT PRIMARY KEY AUTO_INCREMENT,
    match_id INT NOT NULL,
    team_id INT NOT NULL,
    scorer VARCHAR(255),
    minute INT,
    own_goal INT,
    penalty INT,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);former_names