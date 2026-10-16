import os
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import frontmatter
import markdown

app = FastAPI()

# folder with css, js and other things
app.mount("/static", StaticFiles(directory="static"), name="static")

# folder with html
src = Jinja2Templates(directory="src")

# gallery dir (ones with photo)
gal = Path("static/gallery")
# blog dir (here will be md files for blog)
blogs = Path("static/blogs")

def parse_markdown(file_path: Path):
    post = frontmatter.load(file_path)
    html_content = markdown.markdown(
        post.content,
        extensions=["fenced_code", "tables", "nl2br", "sane_lists"]
    )
    return post.metadata, html_content

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
    posts = []
    for file in blogs.glob("*.md"):
        meta, _  = parse_markdown(file)
        posts.append({
            "slug": file.stem,
            "title": meta.get("title", file.stem.replace("-", " ").title()),
            "date": meta.get("date", "")
        })

    posts.sort(key=lambda x: str(x["date"]), reverse=True)
    return src.TemplateResponse("blog.html", {"request": request, "posts": posts})

@app.get("/blog/{slug}")
def blog_detail(request: Request, slug: str):
    file_path = blogs / f"{slug}.md"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Blog post not found")

    meta, html_content = parse_markdown(file_path)
    return src.TemplateResponse(
        "blog_page.html",
        {
            "request": request,
            "title": meta.get("title", slug.replace("-", " ").title()),
            "content": html_content
        }  
    )