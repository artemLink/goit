SELECT DISTINCT sub.name AS subject_name
FROM marks m
JOIN subjects sub ON m.subject_id = sub.id
JOIN students s ON m.student_id = s.id
WHERE s.name = 'Kendra Mcmahon' AND s.lastname = 'Chavez';
