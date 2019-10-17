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

type_defs = load_schema_from_path("schema.graphql")

query = QueryType()
mutation = MutationType()


# Query fields resolvers
@query.field("hello")
def resolve_hello(_, info):
    user_agent = None
    try:
        request = info.context["request"]
        user_agent = request.headers.get("user-agent", "guest")
        app.logger.info('Hello query was successful')
    except Exception as e:
        app.logger.error('error occured while running hello query: %s' % e)

    return "Hello, %s!" % user_agent


@query.field("allUsers")
def resolve_all_users(*_):
    query_results = None
    try:
        query_results = User.query.all()
        app.logger.info('allUsers query was successful')
    except Exception as e:
        app.logger.error('error occured while running allUsers query: %s' % e)

    return query_results


@query.field("user")
def resolve_user(*_, id):
    query_results = None
    try:
        query_results = User.query.get(id)
        app.logger.info('query of user_id: %d was successful' % id)
    except Exception as e:
        app.logger.error('error occured while running user_id: %d query: %s' % (id, e))

    return query_results


@query.field("allEvents")
def resolve_all_events(*_):
    query_results = None
    try:
        query_results = Event.query.all()
        app.logger.info('allEvents query was successful')
    except Exception as e:
        app.logger.error('error occured while running allEvents query: %s' % e)

    return query_results


@query.field("event")
def resolve_event(*_, id):
    query_results = None
    try:
        query_results = Event.query.get(id)
        app.logger.info('query of event_id: %d was successful' % id)
    except Exception as e:
        app.logger.error('error occured while running event_id: %d query: %s' % (id, e))

    return query_results


@query.field("allUserGroups")
def resolve_all_user_groups(*_):
    query_results = None
    try:
        query_results = UserGroup.query.all()
        app.logger.info('allUserGroups query was successful')
    except Exception as e:
        app.logger.error('error occured while running allUserGroups query: %s' % e)

    return query_results


@query.field("userGroup")
def resolve_user_group(*_, id):
    query_results = None
    try:
        query_results = UserGroup.query.get(id)
        app.logger.info('query of userGroup_id: %d was successful' % id)
    except Exception as e:
        app.logger.error('error occured while running userGroup_id: %d query: %s' % (id, e))

    return query_results


# Mutation fields resolvers
@mutation.field("addUser")
def resolve_addUser(*_, input):

    status = False
    error = None
    user_id = None

    try:
        new_user = User(
            email = input["email"],
            firstName = input["firstName"],
            lastName = input["lastName"],
            country = input["country"],
            phoneNumber = input["phoneNumber"],
            userGroup = input["userGroup"],  
            createdAt  = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            updatedAt  = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        )
        app.logger.info('new user: %s' % new_user)
        db.create_all()
        db.session.add(new_user)
        db.session.flush()
        user_id = new_user.id
        db.session.commit()
        app.logger.info('%s added to the database, id: %s ' %(new_user, user_id))
        status=True
    except Exception as e:
        error = e
        app.logger.error(e)
        db.session.rollback()
        db.session.flush() 

    return {"status" : status, "error" : error, "userID" : user_id}


@mutation.field("addEvent")
def resolve_add_event(*_, input):

    status = False
    error = None
    event_id = None

    try:
        new_event = Event(
            eventName = input["eventName"],
            createdByEmail = input["createdByEmail"],
            eventDateAndTime = input["eventDateAndTime"],
            attendees = input["attendees"],
            createdAt  = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            updatedAt  = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        )
        app.logger.info('new event: %s' % new_event)
        db.create_all()
        db.session.add(new_event)
        db.session.flush()
        event_id = new_event.id
        db.session.commit()
        app.logger.info('%s added to the database, id: %s ' %(new_event, event_id))
        status=True
    except Exception as e:
        error = e
        app.logger.error(e)
        db.session.rollback()
        db.session.flush() 
    
    if status:
        email_body = "You have been invited"
        list_of_invited_emails = input["attendees"].split(";")
        app.logger.info('sending event invite email to: %s' % list_of_invited_emails)
        response = send_email(input["createdByEmail"], list_of_invited_emails, input["eventName"], email_body)
        
        if response.status_code == 200:
            app.logger.info('invite email successfully sent')
        else:
            app.logger.error('Error occurred while sending email: %s' %response.json())


    return {"status" : status, "error" : error, "eventID" : event_id}


@mutation.field("addUserGroup")
def resolve_add_user_group(*_, input):

    status = False
    error = None
    user_group_id = None

    try:
        new_user_group = UserGroup(
            groupName = input["groupName"],
            createdAt  = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            updatedAt  = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        )
        app.logger.info('new user group: %s' % new_user_group)
        db.create_all()
        db.session.add(new_user_group)
        db.session.flush()
        user_group_id = new_user_group.id
        db.session.commit()
        app.logger.info('%s added to the database, id: %s ' %(new_user_group, user_group_id))
        status=True
    except Exception as e:
        error = e
        app.logger.error(e)
        db.session.rollback()
        db.session.flush() 

    return {"status" : status, "error" : error, "userGroupID" : user_group_id}


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