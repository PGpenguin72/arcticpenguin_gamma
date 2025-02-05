import discord
from discord import app_commands
from discord.ext import commands
import json
import asyncio

lock = asyncio.Lock()

file_path = './jsons/command/count.json'

async def reload():
    async with lock:
        try:
            with open(file_path, 'r', encoding='utf-8') as JSON_count:
                return json.load(JSON_count)
        except FileNotFoundError:
            with open(file_path, 'w', encoding='utf-8') as JSON_count:
                json.dump({}, JSON_count)
            return {}

class count(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="數數字", description="點此開始數數字吧(從一開始)")
    async def count(self, interaction: discord.Interaction):
        CH_id = interaction.channel_id
        data = await reload()
        
        if "The_Higher_Score" not in data:
            data["The_Higher_Score"] = "0"
            async with lock:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

        if str(CH_id) in data:
            count_number = int(data[str(CH_id)]['count_num'])
            await interaction.response.send_message(f"已在此頻道開啟遊戲，目前已經數到了 {count_number-1} ，請繼續數數。")
        else:
            await interaction.response.send_message("開始數數字，我先來! 0")
            count_number = 1
            JSONdata = {
                f"{CH_id}": {
                    "count_num": str(count_number),
                    "last_counter": "null"
                }
            }
            
            data.update(JSONdata)
            async with lock:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        data = await reload()
        Higher_score = int(data.get("The_Higher_Score", 0))
        CH_Get = data.get(str(message.channel.id), None)
        channel_id = message.channel.id
        channel = self.bot.get_channel(channel_id)

        if CH_Get is None:
            return

        last_Counter = CH_Get["last_counter"]
        Now_Count = int(CH_Get["count_num"])
        member = message.author.id

        if message.content.isdigit():
            if last_Counter == str(member):
                await message.add_reaction("❌")
                await channel.send(f"不，有人連續了，打指令重新開始吧! \n目前全北極最高紀錄: {Higher_score}\n# </數數字:1336367496072003714>")

                del data[str(channel_id)]
                async with lock:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)

            elif int(message.content) == Now_Count:
                
                if Now_Count > Higher_score:
                    data["The_Higher_Score"] = str(Now_Count - 1)

                if Now_Count == Higher_score:
                    await message.add_reaction("🎉")
                else:
                    await message.add_reaction("✅")
                Now_Count += 1

                data[str(channel_id)] = {
                    "count_num": str(Now_Count),
                    "last_counter": str(member)
                }
                async with lock:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)

            else:
                if Now_Count > Higher_score:
                    data["The_Higher_Score"] = str(Now_Count - 1)

                await message.add_reaction("❌")
                await channel.send(f"不，有人失誤了，打指令重新開始吧! \n目前全北極最高紀錄: {Higher_score}\n# </數數字:1336367496072003714>")

                del data[str(channel_id)]

                async with lock:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)

async def setup(bot: commands.Bot):
    await bot.add_cog(count(bot))
