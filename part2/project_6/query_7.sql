SELECT students.lastname, students.name, marks.mark
FROM students
JOIN marks ON students.id = marks.student_id
WHERE students.group_id = 'group 1' AND marks.subject_id = 1;
