from django.template.loader import get_template
from django.http import Http404, HttpResponse
from xhtml2pdf import pisa
from io import BytesIO

def render_report(template_src,report={}):
    template = get_template(template_src)
    html = template.render(report)
    result= BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')),result) 
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='aplication/pdf')
    else:
        return Http404('Error al generar PDF')
    
    