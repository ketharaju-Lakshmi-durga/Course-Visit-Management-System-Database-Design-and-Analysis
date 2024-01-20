USE ADTAssignment2
GO
--3a:Total Number of Times a Course has been Visited or Accessed by All Users:
SELECT courseID, COUNT(visitID) as totalVisits
FROM courseSiteVisit
GROUP BY courseID;
--b. Total Number of Visits for Each Course, Categorized by Program:
SELECT c.courseID, p.name as program, COUNT(v.visitID) as totalVisits
FROM courseSiteVisit v
JOIN depCourse c ON v.courseID = c.courseID
JOIN program p ON c.programID = p.programID
GROUP BY c.courseID, p.name;

--c. Total Number of Students or Users Enrolled in Each Program:
SELECT p.name as program, COUNT(u.userID) as totalUsers
FROM program p
LEFT JOIN users u ON p.programID = u.programID
GROUP BY p.name;

--d Total Number of Unique Visitors per Department by Program:
SELECT c.deptName, p.name as program, COUNT(DISTINCT v.userID) as uniqueVisitors
FROM courseSiteVisit v
JOIN depCourse c ON v.courseID = c.courseID
JOIN program p ON c.programID = p.programID
GROUP BY c.deptName, p.name;
--e:Most Recent Date on Which a User Visited Each Course:
SELECT courseID, MAX([date]) as mostRecentDate
FROM courseSiteVisit
GROUP BY courseID;

--f:Number of Times a User has Visited Each Course:
SELECT userID, courseID, COUNT(visitID) as visitCount
FROM courseSiteVisit
GROUP BY userID, courseID;

--g User who has Visited a Course the Most:
WITH RankedVisits AS (
    SELECT userID, courseID, COUNT(visitID) as visitCount,
           ROW_NUMBER() OVER (PARTITION BY courseID ORDER BY COUNT(visitID) DESC) as rn
    FROM courseSiteVisit
    GROUP BY userID, courseID
)
SELECT userID, courseID, visitCount
FROM RankedVisits
WHERE rn = 1;

--h.User who Visited a Course the Most Times in a Single Day:
WITH MaxVisitsInDay AS (
    SELECT userID, courseID, MAX(visitCount) as maxVisitsInDay
    FROM (
        SELECT userID, courseID, [date], COUNT(visitID) as visitCount
        FROM courseSiteVisit
        GROUP BY userID, courseID, [date]
    ) AS VisitsPerDay
    GROUP BY userID, courseID
)
SELECT userID, courseID, maxVisitsInDay
FROM MaxVisitsInDay
WHERE maxVisitsInDay = 1;

--i  Longest Visit Streak Days per User per Course:
WITH UserCourseVisitCounts AS (
    SELECT userID, courseID, [date],
           ROW_NUMBER() OVER (PARTITION BY userID, courseID ORDER BY [date]) -
           ROW_NUMBER() OVER (PARTITION BY userID, courseID ORDER BY [date]) as visitGroup
    FROM courseSiteVisit
),
LongestStreaks AS (
    SELECT userID, courseID, MIN([date]) as startDate, MAX([date]) as endDate,
           DATEDIFF(day, MIN([date]), MAX([date])) + 1 as streakDays
    FROM UserCourseVisitCounts
    GROUP BY userID, courseID, visitGroup
)
SELECT userID, courseID, startDate, endDate, streakDays
FROM LongestStreaks
ORDER BY streakDays DESC;

--j Longest Gap Between Visits per User and Number of Days in a Single Course:
WITH VisitGaps AS (
    SELECT userID, courseID, [date],
           LAG([date]) OVER (PARTITION BY userID, courseID ORDER BY [date]) as prevDate,
           DATEDIFF(day, LAG([date]) OVER (PARTITION BY userID, courseID ORDER BY [date]), [date]) - 1 as gapDays
    FROM courseSiteVisit
)
SELECT userID, courseID, MAX(gapDays) as longestGapDays
FROM VisitGaps
GROUP BY userID, courseID;
 --K:  User who Visited the Most Courses within a Short Duration:
 WITH CourseDuration AS (
    SELECT courseID, MIN([date]) as startDate, MAX([date]) as endDate,
           DATEDIFF(day, MIN([date]), MAX([date])) + 1 as durationDays
    FROM courseSiteVisit
    GROUP BY courseID
)
SELECT userID, COUNT(DISTINCT cv.courseID) as visitedCourses
FROM courseSiteVisit cv
JOIN CourseDuration cd ON cv.courseID = cd.courseID
WHERE DATEDIFF(day, cd.startDate, cv.[date]) <= 7
GROUP BY userID
ORDER BY visitedCourses DESC;
