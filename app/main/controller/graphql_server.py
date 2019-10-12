from ariadne import QueryType, MutationType, make_executable_schema, load_schema_from_path
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify
from flask_cors import CORS

import json


type_defs = load_schema_from_path("app/main/controller/schema.graphql")

query = QueryType()
mutation = MutationType()


# Query fields resolvers
@query.field("hello")
def resolve_hello(_, info):
    return ""


@query.field("allUsers")
def resolve_allUsers(*_):
    return "" 


@query.field("user")
def resolve_user(*_, id):
    return "" 


@query.field("allEvents")
def resolve_allEvents(*_):
    return "" 


@query.field("event")
def resolve_event(*_, id):
    return "" 


@query.field("allUserGroups")
def resolve_user(*_):
    return "" 


@query.field("userGroup")
def resolve_user(*_, id):
    return "" 


# Mutation fields resolvers
@mutation.field("addUser")
def resolve_addUser(*_, UserInput):
    return ""


@mutation.field("addEvent")
def resolve_addEvent(*_, EventInput):
    return ""


@mutation.field("addUserGroup")
def resolve_addUserGroup(*_, UserGroupInput):
    return ""


schema = make_executable_schema(type_defs, [query, mutation])
app = Flask(__name__)
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