import discord
import json
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from random import choice

class TOS(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name = "服務條款", description = "告訴你北極企鵝的服務條款")
    async def TOS(self, interaction: discord.Interaction):
        embed = discord.Embed(title="服務條款 Terms Of Service",
                      description="北極企鵝#6356(以下簡稱本程式) 係依據本服務條款提供各項服務於Discord(下列簡稱該平台)。當您開始使用本程式時，即表示您已閱讀、詳細了解及同意本程式提供之所有服務內容及服務條款。若您不同意，請立即停止使用本程式。此外，當使用特定功能時，您必須遵守本程式之另行公告之條款或相關規定，請您隨時注意條款的修改或變更。若您於修改或變更後繼續使用本程式及代表您已閱讀及了解條款修改或變更。",
                      colour=0x187cc9,
                      timestamp=datetime.now())

        embed.set_author(name="-# 最後更新日期: 2024/11/10")
        
        embed.add_field(name="# 一. 平台基本服務條款:",
                        value="> 1. 請您遵守 [該平台之使用條款](https://discord.com/terms) 。",
                        inline=False)
        embed.add_field(name="# 二. 使用本程式時:",
                        value="> 1. 使用本程式之任何上傳、儲存、分享、圖片於該平台之行為，您同意會遵守該平台之使用條款，且遵守法律規範。\n> 2. 您同意不會透過本服務發布任何有關: 任何暗示或明確攻擊本程式開發者的內容、動物虐待、情色內容、違反第三方權利、性暗示、仇恨歧視、剝削未成年、暴力非法行為、欺詐賭博及違法或違反該平台之使用條款內容。\n> 3. 若因發佈上述內容而造成後續法律效應、伺服器懲處、平台懲處等處分責任皆屬於您，所發布內容皆與本程式無關且不代表本程式立場。\n> 4. 我們保留追溯所有群組活動、個人操作等紀錄權力，若您不希望被追蹤請立即停止使用本程式，及關閉該平台提供之權限。",
                        inline=False)
        embed.add_field(name="# 三. 公平使用:",
                        value="> 1. 使用本程式之功能時，嚴禁任何連點器、腳本、外掛等第三方程式、或可造成本程式不穩定或破壞的功能。我們保留追溯違反本條款行為之權力及終止您使用本程式。",
                        inline=False)
        embed.add_field(name="# 四. 行為預期:",
                        value="> 1 . 使用本程式時，我們預期您已閱讀並詳細了解如何使用本程式之所有功能，請勿違反該程式制定之使用方式。若因您的行為造成本程式之不可逆損害，我們將保留追溯賠償之權利，若您不同意此運作方式請您立即停止使用。\n> 2. 使用本程式時，我們預期您與其他使用者會有友善及安全之互動，可以理性競爭，但不可不尊重其他使用者或任何辱罵之行為，若違反該使用者有權向我們調取相關資料進行提告。\n> 3. 若其他使用者違反條款，對您造成不當影響，您可至[我們的官方支援伺服器]( https://discord.gg/nt7XCkFav9) 向我們檢舉，我們會幫助您並提供您相關協助，但需要您提供相關資訊給我們。",
                        inline=False)
        embed.add_field(name="# 五. 隱私權條款:",
                        value="> 1.使用本程式即代表您已同意我們的 [隱私權條款]( https://sites.google.com/view/btbot-privacy-policy/) ，若不同意請您立即停止使用本程式",
                        inline=False)
        embed.add_field(name="# 六. 條款更新:",
                        value="> 1.任何條款修正更新會因需求而隨時更新，更新後條款皆會通知於[我們的官方支援伺服器]( https://discord.gg/nt7XCkFav9/ )及程式中的”/服務條款”功能，請隨時查看。",
                        inline=False)
        
        with open("config.json", "r", encoding='utf-8') as CONFIG:
            FILE = json.load(CONFIG)
        footer = FILE["ArcticPenguin"]["embed_footer_text"]
        avatar = FILE["ArcticPenguin"]["avatar"]

        embed.set_footer(text=footer,icon_url=avatar)

        await interaction.response.send_message(embed = embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(TOS(bot))
