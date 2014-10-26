SELECT * FROM workoutbutton.Workouts;

LOAD DATA LOCAL INFILE '/Users/seanokeeffe/Desktop/workoutTable.csv'
INTO TABLE workoutbutton.Workouts 
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r'
IGNORE 1 ROWS;

DELETE FROM workoutbutton.Workouts;

UPDATE workoutbutton.Workouts
SET Reps=8
WHERE ID=3;
