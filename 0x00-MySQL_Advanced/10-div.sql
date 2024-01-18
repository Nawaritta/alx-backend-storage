-- divides (and returns) the first by the second number
DELIMITER $$
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT
BEGIN
    RETURN CASE
        WHEN b = 0 THEN 0
        ELSE a / b
    END;
END;
$$
DELIMITER ;
