import discord
import json
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

def reload():
    with open("jsons/setting/Guild_setting.json", "r", encoding='utf-8') as JSON_file:
        return json.load(JSON_file)

class Guild_Setting(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="伺服器設定", description="設定北極企鵝的一些伺服器功能。")
    @app_commands.describe(選項="請選擇你要設定的內容:", 狀態="選擇狀態(預設關閉):")
    @app_commands.choices(
        選項=[
            Choice(name="DC鏈結自動回覆Embed", value="Link_Reply"),
            Choice(name="語音頻道紀錄器", value="Voice_States"),
            Choice(name="歡迎消息", value="Welcome_Message")
        ],
        狀態=[
            Choice(name="啟用", value="True"),
            Choice(name="停用", value="False")
        ]
    )
    async def Guild_Setting(self, interaction: discord.Interaction, 選項: str = None, 狀態: str = None):
        if 選項 is None or 狀態 is None:
            await interaction.response.send_message("請選擇正確的選項及狀態。(錯誤訊息:傳入資料為None。)", ephemeral=True)
            return
        
        if interaction.user.guild_permissions.administrator:
            guild_id = str(interaction.guild.id)
            settings = reload()

            if guild_id not in settings:
                settings[guild_id] = {"Setting": {}}
            elif "Setting" not in settings[guild_id]:
                settings[guild_id]["Setting"] = {}
                
            settings[guild_id]["Setting"][選項] = (狀態 == "True")

            with open('jsons/setting/Guild_setting.json', 'w', encoding='utf-8') as file:
                json.dump(settings, file, ensure_ascii=False, indent=4)
            
            await interaction.response.send_message(f"已成功更新 `{選項}` 為 `{狀態}`。", ephemeral=True)
        else:
            await interaction.response.send_message("抱歉，你並不是管理員，不可以進行設定。", ephemeral=True)    

async def setup(bot: commands.Bot):
    await bot.add_cog(Guild_Setting(bot))
