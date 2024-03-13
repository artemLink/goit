SELECT s.id, s.name, s.lastname, AVG(m.mark) AS avg_mark
FROM students s
JOIN marks m ON s.id = m.student_id
GROUP BY s.id, s.name, s.lastname
ORDER BY avg_mark DESC
LIMIT 5;
