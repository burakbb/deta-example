from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

from deta import Deta
from typing import Union
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# dto


class FormData(BaseModel):
    firstname: str
    lastname: str
    email: str


# fast api setup
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")


# db setup
load_dotenv()
PROJECT_KEY = os.getenv('PROJECT_KEY')
deta = Deta(PROJECT_KEY)
forms_db = deta.Base("forms_db")

# api


@app.post("/submit")
async def post(formData: FormData):
    forms_db.insert({
        "firstname": formData.firstname,
        "lastname": formData.lastname,
        "email": formData.email
    })
    return "OK"


@app.get("form/{id}")
async def get(id):
    form = forms_db.get(id)
    return form


# html routes

@app.get('/', include_in_schema=False)
async def favicon():
    return FileResponse("static/index.html")


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")
