from django.contrib.contenttypes.models import ContentType


def run():
    def do(Table):
        if Table is not None:
            table_objects = Table.objects.all()
            for i in table_objects:
                i.save(using='slave')

    ContentType.objects.using('slave').all().delete()

    for i in ContentType.objects.all():
        do(i.model_class())
