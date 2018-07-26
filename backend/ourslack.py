from slackclient import SlackClient
import os

def list_users(cursor):
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
