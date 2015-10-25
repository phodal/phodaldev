from django.http import HttpResponse
from wechat.models import WxTextResponse
from wechat.official import WxApplication


class EchoApp(WxApplication):
    SECRET_TOKEN = ''
    APP_ID = ''
    ENCODING_AES_KEY = ''

    def on_text(req):
        return WxTextResponse(req.Content, req)


def wechat(request):
    echo = EchoApp()
    return HttpResponse(echo.process(request.GET, request.body))
