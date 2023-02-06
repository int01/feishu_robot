import logging
import os

import openai
from flask import Flask, redirect, render_template, request, url_for
from redisUtil import build_req_msg_txt, build_resp_msg_txt

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


# https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/events/receive

def snnd_openai_text(question_json_str, open_id):
    if request.method == "POST":
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=generate_prompt(question_json_str, open_id),
                temperature=0.7,
                #     temperature min 0 ，max0.9
                max_tokens=1024,  # 2024
                top_p=1,
                stop=["Human:", "AI:"],  # ["wunike:","sage:"]  ["Human:", "AI:"]
                frequency_penalty=0,
                presence_penalty=0,
            )
            resp_text = response.choices[0].text.lstrip('\n')
            print("openAi api response text --->" + resp_text)
            build_resp_msg_txt(open_id, resp_text)
            # return "问："+question_json_str+" \n答："+response.choices[0].text
            return resp_text
        except Exception as e:
            logging.WARNING(e)
            return "熬，你抓到了一个\"AI API\"接口异常。"


def generate_prompt(question_json_str, open_id):
    req_text = build_req_msg_txt(open_id, question_json_str)
    print("open_id 说 --> ", open_id, req_text)
    return req_text.capitalize()
