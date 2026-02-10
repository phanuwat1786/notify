from pathlib import Path
from discord_webhook import DiscordWebhook,DiscordEmbed
from dotenv import load_dotenv
import os
from typing import Self,Literal
class DiscordNotify():
    """
    Object that store discord webhook url along with some other parameters and function to send messages/embed.

    Args:
        webhook: Discord wehbhook url.
        username: username to replace webhook default username. Default value is 'My-webhook' 
    """

    embeded_red = "dd0531" #red_color code.
    embeded_green = "368c3b" #green color code.

    def __init__(
        self,
        webhook: str = None,
        username: str = "My-webhook"
    ):
        self.webhook = webhook
        self.username = username

    def send_simple_text(self,
                        message: str):
        """
        Send simple text content to webhook.
        
        Args:
            message: message to send to webhook.
        """
        wh = DiscordWebhook(url = self.webhook, content = message, username = self.username)
        wh.execute()

    def send_embeded(
        self,
        embed: DiscordEmbed,
        extra_content: str
    ) :
        """
        Send DiscordEmbed message to webhook.
        
        Args:
            embed: DiscordEmbed class content to send to webhook.
            extra_content: extra text content to send along with embed.
        """
        wh = DiscordWebhook(url = self.webhook,username = self.username, content = extra_content)
        wh.add_embed(embed = embed)
        wh.execute()

def from_env(
    env_path:Path | str = None,
    variable_name: str = 'DISCORD_WEBHOOK',
    username: str = 'My-webhook' 
) -> DiscordNotify:
    """
    Create DiscordNotify class from env.

    This function read webhook from env or stored in .env file.
    
    Args:
        env_path: path to .env file contain webhook.
        varible_name: key name that contain webhook value. default is 'DISCORD_WEBHOOK'.
        username: default username to set in webhook object.

    Returns:
        DiscordNotify: DiscordNotify class with webhook store in env.
    """
    if env_path is not None:
        if isinstance(env_path,str):
            env_path = Path(env_path)

        elif not isinstance(env_path,Path):
            raise ValueError(f"invalid env_path type for type {type(env_path)}. Must be String or pathlib.Path") #place holder for custom Exception

        load_dotenv(dotenv_path = env_path)

    webhook = os.getenv(key = variable_name)
    return DiscordNotify(webhook= webhook,username = username)

def dag_fail_callback(webhook: str ,context: dict):
    """
    callback function for airflow to send message to discord when dag failed.
    
    :param webhook: discord webhook.
    :type webhook: str
    :param context: airflow context at dag fail state in form of dictionary. 
    :type context: dict
    """

    wh = DiscordNotify(webhook= webhook)
    wh.send_simple_text(message= str(context))