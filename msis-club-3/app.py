import os
import json
import eventService, studentService
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)
# In order to use the session to save temporary data, we must set a secret key.
# In a real app this should be stored securely somewhere else
app.secret_key = 'my not-so-secret key'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

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
    # Get events
    eventList = eventService.GetEvents()

    # Render events.html page with the eventList variable
    return render_template("events.html", eventList=eventList)



# Single event page
@app.route("/event", methods=["GET"])
def event():
    # Find the event id in the received GET request
    eventId = request.args.get("id")

    # Get event by id
    event = eventService.GetEvent(eventId)

    eventStudentList = studentService.GetStudentsForEvent(eventId)

    # Render event.html with the event and eventStudentList variables
    return render_template("event.html", event=event, studentList=eventStudentList)



# Add event form
@app.route("/newEvent", methods=["GET"])
def newEvent():
    # Render newEvent.html
    return render_template("newEvent.html")



# Add event form submit
@app.route("/newEvent", methods=["POST"])
def newEventSubmit():
    # Load all values from the form
    name = request.form.get("name")
    capacity = request.form.get("capacity")
    fee = request.form.get("fee")

    # Create an event object
    event = {
        'name': name,
        'capacity': capacity,
        'fee': fee
    }

    # Insert event record
    eventService.CreateEvent(event);

    # Render success.html
    return render_template("success.html", message="Event created successfully!")



# Register form
@app.route("/register", methods=["GET"])
def register():
    # Find the event id in the received GET request
    eventId = request.args.get("id")

    # Render register.html with the eventId variable
    return render_template("register.html", eventId=eventId)



# Register form submit to confirmation page
@app.route("/register", methods=["POST"])
def registerSubmit():
    # Load all values from the form
    eventId = request.form.get("eventId")
    studentId = request.form.get("studentId")
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    major = request.form.get("major")

    # Create a student object
    student = {
        'id': studentId,
        'first_name': firstName,
        'last_name': lastName,
        'major': major
    }

    # Save the student and event id in the session so we can access it later in another function
    session['student'] = json.dumps(student)
    session['eventId'] = eventId

    # Get event by id
    event = eventService.GetEvent(eventId)

    return render_template("registerConfirm.html", student=student, event=event)



# Register form edit (go back to register form)
@app.route("/registerEdit", methods=["GET"])
def registerEdit():
    # Find the student and event id in the session
    eventId = session.get('eventId', 'not set')
    student = json.loads(session.get('student', 'not set'))

    # Render register.html with the eventId and student variables
    return render_template("register.html", eventId=eventId, student=student)



# Register confirmation page submit; register student
@app.route("/registerConfirmed", methods=["POST"])
def registerConfirmed():
    # Find the student and event id in the session
    eventId = session.get('eventId', 'not set')
    student = json.loads(session.get('student', 'not set'))

    # Is the event full?
    if eventService.IsEventFull(eventId):
        # If so, STOP and show an error message
        return render_template("error.html", message="No seats left in this event.")

    # Is this student already registered for this event?
    if eventService.IsRegistered(student['id'], eventId):
        # If so, STOP and show an error message
        return render_template("error.html", message="This student has already registered for this event.")

    # Is there already a student record with this id?
    if studentService.GetStudent(student['id']):
        # If so, update student record
        studentService.UpdateStudent(student)
    else:
        # If not, insert student record
        studentService.CreateStudent(student)

    # At this point, everything is good to go, so we can register the student for the event
    eventService.Register(student['id'], eventId)

    # Render success.html
    return render_template("success.html", message="Student registered successfully!")


# Students list page
@app.route("/students", methods=["GET"])
def students():
    studentList = studentService.GetStudents()

    # Render students.html with the students variable
    return render_template("students.html", studentList=studentList)



# Single student page
@app.route("/student", methods=["GET"])
def student():
    # Find the student id in the received GET request
    studentId = request.args.get("id")

    # Get student by id
    # student is the name of this function so we need a different name for a student variable
    myStudent = studentService.GetStudent(studentId)

    # Get events for which this student is registered
    studentEventList = eventService.GetEventsForStudent(studentId)

    # Render student.html with the student variable and the studentEventList variable
    return render_template("student.html", student=myStudent, eventList=studentEventList)