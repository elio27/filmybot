import discord
import tmdbsimple as tmdb
import urllib.parse
import os, re, datetime
from keep_alive import keep_alive

tmdb.API_KEY = os.getenv("API")

client = discord.Client()
@client.event
async def on_ready():
  print("S/o la prise j'suis connecté")
  await client.change_presence(activity=discord.Game(name='!filmy help'))

@client.event
async def on_message(message):
  if message.content.startswith("!filmy "):
    ex = "(?<=filmy ).*"
    name = re.findall(ex, message.content)[0]
    search = tmdb.Search()
    search.movie(query=name)
    try:
      id = search.results[0]['id']
    except IndexError:
      await message.channel.send("Sorry, this film isn't in the movie database, try check the writing of the name")

    movie = tmdb.Movies(id)
    movie.info()
    poster_url = f"https://image.tmdb.org/t/p/w500{movie.images()['posters'][0]['file_path']}"

    embed = discord.Embed(title=f"{movie.title}", colour=discord.Colour(0x24a8e6), description=movie.overview, timestamp=datetime.datetime.utcfromtimestamp(1609958429))

    embed.set_thumbnail(url=poster_url)
    embed.set_footer(text="Filmy bot#5661", icon_url="https://cdn.discordapp.com/avatars/796361369149898773/c777bcb8d83b883e3326b60de539d6dc.png")

    date = movie.release_date.split("-")
    date = f"{date[1]}/{date[2]}/{date[0]}"

    embed.add_field(name="Informations", value=f"Release date: {date}\nProduced by: {movie.production_companies[0]['name']}\nDuration: {int(movie.runtime/60)}h{movie.runtime%60}min")

    await message.channel.send(embed=embed)
  
  elif "<@!796361369149898773>" in message.content:
    await message.add_reaction("<:ping:796795286995468368>")

keep_alive()
client.run(os.getenv("TOKEN"), bot=True)
