
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routers.users import router as user_router
from database import engine, Base
import models
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse,  include_in_schema=False)
def home():
    return HTMLResponse("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FastAPI Backend</title>
<link rel="icon" href="/static/favicon/FastAPI.png" type="image/png">

<style>
*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}

body{
    background:#0f172a;
    color:#f8fafc;
    display:flex;
    justify-content:center;
    align-items:center;
    min-height:100vh;
    padding:24px;
    text-align:center;
}

main{
    max-width:420px;
    width:100%;
}

h1{
    font-size:2.2rem;
    margin-bottom:10px;
    font-weight:700;
}

p{
    color:#cbd5e1;
    line-height:1.6;
    margin-bottom:28px;
}

.links{
    display:flex;
    flex-direction:column;
    gap:14px;
}

a{
    color:#38bdf8;
    text-decoration:none;
    font-size:1.05rem;
    font-weight:600;
}

a:hover{
    color:#7dd3fc;
}

small{
    display:block;
    margin-top:40px;
    color:#64748b;
}
</style>
</head>

<body>

<main>

<h1>🚀 FastAPI Backend</h1>

<p>
Production-style REST API built with FastAPI, SQLAlchemy,
JWT Authentication, and Role-Based Authorization.
</p>

<div class="links">
    <a href="/docs">📘 API Documentation</a>
    <a href="/redoc">📖 ReDoc</a>
</div>

<small>
Version 1.0 • <span id="year"></span>
</small>

</main>

<script>
document.getElementById("year").textContent =
new Date().getFullYear();
</script>

</body>
</html>
""")

Base.metadata.create_all(bind=engine)

app.include_router(
    user_router,
    prefix="/users",
    tags=["Users"]
    )

