from pathlib import Path
from functools import lru_cache
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

class Settings:
    def __init__(self):
        self.base_dir = BASE_DIR
        self.gemini_api_key = os.getenv('GEMINI_API_KEY', '').strip()
        self.gemini_outline_model = os.getenv('GEMINI_OUTLINE_MODEL', 'gemini-3.8-flash')
        self.gemini_story_model = os.getenv('GEMINI_STORY_MODEL', 'gemini-3.8-flash')
        self.image_provider = os.getenv('IMAGE_PROVIDER', 'diffusers').lower().strip()
        self.image_model_id = os.getenv('IMAGE_MODEL_ID', 'stable-diffusion-v1-5/stable-diffusion-v1-5')
        self.hf_token = os.getenv('HF_TOKEN', '').strip()
        self.mock_mode = os.getenv('MOCK_MODE', 'false').lower() in {'1','true','yes'}
        self.image_width = int(os.getenv('IMAGE_WIDTH', '512'))
        self.image_height = int(os.getenv('IMAGE_HEIGHT', '512'))
        self.image_steps = int(os.getenv('IMAGE_STEPS', '25'))
        self.image_guidance = float(os.getenv('IMAGE_GUIDANCE', '7.5'))
        self.max_panels = int(os.getenv('MAX_PANELS', '5'))
        self.panels_dir = BASE_DIR / os.getenv('PANELS_DIR', 'static/panels')
        self.exports_dir = BASE_DIR / os.getenv('EXPORTS_DIR', 'static/exports')
        self.panels_dir.mkdir(parents=True, exist_ok=True)
        self.exports_dir.mkdir(parents=True, exist_ok=True)

@lru_cache
def get_settings():
    return Settings()
