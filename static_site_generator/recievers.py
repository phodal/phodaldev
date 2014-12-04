import requests
import os
from mezzanine.pages.models import Page
from django.core.handlers.base import BaseHandler  
from django.test.client import RequestFactory  
from mezzanine.pages.views import page
from django.conf import settings
  
class RequestMock(RequestFactory):  
    def request(self, **request):  
        "Construct a generic request object."  
        request = RequestFactory.request(self, **request)  
        handler = BaseHandler()  
        handler.load_middleware()  
        for middleware_method in handler._request_middleware:  
            if middleware_method(request):  
                raise Exception("Couldn't create request mock object - "  
                                "request middleware returned a response")  
        return request


def create_static_file(sender, instance, signal, *args, **kwargs):
    if Page in sender.__bases__ or sender == Page:
        try:
            root_dir = settings.HTML_SITE_ROOT
        except AttributeError:
            root_dir  = settings.PROJECT_ROOT + "/" + "_site"
        try:
            if not os.path.exists(root_dir):
                os.makedirs(root_dir)
        except OSError, e :
            raise e
                    
        current_dir = root_dir
        os.chdir(current_dir)
        while instance:
            request = RequestMock().request()
            response = page(request, instance.slug)
            slug = instance.get_slug()
            slug_parts = slug.split('/')
            pos = 0
            length = len(slug_parts)
            filename = 'index.html'
            while(pos < length):
                current_dir = slug_parts[pos]
                if not os.path.exists(current_dir):
                    os.makedirs(current_dir)                
                os.chdir(current_dir)
                pos += 1
            fobj = open(filename, 'w')
            fobj.write(response.rendered_content)
            fobj.close()
            instance = instance.parent
            os.chdir(root_dir)