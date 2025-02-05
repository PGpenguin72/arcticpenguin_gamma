import discord
import json
from datetime import datetime
from random import choice
from discord.ext import commands
from discord import app_commands

def config():
    with open("config.json", "r", encoding='utf-8') as CONFIG:
        return json.load(CONFIG)

def reload():
    with open("jsons/command/welcome.json", "r", encoding="utf-8") as CONFIG:
        return json.load(CONFIG)

FILE = config()
colors = FILE["color"]
footer = FILE["ArcticPenguin"]["embed_footer_text"]
avatar = FILE["ArcticPenguin"]["avatar"]
group_id = None
group_name = None

class Create(discord.ui.Modal, title="設定歡迎消息"):
    def __init__(self, guild_id: int):
        file_path = './jsons/command/welcome.json'
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[錯誤] 無法讀取 JSON 檔案: {e}")
            data = {}

        guild_data = data.get(str(guild_id), {}).get("Message", {})

        def safe_default(value, max_length=100):
            return value[:max_length] if value else ""

        super().__init__()

        self.Channel = discord.ui.TextInput(
            label="請輸入用來發送歡迎消息的頻道ID:",
            placeholder="開啟設定中的「開發者模式」，右鍵頻道名稱選「複製頻道ID」。",
            max_length=20,
            default=safe_default(data.get(str(guild_id), {}).get("Channel", ""))
        )
        self.Author_Name = discord.ui.TextInput(
            label="輸入大標題歡迎消息。",
            default=safe_default(guild_data.get("Author", {}).get("Name", "歡迎加入 {guild} ，你是第 {count} 位用戶"))
        )
        self.Tittle = discord.ui.TextInput(
            label="請輸入稱呼之用戶",
            default=safe_default(guild_data.get("Title", "用戶 {user} 你好!"))
        )
        self.Image = discord.ui.TextInput(
            label="請輸入當用戶加入時傳送之圖片連結(限制一張)。",
            required=False,
            default=safe_default(guild_data.get("Images", ""))
        )
        self.Description = discord.ui.TextInput(
            label="請輸入歡迎消息。",
            placeholder="不要太長，要不然機器人會爆掉:D",
            style=discord.TextStyle.paragraph,
            max_length=500,
            default=safe_default(guild_data.get("Description", ""))
        )

        self.add_item(self.Channel)
        self.add_item(self.Author_Name)
        self.add_item(self.Tittle)
        self.add_item(self.Image)
        self.add_item(self.Description)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            welcome_msg = {
                f"{group_id}": {
                    "GroupName": f"{group_name}",
                    "Channel": f"{self.Channel.value}",
                    "Message": {
                        "Title": f"{self.Tittle.value}",
                        "Description": f"{self.Description.value}",
                        "Author": {
                            "Name": f"{self.Author_Name.value}"
                        },
                        "Images": f"{self.Image.value}"
                    }
                }
            }

            file_path = './jsons/command/welcome.json'
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                print("[錯誤] 無法讀取 JSON，使用新字典")
                data = {}

            data.update(welcome_msg)

            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            DATA = reload()
            guild_id = str(interaction.guild.id)
            group = DATA[guild_id]
            Message = group["Message"]
            channel_id = int(group["Channel"])
            channel = interaction.client.get_channel(channel_id)

            if channel:
                await channel.send("此頻道已設定歡迎消息，下個用戶加入即會發送出歡迎消息了喔!")
            else:
                await interaction.response.send_message("無法找到指定的頻道，請確認頻道 ID 是否正確!", ephemeral=True)
                return

            embed = self.created_welcome_message(interaction.user, Message)
            await interaction.response.send_message("恭喜你成功設定了歡迎消息! 你的歡迎消息範本在下面:", embed=embed, ephemeral=True)

        except Exception as e:
            print(f"[錯誤] 在 on_submit 發生錯誤: {e}")
            await interaction.response.send_message(f"發生錯誤: {e}", ephemeral=True)

    def created_welcome_message(self, member, Message):
        count = member.guild.member_count
        guild = member.guild.name
        user = member.display_name
        title = Message["Title"].replace("{user}", user)
        author_name = Message["Author"]["Name"]
        author_name = author_name.replace("{guild}", guild)
        author_name = author_name.replace("{count}", str(count))

        embed = discord.Embed(
            title=title,
            description=Message["Description"],
            colour=choice(colors),
            timestamp=datetime.now()
        )

        embed.set_author(name=author_name, icon_url=member.guild.icon)

        if Message.get("Images"):
            embed.set_image(url=Message["Images"])

        embed.set_thumbnail(url=member.display_avatar)
        embed.set_footer(text=footer, icon_url=avatar)

        return embed

class add_welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="設定歡迎消息",
        description="當用戶一加入伺服器就會發送的歡迎訊息。"
    )
    async def add_welcome(self, interaction: discord.Interaction):
        try:
            if interaction.user.guild_permissions.administrator:
                global group_id, group_name
                group_id = interaction.guild.id
                group_name = interaction.guild.name
                await interaction.response.send_modal(Create(group_id))
            else:
                await interaction.response.send_message("抱歉，你並不是管理員，不可以設定歡迎消息喔!", ephemeral=True)
        except Exception as e:
            print(f"[錯誤] 在 add_welcome 指令發生錯誤: {e}")
            await interaction.response.send_message(f"發生錯誤: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(add_welcome(bot))
