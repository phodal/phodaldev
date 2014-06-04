from django.db import models
from django.db.models import signals
from recievers import create_static_file
signals.post_save.connect(create_static_file)
