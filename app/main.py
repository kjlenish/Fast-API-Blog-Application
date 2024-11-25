import logging
from fastapi import FastAPI
from app.dependencies.database import create_db_and_tables
from app.api import users

description = """
Blog API helps user to create, read, update and delete (CRUD) their blogs. The User needs to initially register using an unique email id to access the Blogs, then they can perform CRUD operations on blogs, like or unlike blogs and even add comments.

## Blogs

You will be able to:
* **Create blogs**.
* **Read blogs**.
* **Update blogs**.
* **Delete blogs**.
* **Like or Unlike blogs**.
* **Add comments or remove comments under a blog**.

## Users

You will be able to:

* **Create users**.
* **Read users**.
* **Update users**.
* **Delete users**.
"""
tags_metadata =[
    {
        "name": "Users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "Blogs",
        "description": "Operations with Blogs. The **CRUD** logic is also here.",
    },
    {
        "name": "Comments",
        "description": "Operations with Comments. The **CRUD** logic is also here.",
    },
]


log = logging.getLogger("uvicorn")


app = FastAPI(
    title="Blog App",
    description=description,
    summary="An all in one blogging application.",
    version="0.0.1",
    openapi_tags=tags_metadata
)


@app.on_event("startup")
def on_startup():
    try:
        create_db_and_tables()
        log.info("Successfully connected to database")
    except Exception as e:
        log.error(f"Error occurred while connecting to the database: {e}")


app.include_router(users.router)
