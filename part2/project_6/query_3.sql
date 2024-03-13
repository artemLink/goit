SELECT sub.name AS subject_name, AVG(m.mark) AS avg_mark
FROM subjects sub
JOIN marks m ON sub.id = m.subject_id
GROUP BY sub.name;
