from flask import Flask
from random import randint
from os import environ
from pathlib import Path
from dotenv import load_dotenv
from slack_sdk import WebClient
from slackeventsapi import SlackEventAdapter

env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(environ['SIGNING_SECRET'], '/slack/events', app)


client = WebClient(token=environ['SLACK_TOKEN'])
BOT_ID = client.api_call('auth.test')['user_id']

ADVISORS = ["U072WMN6BJN", "U072UDR1VJR"]


def advisor_selector():
    return ADVISORS[randint(0, len(ADVISORS)-1)]


@slack_event_adapter.on('app_mention')
def message(payload):
    event = payload.get('event', {})
    channel = event.get('channel')
    user_id = event.get('user')
    ts = event.get('ts')
    lucky_one = f'<@{advisor_selector()}> sende burası kankam'
    if user_id != BOT_ID:
        client.chat_postMessage(channel=channel, thread_ts=ts, text=lucky_one)


@app.route("/")
def hello_world():
    return "<p>This is advisor rulet for optimus team</p>"


if __name__ == '__main__':
    app.run(debug=True)
