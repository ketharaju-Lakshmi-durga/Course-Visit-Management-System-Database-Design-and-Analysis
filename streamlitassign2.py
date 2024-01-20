import pypyodbc as odbc
import streamlit as st
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt;
#streamlit run c:/Users/laksh/Desktop/ADTAssignment2/pyconnect.py
# DataBase Connect
DRIVER_NAME='SQL SERVER'
SERVER_NAME='DESKTOP-Q73L16A'
DATEBASE_NAME='ADTAssignment2'
connection_string=f"""
DRIVER={{{DRIVER_NAME}}};
SERVER={SERVER_NAME};
DATABASE={DATEBASE_NAME};
Trust_Connection=yes;
"""
conn=odbc.connect(connection_string)
cursor=conn.cursor()
print(conn)

"""# a: Total Number of Times a Course has been Visited
st.subheader('A:Total Number of Times a Course has been Visited or Accessed by All Users')
query_a = "SELECT courseID, COUNT(visitID) as totalVisits FROM courseSiteVisit GROUP BY courseID;"
result_a = pd.read_sql(query_a, conn)

# Print the result_a DataFrame to debug
st.write(result_a)

# visulaize using streamlit
st.bar_chart(result_a.set_index(result_a.columns[0]))
st.markdown(f"**X Axis Label:** {result_a.columns[0]}")
st.markdown("**Y Axis Label:** Total Visits")


#b. Total Number of Visits for Each Course, Categorized by Program:
st.subheader('B:Total Number of Visits for Each Course, Categorized by Program:')
query_b= "SELECT c.courseID, p.name as program, COUNT(v.visitID) as totalVisits FROM courseSiteVisit v JOIN depCourse c ON v.courseID = c.courseID JOIN program p ON c.programID = p.programID GROUP BY c.courseID, p.name;"
result_b = pd.read_sql(query_b, conn)

# Print the result_a DataFrame to debug
st.write(result_b)

# Visualize using alt.Chart
chart = alt.Chart(result_b).mark_bar().encode(
    x=result_b.columns[0],
    y=result_b.columns[2],
    color=result_b.columns[1]
).interactive()
st.altair_chart(chart)

#c.Total Number of Students or Users Enrolled in Each Program:
st.subheader('C:Total Number of Students or Users Enrolled in Each Program')
query_c= "SELECT p.name as program, COUNT(u.userID) as totalUsers FROM program p LEFT JOIN users u ON p.programID = u.programID GROUP BY p.name;"
result_c = pd.read_sql(query_c, conn)

# Print the result_a DataFrame to debug
st.write(result_c)

# Visualize using alt.Chart
chart = alt.Chart(result_c).mark_bar().encode(
    x=result_c.columns[0],
    y=result_c.columns[1],
    color=result_c.columns[0]
).interactive()
st.altair_chart(chart)

#d.Total Number of Unique Visitors per Department by Program:
st.subheader('D .Total Number of Unique Visitors per Department by Program:')
query_d= "SELECT c.deptName, p.name as program, COUNT(DISTINCT v.userID) as uniqueVisitors FROM courseSiteVisit v JOIN depCourse c ON v.courseID = c.courseID JOIN program p ON c.programID = p.programID GROUP BY c.deptName, p.name;"
result_d = pd.read_sql(query_d, conn)

# Print the result_a DataFrame to debug
st.write(result_d)

# Visualize using alt.Chart
chart = alt.Chart(result_d).mark_bar().encode(
    x=result_d.columns[2],
    y=result_d.columns[0],
    color=result_d.columns[1]
).interactive()
st.altair_chart(chart)

#E: Most Recent Date on Which a User Visited Each Course
st.subheader('E: Most Recent Date on Which a User Visited Each Course')
query_e= "SELECT courseID, MAX([date]) as mostRecentDate FROM courseSiteVisit GROUP BY courseID;"
result_e = pd.read_sql(query_e, conn)
# Print the result_a DataFrame to debug
st.write(result_e)

# Visualize using alt.Chart
chart = alt.Chart(result_e).mark_bar().encode(
    x=result_e.columns[0],
    y=result_e.columns[1],
    color=result_e.columns[0]
).interactive()
st.altair_chart(chart)

#F:Number of Times a User has Visited Each Course
st.subheader('F:Number of Times a User has Visited Each Course')
query_f= "SELECT userID, courseID, COUNT(visitID) as visitCount FROM courseSiteVisit GROUP BY userID, courseID;"
result_f = pd.read_sql(query_f, conn)
# Print the result_a DataFrame to debug
st.write(result_f)

# Visualize using alt.Chart
chart = alt.Chart(result_f).mark_bar().encode(
    x=result_f.columns[0],
    y=result_f.columns[2],
    color=result_f.columns[1]
).interactive()
st.altair_chart(chart)

# G: User who has Visited a Course the Most:
st.subheader('G: User who has Visited a Course the Most')
query_g= "WITH RankedVisits AS ( SELECT userID, courseID, COUNT(visitID) as visitCount, ROW_NUMBER() OVER (PARTITION BY courseID ORDER BY COUNT(visitID) DESC) as rn FROM courseSiteVisit GROUP BY userID, courseID ) SELECT userID, courseID, visitCount FROM RankedVisits WHERE rn = 1;"
result_g= pd.read_sql(query_g, conn)
# Print the result_a DataFrame to debug
st.write(result_g)

# Visualize using alt.Chart
chart = alt.Chart(result_g).mark_bar().encode(
    x=result_g.columns[0],
    y=result_g.columns[2],
    color=result_g.columns[1]
).interactive()
st.altair_chart(chart)

#H .User who Visited a Course the Most Times in a Single Day:
st.subheader('H .User who Visited a Course the Most Times in a Single Day:')
query_h= "WITH MaxVisitsInDay AS ( SELECT userID, courseID, MAX(visitCount) as maxVisitsInDay FROM ( SELECT userID, courseID, [date], COUNT(visitID) as visitCount FROM courseSiteVisit GROUP BY userID, courseID, [date] ) AS VisitsPerDay GROUP BY userID, courseID ) SELECT userID, courseID, maxVisitsInDay FROM MaxVisitsInDay WHERE maxVisitsInDay = 1;"
result_h= pd.read_sql(query_h, conn)
# Print the result_a DataFrame to debug
st.write(result_h)

# Visualize using alt.Chart
chart = alt.Chart(result_h).mark_bar().encode(
    x=result_h.columns[0],
    y=result_h.columns[2],
    color=result_h.columns[1]
).interactive()
st.altair_chart(chart)"""

#I:Longest Visit Streak Days per User per Course:
st.subheader('I:Longest Visit Streak Days per User per Course:')
query_i= "WITH UserCourseVisitCounts AS (SELECT userID, courseID, [date],ROW_NUMBER() OVER (PARTITION BY userID, courseID ORDER BY [date]) - ROW_NUMBER() OVER (PARTITION BY userID, courseID ORDER BY [date]) as visitGroup FROM courseSiteVisit ), LongestStreaks AS ( SELECT userID, courseID, MIN([date]) as startDate, MAX([date]) as endDate, DATEDIFF(day, MIN([date]), MAX([date])) + 1 as streakDays FROM UserCourseVisitCounts GROUP BY userID, courseID, visitGroup) SELECT userID, courseID, startDate, endDate, streakDays FROM LongestStreaks ORDER BY streakDays DESC;"
result_i= pd.read_sql(query_i, conn)
# Print the result_a DataFrame to debug
st.write(result_i)

# Visualize using alt.Chart
chart = alt.Chart(result_i).mark_bar().encode(
    x=result_i.columns[0],
    y=result_i.columns[4],
    color=result_i.columns[1]
).interactive()
st.altair_chart(chart)

# J:Longest Gap Between Visits per User and Number of Days in a Single Course:
st.subheader('J:Longest Gap Between Visits per User and Number of Days in a Single Course:')
query_j="WITH VisitGaps AS ( SELECT userID, courseID, [date], LAG([date]) OVER (PARTITION BY userID, courseID ORDER BY [date]) as prevDate, DATEDIFF(day, LAG([date]) OVER (PARTITION BY userID, courseID ORDER BY [date]), [date]) - 1 as gapDays FROM courseSiteVisit ) SELECT userID, courseID, MAX(gapDays) as longestGapDays FROM VisitGaps GROUP BY userID, courseID;"
result_j= pd.read_sql(query_j, conn)
# Print the result_a DataFrame to debug
st.write(result_j)

# Visualize using alt.Chart
chart = alt.Chart(result_j).mark_bar().encode(
    x=result_j.columns[0],
    y=result_j.columns[2],
    color=result_j.columns[1]
).interactive()
st.altair_chart(chart)

# K:  User who Visited the Most Courses within a Short Duration:
st.subheader('K:  User who Visited the Most Courses within a Short Duration:')
query_k=" WITH CourseDuration AS ( SELECT courseID, MIN([date]) as startDate, MAX([date]) as endDate, DATEDIFF(day, MIN([date]), MAX([date])) + 1 as durationDays FROM courseSiteVisit GROUP BY courseID) SELECT userID, COUNT(DISTINCT cv.courseID) as visitedCourses FROM courseSiteVisit cv JOIN CourseDuration cd ON cv.courseID = cd.courseID WHERE DATEDIFF(day, cd.startDate, cv.[date]) <= 7 GROUP BY userID ORDER BY visitedCourses DESC;"
result_k= pd.read_sql(query_k, conn)
# Print the result_a DataFrame to debug
st.write(result_k)

# Visualize using alt.Chart
chart = alt.Chart(result_k).mark_bar().encode(
    x=result_k.columns[0],
    y=result_k.columns[1],
    color=result_k.columns[0]
).interactive()
st.altair_chart(chart)




cursor.close()
conn.close()
#streamlit run c:/Users/laksh/Desktop/ADTAssignment2/pyconnect.py