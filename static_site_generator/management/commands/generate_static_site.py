from django.core.management.base import NoArgsCommand
from mezzanine.pages.models import Page
class Command(NoArgsCommand):

    
    def handle_noargs(self, **options):
        pages = Page.objects.all()
        for page in pages:
            page.save()
        
        
