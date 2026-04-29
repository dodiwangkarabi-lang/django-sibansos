# from reportlab.pdfgen import canvas
# from django.http import HttpResponse

# def pdf_report(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="laporan.pdf"'

#     p = canvas.Canvas(response)
#     p.drawString(100, 800, "Laporan Data Bantuan")

#     y = 750
#     for item in ModelBantuan.objects.all():
#         p.drawString(100, y, f"{item.id} - {item.catatan} - {item.status}")
#         y -= 20

#     p.showPage()
#     p.save()
#     return response

from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO

# Queryset
from django.db.models import QuerySet

def pdf_report(data: QuerySet, path_html: str ="bantuan/laporan.html") -> bytes:
    html_string = render_to_string(path_html, {"data": data})
    result = BytesIO()
    pisa.CreatePDF(html_string, dest=result)
    pdf = result.getvalue()
    
    return pdf