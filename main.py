from fastapi import FastAPI, Request, Response, HTTPException, status, Depends
from fastapi.responses import PlainTextResponse, HTMLResponse
from pydantic import BaseModel
from typing import List
from datetime import datetime
import base64

app = FastAPI()

posts_memory = []

class Post(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime

# Q1
@app.get("/ping", response_class=PlainTextResponse)
def ping():
    return Response(content="pong", media_type="text/plain")

# Q2
@app.get("/home", response_class=HTMLResponse)
def home():
    return HTMLResponse(content="<h1>Welcome home!</h1>", status_code=200)

# Q3
@app.exception_handler(404)
def not_found_handler(request: Request, exc: HTTPException):
    return HTMLResponse(content="<h1>404 NOT FOUND</h1>", status_code=404)

# Q4
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def add_posts(new_posts: List[Post]):
    posts_memory.extend(new_posts)
    return posts_memory

# Q5
@app.get("/posts")
def get_posts():
    return posts_memory

# Q6
@app.put("/posts")
def update_posts(new_posts: List[Post]):
    for new_post in new_posts:
        for i, existing_post in enumerate(posts_memory):
            if existing_post.title == new_post.title:
                posts_memory[i] = new_post
                break
        else:
            posts_memory.append(new_post)
    return posts_memory

# BONUS
def basic_auth(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Basic "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        encoded = auth.split(" ")[1]
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Authorization format")

    if username != "admin" or password != "123456":
        raise HTTPException(status_code=403, detail="Forbidden")
    return True

@app.get("/ping/auth", response_class=PlainTextResponse)
def ping_auth(auth: bool = Depends(basic_auth)):
    return Response(content="pong", media_type="text/plain")
