# coding: utf-8

import cStringIO

from django.template.loader import render_to_string
from django.http import HttpResponse

import xhtml2pdf.pisa as pisa


class PDFUtils(object):

    @classmethod
    def tmpl2pdf(cls, tmpl, context_data=None):
        context_data = context_data or {}

        html = render_to_string(tmpl, context_data)
        memory_file = cStringIO.StringIO()

        pdf = pisa.CreatePDF(
            html,
            memory_file,
        )

        if pdf.err:
            return None
        else:
            return memory_file

    @classmethod
    def download_pdf(cls, tmpl, context_data=None, filename='pinbot.pdf'):
        pdf = cls.tmpl2pdf(tmpl, context_data)

        if not pdf:
            return HttpResponse('下载失败，请刷新页面重试！')

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        response.write(pdf.getvalue())
        return response
