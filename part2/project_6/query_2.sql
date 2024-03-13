SELECT students.id, lastname, name, AVG(mark) AS avg_mark
FROM students
JOIN marks ON students.id = marks.student_id
WHERE subject_id = 1
GROUP BY students.id, lastname, name
ORDER BY avg_mark DESC
LIMIT 1;
