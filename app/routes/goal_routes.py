import os
from app import db
import requests
from datetime import date
from app.models.goal import Goal
from app.routes.routes_helpers import *
from flask import Blueprint, jsonify, make_response, request

goals_bp = Blueprint('goals_bp', __name__, url_prefix='/goals')

# Index
@goals_bp.route("", methods=["GET", "POST"])
def handle_goals():
    # Get all goals
    if request.method == "GET":
        goals = Goal.query.all()
        goals_response = [goal.to_json() for goal in goals]

        if not goals_response:
            return make_response(jsonify(f"There are no goals"))
        return jsonify(goals_response), 200

    # Create a new goal
    elif request.method == "POST":
        request_body = request.get_json()
        new_goal = {}
        
        if not "title" in request_body:
            return jsonify({
                "details": "Invalid data"
            }), 400

        try:
            new_goal = Goal(title=request_body["title"])
        except KeyError:
            return (f"Invalid data", 400)

        # Add this new instance of goal to the database
        db.session.add(new_goal)
        db.session.commit()

        # Successful response
        return {
            "goal": new_goal.to_json()
        }, 201

# Path/Endpoint to get a single goal
# Include the id of the record to retrieve as a part of the endpoint
@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])

# GET /goal/id
def handle_goal(goal_id):
    # Query our db to grab the goal that has the id we want:
    goal = Goal.query.get(goal_id)

    if not goal:
        return {"message": f"Goal {goal_id} not found"}, 404

    # Show a single goal
    if request.method == "GET":
        return goal.to_json(), 200
    
    # Update a goal
    elif request.method == "PUT":
        request_body = request.get_json()

        goal.title = request_body["title"]

        # Update this goal in the database
        db.session.commit()

        # Successful response
        return {
            "goal": goal.to_json()
        }, 200

    # Delete a goal
    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()

    return {
        "details": f'Goal {goal.goal_id} \"{goal.title}\" successfully deleted',
    }, 202