import discord
import json
from discord.ext import commands

async def reload():
    with open("jsons/setting/Guild_Setting.json", "r", encoding="utf-8") as CONFIG_FILE:
        return json.load(CONFIG_FILE)

async def save_config(data):
    with open("jsons/setting/Guild_Setting.json", "w", encoding="utf-8") as CONFIG_FILE:
        json.dump(data, CONFIG_FILE, indent=4, ensure_ascii=False)

class Join_Guild(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        data = await reload()

        channel = guild.system_channel or next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).create_instant_invite), None)
        invite = await channel.create_invite(max_age=0, max_uses=0, unique=False) if channel else None

        data[str(guild.id)] = {
                    "Guild_name" : guild.name,
                    "Guild_Link": invite.url if invite else "無可用邀請",
                    "Setting" : {
                        "Link_Reply" : False,
                        "Voice_States": False,
                        "Welcome_Message": False
                    }
        }
        await save_config(data)
async def setup(bot: commands.Bot):
    await bot.add_cog(Join_Guild(bot))