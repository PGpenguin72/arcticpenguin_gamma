import discord
import json
import asyncio
import os
import json
import subprocess
import sys
from typing import Optional
from discord.app_commands import Choice
from discord import app_commands
from datetime import datetime
from discord.ext import commands

def reload():
    with open("config.json", "r", encoding='utf-8') as CONFIG:
        return json.load(CONFIG)
    
def save_count(data):
    with open("jsons/command/count.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
def reload_count():
    with open("jsons/command/count.json", "r", encoding='utf-8') as COUNT:
        return json.load(COUNT)

with open('keys.json',"r", encoding='utf-8')as KEY_FILE:
    KEYS = json.load(KEY_FILE)

discord_key = KEYS["discord_bot"]
FILE = reload()
id = FILE["ArcticPenguin"]["id"]
intents = discord.Intents.all()
activity = discord.Game(name="正在開發北極企鵝中:D")
bot = commands.Bot(command_prefix = f"<@{id}> ", intents = intents,activity = activity, status=discord.Status.online)

class StatusModal(discord.ui.Modal, title="更改北極企鵝的狀態"):
    狀態 = discord.ui.TextInput(
        label="請輸入北極企鵝狀態",
        placeholder="online, idle, dnd, invisible",
        required=True,
    )
    活動類型 = discord.ui.TextInput(
        label="請輸入活動類型",
        placeholder="playing, watching, listening, streaming",
        required=True
    )   
    活動內容 = discord.ui.TextInput(
        label="活動內容",
        placeholder="輸入活動名稱，例如 'Minecraft'",
        required=True,
    )
    活動鏈結 = discord.ui.TextInput(
        label="活動鏈結(僅在streaming模式有效)",
        default="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        required=False,
    )

    async def on_submit(self, interaction: discord.Interaction):
        status_mapping = {
            "online": discord.Status.online,
            "idle": discord.Status.idle,
            "dnd": discord.Status.dnd,
            "invisible": discord.Status.invisible,
        }

        status = status_mapping.get(self.狀態.value.lower())
        if not status:
            await interaction.response.send_message("無效的狀態類型，請輸入 online, idle, dnd 或 invisible。", ephemeral=True)
            return

        activity = None
        if self.活動類型.value.lower() == "playing":
            activity = discord.Game(name=self.活動內容.value)
        elif self.活動類型.value.lower() == "watching":
            activity = discord.Activity(type=discord.ActivityType.watching, name=self.活動內容.value)
        elif self.活動類型.value.lower() == "listening":
            activity = discord.Activity(type=discord.ActivityType.listening, name=self.活動內容.value)
        elif self.活動類型.value.lower() == "streaming":
            activity = discord.Streaming(name=self.活動內容.value, url=self.活動鏈結.value)
        else:
            await interaction.response.send_message("無效的活動類型，請輸入 playing, watching, listening 或 streaming。", ephemeral=True)
            return

        FILE = reload()
        footer = FILE["ArcticPenguin"]["embed_footer_text"]
        avatar = FILE["ArcticPenguin"]["avatar"]
        await bot.change_presence(status=status, activity=activity)

        embed = discord.Embed(
            title="北極企鵝狀態已更新",
            description=f"**狀態:** {self.狀態.value}\n**活動:** {self.活動類型.value} - {self.活動內容.value}",
            colour=0x00ff00,
            timestamp=datetime.now()
        )
        embed.set_footer(text=footer,icon_url=avatar) 
        await interaction.response.send_message(embed=embed)
        channel_id = FILE["ArcticPenguin"]["record_channel"]
        channel = bot.get_channel(channel_id)
        await channel.send(embed=embed)

class Say(discord.ui.Modal, title="讓北極企鵝說"):
    內容 = discord.ui.TextInput(
        label="請輸入要讓北極企鵝說的內容",
        placeholder="",
        style= discord.TextStyle.long,
        required=True,
    )
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(self.內容.value, ephemeral=True)
        await interaction.channel.send(self.內容.value)
        FILE = reload()
        footer = FILE["ArcticPenguin"]["embed_footer_text"]
        avatar = FILE["ArcticPenguin"]["avatar"]
        embed = discord.Embed(
            title=f"北極企鵝發送了一則訊息",
            description=self.內容.value,
            colour=0x00b0f4,
            timestamp=datetime.now()
        )
        embed.add_field(name="發送者:", value=f"<@{interaction.user.id}>")
        embed.add_field(name="發送位置:", value=f"<#{interaction.channel.id}>")
        embed.set_footer(text=footer,icon_url=avatar)
        channel_id = FILE["ArcticPenguin"]["record_channel"]
        channel = bot.get_channel(channel_id)
        await channel.send(embed=embed)

class Embed(discord.ui.Modal, title="讓北極企鵝發送Embed"):
    顏色 = discord.ui.TextInput(
        label="請輸入16進制顏色號",
        default="0x00b0f4",
        style= discord.TextStyle.short
    )
    作者名稱 = discord.ui.TextInput(
        label="請輸入要顯示的作者名稱",
        placeholder="",
        style= discord.TextStyle.short,
        required= False
    )
    標題 = discord.ui.TextInput(
        label="請輸入標題",
        placeholder="",
        style= discord.TextStyle.short
    )
    內容 = discord.ui.TextInput(
        label="請輸入內容",
        placeholder="",
        style= discord.TextStyle.paragraph
    )
    圖片 = discord.ui.TextInput(
        label="請輸入圖片網址",
        placeholder="",
        style= discord.TextStyle.short,
        required= False
    )

    async def on_submit(self, interaction: discord.Interaction):
        FILE = reload()
        footer = FILE["ArcticPenguin"]["embed_footer_text"]
        avatar = FILE["ArcticPenguin"]["avatar"]
        embed = discord.Embed(title=self.標題.value,
                      description=self.內容.value,
                      colour=int(self.顏色.value, 16),
                      timestamp=datetime.now())
        if not self.作者名稱.value:
            pass
        else:
            embed.set_author(name=self.作者名稱.value)
        if not self.圖片.value:
            pass
        else:
            embed.set_image(url=self.圖片.value)
        embed.set_footer(text=footer,icon_url=avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.channel.send(embed=embed)
        FILE = reload()
        embed.add_field(name="發送者:", value=f"<@{interaction.user.id}>")
        embed.add_field(name="發送位置:", value=f"<#{interaction.channel.id}>")
        channel_id = FILE["ArcticPenguin"]["record_channel"]
        channel = bot.get_channel(channel_id)
        await channel.send("# 北極企鵝發送了一則Embed訊息")
        await channel.send(embed=embed)

class Count(discord.ui.Modal, title="數數字功能的後台"):
    def __init__(self):
        FILE = reload_count()
        Higher = str(FILE["The_Higher_Score"])
        
        super().__init__()
        
        self.最高紀錄.default = Higher 
    FILE = reload_count()
    Higher = str(FILE["The_Higher_Score"])
    最高紀錄 = discord.ui.TextInput(
        label="更改最高的數字",
        default=Higher,
        style=discord.TextStyle.short,
        required=False
    )
    頻道 = discord.ui.TextInput(
        label="更改數數字頻道的頻道 ID",
        default="",
        style=discord.TextStyle.short,
        required=False
    )
    數字 = discord.ui.TextInput(
        label="更改數數字頻道該數的數字",
        default="",
        style=discord.TextStyle.short,
        required=False
    )
    用戶 = discord.ui.TextInput(
        label="更改數數字頻道上個數數字用戶",
        default="",
        style=discord.TextStyle.short,
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction):
        FILE = reload_count()
        Higher = str(FILE["The_Higher_Score"])

        FILE_2 = reload()
        footer = FILE_2["ArcticPenguin"]["embed_footer_text"]
        avatar = FILE_2["ArcticPenguin"]["avatar"]

        embed = discord.Embed(
            title="數數字記錄更改",
            colour=0x00b0f4,
            timestamp=datetime.now()
        )
        embed.add_field(name="操作者:", value=f"<@{interaction.user.id}>", inline=False)
        embed.add_field(name="操作內容:", value="(若有操作下方會顯示)", inline=False)

        if self.最高紀錄.value and self.最高紀錄.value.isdigit():
            new_high_score = int(self.最高紀錄.value)
            if new_high_score != int(Higher):
                embed.add_field(name="最高數字", value=f"原為 {Higher}, 現為 {new_high_score}")
                FILE["The_Higher_Score"] = new_high_score
                save_count(FILE)

        if self.頻道.value:
            embed.add_field(name="變動的頻道:", value=f"<#{self.頻道.value}>")
            channel_id = str(self.頻道.value)
            if channel_id in FILE:
                if self.數字.value and self.數字.value.isdigit():
                    new_count = int(self.數字.value)
                    embed.add_field(name="目前該數之數", value=f"更變為 {new_count}")
                    FILE[channel_id]["count_num"] = new_count
                if self.用戶.value:
                    embed.add_field(name="上個數數用戶", value=f"更變為 {self.用戶.value}")
                    FILE[channel_id]["last_counter"] = self.用戶.value
                save_count(FILE)
        
        embed.set_footer(text=footer, icon_url=avatar)
        await interaction.response.send_message(embed=embed)

        record_channel_id = FILE_2["ArcticPenguin"]["record_channel"]
        channel = interaction.client.get_channel(record_channel_id)
        if channel:
            await channel.send(embed=embed)

@bot.tree.command(name = "開發者選項", description = "北極企鵝的開發者專用的功能")
@app_commands.describe(動作 = "請選擇你要執行的動作",
                        選擇更新的cog模組 = "(你可以選擇你要更新的Cog。)",
                        選擇更新的event模組 = "(你可以選擇你要更新的Event。)",
                        選擇更新的slash模組 = "(你可以選擇你要更新的Slash。)"
                    )
@app_commands.choices(動作=[
        Choice(name="重新啟動", value="restart"),
        Choice(name="關機", value="stop"),
        Choice(name="更改北極企鵝狀態", value="status"),
        Choice(name="重新載入模組", value="reload"),
        Choice(name="取消載入模組", value="unload"),
        Choice(name="載入模組", value="load"),
        Choice(name="讓北極企鵝說", value="say"),
        Choice(name="讓北極企鵝發送Embed", value="embed"),
        Choice(name="數數字資料更新", value="count")
    ]
    )
@app_commands.choices(選擇更新的cog模組=[
        Choice(name="全部Cog", value="all"),
        Choice(name="加入建檔器", value="Join_Guild"),
        Choice(name="訊息自動回覆Embed", value="Link_Reply"),
        Choice(name="語音紀錄器", value="Voice_States"),
        Choice(name="歡迎消息發送器", value="Welcome_Message")
    ]
    )
@app_commands.choices(選擇更新的event模組=[
        Choice(name="全部Event", value="all")
    ]
    )
@app_commands.choices(選擇更新的slash模組=[
        Choice(name="全部Slash", value="all"),
        Choice(name="數數字", value="count"),
        Choice(name="設定歡迎消息", value="Create_Welcome_Message"),
        Choice(name="伺服器設定", value="Guild_setting"),
        Choice(name="幫助", value="help"),
        Choice(name="服務條款", value="TOS"),
        Choice(name="更新公告", value="update")
    ]
    )

async def developer(interaction: discord.Interaction,
                    動作: str,
                    選擇更新的cog模組: Optional[str],
                    選擇更新的event模組: Optional[str],
                    選擇更新的slash模組: Optional[str]
                    ):
    FILE = reload()
    Check = FILE["admin"]
    if interaction.user.id in Check:
        channel_id = FILE["ArcticPenguin"]["record_channel"]
        channel = bot.get_channel(channel_id)
        footer = FILE["ArcticPenguin"]["embed_footer_text"]
        avatar = FILE["ArcticPenguin"]["avatar"]

        if 動作 == "restart":
            embed = discord.Embed(
                title="北極企鵝重新啟動中",
                description=f"執行者: {interaction.user.global_name}",
                colour=0xd8d222,
                timestamp=datetime.now()
            )
            embed.set_footer(text=footer,icon_url=avatar)
            await interaction.response.send_message(embed=embed)
            await channel.send(embed=embed)
            os.system('cls')
            subprocess.Popen([sys.executable] + sys.argv)
            await bot.close()
            
        elif 動作 == "stop":
            embed = discord.Embed(title="北極企鵝關機中",
                    description=f"執行者: {interaction.user.global_name}",
                    timestamp=datetime.now())

            embed.set_footer(text=footer,icon_url=avatar) 
            await interaction.response.send_message(embed=embed)
            await channel.send(embed=embed)
            await bot.close()

        elif 動作 == "reload":
            reload_list = []
            unreload_list = []
            if 選擇更新的cog模組 == "all" or 選擇更新的event模組 == "all" or 選擇更新的slash模組 == "all":
                embed = discord.Embed(title="所有 模組 皆已嘗試重新讀取",
                    description=f"執行者: {interaction.user.global_name}",
                    colour=0xd8d222,
                    timestamp=datetime.now())
                embed.set_footer(text=footer,icon_url=avatar) 

                if not 選擇更新的cog模組:
                    pass
                else:
                    for filename in os.listdir("./cogs/cogs"):
                        if filename.endswith(".py"):
                            try:
                                await bot.reload_extension(f"cogs.cogs.{filename[:-3]}")
                                reload_list.append(f"cogs {filename[:-3]}")
                            except Exception as e:
                                unreload_list.append(f"cogs {filename[:-3]} \n")
                if not 選擇更新的event模組:
                    pass
                else:
                    for filename in os.listdir("./cogs/events"):
                        if filename.endswith(".py"):
                            try:
                                await bot.reload_extension(f"cogs.events.{filename[:-3]}")
                                reload_list.append(f"events {filename[:-3]}")
                            except Exception as e:
                                unreload_list.append(f"events {filename[:-3]} \n")
                if not 選擇更新的slash模組:
                    pass
                else:
                    for filename in os.listdir("./cogs/slashs"):
                        if filename.endswith(".py"):
                            try:
                                await bot.reload_extension(f"cogs.slashs.{filename[:-3]}")
                                reload_list.append(f"slashs {filename[:-3]}")
                            except Exception as e:
                                unreload_list.append(f"slashs {filename[:-3]} \n")

                embed.add_field(name="以下模組更新成功", value=reload_list, inline=False)
                embed.add_field(name="以下模組更新失敗", value=unreload_list, inline=False)
                
                await interaction.response.send_message(embed=embed)

            else:
                embed = discord.Embed(title=f"模組 {選擇更新的cog模組} {選擇更新的event模組} {選擇更新的slash模組} 已嘗試重新讀取",
                    description=f"執行者: {interaction.user.global_name}",
                    colour=0xd8d222,
                    timestamp=datetime.now())
                embed.set_footer(text=footer,icon_url=avatar) 

                if not 選擇更新的cog模組:
                    pass
                else:
                    try:
                        await bot.reload_extension(f"cogs.cogs.{選擇更新的cog模組}")
                        embed.add_field(name=f"{選擇更新的cog模組}", value=f"重新讀取成功!", inline=False)
                    except Exception as e:
                                embed.add_field(name="此Cog 重新讀取失敗: ", value=f"{e}", inline=False)
                if not 選擇更新的event模組:
                    pass
                else:
                    try:
                        await bot.reload_extension(f"cogs.events.{選擇更新的event模組}")
                        embed.add_field(name=f"{選擇更新的event模組}", value=f"重新讀取成功!", inline=False)
                    except Exception as e:
                                embed.add_field(name="此Events 重新讀取失敗: ", value=f"{e}", inline=False)
                if not 選擇更新的slash模組:
                    pass
                else:
                    try:
                        await bot.reload_extension(f"cogs.slashs.{選擇更新的slash模組}")
                        embed.add_field(name=f"{選擇更新的slash模組}", value=f"重新讀取成功!", inline=False)
                    except Exception as e:
                                embed.add_field(name="此Slash 重新讀取失敗: ", value=f"{e}", inline=False)

                await interaction.response.send_message(embed=embed)
                
            embed = discord.Embed(title=f"模組 {選擇更新的cog模組} {選擇更新的event模組} {選擇更新的slash模組} 已重新讀取",
                      description=f"執行者: {interaction.user.global_name}",
                      colour=0xd8d222,
                      timestamp=datetime.now())
            embed.set_footer(text=footer,icon_url=avatar) 
            await channel.send(embed=embed)

        elif 動作 == "load":
            load_list = []
            unload_list = []
            if 選擇更新的cog模組 == "all" or 選擇更新的event模組 == "all" or 選擇更新的slash模組 == "all":
                embed = discord.Embed(title="所有 模組 皆已嘗試讀取",
                    description=f"執行者: {interaction.user.global_name}",
                    colour=0xd8d222,
                    timestamp=datetime.now())
                embed.set_footer(text=footer,icon_url=avatar) 

                if not 選擇更新的cog模組:
                    pass
                else:
                    for filename in os.listdir("./cogs/cogs"):
                        if filename.endswith(".py"):
                            try:
                                await bot.load_extension(f"cogs.cogs.{filename[:-3]}")
                                load_list.append(f"cogs {filename[:-3]}")
                            except Exception as e:
                                unload_list.append(f"cogs {filename[:-3]} \n")
                if not 選擇更新的event模組:
                    pass
                else:
                    for filename in os.listdir("./cogs/events"):
                        if filename.endswith(".py"):
                            try:
                                await bot.load_extension(f"cogs.events.{filename[:-3]}")
                                load_list.append(f"events {filename[:-3]}")
                            except Exception as e:
                                unload_list.append(f"events {filename[:-3]} \n")
                if not 選擇更新的slash模組:
                    pass
                else:
                    for filename in os.listdir("./cogs/slashs"):
                        if filename.endswith(".py"):
                            try:
                                await bot.load_extension(f"cogs.slashs.{filename[:-3]}")
                                load_list.append(f"slashs {filename[:-3]}")
                            except Exception as e:
                                unload_list.append(f"slashs {filename[:-3]} \n")

                embed.add_field(name="以下模組讀取成功", value=load_list, inline=False)
                embed.add_field(name="以下模組讀取失敗", value=unload_list, inline=False)
                
                await interaction.response.send_message(embed=embed)

            else:
                embed = discord.Embed(title=f"模組 {選擇更新的cog模組} {選擇更新的event模組} {選擇更新的slash模組} 已嘗試讀取",
                    description=f"執行者: {interaction.user.global_name}",
                    colour=0xd8d222,
                    timestamp=datetime.now())
                embed.set_footer(text=footer,icon_url=avatar) 

                if not 選擇更新的cog模組:
                    pass
                else:
                    try:
                        await bot.load_extension(f"cogs.cogs.{選擇更新的cog模組}")
                        embed.add_field(name=f"{選擇更新的cog模組}", value=f"讀取成功!", inline=False)
                    except Exception as e:
                                embed.add_field(name="此Cog 讀取失敗: ", value=f"{e}", inline=False)
                if not 選擇更新的event模組:
                    pass
                else:
                    try:
                        await bot.load_extension(f"cogs.events.{選擇更新的event模組}")
                        embed.add_field(name=f"{選擇更新的event模組}", value=f"讀取成功!", inline=False)
                    except Exception as e:
                                embed.add_field(name="此Events 讀取失敗: ", value=f"{e}", inline=False)
                if not 選擇更新的slash模組:
                    pass
                else:
                    try:
                        await bot.load_extension(f"cogs.slashs.{選擇更新的slash模組}")
                        embed.add_field(name=f"{選擇更新的slash模組}", value=f"讀取成功!", inline=False)
                    except Exception as e:
                                embed.add_field(name="此Slash 讀取失敗: ", value=f"{e}", inline=False)

                await interaction.response.send_message(embed=embed)
                
            embed = discord.Embed(title=f"模組 {選擇更新的cog模組} {選擇更新的event模組} {選擇更新的slash模組} 已讀取",
                      description=f"執行者: {interaction.user.global_name}",
                      colour=0xd8d222,
                      timestamp=datetime.now())
            embed.set_footer(text=footer,icon_url=avatar) 
            await channel.send(embed=embed)

        elif 動作 == "unload":
            unload_list = []
            ununload_list = []
            if 選擇更新的cog模組 == "all" or 選擇更新的event模組 == "all" or 選擇更新的slash模組 == "all":
                embed = discord.Embed(title="所有 模組 皆已嘗試取消讀取",
                    description=f"執行者: {interaction.user.global_name}",
                    colour=0xd8d222,
                    timestamp=datetime.now())
                embed.set_footer(text=footer,icon_url=avatar) 

                if not 選擇更新的cog模組:
                    pass
                else:
                    for filename in os.listdir("./cogs/cogs"):
                        if filename.endswith(".py"):
                            try:
                                await bot.unload_extension(f"cogs.cogs.{filename[:-3]}")
                                unload_list.append(f"cogs {filename[:-3]}")
                            except Exception as e:
                                ununload_list.append(f"cogs {filename[:-3]} \n")
                if not 選擇更新的event模組:
                    pass
                else:
                    for filename in os.listdir("./cogs/events"):
                        if filename.endswith(".py"):
                            try:
                                await bot.unload_extension(f"cogs.events.{filename[:-3]}")
                                unload_list.append(f"events {filename[:-3]}")
                            except Exception as e:
                                ununload_list.append(f"events {filename[:-3]} \n")
                if not 選擇更新的slash模組:
                    pass
                else:
                    for filename in os.listdir("./cogs/slashs"):
                        if filename.endswith(".py"):
                            try:
                                await bot.unload_extension(f"cogs.slashs.{filename[:-3]}")
                                unload_list.append(f"slashs {filename[:-3]}")
                            except Exception as e:
                                ununload_list.append(f"slashs {filename[:-3]} \n")

                embed.add_field(name="以下模組更新成功", value=unload_list, inline=False)
                embed.add_field(name="以下模組更新失敗", value=ununload_list, inline=False)
                
                await interaction.response.send_message(embed=embed)

            else:
                embed = discord.Embed(title=f"模組 {選擇更新的cog模組} {選擇更新的event模組} {選擇更新的slash模組} 已嘗試取消讀取",
                    description=f"執行者: {interaction.user.global_name}",
                    colour=0xd8d222,
                    timestamp=datetime.now())
                embed.set_footer(text=footer,icon_url=avatar) 

                if not 選擇更新的cog模組:
                    pass
                else:
                    try:
                        await bot.unload_extension(f"cogs.cogs.{選擇更新的cog模組}")
                        embed.add_field(name=f"{選擇更新的cog模組}", value=f"取消讀取成功!", inline=False)
                    except Exception as e:
                                embed.add_field(name="此Cog 取消讀取失敗: ", value=f"{e}", inline=False)
                if not 選擇更新的event模組:
                    pass
                else:
                    try:
                        await bot.unload_extension(f"cogs.events.{選擇更新的event模組}")
                        embed.add_field(name=f"{選擇更新的event模組}", value=f"取消讀取成功!", inline=False)
                    except Exception as e:
                                embed.add_field(name="此Events 取消讀取失敗: ", value=f"{e}", inline=False)
                if not 選擇更新的slash模組:
                    pass
                else:
                    try:
                        await bot.unload_extension(f"cogs.slashs.{選擇更新的slash模組}")
                        embed.add_field(name=f"{選擇更新的slash模組}", value=f"取消讀取成功!", inline=False)
                    except Exception as e:
                                embed.add_field(name="此Slash 取消讀取失敗: ", value=f"{e}", inline=False)

                await interaction.response.send_message(embed=embed)
                
            embed = discord.Embed(title=f"模組 {選擇更新的cog模組} {選擇更新的event模組} {選擇更新的slash模組} 已取消讀取",
                      description=f"執行者: {interaction.user.global_name}",
                      colour=0xd8d222,
                      timestamp=datetime.now())
            embed.set_footer(text=footer,icon_url=avatar) 
            await channel.send(embed=embed)
            
        elif 動作 == "status":
            await interaction.response.send_modal(StatusModal())

        elif 動作 == "say":
            await interaction.response.send_modal(Say())

        elif 動作 == "embed":
            await interaction.response.send_modal(Embed())

        elif 動作 == "count":
            await interaction.response.send_modal(Count())

        else:
            await interaction.response.send_message("抱歉，你使用了無法使用的功能。")

    else:
        await interaction.response.send_message("抱歉，你並不是北極企鵝開發者，不可以設定北極企鵝開發者設定喔!", ephemeral=True)    
        
async def load_cogs():
    for filename in os.listdir("./cogs/cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.cogs.{filename[:-3]}")
    for filename in os.listdir("./cogs/slashs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.slashs.{filename[:-3]}")
    for filename in os.listdir("./cogs/events"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.events.{filename[:-3]}")

@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    regular_commands = list(bot.commands)

    print(f"$$$目前登錄身分: {bot.user}")
    print(f"載入了 {len(slash)} 個斜線指令。")
    print(f"\n載入了 {len(regular_commands)} 個一般指令:")
    for cmd in regular_commands:
        print(f"- 一般指令: {bot.command_prefix}{cmd.name}")
    print(f"\n總共載入了 {len(slash) + len(regular_commands)} 個指令")
    print("Bot is ready!")
    embed = discord.Embed(title="北極企鵝上線了!",
                      colour=0x44ff00,
                      timestamp=datetime.now())
    FILE = reload()
    footer = FILE["ArcticPenguin"]["embed_footer_text"]
    avatar = FILE["ArcticPenguin"]["avatar"]
    embed.set_footer(text=footer,icon_url=avatar)
    channel_id = FILE["ArcticPenguin"]["record_channel"]
    channel = bot.get_channel(channel_id)
    await channel.send(embed=embed)

async def main():
    async with bot:
        await load_cogs()
        await bot.start(discord_key)

if __name__ == "__main__":
    asyncio.run(main())