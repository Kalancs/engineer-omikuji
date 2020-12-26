from flask import Flask, request, abort
import os,json,shutil
from dic import dic
from make_mikuji import make_mikuji
import urllib
from PIL import Image, ImageDraw, ImageFont
from PIL import Image
from massage import res

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, PostbackTemplateAction, PostbackEvent, PostbackAction, QuickReplyButton, QuickReply,
    FlexSendMessage, BubbleContainer, CarouselContainer, TextSendMessage,ImageSendMessage,
    TemplateSendMessage,ButtonsTemplate,URIAction
)


app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "Hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if (event.message.text == "おみくじ" or event.message.text == "おみくじをひく!"):

        omikuji(event)
        
        """
        image_link, lucky_text = make_mikuji.get_mikuji()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=lucky_text)
        )

        image_message = ImageSendMessage(
            content_url = image_link,
        )
        line_bot_api.reply_message(event.reply_token,image_message)
        """
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

def omikuji(event):
    '''
    
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    template_env = Environment(
        loader=FileSystemLoader('py-linebot/templates'),
        autoescape=select_autoescape(['html', 'xml', 'json'])
    )
    les = "les"
    template = template_env.get_template('test.json')
    data = template.render(dict(items=les))

    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text="items",
            contents=CarouselContainer.new_from_json_dict(json.loads(data))
        )
    )
    


 

    
    text=dic()
    #path="https://hackathon-engineer-omikuji.herokuapp.com/static/mikuji/base.jpg"
    #image = Image.open('py-linebot/static/mikuji/base.jpg')

    image_path,comment=make_mikuji(text)
    import os
    path = os.getcwd()
    files = os.listdir(path)
    print(type(files))  # <class 'list'>
    print(files) 

    url = f"https://winter-hackathon2020.herokuapp.com/static/mikuji/{image_path}"

    #image_path = "base.jpg"
    #comment='test'
    
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text="占い結果",
            template=ButtonsTemplate(
                text=comment + "だよ～",
                title="占い結果",
                image_size="contain",
                thumbnail_image_url=url,
                actions=[
                    URIAction(
                        uri="https://twitter.com/intent/tweet?" + 
                            urllib.parse.urlencode(
                            {
                                "img": url,
                                "hashtags": "えんじにあうらない",
                                "text": comment + "だよ～"
                            }
                        ),
                        label="Twitterで共有"
                    )
                ]
            )
        )
    )

if (__name__ == "__main__"):

    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port = port)

