import discord
import tmdbsimple as tmdb
import os, re, datetime
# from keep_alive import keep_alive -> trick to host on repl.it

tmdb.API_KEY = os.getenv("API")

client = discord.Client()
@client.event
async def on_ready():
  print("S/o la prise j'suis connecté")
  await client.change_presence(activity=discord.Game(name='!filmy help'))

@client.event
async def on_message(message):
  if message.content.startswith("!filmy help"):
    embed = discord.Embed(title="Filmy Bot Help Page", colour=discord.Colour(0x5da26c), description="Filmy")

    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/796361369149898773/c777bcb8d83b883e3326b60de539d6dc.png?size=512")
    embed.set_footer(text="Filmy Bot by elio 27#0601", icon_url="https://cdn.discordapp.com/avatars/424188671332319233/3f081a930ca4bd8fd19f46a374d1ca86.png")

    embed.add_field(name="!filmy {movie name}", value="Return an embed with a lot of informations about the movie, like his poster, synopsis, release date etc...")
    embed.add_field(name="!filmy invite", value="Return the [link](https://bit.ly/filmy-bot) to invite me in your server !")
    embed.add_field(name="!filmy help", value="Return the page you are reading\n\n")
    embed.add_field(name="Other informations:", value="[Source Code on Github](https://github.com/elio27/filmybot)\n[Vote](https://top.gg/bot/796361369149898773)")

    await message.channel.send(embed=embed)

  elif message.content.startswith("!filmy invite"):
    await message.channel.send("https://bit.ly/filmy-bot")

  elif message.content.startswith("!filmy "):
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

    base_average = movie.vote_average
    average = round(base_average)

    if base_average - int(base_average) <= 0.5:
      if round(base_average + 0.25) == round(average + 0.5):
        note = average + 0.5
      else:
        note = average
    else:
      if round(base_average - 0.25) != round(average - 0.5):
        note = average - 0.5
      else:
        note = average
    note /= 2

    vote = "<:fullstar:798903898189463592>"*int(note)
    if note - int(note) != 0:
      vote = f"{vote}<:halfastar:798903936362610719>"

    embed.add_field(name="Informations", value=f"Release date: {date}\nProduced by: {movie.production_companies[0]['name']}\nDuration: {int(movie.runtime/60)}h{movie.runtime%60}min\nViewer rating:\n{vote}")

    await message.channel.send(embed=embed)


#keep_alive() -> the same trick to host on repl.it
client.run(os.getenv("TOKEN"), bot=True)
