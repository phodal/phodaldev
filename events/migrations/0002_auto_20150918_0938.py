# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('url', models.URLField()),
                ('content', mezzanine.core.fields.RichTextField(verbose_name=b'Content')),
                ('date', models.DateField()),
                ('is_active', models.BooleanField(default=False, help_text=b"Tick to make this event live (see also the publication date). Note that administrators (like yourself) are allowed to preview inactive events whereas the general public aren't.")),
                ('pub_date', models.DateTimeField(help_text=b'For an event to be published, it must be active and its publication date must be in the past.', verbose_name=b'Publication date')),
            ],
            options={
                'ordering': ('-pub_date',),
                'get_latest_by': 'pub_date',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='event',
            name='content',
            field=mezzanine.core.fields.RichTextField(verbose_name=b'Content'),
        ),
    ]
