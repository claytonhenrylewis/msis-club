from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///msis_club.db")



def GetStudent(studentId):
    # Load student from database by id
    studentList = db.execute("SELECT * FROM student WHERE id=?", studentId)
    if studentList:
        return studentList[0]
    return None



def CreateStudent(studentId, firstName, lastName, major):
    # Insert student into database
    db.execute("INSERT INTO student VALUES (?,?,?,?)", studentId, firstName, lastName, major)



def GetStudents():
    # Load all students from the database
    studentList = db.execute("SELECT * FROM student")
    return studentList



def GetStudentsForEvent(eventId):
    # Load id and name of all students registered for this event
    eventStudentList = db.execute("SELECT id, first_name, last_name FROM student_event INNER JOIN student ON student_id=id WHERE event_id=?", eventId)
    return eventStudentList