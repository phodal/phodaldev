# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from mezzanine.blog.models import BlogPost

from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, \
    EventMessage

from MK_dream.local_settings import WECHAT_TOKEN, AppID, AppSecret

wechat_instance = WechatBasic(
    token=WECHAT_TOKEN,
    appid=AppID,
    appsecret=AppSecret
)


@csrf_exempt
def wechat(request):
    if request.method == 'GET':
        # 检验合法性
        # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')

        if not wechat_instance.check_signature(
                signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')

        return HttpResponse(
            request.GET.get('echostr', ''), content_type="text/plain")


    # 解析本次请求的 XML 数据
    try:
        wechat_instance.parse_data(data=request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')

    # 获取解析好的微信请求信息
    message = wechat_instance.get_message()

    if isinstance(message, TextMessage):
        # 当前会话内容
        content = message.content.strip()
        if content == '博客' or content == 'blog' or content == '最新':
            return HttpResponse(wechat_instance.response_news(get_new_blogposts(request)), content_type="application/xml")
        if content == '功能':
            reply_text = (
                '目前支持的功能：最新博客\n'
                '正在实现: 博客搜索、标签搜索、Google、Wiki'
            )
            response = wechat_instance.response_text(content=reply_text)
            return HttpResponse(response, content_type="application/xml")

        if 'wiki' in content or '维基' in content:
            import wikipedia
            wiki_content = content.replace("wiki:", "")
            print wiki_content
            wiki = wikipedia.page(wiki_content)

            print wiki.title,wiki.summary,wiki.url
            message = [{
                'title': wiki.title,
                'picurl': '',
                'description': wiki.summary,
                'url': wiki.url
            }]

            return HttpResponse(wechat_instance.response_news(message), content_type="application/xml")

        if 'google' in content:
            from google import search
            for url in search(content.replace('google:', ''), stop=1):
                print(url)

            return HttpResponse(wechat_instance.response_news(get_new_blogposts(request)), content_type="application/xml")
        else:
            response = get_new_blogposts(request)
            message = {
                'title': '稍等：Phodal君正在实现功能中。正在为你返回最新文章。',
                'picurl': 'https://www.phodal.com/static/phodal/images/bg.jpg',
                'description': '稍等：Phodal君正在实现功能中。现在为你返回最新文章。',
                'url': 'https://www.phodal.com/',
            }
            response.insert(0, message)
            return HttpResponse(wechat_instance.response_news(response), content_type="application/xml")

    elif isinstance(message, VoiceMessage):
        reply_text = '语音信息我听不懂/:P-(/:P-(/:P-('
    elif isinstance(message, ImageMessage):
        reply_text = '图片信息我也看不懂/:P-(/:P-(/:P-('
    elif isinstance(message, VideoMessage):
        reply_text = '视频我不会看/:P-('
    elif isinstance(message, LinkMessage):
        reply_text = '链接信息'
    elif isinstance(message, LocationMessage):
        reply_text = '地理位置信息'
    elif isinstance(message, EventMessage):
        if message.type == 'subscribe':
            reply_text = '感谢您的关注！回复【功能】返回使用指南'
            if message.key and message.ticket:
                reply_text += '\n来源：扫描二维码'
            else:
                reply_text += '\n来源：搜索名称'
        elif message.type == 'unsubscribe':
            reply_text = '取消关注事件'
        elif message.type == 'scan':
            reply_text = '已关注用户扫描二维码！'
        elif message.type == 'location':
            reply_text = '上报地理位置'
        elif message.type == 'click':
            reply_text = '自定义菜单点击'
        elif message.type == 'view':
            reply_text = '自定义菜单跳转链接'
        elif message.type == 'templatesendjobfinish':
            reply_text = '模板消息'
    else:
        reply_text = '稍等：Phodal君正在实现功能中。'

    response = wechat_instance.response_text(content=reply_text)
    return HttpResponse(response, content_type="application/xml")


def get_new_blogposts(request):
    blog_posts = BlogPost.objects.published(for_user=request.user)
    prefetch = ("categories", "keywords__keyword")
    blog_posts = blog_posts.select_related("user").prefetch_related(*prefetch)[:5]
    picurl = 'https://avatars1.githubusercontent.com/u/472311?v=3&s=460'
    response = [
        {
            'title': blog_posts[0].title,
            'picurl': 'https://www.phodal.com/static/phodal/images/bg.jpg',
            'description': blog_posts[0].description,
            'url': blog_posts[0].slug,
        }, {
            'title': blog_posts[1].title,
            'picurl': picurl,
            'url': blog_posts[1].slug,
        }, {
            'title': blog_posts[2].title,
            'picurl': picurl,
            'url': blog_posts[2].slug,
        }, {
            'title': blog_posts[3].title,
            'picurl': picurl,
            'url': blog_posts[3].slug,
        }, {
            'title': blog_posts[4].title,
            'picurl': picurl,
            'url': blog_posts[4].slug,
        }
    ]
    return response
