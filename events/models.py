from django.db import models
from django.utils import timezone
from mezzanine.core.fields import RichTextField


class EventQuerySet(models.query.QuerySet):
    def published(self):
        return self.active().filter(pub_date__lte=timezone.now())

    def active(self):
        return self.filter(is_active=True)

    def past(self):
        return self.filter(date__lte=timezone.now()).order_by('-date')

    def future(self):
        return self.filter(date__gte=timezone.now()).order_by('date')


class Event(models.Model):
    content = RichTextField("Content")
    date = models.DateField()
    location = models.CharField(max_length=100)
    is_active = models.BooleanField(
        help_text=(
            "Tick to make this event live (see also the publication date). "
            "Note that administrators (like yourself) are allowed to preview "
            "inactive events whereas the general public aren't."
        ),
        default=False,
    )
    pub_date = models.DateTimeField(
        verbose_name=("Publication date"),
        help_text=(
            "For an event to be published, it must be active and its "
            "publication date must be in the past."
        ),
    )

    objects = EventQuerySet.as_manager()

    class Meta:
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'

    def is_published(self):
        """
        Return True if the event is publicly accessible.
        """
        return self.is_active and self.pub_date <= timezone.now()

    is_published.boolean = True


class Ad(models.Model):
    content = RichTextField("Content")
    date = models.DateField()
    is_active = models.BooleanField(
        help_text=(
            "Tick to make this event live (see also the publication date). "
            "Note that administrators (like yourself) are allowed to preview "
            "inactive events whereas the general public aren't."
        ),
        default=False,
    )
    pub_date = models.DateTimeField(
        verbose_name=("Publication date"),
        help_text=(
            "For an event to be published, it must be active and its "
            "publication date must be in the past."
        ),
    )

    objects = EventQuerySet.as_manager()

    class Meta:
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'

    def is_published(self):
        return self.is_active and self.pub_date <= timezone.now()

    is_published.boolean = True
