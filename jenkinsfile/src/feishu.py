import argparse
import json
import requests

def send_feishu_card(result, date, details, link):
    if result == 'SUCCESS':
        color = 'Green'
        button_type = 'primary'
    if result == "FAILURE":
        color = 'Red'
        button_type = 'danger'
    if result == "ABORTED":
        color = 'Grey'
        button_type = 'aborted'

    data = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f'{result}'+"\n"+f'{date}'
                },
                "template": f"{color}"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"{details} "
                    }
                },
                {
                    "tag": "action",
                    "actions": [{
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "open the job link",
                        },
                        "url": f"{link}",
                        "type": f"{button_type}",
                        "value": {}
                    }]
                }
            ]
        }
    }
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/660e3a43-2f8f-4883-9ecc-240a02287c88"
    res = requests.post(url, data=json.dumps(data))
    print(res.content)
    assert res.status_code == 200

def main():
    parser = argparse.ArgumentParser(description='Check if savepb jobs are done')
    parser.add_argument('--result', type=str, required=True, help="jenkins job result: SUCCESS, FAILED, ABORTED, etc.")
    parser.add_argument('--date', type=str, required=True, help=" 2021-08-18/10:22:90")
    parser.add_argument('--details', type=str, required=True, help="card content")
    parser.add_argument('--link', type=str, required=True, help="jenkins job link")
    args = parser.parse_args()
    send_feishu_card(args.result, args.date, args.details, args.link)

if __name__ == '__main__':
    main()
# python3 feishu_notification.py --result SUCCESS --date 2021-08-18/10:22:90  --details 啊哈哈 --link 定时发撒