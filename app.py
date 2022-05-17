from bleach import clean
import uvicorn
from fastapi import FastAPI, Request, HTTPException
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from starlette.responses import HTMLResponse
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from forms import UserRegForm


# init stuff
load_dotenv()
app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

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


@app.get("/", response_class=HTMLResponse,tags=["GET Register Page"])
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/", response_class=HTMLResponse, tags=["POST Endpoint to Register Teams"])
async def register(user: UserRegForm, request: Request):
    if not (
        (user.email1.__contains__("@"))
        or (user.email2.__contains__("@"))
        or (user.email1.__contains__("@"))
    ):
        raise HTTPException(status_code=422, detail="Please enter correct email ID.")
    if len(str(user.phone)) != 10:
        raise HTTPException(
            status_code=422, detail="Please enter a valid phone number."
        )
    if part_form.find_one({"TeamName": user.TeamName}):
        raise HTTPException(status_code=422, detail="Team Name already taken.")
    else:

        if bool(
            (
                part_form.find_one({"email1": user.email1})
                or part_form.find_one({"email3": user.email3})
                or part_form.find_one({"email2": user.email2})
            )
        ):
            raise HTTPException(
                status_code=422,
                detail="Email(s) already registered. Please register new email-ids ",
            )
        else:
            part_form.insert_one(
                {
                    "TeamName": clean(user.TeamName),
                    "PhoneNumber": clean(str(user.phone)),
                    "P1Name": clean(user.Player1Name),
                    "P2Name": clean(user.Player2Name),
                    "P3Name": clean(user.Player3Name),
                    "email1": user.email1,
                    "email2": user.email2,
                    "email3": user.email3,
                }
            )
    return "Succesful request."


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True, host="127.0.0.1", port=5000)