import discord
import re
import io
import json
from discord.ext import commands
from random import choice

with open("config.json","r") as CONFIG:
    Config = json.load(CONFIG)
colors = Config["color"]

def reload():
    with open("config.json", "r", encoding='utf-8') as CONFIG:
        return json.load(CONFIG)

class Link_Reply(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message):
        with open("jsons/setting/Guild_setting.json","r", encoding='utf-8') as SETTINGS:
            setting = json.load(SETTINGS)
        Check = setting[str(message.guild.id)]["Setting"]["Link_Reply"]
        
        if Check:
            match = re.match(r'^https://discord\.com/channels/(\d+)/(\d+)/(\d+)$', message.content)
            if match:
                guild_id, channel_id, message_id = map(int, match.groups())

                channel = self.bot.get_channel(channel_id)
                if channel is None:
                    return

                mentioned = await channel.fetch_message(message_id)
                reply_content = f"{mentioned.author.mention} {discord.utils.format_dt(mentioned.created_at, 'F')}, 在 {mentioned.channel.mention}, 在 {mentioned.guild.name}"

                files = []
                has_video = False
                image_file = None

                for attachment in mentioned.attachments:
                    file_data = await attachment.read()
                    file = discord.File(io.BytesIO(file_data), filename=attachment.filename)

                    if attachment.filename.lower().endswith(('.mp4', '.mov', '.avi', '.webm')):
                        has_video = True
                        files.append(file)
                    elif not image_file and attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                        image_file = file
                    else:
                        files.append(file)

                if has_video:
                    full_content = f"{reply_content}\n\n{mentioned.content}" if mentioned.content else reply_content
                    await message.reply(
                        content=full_content,
                        files=files,
                        allowed_mentions=discord.AllowedMentions.none(),
                        silent=True
                    )
                else:
                    embeds = []
                    
                    if mentioned.author.color == discord.Color.default():  # 檢查是否為預設顏色
                        COLOR = choice(colors)  # 如果是預設顏色，則隨機選擇顏色
                    else:
                        COLOR = mentioned.author.color

                    FILE = reload()
                    footer = FILE["ArcticPenguin"]["embed_footer_text"]
                    footer = FILE["ArcticPenguin"]["avatar"]
                    if mentioned.content or not mentioned.embeds:
                        main_embed = discord.Embed(
                            description=mentioned.content if mentioned.content else "",
                            color=COLOR,
                            timestamp=mentioned.created_at
                        )
                        main_embed.set_author(name=mentioned.author.name, icon_url=mentioned.author.display_avatar.url)
                        main_embed.set_footer(text=footer, icon_url=footer)
                        if image_file:
                            files.append(image_file)
                            main_embed.set_image(url=f"attachment://{image_file.filename}")
                        embeds.append(main_embed)
                    embeds.extend(mentioned.embeds)

                    await message.reply(
                        content=reply_content,
                        embeds=embeds,
                        files=files,
                        allowed_mentions=discord.AllowedMentions.none(),
                        silent=True
                    )
            await self.bot.process_commands(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Link_Reply(bot))