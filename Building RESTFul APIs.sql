CREATE DATABASE fitness_center;
USE fitness_center;

CREATE TABLE Members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE WorkoutSessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    workout_type VARCHAR(100),
    duration INT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES Members(id)
);
