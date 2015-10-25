# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, \
    EventMessage

WECHAT_TOKEN = 'thisislooklikeatookenmaybe'
AppID = 'wxd196ba4c0237a839'
AppSecret = 'd760de12c8c2a71ef808f2d4837428ce'

# 实例化 WechatBasic
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

    # 关注事件以及不匹配时的默认回复
    response = wechat_instance.response_text(
        content=(
            '感谢您的关注！\n回复【功能】两个字查看支持的功能，还可以回复任意内容开始聊天！\nPhodal君正在实现功能中。'
        ))
    if isinstance(message, TextMessage):
        # 当前会话内容
        content = message.content.strip()
        if content == '功能':
            reply_text = (
                '目前支持的功能：\n' +
                'Phodal君正在实现功能中。'
            )
        else:
            reply_text = '稍等：Phodal君正在实现功能中。'
            
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
    elif isinstance(message, EventMessage):  # 事件信息
        if message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
            follow_event = KeyWordModel.objects.get(keyword='关注事件')
            reply_text = follow_event.content

            # 如果 key 和 ticket 均不为空，则是扫描二维码造成的关注事件
            if message.key and message.ticket:
                reply_text += '\n来源：扫描二维码关注'
            else:
                reply_text += '\n来源：搜索名称关注'
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

    response = wechat_instance.response_text(content=reply_text)

    return HttpResponse(response, content_type="application/xml")
