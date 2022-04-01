from config import BOT_TOKEN
import discord
from discord import PermissionOverwrite
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
    async def start_game(self, ctx, doc='есть', com='есть'):
        if ((com == 'есть') or (com == 'нету')) and ((doc == 'есть') or (doc == 'нету')):
            await ctx.send('Некоректные настройки')
            return

        # список игроков
        players = ctx.message.author.voice.channel.members
        access = {'manage_channels': True, 'manage_roles': True, 'read_messages': True, 'connect': True, 'speak': True}
        ban = {'manage_channels': False, 'manage_roles': False, 'read_messages': False, 'connect': False, 'speak': False}
        for i in players:
            if 'mafia#7771' == str(i):
                players.pop(players.index(i))

        if len(players) < 6:
            await ctx.send('Вас слишком мало')
            return

        # выдаем роли
        n_mafia = round(len(players) / 3.5)
        mafia = {i: discord.PermissionOverwrite(**access) for i in random.sample(players, n_mafia)}
        for i in mafia:
            players.pop(players.index(i))
        if com == 'есть':
            sheriff = random.choice(players)
            players.pop(players.index(sheriff))
        if doc == 'есть':
            doctor = random.choice(players)
            players.pop(players.index(doctor))

        # создаем новые приватные категорию, голосоой чат и чаты для мафии, комиссар и доктора
        guild = ctx.guild
        game = await guild.create_category('Мафия', overwrites={i: PermissionOverwrite(**access) for i in ctx.message.author.voice.channel.members})
        await game.set_permissions(guild.default_role, overwrite=PermissionOverwrite(**ban))
        voice = await guild.create_voice_channel('Игра', category=game)
        await voice.set_permissions(guild.default_role, overwrite=PermissionOverwrite(**ban))
        mafia_text = await guild.create_text_channel('Игра', category=game)
        await mafia_text.set_permissions(guild.default_role, overwrite=PermissionOverwrite(**ban))
        mafia_text = await guild.create_text_channel('Мафия', category=game, overwrites=mafia)
        await mafia_text.set_permissions(guild.default_role, overwrite=PermissionOverwrite(**ban))
        if com == 'есть':
            sheriff_text = await guild.create_text_channel('Шериф', category=game, overwrites={sheriff: PermissionOverwrite(**access)})
            await sheriff_text.set_permissions(guild.default_role, overwrite=PermissionOverwrite(**ban))
        if doc == 'есть':
            doctor_text = await guild.create_text_channel('Доктор', category=game, overwrites={doctor: PermissionOverwrite(**access)})
            await doctor_text.set_permissions(guild.default_role, overwrite=PermissionOverwrite(**ban))

        # перемещанм всех игроков в игровой войс канал
        for i in players:
            await i.move_to(voice)
        await get(bot.voice_clients).move_to(voice)


bot.add_cog(Leading(bot))
bot.run(BOT_TOKEN)
