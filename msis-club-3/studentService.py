from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///msis_club.db")



def GetStudent(studentId):
    # Load student from database by id
    studentList = db.execute("SELECT * FROM student WHERE id=?", studentId)
    if studentList:
        return studentList[0]
    return None



def CreateStudent(student):
    # Insert student into database
    # student should be an object instead of four separate values
    db.execute("INSERT INTO student VALUES (?,?,?,?)", student['id'], student['first_name'], student['last_name'], student['major'])



def UpdateStudent(student):
    # Update student in database
    db.execute("UPDATE student SET first_name=?, last_name=?, major=? WHERE id=?", student['first_name'], student['last_name'], student['major'], student['id'])



def GetStudents():
    # Load all students from the database
    studentList = db.execute("SELECT * FROM student")
    return studentList



def GetStudentsForEvent(eventId):
    # Load id and name of all students registered for this event
    eventStudentList = db.execute("SELECT id, first_name, last_name FROM student_event INNER JOIN student ON student_id=id WHERE event_id=?", eventId)
    return eventStudentList