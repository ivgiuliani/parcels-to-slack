import base64
from slackclient import SlackClient
import os

SLACK_BOT = SlackClient(os.environ["MAILBOT_SLACK_API_TOKEN"])

def send_parcel_notification(user_id=None, base64_image=None):
    if user_id == None:
        send_to_general(base64_image)
        return

    if base64_image == None:
        SLACK_BOT.api_call("chat.postMessage", channel=user_id, text="You've got a parcel!")
        return

    SLACK_BOT.api_call(
        "files.upload",
        file=base64.b64decode(base64_image),
        filetype="png",
        channels=user_id,
        title="You have a parcel!",
        initial_comment="👋📦"
    )

def send_to_general(base64_image):
    SLACK_BOT.api_call(
        "files.upload",
        file=base64.b64decode(base64_image),
        filetype="png",
        channels="#general",
        initial_comment="Parcel for somebody! Don't know who! 📦📦📦"
    )

def all_users():
    """
    Gets a list of all slack users
    """
    first_page_of_users = list_users()
    next_cursor = first_page_of_users["cursor"]
    member_list = first_page_of_users["members"]
    while next_cursor != "":
        next_page_of_users = list_users(cursor=next_cursor)
        member_list.append(next_page_of_users["members"])
        next_cursor = next_page_of_users["cursor"]

    return member_list


def list_users(cursor=None):
    """Gets a page of users from Slack

    Args:
    cursor: the cursor to read from, for pagination
    """
    sbToken = os.environ["MAILBOT_SLACK_API_TOKEN"]
    sc = SlackClient(sbToken)
    # Note that 500 is 'aspirational...'
    results = sc.api_call("users.list", cursor=cursor, limit=500)
    members = []
    for m in results["members"]:
        members.append({"name": m["real_name"], "id": m["id"]})

    next_cursor = None
    if "response_metadata" in results:
        next_cursor = results["response_metadata"]["next_cursor"]

    return { "members": members, "cursor": next_cursor }
