import discord
from discord.ext import commands
from decouple import config
from apis.films import searchFilms

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')


@bot.command()
async def whoiam(ctx):
    message = "Olá, eu sou um bot de filmes! Aqui estão algumas das minhas funcionalidades:\n"
    message += "- Consultar informações sobre filmes, como título, ano, gênero e sinopse.\n"
    message += "- Armazenar notas e avaliações de filmes para referência futura.\n"
    message += "- Recomendar filmes com base nas preferências dos usuários.\n"
    message += "- Fornecer informações sobre filmes em cartaz e próximos lançamentos.\n"
    message += "Sinta-se à vontade para explorar e utilizar os comandos disponíveis! 😊"
    
    await ctx.send(message)
    
@bot.command()
async def search(ctx):
    await ctx.send(f"- {ctx.author } \nDigite o título do filme:")
    
    message = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    title = message.content
    data = searchFilms(title)
    
    if 'Search' in data:
        message = ''
        for item in data['Search']:
            message += f'- {item["Title"]}: {item["Year"]}\n'
            
        embed = discord.Embed(title="Filmes", description=message, color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Erro!!", description=f'Erro ao achar {title}', color=discord.Color.red())
        await ctx.send(embed=embed)
        
    



bot.run(config('TOKEN_DISCORD'))

