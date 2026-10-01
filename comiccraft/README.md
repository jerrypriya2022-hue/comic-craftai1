# ComicCraft — AI Comic Story Creator

This implementation follows the supplied ComicCraft document: FastAPI + Jinja2 frontend, a 5-panel outline, Gemini text stages, Stable Diffusion image generation, panel layout, and FPDF PDF export.

## Quick start — Windows PowerShell

```powershell
cd comiccraft
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

For a first test without downloading a large image model, edit `.env` and set:

```env
MOCK_MODE=true
IMAGE_PROVIDER=mock
```

Then run:

```powershell
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` and API docs at `http://127.0.0.1:8000/docs`.

## Real AI mode

Set `MOCK_MODE=false`, add `GEMINI_API_KEY`, and use `IMAGE_PROVIDER=diffusers`. The first image generation downloads `stable-diffusion-v1-5/stable-diffusion-v1-5` from Hugging Face. A CUDA NVIDIA GPU is strongly recommended; CPU is supported but slow.

## API

POST JSON to `/generate-comic/json` with `story_prompt`, `character_name`, `setting`, `tone`, and `art_style`.

## Tests

```powershell
pytest -q
```
