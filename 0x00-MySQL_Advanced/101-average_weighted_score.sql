-- This script creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and stores the average weighted score for all students

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE user_id INT;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        UPDATE users
        SET average_score = (
            SELECT SUM(corrections.score * projects.weight) / SUM(projects.weight)
            FROM corrections
            JOIN projects ON projects.id = corrections.project_id AND corrections.user_id = user_id
        )
        WHERE id = user_id;
    END LOOP;

    CLOSE cur;
END //

DELIMITER ;
