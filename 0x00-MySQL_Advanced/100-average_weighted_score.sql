-- creates a stored procedure ComputeAverageWeightedScoreForUser
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
BEGIN
	DECLARE sum_scorexW FLOAT;
    DECLARE sum_weights FLOAT;
	SELECT SUM(corrections.score * projects.weight) INTO sum_scorexW
    FROM corrections
    JOIN projects ON projects.id = corrections.project_id
    WHERE corrections.user_id = user_id;

	SELECT SUM(projects.weight) INTO sum_weights
    FROM projects
    JOIN corrections ON projects.id = corrections.project_id
    WHERE corrections.user_id = user_id;

	UPDATE users SET average_score = sum_scorexW / sum_weights WHERE id = user_id;
END $$
DELIMITER ;