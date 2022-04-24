import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///msis_club.db")

# Ensure responses aren't cached so we can test changes to our app without issue
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# App home page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")



# Events list page
@app.route("/events", methods=["GET"])
def events():
    # Load all events from database
    eventList = db.execute("SELECT * FROM event")

    # Render events.html page with the eventList variable
    return render_template("events.html", eventList=eventList)



# Single event page
@app.route("/event", methods=["GET"])
def event():
    # Find the event id in the received GET request
    eventId = request.args.get("id")

    # Load event from database by id
    eventList = db.execute("SELECT * FROM event WHERE id=?", eventId)
    # We know that there is only one event with this id (and SQL does too), but python doesn't know or care
    # The result of executing the select statement will be a list, regardless of how many items were found
    # So, in this case we just get the first element of the list. You could do this all on one line like:
    # event = db.execute("SELECT * FROM event WHERE id=?", eventId)[0]
    event = eventList[0]

    # Render event.html with the event variable
    return render_template("event.html", event=event)



# Register form submit
@app.route("/register", methods=["POST"])
def register():
    # Load all values from the form
    eventId = request.form.get("eventId")
    studentId = request.form.get("studentId")
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    major = request.form.get("major")

    # Are there any seats left in this event?
    eventList = db.execute("SELECT * FROM event WHERE id=?", eventId)
    event = eventList[0]
    if (event['capacity'] - event['registered'] <= 0):
        # If not, STOP and show an error message
        return render_template("error.html", message="No seats left in this event.")

    # Is this student already registered for this event?
    registrationList = db.execute("SELECT * FROM student_event WHERE student_id=? AND event_id=?", studentId, eventId)
    if registrationList:
        # If so, STOP and show an error message
        return render_template("error.html", message="This student has already registered for this event.")

    # Is there already a student record with this id?
    studentList = db.execute("SELECT * FROM student WHERE id=?", studentId)
    if not studentList:
        # If not, insert student record
        db.execute("INSERT INTO student VALUES (?,?,?,?)", studentId, firstName, lastName, major)

    # At this point, everything is good to go, so we can register the student for the event
    # Insert registration record
    db.execute("INSERT INTO student_event VALUES (?,?)", studentId, eventId)
    # Update the 'registered' count for the event
    db.execute("UPDATE event SET registered=? WHERE id=?", event['registered'] + 1, eventId)

    # Render success.html
    return render_template("success.html")



# Students list page
@app.route("/students", methods=["GET"])
def students():
    # Load all students from the database
    studentList = db.execute("SELECT * FROM student")

    # Render students.html with the students variable
    return render_template("students.html", studentList=studentList)



# Single student page
@app.route("/student", methods=["GET"])
def student():
    # Find the student id in the received GET request
    studentId = request.args.get("id")

    # Load student from database by id
    # student is the name of this function so we need a different name for a student variable
    myStudent = db.execute("SELECT * FROM student WHERE id=?", studentId)[0]

    # Load id and name of all events for which this student is registered
    studentEventList = db.execute("SELECT id, name FROM student_event INNER JOIN event ON event_id=id WHERE student_id=?", studentId)

    # Render student.html with the student variable and the studentEventList variable
    return render_template("student.html", student=myStudent, eventList=studentEventList)