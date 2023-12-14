-- Create the ComputeAverageWeightedScoreForUser procedure

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight FLOAT;
    
    -- Initialize variables
    SET total_weighted_score = 0;
    SET total_weight = 0;
    
    -- Calculate the weighted average score for the user
    SELECT SUM(corrections.score * projects.weight) INTO total_weighted_score, SUM(projects.weight) INTO total_weight
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;
    
    -- Update the user's average score
    IF total_weight > 0 THEN
        UPDATE users SET average_score = total_weighted_score / total_weight WHERE id = user_id;
    ELSE
        UPDATE users SET average_score = 0 WHERE id = user_id;
    END IF;
END//

DELIMITER ;
