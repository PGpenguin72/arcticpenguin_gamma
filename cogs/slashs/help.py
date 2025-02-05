import discord
import json
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from random import choice
from discord.app_commands import Choice
from typing import Optional

def reload():
    with open("config.json", "r", encoding='utf-8') as CONFIG:
        return json.load(CONFIG)

class Role_select(discord.ui.Select):
    def __init__(self):
            options = [
                discord.SelectOption(label="普通用戶", description="北極企鵝在任何地方的功能", value="normal",emoji="👤"),
                discord.SelectOption(label="伺服器管理者", description="北極企鵝在伺服器的功能", value="admin",emoji="👑"),
                discord.SelectOption(label="開發人員", description="北極企鵝開發者專用的功能", value="developer",emoji="🔧")
            ]
            super().__init__(placeholder="請選擇身分", min_values=1, max_values=1, options=options, custom_id="role_select")

    async def callback(self, interaction: discord.Interaction):
        class command_seclect_normal(discord.ui.Select):
            def __init__(self):
                    options = [
                        discord.SelectOption(label="/更新公告", description="告訴你北極企鵝最近更新了個啥", value="update",emoji="📢"),
                        discord.SelectOption(label="/服務條款", description="告訴你北極企鵝的服務條款", value="TOS",emoji="📃"),
                        discord.SelectOption(label="/數數字", description="點此開始數數字吧(從一開始)", value="count",emoji="🔢"),
                        discord.SelectOption(label="/幫助", description="教你如何使用北極企鵝", value="help",emoji="🤝")
                    ]
                    super().__init__(placeholder="選擇指令", min_values=1, max_values=1, options=options)

            async def callback(self, interaction: discord.Interaction):
                FILE = reload()
                footer = FILE["ArcticPenguin"]["embed_footer_text"]
                avatar = FILE["ArcticPenguin"]["avatar"]
                colors = FILE["color"]
                if self.values[0] == "update":
                    embed = discord.Embed(title="</更新公告:1336297728757465098>",
                    description="告訴你北極企鵝最近更新了個啥",
                    colour=choice(colors),
                    timestamp=datetime.now())
                    embed.add_field(name="功能特色",
                                    value="1. 隨時隨地查看北極企鵝的更新狀態",
                                    inline=False)                    
                    embed.add_field(name="使用方法",
                                    value="1. 發出最新的更新公告 \n```/更新公告```",
                                    inline=False)
                    embed.add_field(name="格式",
                                    value="``<>``是一定要填的參數``[]``是選填的參數\n```/更新公告```",
                                    inline=False)
                    embed.set_footer(text=footer, icon_url=avatar) 
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                elif self.values[0] == "TOS":
                    embed = discord.Embed(title="</服務條款:1335878896972730460>",
                    description="告訴你北極企鵝的服務條款",
                    colour=choice(colors),
                    timestamp=datetime.now())
                    embed.add_field(name="功能特色",
                                    value="1. 隨時隨地查看北極企鵝的服務條款",
                                    inline=False)                 
                    embed.add_field(name="使用方法",
                                    value="1. 發出服務條款 \n```/服務條款```",
                                    inline=False)
                    embed.add_field(name="格式",
                                    value="``<>``是一定要填的參數``[]``是選填的參數\n```/服務條款```",
                                    inline=False)
                    embed.set_footer(text=footer, icon_url=avatar) 
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                elif self.values[0] == "count":
                    embed = discord.Embed(title="</數數字:1336367496072003714>",
                    description="點此開始數數字吧(從一開始)",
                    colour=choice(colors),
                    timestamp=datetime.now())
                    embed.add_field(name="功能特色",
                                    value="1. 和朋友一起數數字，從一數到錯誤為止!\n2. 若同一用戶連續發送兩次連續數字，將視為失誤。\n3. 當你超過了全北極最高紀錄後，會多一個拉炮表情符號。",
                                    inline=False)                 
                    embed.add_field(name="使用方法",
                                    value="1. 開始數數字 \n```/數數字```",
                                    inline=False)
                    embed.add_field(name="格式",
                                    value="``<>``是一定要填的參數``[]``是選填的參數\n```/數數字```",
                                    inline=False)
                    embed.set_footer(text=footer, icon_url=avatar) 
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                elif self.values[0] == "help":
                    embed = discord.Embed(title="</幫助:1336305593249431715>",
                    description="教你如何使用北極企鵝",
                    colour=choice(colors),
                    timestamp=datetime.now())
                    embed.add_field(name="功能特色",
                                    value="1. 教你如何使用北極企鵝\n2. 有身分選擇，讓你知道你可以用什麼功能。\n3. 如同維基百科般寫的超級詳盡:D",
                                    inline=False)                 
                    embed.add_field(name="使用方法",
                                    value="1. 發出幫助教學選單 \n```/幫助```",
                                    inline=False)
                    embed.add_field(name="格式",
                                    value="``<>``是一定要填的參數``[]``是選填的參數\n```/幫助```",
                                    inline=False)
                    embed.set_footer(text=footer, icon_url=avatar) 
                    await interaction.response.send_message(embed=embed, ephemeral=True)
        
        class command_seclect_admin(discord.ui.Select):
            def __init__(self):
                    options = [
                        discord.SelectOption(label="/伺服器設定", description="設定北極企鵝的一些伺服器功能", value="Guild_setting",emoji="⚙️"),
                        discord.SelectOption(label="/設定歡迎消息 ", description="當用戶一加入伺服器就會發送的歡迎訊息。", value="Create_Welcome_Message",emoji="💬")
                    ]
                    super().__init__(placeholder="選擇指令", min_values=1, max_values=1, options=options)

            async def callback(self, interaction: discord.Interaction):
                FILE = reload()
                footer = FILE["ArcticPenguin"]["embed_footer_text"]
                avatar = FILE["ArcticPenguin"]["avatar"]
                colors = FILE["color"]
                if self.values[0] == "Guild_setting":
                    embed = discord.Embed(title="</伺服器設定:1335891562873225217>",
                    description="設定北極企鵝的一些伺服器功能",
                    colour=choice(colors),
                    timestamp=datetime.now())
                    embed.add_field(name="功能特色",
                                    value="1. 自由設定北極企鵝在你伺服器的功能。\n2. ``DC鏈結自動回覆Embed``為當你發送了一個Discord訊息鏈結，北極企鵝會自動回覆你訊息的內容。\n3. ``語音頻道紀錄器``為當有人加入離開或切換語音頻道時，北極企鵝會自動發送一條訊息到語音頻道中的文字頻道。",
                                    inline=False)                 
                    embed.add_field(name="使用方法",
                                    value="1. 開啟DC鏈結自動回覆Embed \n```/伺服器設定 DC鏈結自動回覆Embed 啟用```\n2. 關閉語音頻道紀錄器 \n```/伺服器設定 語音頻道紀錄器 停用\n3. 關閉歡迎消息 \n```/伺服器設定 歡迎消息 停用",
                                    inline=False)
                    embed.add_field(name="格式",
                                    value="``<>``是一定要填的參數``[]``是選填的參數\n```/伺服器設定 <選項> <狀態>```",
                                    inline=False)
                    embed.set_footer(text=footer, icon_url=avatar) 
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                elif self.values[0] == "Create_Welcome_Message":
                    embed = discord.Embed(title="</設定歡迎消息:1336554637469286410>",
                    description="當用戶一加入伺服器就會發送的歡迎訊息。",
                    colour=choice(colors),
                    timestamp=datetime.now())
                    embed.add_field(name="功能特色",
                                    value="1. 當有新用戶加入會自對發送出歡迎消息\n2. 表單的設定方式簡易明瞭\n3. {count}為伺服器人數, {user}為用戶名稱, {guild}為伺服器名稱。",
                                    inline=False)                 
                    embed.add_field(name="使用方法",
                                    value="1. 開始設定加入伺服器的歡迎消息 \n```/設定歡迎消息 ```",
                                    inline=False)
                    embed.add_field(name="格式",
                                    value="``<>``是一定要填的參數``[]``是選填的參數\n```/設定歡迎消息 ```",
                                    inline=False)
                    embed.set_footer(text=footer, icon_url=avatar) 
                    await interaction.response.send_message(embed=embed, ephemeral=True)
        
        class command_seclect_developer(discord.ui.Select):
            def __init__(self):
                    options = [
                        discord.SelectOption(label="/開發者選項", description="北極企鵝的開發者專用的功能", value="bot",emoji="⚙️")
                    ]
                    super().__init__(placeholder="選擇指令", min_values=1, max_values=1, options=options)

            async def callback(self, interaction: discord.Interaction):
                FILE = reload()
                footer = FILE["ArcticPenguin"]["embed_footer_text"]
                avatar = FILE["ArcticPenguin"]["avatar"]
                colors = FILE["color"]
                if self.values[0] == "bot":
                    embed = discord.Embed(title="</開發者選項:1336018163527192716>",
                    description="北極企鵝的開發者專用的功能",
                    colour=choice(colors),
                    timestamp=datetime.now())
                    embed.add_field(name="功能特色",
                                    value="1. 隨時隨地控制北極企鵝，讓你享受掌控機器的感覺:D",
                                    inline=False)                 
                    embed.add_field(name="使用方法",
                                    value="1. 重新啟動北極企鵝 \n```/開發者選項 重新啟動```\n2. 把北極企鵝關機\n```/開發者選項 關機```\n3. 更改北極企鵝的狀態\n```/開發者選項 關機```\n4. 重新載入all all all模組\n```/開發者選項 重新載入模組 全部Cog 全部Event 全部Slash```\n5. 取消載入加入建檔器\n```/開發者選項 取消載入模組 加入建檔器```\n6. 載入all none none模組\n```/開發者選項 全部Cog```\n7. 讓北極企鵝說一些話\n```/開發者選項 讓北極企鵝說```\n8. 讓北極企鵝發送自訂Embed \n```/開發者選項 讓北極企鵝發送Embed```\n9. 更新數數字的資料庫\n```/開發者選項 數數字資料更新```",
                                    inline=False)
                    embed.add_field(name="格式",
                                    value="``<>``是一定要填的參數``[]``是選填的參數\n```/開發者選項 <動作> [選擇更新的cog模組] [選擇更新的event模組] [選擇更新的slash模組]```",
                                    inline=False)
                    embed.set_footer(text=footer, icon_url=avatar) 
                    await interaction.response.send_message(embed=embed, ephemeral=True)
        FILE = reload()
        colors = FILE["color"]
        if self.values[0] == "normal":
            embed = discord.Embed(title="普通用戶",
                      colour=choice(colors),
                      timestamp=datetime.now())
            view_normal = discord.ui.View()
            view_normal.add_item(command_seclect_normal())
            message = await interaction.response.send_message(embed=embed, view=view_normal, ephemeral=True)
            original_message = await interaction.channel.fetch_message(interaction.channel.last_message_id)
            view_normal.message = original_message
        elif self.values[0] == "admin":
            embed = discord.Embed(title="伺服器管理者",
                      colour=choice(colors),
                      timestamp=datetime.now())
            view_admin = discord.ui.View()
            view_admin.add_item(command_seclect_admin())
            message = await interaction.response.send_message(embed=embed, view=view_admin, ephemeral=True)
            original_message = await interaction.channel.fetch_message(interaction.channel.last_message_id)
            view_admin.message = original_message 
        elif self.values[0] == "developer":
            embed = discord.Embed(title="開發人員",
                      colour=choice(colors),
                      timestamp=datetime.now())
            view_developer = discord.ui.View()
            view_developer.add_item(command_seclect_developer())
            message = await interaction.response.send_message(embed=embed, view=view_developer, ephemeral=True)
            original_message = await interaction.channel.fetch_message(interaction.channel.last_message_id)
            view_developer.message = original_message
        
class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Role_select())


class help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="幫助", description="教你如何使用北極企鵝")
    async def help(self, interaction: discord.Interaction):

        FILE = reload()
        footer = FILE["ArcticPenguin"]["embed_footer_text"]
        avatar = FILE["ArcticPenguin"]["avatar"]
        colors = FILE["color"]

        embed = discord.Embed(
            title="歡迎使用北極企鵝的幫助系統!",
            description="北極企鵝是一隻由PG企鵝及北極貓開發的機器人喔~",
            colour=choice(colors),
            timestamp=datetime.now()
            )
        embed.add_field(
            name="如何使用幫助呢?",
            value="請你點選下面的'選擇身分'來選擇你的身分，就可以開始選擇功能了喔!",
            inline=False
            )
        embed.set_footer(text=footer,icon_url=avatar)
        view = PersistentView()
        message = await interaction.response.send_message(embed=embed, view=view)
        original_message = await interaction.channel.fetch_message(interaction.channel.last_message_id)
        view.message = original_message

async def setup(bot: commands.Bot):
    await bot.add_cog(help(bot))  
    bot.add_view(PersistentView())