import os
os.environ['MOCK_MODE']='true'
from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health():
    r=client.get('/health'); assert r.status_code==200; assert r.json()['status']=='ok'
def test_home():
    r=client.get('/'); assert r.status_code==200; assert 'ComicCraft' in r.text
def test_json_generation_mock():
    p={'story_prompt':'A brave fox exploring an enchanted forest.','character_name':'Fenn','setting':'Forest','tone':'Funny','art_style':'Comic book'}
    r=client.post('/generate-comic/json',json=p); assert r.status_code==200; d=r.json(); assert d['success']; assert len(d['layout'])==5; assert d['pdf_path'].endswith('.pdf')
