import discord
from discord.ext import commands
from decouple import config
from apis.films import searchFilms,searchId
from googletrans import Translator

exist_url = lambda value: 'https://www.inovegas.com.br/site/wp-content/uploads/2017/08/sem-foto.jpg' if value == 'N/A' else value


bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())
translator = Translator()

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')


@bot.command()
async def sobre(ctx):
    message = "Olá, eu sou um bot de filmes! Aqui estão algumas das minhas funcionalidades:\n"
    message += "- Consultar informações sobre filmes, como título, ano, gênero e sinopse.\n"
    message += "- Armazenar notas e avaliações de filmes para referência futura.\n"
    message += "- Recomendar filmes com base nas preferências dos usuários.\n"
    message += "- Fornecer informações sobre filmes em cartaz e próximos lançamentos.\n"
    message += "Sinta-se à vontade para explorar e utilizar os comandos disponíveis! 😊"
    
    await ctx.send(message)

@bot.command()    
async def sair(ctx):
    embed = discord.Embed(title="Tchau!!", description=f'Embora parta, você sempre será lembrado com carinho em nossos corações virtuais. :smiling_face_with_tear:', color=discord.Color.yellow())
    await ctx.send(embed=embed)  
    
@bot.command()
async def buscar(ctx):
    await ctx.send(f"- {ctx.author } \nDigite o título do filme:")
    
    message = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    title = message.content
    if title.lower() == '.sair':
        sair(ctx)
    else:    
        data = searchFilms(title)

        if 'Search' in data:
            cont = 1
            list_films = {}
            message = ''
            async with ctx.typing():
                for item in data['Search']:
                    message += f'{cont} - {translator.translate(item["Title"], dest="pt").text}: {item["Year"]}\n'
                    list_films[cont] = item['imdbID']
                    cont += 1
                        
            embed = discord.Embed(title="Filmes", description=message, color=discord.Color.blue())
            embed.add_field(name="Escolha", value="Digite o número correspondente ao filme desejado ou escreva '.SAIR'", inline=False)
            await ctx.send(embed=embed)
            
            while True:
                message = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
                number = message.content

                if number.isdigit() and int(len(list_films)) >= 1  and int(len(list_films)) >= int(number):
                    if list_films[int(number)]:
                        async with ctx.typing():
                            ratings = ''
                            data = searchId(list_films[int(number)])
                            
                            if data['Ratings']:
                                for rating in data['Ratings']:
                                    ratings += f'- {rating["Source"]} || {rating["Value"]} \n'
                    
                            embed = discord.Embed(title=translator.translate(data['Title'], dest="pt").text, color=discord.Color.blue())
                            embed.set_image(url=exist_url(data['Poster']))
                            embed.add_field(name= 'Descrição', value=translator.translate(data['Plot'], dest="pt").text, inline=False)
                            embed.add_field(name= 'Lançamento', value=data['Released'], inline=False)
                            embed.add_field(name= 'Duração', value=data['Runtime'], inline=False)
                            embed.add_field(name= 'Autores', value=data['Actors'], inline=False)
                            embed.add_field(name= 'Genero', value=data['Genre'], inline=False)
                            embed.add_field(name= 'Tipo', value=translator.translate(data['Type'], dest="pt").text, inline=False)
                            embed.add_field(name= 'Avaliações', value=ratings, inline=False)
                            await ctx.send(embed=embed)             
                            break
                elif number.lower() == '.sair':
                    sair(ctx)
                    break        
                else:
                    embed = discord.Embed(title="Erro!!", description=f'opção escolida não existe!!', color=discord.Color.red())
                    await ctx.send(embed=embed)
                    continue
        else:
            embed = discord.Embed(title="Erro!!", description=f'Erro ao achar {title}', color=discord.Color.red())
            await ctx.send(embed=embed)

  
              
    
bot.run(config('TOKEN_DISCORD'))

