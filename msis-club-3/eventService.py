from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///msis_club.db")



def GetEvents():
    # Load all events from database
    return db.execute("SELECT * FROM event")



def GetEvent(eventId):
    # Load event from database by id
    eventList = db.execute("SELECT * FROM event WHERE id=?", eventId)
    # We know that there is only one event with this id (and SQL does too), but python doesn't know or care
    # The result of executing the select statement will be a list, regardless of how many items were found
    # So, in this case we just get the first element of the list. You could do this all on one line like:
    # event = db.execute("SELECT * FROM event WHERE id=?", eventId)[0]
    event = eventList[0]
    return event



def IsEventFull(eventId):
    # Load event from database by id
    eventList = db.execute("SELECT * FROM event WHERE id=?", eventId)
    event = eventList[0]
    # The event is full if the registered number is greater than or equal to the capacity
    return (event['capacity'] - event['registered'] <= 0)



def IsRegistered(studentId, eventId):
    # Is studentId registered for eventId?
    registrationList = db.execute("SELECT * FROM student_event WHERE student_id=? AND event_id=?", studentId, eventId)
    return registrationList



def Register(studentId, eventId):
    # Insert registration record
    db.execute("INSERT INTO student_event VALUES (?,?)", studentId, eventId)
    # Update the 'registered' count for the event
    event = GetEvent(eventId)
    db.execute("UPDATE event SET registered=? WHERE id=?", event['registered'] + 1, eventId)



def GetEventsForStudent(studentId):
    # Load id and name of all events for which this student is registered
    studentEventList = db.execute("SELECT id, name FROM student_event INNER JOIN event ON event_id=id WHERE student_id=?", studentId)
    return studentEventList