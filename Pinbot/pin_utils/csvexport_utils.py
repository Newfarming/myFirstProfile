# coding: utf-8

import csv
from django.http import HttpResponse


class CSVExportUtils(object):

    @classmethod
    def generate_csv_response(cls, label, data, filename='csv_export'):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % filename

        response.write('\xEF\xBB\xBF')
        writer = csv.writer(response)
        writer.writerow(label)
        for line in data:
            writer.writerow(line)
        return response
