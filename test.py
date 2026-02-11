from notify.discord import DiscordNotify
from discord_webhook import DiscordEmbed

webhook = "https://discord.com/api/webhooks/1470630646845014016/DxCWAj1JA0wOLcAwgZL8vpfc02Ba_QsV3AkuN_Duw5yX1OumUPVg7HXwvJ_YlTj5njOl" 
wh = DiscordNotify(webhook= webhook,username= "Dag Run Error")

# embed = DiscordEmbed(title = "Dag run error.",color = DiscordNotify.embeded_red)
# embed.set_timestamp()
# embed.add_embed_field(name = "Dag id",value= 'test')
# embed.add_embed_field(name = "Task id",value= 'test')
# embed.add_embed_field(name = "detail",value= 'test')


# wh.send_embeded(embed = embed)

text = 'this is text'

import io 

f = io.StringIO(text)
wh.send_text_attachment(text=text)