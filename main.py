from config import BOT_TOKEN
import discord
from discord.ext import commands
from discord.utils import get
import random


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

    # вспомогательная функция для очистки чата (потом удалить)
    @commands.command(name='clear')
    async def clear(self, ctx, a=None):
        if a is None:
            await ctx.send('скока? в конце напиши')
        else:
            await ctx.channel.purge(limit=int(a))

    # функция игры
    @commands.command(name='start')
    async def start_game(self, ctx):
        # список игроков
        players = ctx.message.author.voice.channel.members

        if len(players) < 6:
            await ctx.send('Вас слишком мало')
            return

            # выдаем роли
        n_mafia = round(len(players) / 3.5)
        mafia = {i: discord.PermissionOverwrite for i in random.sample(players, n_mafia)}
        for i in mafia:
            players.pop(players.index(i))
        sheriff = random.choice(players)
        players.pop(players.index(sheriff))
        doctor = random.choice(players)
        players.pop(players.index(doctor))

        # создаем новую категория, голосоой чат и чат для мафии
        guild = ctx.guild
        game = await guild.create_category('Мафия')
        voice = await guild.create_voice_channel('Игра', category=game)
        mafia_text = await guild.create_text_channel('Мафия', category=game, overwrites=mafia)

        # перемещанм всех игроков в игровой войс канал
        for i in players:
            await i.move_to(voice)


bot.add_cog(Leading(bot))
bot.run(BOT_TOKEN)