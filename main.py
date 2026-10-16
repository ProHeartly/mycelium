import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# folder with css, js and other things
app.mount("/static", StaticFiles(directory="static"), name="static")

# folder with html
src = Jinja2Templates(directory="src")

# gallery dir (ones with photo)
gal = Path("static/gallery")

# THis is index aka the main root
@app.get("/")
def index(request: Request):
    return src.TemplateResponse("index.html", {"request": request})

@app.get("/about")
def about(request: Request):
    return src.TemplateResponse("about.html", {"request": request})

@app.get("/contact")
def contact(request: Request):
    return src.TemplateResponse("contact.html", {"request": request})

@app.get("/projects")
def projects(request: Request):
    return src.TemplateResponse("projects.html", {"request": request})

@app.get("/gallery")
def gallery(request: Request):
    images = []
    if gal.exists():
        for file in gal.iterdir():
            images.append(file.name)

    return src.TemplateResponse(
        "gallery.html",
        {"request": request, "images": images}
    )

@app.get("/joke")
def joke(request: Request):
    return src.TemplateResponse("joke.html", {"request": request})

@app.get("/blog")
def blog(request: Request):
    return src.TemplateResponse("blog.html", {"request": request})