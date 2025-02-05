import discord
import json
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from random import choice

def reload():
    with open("config.json", "r", encoding='utf-8') as CONFIG:
        return json.load(CONFIG)

class update(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    FILE = reload()
    var = {FILE["ArcticPenguin"]["var"]}

    @app_commands.command(name = "更新公告", description = f"告訴你北極企鵝最近更新了個啥")
    async def update(self, interaction: discord.Interaction):
        FILE = reload()
        var = {FILE["ArcticPenguin"]["var"]}
        footer = FILE["ArcticPenguin"]["embed_footer_text"]
        avatar = FILE["ArcticPenguin"]["avatar"]

        embed = discord.Embed(title=f"北極企鵝版本{var}",
                              description="新增以下功能:",
                              colour=0x07dfd0,
                              timestamp=datetime.now())

        embed.set_author(name="###北極企鵝更新公告###")

        embed.add_field(name="</伺服器設定:1335891562873225217> <選項> <狀態>", value="設定北極企鵝的一些伺服器功能", inline=False)
        embed.add_field(name="</更新公告:1336297728757465098>", value="發送北極企鵝的更新公告。", inline=False)
        embed.add_field(name="</服務條款:1335878896972730460>", value="發送一則北極企鵝服務條款。", inline=False)
        embed.add_field(name="</開發者選項:1336018163527192716><動作>[選擇更新的cog模組][選擇更新的event模組][選擇更新的slash模組]", value="只有北極企鵝的開發者才能使用的功能。", inline=False)
        embed.add_field(name="</數數字:1336367496072003714>", value="點此開始數數字吧(從一開始)", inline=False)

        embed.set_footer(text=footer, icon_url=avatar) 
        await interaction.response.send_message(embed = embed)

async def setup(bot: commands.Bot):

    await bot.add_cog(update(bot))
