class Slacker(object):
    """The summary of the class
    the class send message to slack
    Args:
        incoming_webhook_url (str): slack_incoming_webhook_url
        slack_token (str): slack_token
    Attributes:
        None
    Methods:
        slack_messenger: to send message
        get_slack_members_id_dict: get slack members id as a dictionary type
    """
    def __init__(self, incoming_webhook_url, slack_token):
        self._webhook_url = incoming_webhook_url
        self._slack_token = slack_token

    def slack_messenger(self, main_message, channel, user_name, icon_emoji, attachments=None, mention_members=[], 
                        is_link_name=1, at_here=False, at_channel=False):
        """The summary line
        This method send a message to slack.
        Args:
            webhook_url (str): webhook_url of your slack channel
            main_message (str): you can use markdown. if you want mantion, <@userID> or <!here>
            channel (str): the channel whichi you want to send a message
            user_name (str): the name who send a message
            icon_emoji (str): the image who send a message
            is_link_name (int): if 1, channel name links the channel (examle: #general)
            mention_members (list of str): who you want to mention. you can choose many people.
            at_here (bool): if true, a message mention @here automatically
            at_channel (bool): if true, a message mention @channel automatically
        Returns:
            None
        """ 
        if len(mention_members) > 0:
            mention_text = self.mention_text_creater(mention_members)
            main_message += mention_text
        if at_here:
            main_message += "<!here>"
        if at_channel:
            main_message += "<!channel>"
        payload = json.dumps({
            'text': main_message,
            'channel': channel,
            'username': user_name,
            'icon_emoji': icon_emoji,
            'link_names': is_link_name,
            "attachments": attachments
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
    
    def mention_text_creater(self, mention_members):
        """The summary line
        This method create text for mention
        It insert main_message
        This text format follows slack format rules
        Args:
            mention_menvers (list of str): who you want to mention. you can choose many people.
        Returns:
            mention_text (str): mention_text of menmers who you want to mention
        """
        slack_members_id_dict = self.get_slack_members_id_dict()
        mention_text = ""
        for name in mention_members:
            slack_id = slack_members_id_dict[name]
            mention_text += "<@{}>".format(slack_id)
        return mention_text
    
    def attachment_creater(self, fallback="", color="", pretext="", auther_name="", auther_link="", 
                            auther_icon="", title="", title_link="", text="", fields=[], actions=[], 
                            image_url="", thumb_url="", footer="", footer_icon="", ts=0, isnow=False):
        """The summary line.
        This method return slack attachments.
        Args:
            fallback (str): summary of this attachment. sometimes is displayed in the notification
            color (str): good, warning, danger, or color code like #000000
            pretext (str): explanation of the attachement
            auther_name (str): who created this attachment
            auther_link (str): a url links auther_name
            auther_icon (str): a image url representing the auther
            title (str): 
            tille_link (str): a url link to title
            text (str): Optional text that appears within the attachment
            fields (list of json): Fields get displayed in a table-like way.
                field (json): Args: Title(str), value(str), short. if you choose short, a field puts two horizontal direction 
            actions (list of json): Button and Select. you can make responsive action. (but not yet)
            image_url (str): a image url to send slack (max width:360px, max height:500px)
            thumb_url (str): a image url places thumbnail on the right side of a message (max width height 75px)
            footer (str): footer message
            footer_icon (str): a image url of footer icon (max width height 16px)
            ts (int): epoch time
        Returns:
            attachemt_json (json): slack attachment that follows slack rule
        Attention:
            slack data api attachments can contain some attachemnts
            you should create list of the return and give slack_messenger
        """
        attachments_json = {}
        # if no parameters, list str dict, it will be False
        if fallback:
            attachments_json["fallback"] = fallback
        if color:
            attachments_json["color"] = color
        if pretext:
            attachments_json["pretext"] = pretext
        if auther_name:
            attachments_json["auther_name"] = auther_name
            if auther_link:
                attachments_json["auther_link"] = auther_link
            if auther_icon:
                attachments_json["auther_icon"] = auther_icon
        if title:
            attachments_json["title"] = title
            if title_link:
                attachments_json["title_link"] = title_link
        if text:
            attachments_json["text"] = text
        if fields:
            attachments_json["fields"] = fields
        if actions:
            attachments_json["actions"] = actions
        if image_url:
            attachments_json["image_url"] = image_url
        if thumb_url:
            attachments_json["thumb_url"] = thumb_url
        if footer:
            attachments_json["footer"] = footer
        if footer_icon:
            attachments_json["footer_icon"] = footer_icon
        if ts:
            attachments_json["ts"] = ts
        if isnow:
            attachments_json["ts"] = self._ts_creater_at_now()
        return attachments_json
    
    def _ts_creater_at_now(self):
        """return now unix time"""
        now = datetime.datetime.now()
        unix_time = int(time.mktime(now.timetuple()))
        return unix_time
        
    def url_button_creater(self, button_name, text, link_url, style="default", isConfirm=False):
        """The summary line.
        This method slack action of button.
        Args:
            style (str): button style. it has patterns, deafult, primary, danger
            text (str): text of button
            link_url (str): a url links button
            isComfirm (bool): if true, you will comfirm to jump url
        Returns:
            action_json (json): slack action of button that follows slack rule
        Attention:
            slack data api actions can contain some actions
            you should create list of the return and give slack_messenger
        """
        action_json = {"type":"button"}
        if isConfirm:
            action_json["confirm"] = {  # this parameters are default
                        "title": "Are you sure?",
                        "text": "Wouldn't you prefer a good game of chess?",
                        "ok_text": "Yes",
                        "dismiss_text": "No"
                    }
        action_json["name"] = button_name
        action_json["text"] = text
        action_json["url"] = link_url
        if style not in ["default", "primary", "danger"]:
            raise "this style not compatible slack rule"
        action_json["style"] = style
        return action_json
    
    def menu_creater(self,menu_name, menu_list, placeholder=""):
        """The summary line.
        This method slack action of menu.
        Args:
            menu_name (str): menu_name. its note desplayed slack
            placeholder (str):  this will be inputed in the menu bar at first
            menu_list (list): these are the list of menu
        Returns:
            action_json (json): slack action of menu that follows slack rule
        Attention:
            slack data api actions can contain some actions
            you should create list of the return and give slack_messenger
        """
        action_json = {"type": "select"}
        action_json["name"] = menu_name
        action_json["text"] = placeholder
        options = []
        if len(menu_list) == 0:
            raise "nothing inthe menu_list"
        for menu_text in menu_list:
            option = {
                "text": menu_text,
                "value": "null"  # setup later
            }
            options.append(option)
        action_json["options"] = options
        return action_json
