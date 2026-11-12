import os
import re
import logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

app_token=os.environ.get("SLACK_APP_TOKEN")
bot_token=os.environ.get("SLACK_BOT_TOKEN")
user_token=os.environ.get("SLACK_USER_TOKEN")

app=App(token=bot_token)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def handle_request(respond_fn, user_message, user_channel_id):

    match=re.search(r"<@([A-Z0-9]+)", user_message)

    if match:
        user_id=match.group(1)
    else:
        respond_fn("Please provide a valid user mention.")
        return

    channel_match = re.search(r"<#([A-Z0-9]+)", user_message)

    if channel_match:
        channel_id=channel_match.group(1)
    else:
        channel_id=user_channel_id
        respond_fn(f"Channel not specified. Defaulting to the current channel <#{channel_id}>.")
    try:
        total_messages=get_total_messages_via_search(user_id, channel_id)
        if total_messages:
            respond_fn(f"<@{user_id}> has sent a total of *{total_messages}* messages in channel <#{channel_id}>.")
            return
        elif total_messages==0:
            respond_fn(f"No messages found for <@{user_id}> in channel <#{channel_id}>.")
            return
        else:
            respond_fn("Can't fetch messages via search. Trying with conversation history...")
    except Exception as e:
        logging.error(f"Error occurred while fetching messages: {e}")
        respond_fn("An error occurred while fetching messages. Please try again later.")

    try:
        total_messages=get_total_messages_via_conversation(user_id, channel_id)
        if total_messages:
            respond_fn(f"<@{user_id}> has sent a total of *{total_messages}* messages in channel <#{channel_id}>.")
            return
        elif total_messages==0:
            respond_fn(f"No messages found for <@{user_id}> in channel <#{channel_id}>.")
            return
        else:
            respond_fn("Can't fetch messages via search and conversation history. Please try again later.")
    except Exception as e:
        logging.error(f"Error occurred while fetching messages: {e}")
        respond_fn("An error occurred while fetching messages. Please try again later.")

def get_total_messages_via_search(user_id, channel_id):
    # to be implemented
    pass

def get_total_messages_via_conversation(user_id, channel_id):
    # to be implemented
    pass

@app.command("/message-count")
def handle_some_command(ack, respond, command, logger):
    ack()
    logger.info(f"Queue called by {command['user_name']}({command['user_id']}) in channel {command['channel_name']}({command['channel_id']}) using command {command['command']}")

    user_message=command.get("text", "").strip()
    user_channel_id=command["channel_id"]
    handle_request(respond, user_message, user_channel_id)

@app.event("app_mention")
def handle_app_mention(event, say, logger):
    logger.info(f"Queue called by {event['user']} in channel {event['channel']} using app mention")

    thread_timestamp=event.get("ts")
    user_message=event.get("text", "").strip()
    user_channel_id=event.get("channel")

    respond_fn=lambda text: say(text=text, thread_ts=thread_timestamp)
    handle_request(respond_fn, user_message, user_channel_id)

if __name__ == "__main__":
    SocketModeHandler(app, app_token).start()