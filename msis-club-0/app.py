import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///msis_club.db")

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

    # Render event.html with the event and eventStudentList variables
    return render_template("event.html", event=event)