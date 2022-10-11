from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

from deta import Deta
from typing import Union
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests

# dto


class FormData(BaseModel):
    firstname: str
    lastname: str
    email: str
    captcha_id: str
    captcha_text: str


# fast api setup
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")


# db setup
load_dotenv()
PROJECT_KEY = os.getenv('PROJECT_KEY')
deta = Deta(PROJECT_KEY)
forms_db = deta.Base("forms_db")
captcha_db = deta.Base("captcha_db")

# api


@app.post("/submit")
async def post(formData: FormData):
    captcha = get_captcha(formData.captcha_id)
    if captcha is None:
        raise HTTPException(status_code=404, detail="Captcha not found")

    if captcha["text_of_captcha"] == formData.captcha_text:
        if not captcha["is_used"]:

            captcha_db.update({
                "is_used": True,
            }, captcha["key"])
            forms_db.insert({
                "firstname": formData.firstname,
                "lastname": formData.lastname,
                "email": formData.email
            })
            return "OK"
        else:
            return "USED_CAPTCHA"
    else:
        return "NOT_OK"


@app.get("form/{id}")
async def get(id):
    form = forms_db.get(id)
    return form


# html routes

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")


@app.get('/', include_in_schema=False)
async def root(request: Request):
    captcha_id = create_captcha()
    return templates.TemplateResponse("index.html", {"request": request, "captcha_id": captcha_id})


def create_captcha():
    url = "https://privatesimplecaptchaapi.deta.dev/create-random-captcha?number_of_words=2"
    response = requests.get(url)
    data = response.json()
    captcha_db.insert({
        "image_url": data["image_url"],
        "audio_url": data["audio_url"],
        "text_of_captcha": data["text_of_captcha"],
        "audio_captcha_numbers":  data["audio_captcha_numbers"],
        "how_many_times_accessed": data["how_many_times_accessed"],
        "is_used": False
    }, data["captcha_id"])
    return data["captcha_id"]


def get_captcha(captcha_id):
    return captcha_db.get(captcha_id)
