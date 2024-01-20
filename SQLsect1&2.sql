--Database Schema Design (1 marks)
-- Create the ADTAssignment2 database
CREATE DATABASE ADTAssignment2;
GO
-- Use the ADTAssignment2 database
USE ADTAssignment2;
GO

-- Create the program table
CREATE TABLE program (
    programID INT PRIMARY KEY,
    name NVARCHAR(255) NOT NULL
);
GO

-- Create the depCourse table
CREATE TABLE depCourse (
    courseID INT PRIMARY KEY,
    deptName NVARCHAR(255) NOT NULL,
    programID INT FOREIGN KEY REFERENCES program(programID)
);
GO

-- Create the users table
CREATE TABLE users (
    userID INT PRIMARY KEY,
    programID INT FOREIGN KEY REFERENCES program(programID)
);
GO

-- Create the courseSiteVisit table
CREATE TABLE courseSiteVisit (
    visitID INT PRIMARY KEY,
    courseID INT FOREIGN KEY REFERENCES depCourse(courseID),
    userID INT FOREIGN KEY REFERENCES users(userID),
    [date] DATE
);
GO
-- Insert sample data into the program table
INSERT INTO program (programID, name) VALUES
(1, 'Undergrad'),
(2, 'Master');

-- Insert sample data into the depCourse table
INSERT INTO depCourse (courseID, deptName, programID) VALUES
(1, 'Computer Science', 1),
(2, 'Computer Science', 1),
(3, 'Maths', 1),
(4, 'Maths', 2),
(5, 'Computer Science', 2),
(6, 'Maths', 2),
(7,'Mech',2),
(8,'Mech',1);

-- Insert sample data into the users table
INSERT INTO users (userID, programID) VALUES
(1, 1),
(2, 1),
(3, 1),
(4, 2),
(5, 2),
(6, 2),
(7,1),
(8,1),
(9,1),
(10,2),
(11,2),
(12,2),
(13,2);


-- Insert sample data into the courseSiteVisit table
-- For simplicity, assuming today's date is '2023-01-01'

-- i. there are at least 2 users visited all courses
INSERT INTO courseSiteVisit (visitID, courseID, userID, [date])
SELECT 
    ROW_NUMBER() OVER (ORDER BY c.courseID, u.userID, NEWID()), 
    c.courseID, 
    u.userID, 
    '2023-02-01' 
FROM depCourse c
CROSS JOIN users u;

-- ii. all users should have visited at least 1 course
INSERT INTO courseSiteVisit (visitID, courseID, userID, [date])
SELECT 
    ROW_NUMBER() OVER (ORDER BY c.courseID, u.userID, NEWID()), 
    c.courseID, 
    u.userID, 
    '2023-01-02' 
FROM depCourse c
CROSS JOIN users u
WHERE RAND() < 0.5;

-- iii. each user should have visited at least 1 course multiple times on the same date
INSERT INTO courseSiteVisit (visitID, courseID, userID, [date])
SELECT 
    ROW_NUMBER() OVER (ORDER BY c.courseID, u.userID, NEWID()), 
    c.courseID, 
    u.userID, 
    '2023-01-03' 
FROM depCourse c
CROSS JOIN users u
WHERE RAND() < 0.8;

-- iv. each user should have visited multiple dates per a single course
INSERT INTO courseSiteVisit (visitID, courseID, userID, [date])
SELECT 
    ROW_NUMBER() OVER (ORDER BY c.courseID, u.userID, NEWID()), 
    c.courseID, 
    u.userID, 
    '2023-01-04' 
FROM depCourse c
CROSS JOIN users u
WHERE RAND() < 0.4;
SELECT COUNT(*) FROM courseSiteVisit;
select * from courseSiteVisit

INSERT INTO courseSiteVisit (visitID, courseID, userID, [date]) values(107,1,1,'2023-02-04')

DECLARE @i INTEGER;
SET @i=1;
WHILE @i<=4
BEGIN
	INSERT INTO courseSiteVisit (visitID, courseID, userID, [date]) values(215+@i,@i,@i+1,'2023-09-04')	
	SET @i=@i+1;
END;
	