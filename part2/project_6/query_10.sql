SELECT DISTINCT subjects.name
    FROM marks
    JOIN students ON marks.student_id = students.id
    JOIN subjects ON marks.subject_id = subjects.id
    JOIN lectors ON subjects.lector_id = lectors.id
    WHERE students.id = 1 AND lectors.id = 5