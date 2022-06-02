import os
import eventService, studentService
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

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



# Register form
@app.route("/register", methods=["GET"])
def register():
    # Find the event id in the received GET request
    eventId = request.args.get("id")

    # Render register.html with the eventId variable
    return render_template("register.html", eventId=eventId)



# Register form submit
@app.route("/register", methods=["POST"])
def registerSubmit():
    # Load all values from the form
    eventId = request.form.get("eventId")
    studentId = request.form.get("studentId")
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    major = request.form.get("major")

    # Is the event full?
    if eventService.IsEventFull(eventId):
        # If so, STOP and show an error message
        return render_template("error.html", message="No seats left in this event.")

    # Is this student already registered for this event?
    if eventService.IsRegistered(studentId, eventId):
        # If so, STOP and show an error message
        return render_template("error.html", message="This student has already registered for this event.")

    # Is there already a student record with this id?
    if not studentService.GetStudent(studentId):
        # If not, insert student record
        studentService.CreateStudent(studentId, firstName, lastName, major)

    # At this point, everything is good to go, so we can register the student for the event
    eventService.Register(studentId, eventId)

    # Render success.html
    return render_template("success.html")



# Students list page
@app.route("/students", methods=["GET"])
def students():
    studentList = studentService.GetStudents()

    # Render students.html with the studentList variable
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