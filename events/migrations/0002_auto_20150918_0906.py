# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='content',
            field=mezzanine.core.fields.RichTextField(verbose_name=b'Content'),
        ),
    ]
