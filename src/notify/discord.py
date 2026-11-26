from pathlib import Path
from discord_webhook import DiscordWebhook,DiscordEmbed
from dotenv import load_dotenv
import os
from typing import Literal
from airflow.models import Variable
import io
import pendulum
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
        extra_content: str = None
    ) :
        """
        Send DiscordEmbed message to webhook.
        
        Args:
            embed: DiscordEmbed class content to send to webhook.
            extra_content: extra text content to send along with embed.
        """
        wh = DiscordWebhook(url = self.webhook,username = self.username, content = extra_content )
        wh.add_embed(embed = embed)
        wh.execute()

    def send_text_attachment(
        self,
        text: str
    ):
        f = io.StringIO(text)
        wh = DiscordWebhook(url = self.webhook, username = self.username)
        wh.add_file(file = f.read(), filename= 'exception.txt')
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

def task_fail_callback(webhook_variable_key: str,context: dict):
    """
    callback function for airflow to send message to discord when task failed.

    This function read Task and Dag run detail from airflow provided's context  then send notify message to discord.

    :param webhook_variable_key: airflow variable key that store designated discord webhook.
    :param context: airflow context at dag fail state from task.
    """
    webhook = Variable.get(webhook_variable_key)
    wh = DiscordNotify(webhook= webhook,username= "Dag run error")

    ti = context['ti']
    dag_id = str(ti.dag_id)
    task_id = str(ti.task_id)
    execution_time = pendulum.instance(ti.start_date).in_timezone( tz = "Asia/Bangkok").to_datetime_string()
    prev_success_time = context["prev_start_date_success"].in_timezone(tz = 'Asia/Bangkok').to_datetime_string()
    
    embed = DiscordEmbed(title = "Dag Run Error", color = DiscordNotify.embeded_red)
    embed.add_embed_field(name = "Dag id",value = dag_id)
    embed.add_embed_field(name = "Task id", value = task_id)
    embed.add_embed_field(name = "เวลารัน", value = execution_time,inline = False)
    embed.add_embed_field(name = "เวลารันที่รันสำเร็จครั้งล่าสุด", value = prev_success_time if prev_success_time is not None else 'ไม่มี', inline = False)

    wh.send_embeded(embed= embed)

    exception = str(dict(context).get('exception'))
    wh.send_text_attachment(text= exception)