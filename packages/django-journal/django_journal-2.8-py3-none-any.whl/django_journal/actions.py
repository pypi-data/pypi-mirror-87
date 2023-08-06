import csv


from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.utils.encoding import force_text


from . import models

def export_as_csv_generator(queryset):
    header = ['time', 'tag', 'message']
    tags = set(models.Tag.objects.filter(objectdata__journal__in=queryset).values_list('name', flat=True))
    for tag in list(tags):
        tags.add('%s__id' % tag)
    tags |= set(models.Tag.objects.filter(stringdata__journal__in=queryset).values_list('name', flat=True))
    extra_headers = list(sorted(tags))
    yield header+extra_headers
    for journal in queryset:
        row = {
                'time': journal.time.isoformat(' '),
                'tag': force_text(journal.tag.name),
                'message': force_text(journal),
              }
        for stringdata in journal.stringdata_set.all():
            row_name = stringdata.tag.name.encode('utf-8')
            row[force_text(row_name)] = force_text(stringdata.content)
        for objectdata in journal.objectdata_set.all():
            row_name = force_text(objectdata.tag.name)
            row[row_name + '__id'] = str(objectdata.object_id)
            if objectdata.content_object is None:
                row[row_name] = '<deleted>'
            else:
                row[row_name] = force_text(objectdata.content_object)
        yield row

def export_as_csv(modeladmin, request, queryset):
    """
    CSV export for journal
    """
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=journal.csv'
    l = export_as_csv_generator(queryset)
    header = l.next()
    writer = csv.DictWriter(response, header)
    writer.writerow(dict(zip(header, header)))
    for row in l:
        writer.writerow(row)
    return response
export_as_csv.short_description = _(u"Export CSV file")
