from datetime import datetime
from pathlib import Path
from fpdf import FPDF
from app.config import get_settings

def _local_image(url_path):
    s = get_settings()
    return s.base_dir / 'static' / url_path.replace('/static/', '', 1)

def _text(value):
    return str(value).encode('latin-1','replace').decode('latin-1')

def save_pdf(layout):
    s = get_settings()
    filename = f"comic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    out = s.exports_dir / filename
    pdf = FPDF('P','mm','A4')
    pdf.set_auto_page_break(True, 15)
    for p in layout:
        pdf.add_page()
        pdf.set_font('Helvetica','B',18)
        pdf.cell(0,12,_text(f"Panel {p['panel_number']}: {p['title']}"),ln=True)
        img = _local_image(p['image_path'])
        if img.exists(): pdf.image(str(img), x=15, y=30, w=180)
        pdf.ln(110)
        pdf.set_font('Helvetica','I',11); pdf.multi_cell(180,7,_text(p['scene_description']))
        pdf.ln(3); pdf.set_font('Helvetica','B',11); pdf.multi_cell(180,7,'Caption')
        pdf.set_font('Helvetica','',11); pdf.multi_cell(180,7,_text(p.get('caption','')))
        pdf.ln(2); pdf.set_font('Helvetica','B',11); pdf.multi_cell(180,7,'Narration')
        pdf.set_font('Helvetica','',11); pdf.multi_cell(180,7,_text(p.get('narration','')))
        if p.get('dialogue'):
            pdf.ln(2); pdf.set_font('Helvetica','B',11); pdf.multi_cell(180,7,'Dialogue')
            pdf.set_font('Helvetica','',11); pdf.multi_cell(180,7,_text(p['dialogue']))
    pdf.output(str(out))
    return f'/static/exports/{filename}'
