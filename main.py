from config import BOT_TOKEN
import discord
from discord.ext import commands
from discord.utils import get


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Бот робит')
    await bot.change_presence(activity=discord.Game('!help'), status=discord.Status.online)


class Leading(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.voice = None

    # личное сообщение для автора
    @commands.command(name='lsa')
    async def send_ls_msg_a(self, ctx):
        await ctx.author.send('Hello World')

    # личное сообщение для какого-то пользователя
    @commands.command(name='lsm')
    async def send_ls_msg_u(self, ctx, member: discord.Member):
        await member.send(f'Hello World от {ctx.author.name}')

    # подключение к голосовому чату
    @commands.command(name='join')
    async def join_voice_chat(self, ctx):
        voice = get(bot.voice_clients)
        channel = ctx.message.author.voice.channel
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.send(f'Бот присоединился к: {channel}')

    # отключение от голосового чата
    @commands.command(name='leave')
    async def leave_voice_chat(self, ctx):
        voice = get(bot.voice_clients, guild=ctx.guild)
        channel = ctx.message.author.voice.channel
        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f'Бот отключился от: {channel}')


bot.add_cog(Leading(bot))
bot.run(BOT_TOKEN)