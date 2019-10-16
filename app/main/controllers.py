import os
import json
from datetime import datetime

from ariadne import graphql_sync, QueryType, MutationType, make_executable_schema, load_schema_from_path
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify
from flask_cors import CORS

from create_app_factory import create_app, db
from models import User, Event, UserGroup
from services import send_email


type_defs = load_schema_from_path("app/main/schema.graphql")

query = QueryType()
mutation = MutationType()


# Query fields resolvers
@query.field("hello")
def resolve_hello(_, info):
    request = info.context["request"]
    user_agent = request.headers.get("user-agent", "guest")

    return "Hello, %s!" % user_agent


@query.field("allUsers")
def resolve_all_users(*_):
    all_users = []
    results = User.query.all()
    for row in results:
        all_users.append(row._asdict())

    return all_users


@query.field("user")
def resolve_user(*_, id):
    return User.query.get(id)._asdict()


@query.field("allEvents")
def resolve_all_events(*_):
    all_events = []
    results = Event.query.all()
    for row in results:
        all_events.append(row._asdict())

    return all_events


@query.field("event")
def resolve_event(*_, id):
    return Event.query.get(id)._asdict()


@query.field("allUserGroups")
def resolve_all_user_groups(*_):
    all_user_groups = []
    results = UserGroup.query.all()
    for row in results:
        all_user_groups.append(row._asdict())

    return all_user_groups


@query.field("userGroup")
def resolve_user_group(*_, id):
    return UserGroup.query.get(id)._asdict()


# Mutation fields resolvers
@mutation.field("addUser")
def resolve_addUser(*_, user_input):
    clean_user_input = {
        "uid" : user_input["uid"],
        "email" : user_input["email"],
        "firstName": user_input["firstName"],
        "lastName" : user_input["lastName"],
        "country" : user_input["country"],
        "phoneNumber" : user_input["phoneNumber"],
        "legalName" : user_input["legalName"],
        "businessLegalEntity" : user_input["businessLegalEntity"],
        "businessLegalEntityOrg" : user_input["businessLegalEntityOrg"],
        "insurerRepresenting" : user_input["insurerRepresenting"],
        "insurerAdminEmail" : user_input["insurerAdminEmail"],
        "userType" : user_input["userType"]
    }
    status = False
    error = None
    user = None

    try:
        new_user = User(
            uid = clean_user_input["uid"],
            email = clean_user_input["email"],
            firstName = clean_user_input["firstName"],
            lastName = clean_user_input["lastName"],
            country = clean_user_input["country"],
            phoneNumber = clean_user_input["phoneNumber"],
            legalName = clean_user_input["legalName"],
            businessLegalEntity = clean_user_input["businessLegalEntity"],
            businessLegalEntityOrg = clean_user_input["businessLegalEntityOrg"],
            insurerRepresenting = clean_user_input["insurerRepresenting"],
            insurerAdminEmail = clean_user_input["insurerAdminEmail"],
            userType = clean_user_input["userType"],
            emailConfirmed  = False,    
            phoneConfirmed  = False,  
            profileComplete  = True,    
            isActive  = False,   
            createdAt  = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            updatedAt  = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        )
        db.session.add(new_user)
        db.session.flush()
        user = new_user.id
        db.session.commit()
        status=True
    except Exception as e:
        db.session.rollback()
        db.session.flush() 

    return {"status" : status, "error" : error, "user" : user}


@mutation.field("addEvent")
def resolve_add_event(*_, event_input):
    clean_event_input = {
        "eventName": event_input["eventName"],
        "createdByEmail" : event_input["createdByEmail"],
        "eventDateAndTime" : event_input["eventDateAndTime"],
        "timeFormat" : event_input["timeFormat"],
        "attendees" : event_input["attendees"]
    }
    status = False
    error = None
    event = None

    try:
        new_event = Event(
            eventName = clean_event_input["eventName"],
            createdByEmail = clean_event_input["createdByEmail"],
            eventDateAndTime = clean_event_input["eventDateAndTime"],
            timeFormat = clean_event_input["timeFormat"],
            attendees = clean_event_input["attendees"],
            createdAt  = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            updatedAt  = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        )
        db.session.add(new_event)
        db.session.flush()
        event = new_event.id
        db.session.commit()
        status=True
    except Exception as e:
        db.session.rollback()
        db.session.flush() 
    
    if status:
        email_body = ""
        list_of_invited_emails = clean_event_input["attendees"].split(";")
        send_email(clean_event_input["createdByEmail"], list_of_invited_emails, clean_event_input["eventName"], email_body)

    return {"status" : status, "error" : error, "event" : event}


@mutation.field("addUserGroup")
def resolve_add_user_group(*_, user_group_input):
    clean_user_group_input = {
        "groupName" : user_group_input["groupName"],
    }
    status = False
    error = None
    user_group = None

    try:
        new_user_group = UserGroup(
            groupName = clean_user_group_input["createdByEmail"],
            createdAt  = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            updatedAt  = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        )
        db.session.add(new_user_group)
        db.session.flush()
        user_group = new_user_group.id
        db.session.commit()
        status=True
    except Exception as e:
        db.session.rollback()
        db.session.flush() 

    return {"status" : status, "error" : error, "userGroup" : user_group}


schema = make_executable_schema(type_defs, [query, mutation])
app = create_app(os.getenv('CALENDAR_EVENT_ENV') or 'dev')
app.app_context().push()
CORS(app)


@app.route("/graphql", methods=["GET"])
def graphql_playgroud():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    json = jsonify(result)
    return json, status_code

if __name__ == "__main__":
    app.run(debug=True)