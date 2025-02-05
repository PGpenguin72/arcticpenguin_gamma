import discord
import json
from discord.ext import commands
from datetime import datetime
from random import choice

def reload():
    with open("config.json", "r", encoding='utf-8') as CONFIG:
        return json.load(CONFIG)
def setting():
    with open("jsons/setting/Guild_setting.json", "r", encoding='utf-8') as CONFIG:
        return json.load(CONFIG)
    
FILE = reload()
colors = FILE["color"]
footer = FILE["ArcticPenguin"]["embed_footer_text"]
avatar = FILE["ArcticPenguin"]["avatar"]

class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def format_welcome_message(self, member, DATA):
        count = member.guild.member_count
        guild = member.guild.name
        user = member.display_name
        title = DATA["Title"].replace("{user}", user)
        author_name = DATA["Author"]["Name"]
        author_name = author_name.replace("{guild}", guild)
        author_name = author_name.replace("{count}", str(count))
        
        return title, author_name

    async def send_welcome_embed(self, channel, member, Message, title, author_name):
        embed = discord.Embed(
            title=title,
            description=Message["Description"],
            colour=choice(colors),
            timestamp=datetime.now()
        )

        embed.set_author(name=author_name, icon_url = member.guild.icon)

        if Message.get("Images"):
            embed.set_image(url=Message["Images"])
            
        embed.set_thumbnail(url=member.display_avatar)
        embed.set_footer(text=footer, icon_url=avatar)

        await channel.send(f"<@{member.id}>",embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        CONFIG = setting()
        if CONFIG[member.guild.id]["Setting"]["Welcome_Message"]:
            guild_id = str(member.guild.id)
            with open('./jsons/command/welcome.json', 'r', encoding='utf-8') as JSON_welcome:
                data = json.load(JSON_welcome)
            if guild_id not in data:
                return

            group = data[guild_id]
            Message = group["Message"]

            channel_id = int(group["Channel"])
            channel = self.bot.get_channel(channel_id)

            if not channel:
                return

            title, author_name = self.format_welcome_message(member, Message)

            await self.send_welcome_embed(channel, member, Message, title, author_name)

async def setup(bot: commands.Bot):
    await bot.add_cog(Welcome(bot))