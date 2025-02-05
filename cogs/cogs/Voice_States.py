import discord
import datetime
import discord.voice_state
import json
from discord.ext import commands

def reload():
    with open("config.json", "r", encoding='utf-8') as CONFIG:
        return json.load(CONFIG)

class VoiceStateTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
     
    def create_base_embed(self, title: str, color: discord.Color, member: discord.Member, channel: discord.VoiceChannel) -> discord.Embed:
        timestamp = int(datetime.datetime.now().timestamp())
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        
        embed = discord.Embed(title=title, color=color)
        embed.add_field(
            name='',
            value=(
                f'時間：<t:{timestamp}:d> <t:{timestamp}:T> <t:{timestamp}:R>\n'
                f'用戶：{member.mention} ({member.name})\n'
                f'頻道：{channel.mention}'
            ),
            inline=False
        )
        embed.set_thumbnail(url=avatar_url)

        FILE = reload()
        footer = FILE["ArcticPenguin"]["embed_footer_text"]
        avatar = FILE["ArcticPenguin"]["avatar"]

        embed.set_footer(text=footer,icon_url=avatar)
        return embed

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        with open("jsons/setting/Guild_setting.json",'r', encoding='utf-8') as SETTINGS:
            setting = json.load(SETTINGS)
        guild_id = member.guild.id
        Check = setting[str(guild_id)]["Setting"]["Voice_States"]

        if Check:
            if before.channel != after.channel:
                if not before.channel and after.channel:
                    embed = self.create_base_embed(
                        "> :inbox_tray: 加入語音頻道",
                        discord.Color.green(),
                        member,
                        after.channel
                    )
                    await after.channel.send(embed=embed)

                elif before.channel and not after.channel:
                    embed = self.create_base_embed(
                        "> :outbox_tray: 離開語音頻道",
                        discord.Color.red(),
                        member,
                        before.channel
                    )
                    await before.channel.send(embed=embed)

                elif before.channel and after.channel:
                    embed = self.create_base_embed(
                        "> :outbox_tray: 切換語音頻道 :inbox_tray:",
                        discord.Color.blue(),
                        member,
                        after.channel
                    )
                    embed.add_field(
                        name='',
                        value=f'來自：{before.channel.mention}',
                        inline=False
                    )
                    await before.channel.send(embed=embed)
                    await after.channel.send(embed=embed)

            current_channel = after.channel
            if not current_channel:
                return

async def setup(bot):
    await bot.add_cog(VoiceStateTracker(bot))