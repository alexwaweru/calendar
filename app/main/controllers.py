import os
import json
from datetime import datetime, timedelta

from ariadne import graphql_sync, QueryType, MutationType, make_executable_schema, load_schema_from_path
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify
from flask_cors import CORS

from create_app_factory import create_app, db
from models import User, Event, UserGroup
from services import send_email, send_scheduled_email

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
            createdAt  = datetime.now(),
            updatedAt  = datetime.now()
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


@mutation.field("updateUser")
def resolve_update_user(*_, input):

    status = False
    error = None
    user = None

    try:
        keys = input.keys()
        user = User.query.get(input["id"])
        if user:
            app.logger.info('updating user with id: %s ' % user.id)
            if "email" in keys:
                user.email = input["email"]
            if "firstName" in keys:
                user.firstName = input["firstName"]
            if "lastName" in keys:
                user.lastName = input["lastName"]
            if "country" in keys:
                user.country = input["country"]
            if "phoneNumber" in keys:
                user.phoneNumber = input["phoneNumber"]
            if "userGroup" in keys:
                user.userGroup = input["userGroup"]
            user.updatedAt = datetime.now()
            db.session.commit()
            status = True
            app.logger.info('user with id: %s was updated successfully' % user.id)
        else:
            error = 'no user with id: %s exists' % id
            app.logger.error('no user with id: %s exists' % id)
    except Exception as e:
        error = e
        app.logger.error('error occurred while updating user with id: %d, %s' % (input["id"], e))

    return {"status": status, "error": error, "user": user}


@mutation.field("deleteUser")
def resolve_delete_user(*_, id):

    status = False
    error = None
    user_id = None

    try:
        user = User.query.get(id)
        if user:
            user_id = user.id
            db.session.delete(user)
            db.session.commit()
            status = True
        else:
            error = 'no user with id: %s exists' % id
            app.logger.error('no user with id: %s exists' % id)
    except Exception as e:
        error = e
        app.logger.error('error occurred while deleting user with id: %d, %s' % (id, e))
    
    return {"status": status, "error": error, "userID": user_id}


@mutation.field("addEvent")
def resolve_add_event(*_, input):

    status = False
    error = None
    event_id = None
    new_event = None

    try:
        new_event = Event(
            eventName = input["eventName"],
            createdByEmail = input["createdByEmail"],
            eventDateAndTime = datetime.strptime(input["eventDateAndTime"], '%m/%d/%Y %H:%M:%S'),
            attendees = input["attendees"],
            createdAt  = datetime.now(),
            updatedAt  = datetime.now()
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
        response1 = send_email(input["createdByEmail"], list_of_invited_emails, input["eventName"], email_body)
        # Send email reminder 15 minutes to time
        reminder_time = datetime.strptime(new_event.eventDateAndTime, '%Y-%m-%d %H:%M:%S') - timedelta(hours=0, minutes=15) 
        response2 = send_scheduled_email(input["createdByEmail"], list_of_invited_emails, input["eventName"], email_body, reminder_time)

        if response1.status_code == 200:
            app.logger.info('invite email successfully sent')
        else:
            app.logger.error('Error occurred while sending email: %s' %response1.json())

        if response2.status_code == 200:
            app.logger.info('event reminder email successfully scheduled')
        else:
            app.logger.error('Error occurred while scheduling event reminder email: %s' %response2.json())


    return {"status" : status, "error" : error, "eventID" : event_id}


@mutation.field("updateEvent")
def resolve_update_event(*_, input):

    status = False
    error = None
    event = None

    try:
        keys = input.keys()
        event = Event.query.get(input["id"])
        if event:
            app.logger.info('updating event with id: %s ' % event.id)
            if "eventName" in keys:
                event.eventName = input["eventName"]
            if "eventDateAndTime" in keys:
                event.eventDateAndTime = datetime.strptime(input["eventDateAndTime"], '%m/%d/%Y %H:%M:%S')
            if "attendees" in keys:
                event.attendees = input["attendees"]
            event.updatedAt = datetime.now()
            db.session.commit()
            status = True
            app.logger.info('event with id: %s was updated successfully' % event.id)
        else:
            error = 'no event with id: %s exists' % id
            app.logger.error('no event with id: %s exists' % id)
    except Exception as e:
        error = e
        app.logger.error('error occurred while updating event with id: %d, %s' % (input["id"], e))

    if status:
        email_body = "Event has been updated"
        list_of_invited_emails = event.attendees.split(";")
        app.logger.info('sending event update email to: %s' % list_of_invited_emails)
        response = send_email(event.createdByEmail, list_of_invited_emails, event.eventName, email_body)

        if response.status_code == 200:
            app.logger.info('event update email successfully sent')
        else:
            app.logger.error('Error occurred while sending event update email: %s' %response.json())

    return {"status": status, "error": error, "event": event}


@mutation.field("deleteEvent")
def resolve_delete_event(*_, id):

    status = False
    error = None
    event_id = None
    event = None

    try:
        event = Event.query.get(id)
        if event:
            event_id = event.id
            db.session.delete(event)
            db.session.commit()
            status = True
        else:
            error = 'no event with id: %s exists' % id
            app.logger.error('no event with id: %s exists' % id)
    except Exception as e:
        error = e
        app.logger.error('error occurred while deleting event with id: %d, %s' % (id, e))

    if status:
        email_body = "Event has been cancelled"
        list_of_invited_emails = event.attendees.split(";")
        app.logger.info('sending event cancellation email to: %s' % list_of_invited_emails)
        response = send_email(event.createdByEmail, list_of_invited_emails, event.eventName, email_body)

        if response.status_code == 200:
            app.logger.info('event cancellation email successfully sent')
        else:
            app.logger.error('Error occurred while sending event cancellation email: %s' %response.json())
    
    return {"status": status, "error": error, "eventID": event_id}


@mutation.field("addUserGroup")
def resolve_add_user_group(*_, input):

    status = False
    error = None
    user_group_id = None

    try:
        new_user_group = UserGroup(
            groupName = input["groupName"],
            createdAt  = datetime.now(),
            updatedAt  = datetime.now()
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


@mutation.field("updateUserGroup")
def resolve_update_user_group(*_, input):

    status = False
    error = None
    user_group = None

    try:
        keys = input.keys()
        user_group = UserGroup.query.get(input["id"])
        if user_group:

            app.logger.info('updating user_group with id: %s ' % user_group.id)
            if "groupName" in keys:
                user_group.groupName = input["groupName"]
            user_group.updatedAt = datetime.now()
            db.session.commit()
            status = True
            app.logger.info('user_group with id: %s was updated successfully' % user_group.id)
        else:
            error = 'no user_group with id: %s exists' % id
            app.logger.error('no user_group with id: %s exists' % id)
    except Exception as e:
        error = e
        app.logger.error('error occurred while updating user_group with id: %d, %s' % (input["id"], e))

    return {"status": status, "error": error, "userGroup": user_group}


@mutation.field("deleteUserGroup")
def resolve_delete_user_group(*_, id):

    status = False
    error = None
    user_group_id = None

    try:
        user_group = UserGroup.query.get(id)
        if user_group:
            user_group_id = user_group.id
            db.session.delete(user_group)
            db.session.commit()
            status = True
        else:
            error = 'no user_group with id: %s exists' % id
            app.logger.error('no user_group with id: %s exists' % id)
    except Exception as e:
        error = e
        app.logger.error('error occurred while deleting user_group with id: %d, %s' % (id, e))
    
    return {"status": status, "error": error, "userGroupID": user_group_id}


@mutation.field("addGroupEvent")
def resolve_add_group_event(*_, input):

    status = False
    error = None
    event_id = None
    new_event = None

    groupName = input["groupName"]
    group_members = User.query.filter(User.userGroup == groupName).all()
    emails_of_group_members = ""
    for member in group_members:
        emails_of_group_members = emails_of_group_members + member.email + ";"

    try:
        new_event = Event(
            eventName = input["eventName"],
            createdByEmail = input["createdByEmail"],
            eventDateAndTime = datetime.strptime(input["eventDateAndTime"], '%m/%d/%Y %H:%M:%S'),
            attendees = emails_of_group_members,
            createdAt  = datetime.now(),
            updatedAt  = datetime.now()
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
        list_of_invited_emails = emails_of_group_members.split(";")
        app.logger.info('sending event invite email to: %s' % list_of_invited_emails)
        response1 = send_email(input["createdByEmail"], list_of_invited_emails, input["eventName"], email_body)
        # Send email reminder 15 minutes to time
        reminder_time = datetime.strptime(new_event.eventDateAndTime, '%Y-%m-%d %H:%M:%S') - timedelta(hours=0, minutes=15) 
        response2 = send_scheduled_email(input["createdByEmail"], list_of_invited_emails, input["eventName"], email_body, reminder_time)

        if response1.status_code == 200:
            app.logger.info('group invite email successfully sent')
        else:
            app.logger.error('Error occurred while sending group invite email: %s' %response1.json())

        if response2.status_code == 200:
            app.logger.info('group event reminder email successfully scheduled')
        else:
            app.logger.error('Error occurred while scheduling group event reminder email: %s' %response2.json())


    return {"status" : status, "error" : error, "eventID" : event_id}




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