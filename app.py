from bleach import clean
import uvicorn
from fastapi import FastAPI, Request, HTTPException, Form
import os
from typing import Optional
from pymongo import MongoClient
from dotenv import load_dotenv
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from forms import UserRegForm


# init stuff
load_dotenv()
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

MONGODB_CONNECTION_URI = os.getenv("MONGODB_CONNECTION_URI")
client = MongoClient(MONGODB_CONNECTION_URI)
db = client["astellar"]
part_form = db["offlineTeams"]

try:
    client.admin.command("ping")
    print("Successfully connected to MongoDB")

except:
    print("Server not available")


@app.get("/", response_class=HTMLResponse, tags=["GET Register Page"])
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/", response_class=HTMLResponse, tags=["POST Endpoint to Register Teams"])
async def register(
    request: Request,
    TeamName: Optional[str] = Form(...),
    Player1Name: Optional[str] = Form(...),
    Player2Name: Optional[str] = Form(...),
    Player3Name: Optional[str] = Form(...),
    email1: Optional[str] = Form(...),
    email2: Optional[str] = Form(...),
    email3: Optional[str] = Form(...),
    phone: Optional[int] = Form(...),
):

    user = UserRegForm(
        TeamName=clean(TeamName),
        Player1Name=clean(Player1Name),
        Player2Name=clean(Player2Name),
        Player3Name=clean(Player3Name),
        email1=clean(email1),
        email2=clean(email2),
        email3=clean(email3),
        phone=phone,
    )

    if not (
        (email1.__contains__("@    "))
        or (email2.__contains__("@"))
        or (email1.__contains__("@"))
    ):
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "Teamname": TeamName,
                "errordetail": "Please enter a valid email ID.",
            },
        )
    if len(str(phone)) != 10:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "Teamname": TeamName,
                "errordetail": "Please enter correct phone number.",
            },
        )
    if part_form.find_one({"TeamName": TeamName}):
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "Teamname": TeamName,
                "errordetail": "Team name is already taken. Please register with a different name.",
            },
        )
    else:

        if bool(
            (
                part_form.find_one({"email1": email1})
                or part_form.find_one({"email3": email3})
                or part_form.find_one({"email2": email2})
            )
        ):
            return templates.TemplateResponse(
                "error.html",
                {
                    "request": request,
                    "Teamname": TeamName,
                    "errordetail": "Email ID(s) already registered. Please register with new Email ID(s)",
                },
            )
        else:
            part_form.insert_one(user.dict())

    return templates.TemplateResponse(
        "success.html", {"request": request, "Teamname": TeamName}
    )


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True, host="127.0.0.1", port=5000)
