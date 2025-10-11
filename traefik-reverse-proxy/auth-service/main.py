from fastapi import FastAPI, Request, Form, Response, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from itsdangerous import TimestampSigner, BadSignature, SignatureExpired
import json
import uuid


app = FastAPI()
templates = Jinja2Templates(directory="templates")
with open("users.json") as f:
    users = json.load(f)


SECRET_KEY = "supersecretkey"  # change this
signer = TimestampSigner(SECRET_KEY)
sessions = {}


# --- UTILS ---
def verify_token(token: str):
    try:
        # username = users['users'] # signer.unsign(token, max_age=86400).decode()
        print(f"sessions: {sessions}")
        username = sessions[token]
        print(f"username: {username}")
        return username
    except (BadSignature, SignatureExpired):
        return None


def get_current_user(request: Request):
    token = request.cookies.get("auth_token")
    if token:
        return verify_token(token)
    return None


# --- ROUTES ---


@app.get("/login", response_class=HTMLResponse)
def login_page(next: str = "/"):
    return f"""
    <form action="/login" method="post">
      <input name="username" placeholder="Username">
      <input name="password" placeholder="Password" type="password">
      <input type="hidden" name="next" value="{next}">
      <button type="submit">Login</button>
    </form>
    """


@app.post("/login")
def login(
    username: str = Form(...), password: str = Form(...), next: str = Form("/")
):
    print(
        f"login request - username: {username} password: {password}, next:{next}"
    )
    print(f"users:{users}")
    for user in users["users"]:
        print(f"user: {user}")
        n = user.get("username")
        p = user.get("password")
        print(f"username:{n}, password: {p}")
        if n == username and p == password:
            print(f"username match: {username}")
            session_id = str(uuid.uuid4())
            sessions[session_id] = username
            print(f"next redirect: {next}")
            resp = RedirectResponse(next, status_code=303)
            resp.set_cookie(key="session", value=session_id, httponly=True)
            return resp

    print(f"next: {next}")
    return RedirectResponse(url="/login?next=" + next)


@app.get("/success", response_class=HTMLResponse)
async def success(request: Request, user: str = Depends(get_current_user)):
    if not user:
        return RedirectResponse("/login")
    return f"<h3>Welcome, {user}! Auth successful.</h3>"


@app.get("/verify")
async def verify(request: Request):
    """This is the endpoint Traefik calls for ForwardAuth"""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1]
        if verify_token(token):
            return Response(status_code=200)

    cookie = request.cookies.get("session")
    if cookie and verify_token(cookie):
        return Response(status_code=200)

    # Not authorized → redirect to login
    return Response(status_code=401)
