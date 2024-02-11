#!/usr/bin/env python3
# python example.py --dfd | dot -Tpng -o images/example.png

from pytm import (
    TM,
    Actor,
    Boundary,
    Classification,
    Data,
    Dataflow,
    Datastore,
    Lambda,
    Server,
    DatastoreType,
)

tm = TM(
    "my test tm",
    description="This is a sample threat model of a very simple system - a web-based comment system. The user enters comments and these are added to a database and displayed back to the user. The thought is that it is, though simple, a complete enough example to express meaningful threats.",
    isOrdered=True,
    mergeResponses=True,
    assumptions=[
        "Here you can document a list of assumptions about the system",
    ]
)

internet = Boundary("Internet")
server_db = Boundary(
    "Server/DB",
    levels=[2]
)

vpc = Boundary("AWS VPC")

user = Actor(
    "User",
    inBoundary=internet,
    levels=[2]
)

web = Server(
    "Web Server",
    OS="Ubuntu",
)
web.controls.isHardened = True
web.controls.sanitizesInput = False
web.controls.encodesOutput = True
web.controls.authorizesSource = False
web.sourceFiles = ["pytm/json.py", "docs/template.md"]

db = Datastore(
    "SQL Database",
    OS="CentOS",
    inBoundary=server_db,
    type=DatastoreType.SQL,
    inScope=True,
    maxClassification=Classification.RESTRICTED,
    levels=[2]
)
db.controls.isHardened = False

secretDb = Datastore(
    "Real Identity Database",
    OS="CentOS",
    inBoundary=server_db,
    type=DatastoreType.SQL,
    inScope=True,
    storesPII=True,
    maxClassification=Classification.TOP_SECRET
)

secretDb.sourceFiles = ["pytm/pytm.py"]
secretDb.controls.isHardened = True

my_lambda = Lambda(
    "AWS Lambda",
    inBoundary=vpc,
    levels=[1, 2]
)
my_lambda.controls.hasAccessControl = True

token_user_identity = Data(
    "Token verifying user identity",
    classification=Classification.SECRET
)

db_to_secretDb = Dataflow(
    db,
    secretDb,
    "Database verify real user identity",
    protocol="RDA-TCP",
    dstPort=40234,
    data=token_user_identity,
    note="Verifying that the user is who they say they are.",
    maxClassification=Classification.SECRET
)

comments_in_text = Data(
    "Comments in HTML or Markdown",
    classification=Classification.PUBLIC
)

user_to_web = Dataflow(
    user,
    web,
    "User enters comments (*)",
    protocol="HTTP",
    dstPort=80,
    data=comments_in_text,
    note="This is a simple web app\nthat stores and retrieves user comments."
)

query_insert = Data(
    "Insert query with comments",
    classification=Classification.PUBLIC
)

web_to_db = Dataflow(
    web,
    db,
    "Insert query with comments",
    protocol="MySQL",
    dstPort=3306,
    data=query_insert,
    note=(
        "Web server inserts user comments\ninto it's SQL query and stores them in the DB."
    )
)

comment_retrieved = Data(
    "Web server retrieves comments from DB",
    classification=Classification.PUBLIC
)

db_to_web = Dataflow(
    db,
    web,
    "Retrieve comments",
    protocol="MySQL",
    dstPort=80,
    data=comment_retrieved,
    responseTo=web_to_db
)

comment_to_show = Data(
    "Web server shows comments to the end user",
    classifcation=Classification.PUBLIC
)

web_to_user = Dataflow(
    web,
    user,
    "Show comments (*)",
    protocol="HTTP",
    data=comment_to_show,
    responseTo=user_to_web
)

clear_op = Data(
    "Serverless function clears DB",
    classification=Classification.PUBLIC
)

my_lambda_to_db = Dataflow(
    my_lambda,
    db,
    "Serverless function periodically cleans DB",
    protocol="MySQL",
    dstPort=3306,
    data=clear_op
)

userIdToken = Data(
    name="User ID Token",
    description="Some unique token that represents the user real data in the secret database",
    classification=Classification.TOP_SECRET,
    traverses=[user_to_web, db_to_secretDb],
    processedBy=[db, secretDb],
)

if __name__ == "__main__":
    tm.process()
