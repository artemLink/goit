SELECT l.name, l.lastname, AVG(m.mark) AS avg_mark
FROM lectors l
JOIN subjects sub ON l.id = sub.lector_id
JOIN marks m ON sub.id = m.subject_id
GROUP BY l.name, l.lastname;
