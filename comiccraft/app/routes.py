from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from pathlib import Path

from app.config import get_settings
from app.models import PromptRequest
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout
from app.services.exporters import save_pdf


router = APIRouter()

settings = get_settings()

templates = Jinja2Templates(
    directory=str(settings.base_dir / "templates")
)


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "error": None
        }
    )


@router.post("/generate")
def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):

    try:
        req = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style
        )

        # Create 5-panel outline
        outline = generate_outline(
            req.story_prompt,
            req.character_name,
            req.setting,
            req.tone,
            req.art_style
        )

        # Create story
        story = generate_story(
            outline,
            req.character_name,
            req.setting,
            req.tone,
            req.art_style
        )

        # Create images
        image_paths = []

        for panel in story[:5]:
            image_path = generate_image(
                panel["image_prompt"],
                panel["panel_number"],
                panel["panel_number"] * 12345
            )

            image_paths.append(image_path)

        # Build comic layout
        layout = build_comic_layout(
            story[:5],
            image_paths
        )

        # Save PDF
        pdf_path = save_pdf(layout)

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "request": request,
                "layout": layout,
                "pdf_path": pdf_path
            }
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "error": str(exc)
            },
            status_code=500
        )


@router.post("/generate-comic/json")
def generate_json(req: PromptRequest):

    try:

        outline = generate_outline(
            req.story_prompt,
            req.character_name,
            req.setting,
            req.tone,
            req.art_style
        )

        story = generate_story(
            outline,
            req.character_name,
            req.setting,
            req.tone,
            req.art_style
        )

        image_paths = []

        for panel in story[:5]:

            image_path = generate_image(
                panel["image_prompt"],
                panel["panel_number"],
                panel["panel_number"] * 12345
            )

            image_paths.append(image_path)

        layout = build_comic_layout(
            story[:5],
            image_paths
        )

        pdf_path = save_pdf(layout)

        return {
            "success": True,
            "layout": layout,
            "pdf_path": pdf_path
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


@router.post("/test-image")
def test_image(prompt: str = Form(...)):

    try:

        image_path = generate_image(
            prompt,
            1,
            12345
        )

        return {
            "success": True,
            "image_path": image_path
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


@router.get("/download/{filename}")
def download(filename: str):

    path = settings.exports_dir / Path(filename).name

    if not path.exists():

        raise HTTPException(
            status_code=404,
            detail="PDF not found"
        )

    return FileResponse(
        path,
        media_type="application/pdf",
        filename=path.name
    )