from haystack import indexes

from django.utils import timezone

from mezzanine.blog.models import BlogPost


class BlogPostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    body = indexes.CharField(model_attr='body')

    def get_model(self):
        return BlogPost

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        print "----"
        return self.get_model().objects.filter(timestamp__lte=timezone.now())