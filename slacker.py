class Slacker(object):
    """The summary of the class
    the class send messege to slack
    Args:
        incoming_webhook_url (str): slack_incoming_webhook_url
        slack_token (str): slack_token
    Attributes:
        None
    Methods:
        slack_messenger: to send messege
        get_slack_members_id_dict: get slack members id as a dictionary type
    """
    def __init__(self, incoming_webhook_url, slack_token):
        self._webhook_url = incoming_webhook_url
        self._slack_token = slack_token

    def slack_messenger(self, main_messege, channel, user_name, icon_emoji, mention_members, 
                        is_link_name=1, at_here=False, at_channel=False):
        """The summary line
        This method send a messege to slack.
        Args:
            webhook_url (str): webhook_url of your slack channel
            main_messege (str): you can use markdown. if you want mantion, <@userID> or <!here>
            channel (str): the channel whichi you want to send a messege
            user_name (str): the name who send a messege
            icon_emoji (str): the image who send a messege
            is_link_name (int): if 1, channel name links the channel (examle: #general)
            mention_members (list of str): who you want to mention. you can choose many people.
            at_here (bool): if true, a messege mention @here automatically
            at_channel (bool): if true, a messege mention @channel automatically
        Returns:
            None
        """ 
        payload = json.dumps({
            'text': main_messege,
            'channel': channel,
            'username': user_name,
            'icon_emoji': icon_emoji,
            'link_names': is_link_name
        })
        requests.post(self._webhook_url, data=payload)
        return

    def get_slack_members_id_dict(self):
        """The summary line
        This method create dictionary pair of slack_id and slack_names
        Args:
            slacke_token (str): Slack api token.
        Returns:
            slack_members_id (dict): {slack_name: slack_id}
        """
        slack_members_id = {}
        slack_user_list_url = "https://slack.com/api/users.list?token=" + self._slack_token
        slack_user_list_api = requests.get(slack_user_list_url)
        slack_user_list_jcon = json.loads(slack_user_list_api.text)
        slack_user_list_members = slack_user_list_jcon["members"]
        for member_data in slack_user_list_members:
            slack_members_id[member_data["real_name"]] = member_data["id"]
        return slack_members_id
