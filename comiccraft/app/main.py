from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from app.routes import router
s=get_settings()
app=FastAPI(title='ComicCraft - AI Comic Story Creator',version='1.0.0')
app.mount('/static',StaticFiles(directory=str(s.base_dir/'static')),name='static')
app.include_router(router)
@app.get('/health')
def health():
    return {'status':'ok','mock_mode':s.mock_mode,'image_provider':s.image_provider,'gemini_configured':bool(s.gemini_api_key)}
