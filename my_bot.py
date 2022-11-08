#import discord
from ast import arg
from distutils.log import info
from email import header, message
from pydoc import cli
from unicodedata import name
from urllib import response
from aiohttp import request
import discord
from discord.ext import commands
import requests
import json
import secrets
import time


#client our bot
client = commands.Bot(command_prefix='.')

#dictionary that will hold the image urls of the airlines
logoDict = {}

@client.command()
async def helpBot(name="helpBot"):
    bot_channel = client.get_channel(1023311688767897711)
    await bot_channel.send('Use .flightinfo "flight number" to find information about certain flights')
    return

##############
#FLIGHT API GETTER
def getFlight(cxt):
    
    params ={
        'api_key': secrets.API_KEY,
        'flight_iata': cxt
    }

    url_base = 'http://airlabs.co/api/v9/flight'
    #method = 'flight'
    api_result = requests.get(url_base, params) #need to add check if response from API is valid if not then prompt user to re enter
    api_response = json.loads(api_result.text)
    
    #flight_num = api_response['response']['flight_iata']

    flight_data ={
        'name': api_response['response']['airline_name'], #airline name Air Canada
        'flight_num':api_response['response']['flight_iata'], #flight number AC776
        'dep_full': api_response['response']['dep_name'], #departing airport full name Los Angeles International Airport
        'dep_short': api_response['response']['dep_iata'], #dep airport tag LAX
        'dep_time':api_response['response']['dep_time'], #departure time and date will parse
        'arr_full':api_response['response']['arr_name'], #Montreal-Pierre Elliott Trudeau International Airport'
        'arr_short':api_response['response']['arr_iata'],#YUL
        'arr_time':api_response['response']['arr_time'], #arrival time
        'duration':api_response['response']['duration'] #duration in minutes
    }
    return(flight_data)

#getting airline logo
def get_Logo_URL(airline_name):
    params ={
        'api_key': secrets.SEARCH_API_KEY,
        'q': airline_name +" logo"
    }

    api_result = requests.get('https://serpapi.com/search', params) #need to add check if response from API is valid if not then prompt user to re enter
    api_response = json.loads(api_result.text)
    #string = 
    return(api_response['inline_images'][0]['original'])




#formatting time output
def format_time(minutes):
    hours_total = minutes // 60
    # Get additional minutes with modulus
    minutes_total = minutes % 60
    # Create time as a string
    time_string = "{} hours {} minutes".format(hours_total, minutes_total)
    return time_string

#command to start reading the input
@client.command()
async def flightinfo(ctx, arg=None):
    #setting the arg to None
    if arg == None: #if no valid input display error msg
        bot_channel = client.get_channel(1023311688767897711)
        await bot_channel.send('Please input a valid flight number!')
        return

    #calling function to get the correct data needed
    try:
        flight_info = getFlight(arg)
    except KeyError: #if there is a case where the user inputs an invalid flight number it will prompt the user to re enter that number
        bot_channel = client.get_channel(1023311688767897711) 
        await bot_channel.send("Please input a valid flight number!")
        return
    
    bot_channel = client.get_channel(1023311688767897711)
    flightEmbed=discord.Embed(title=flight_info['name']+" "+ flight_info['flight_num'], description="This flight is departing from " + flight_info['dep_full'] + " (" +flight_info['dep_short']+ ") and will arrive at "+ flight_info['arr_full']+" ("+flight_info['arr_short'] +").", color=0x2596be)
    flightEmbed.add_field(name="Departure:", value=flight_info['dep_time'], inline=False)
    flightEmbed.add_field(name="Arrival:", value=flight_info['arr_time'], inline=False)
    flightEmbed.add_field(name="Duration:", value=format_time(flight_info['duration']), inline=False)
    flightEmbed.set_footer(text="Operated by " + flight_info['name'])
    
    #setting thumbnail
    if flight_info['name'] not in logoDict:
        url = get_Logo_URL(flight_info['name'])
        logoDict[flight_info['name']] = url
    
    flightEmbed.set_thumbnail(url = logoDict[flight_info['name']])


    await bot_channel.send(embed=flightEmbed)

#testing how to print out the flight info
@client.command(name='test')
async def test(ctx):
    name ="Air Canada"

    bot_channel = client.get_channel(1023311688767897711)
    myEmbed = discord.Embed(title=name+" AC776", description="This flight is departing from Los Angeles International Airport (LAX) and will arrive at Montreal-Pierre Elliott Trudeau International Airport (YUL).", color=0xFF0000)
    myEmbed.add_field(name="Departure:", value="12:05", inline=False)
    myEmbed.add_field(name="Arrival:", value="20:15", inline=False)
    myEmbed.add_field(name="Duration:", value="5h 10m", inline=False)
    myEmbed.set_footer(text="Operated by Air Canada")
    """
    if flight_info['name'] is not in logoDict:
        get from api // url = get_Logo_URL(flight_info['name'])
        put flight_info['name'] = url link for img from api //logoDict['name'] = url
    else:
        flightEmbed.set_thumnail(url = logoDict[flight_info['name']])
    """
    myEmbed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Air_Canada_Logo.svg/2560px-Air_Canada_Logo.svg.png")

    await bot_channel.send(embed=myEmbed)


#ping pong
@client.command(name='ping')
async def ping(ctx):
    
    await ctx.channel.send('pong!')

#clear chat
@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

#.version command gives version of the bot
@client.command(name='version')
async def version(context):
    bot_channel = client.get_channel(1023311688767897711)
    myEmbed = discord.Embed(title="Current Version", description="The bot is in Version 1.0", color=0x00ff00)
    myEmbed.add_field(name="Version Code:", value="v1.1.2", inline=False)
    myEmbed.add_field(name="Date Released:", value="August 1, 2022", inline=False)
    myEmbed.set_footer(text="A flight tracking bot!")
    myEmbed.set_author(name="Jason Le")

    await bot_channel.send(embed=myEmbed)
    
#bot will say hello when first turned on
@client.event
async def on_ready():
    #Do stuff
    bot_channel = client.get_channel(1023311688767897711)
    await bot_channel.send('Xinh chao cac ban!')

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return(quote)

#reading certain input then process it
@client.event
async def on_message(message):
    if message.content=="what is this version":
        bot_channel = client.get_channel(1023311688767897711)
        myEmbed = discord.Embed(title="Current Version", description="The bot is in Version 1.0", color=0x00ff00)
        myEmbed.add_field(name="Version Code:", value="v1.0.0", inline=False)
        myEmbed.add_field(name="Date Released:", value="Septemeber 24, 2022", inline=False)
        myEmbed.set_footer(text="This is a sample footer")
        myEmbed.set_author(name="Jason Le")

        await bot_channel.send(embed=myEmbed)
    await client.process_commands(message)
    
    if message.content.startswith('-inspire'):
        
        quote = get_quote()
        await message.channel.send(quote)
    if message.content =="fuck you bot":
        bot_channel = client.get_channel(1023311688767897711)
        await bot_channel.send('du ma may')

#run the client on server
client.run(secrets.TOKEN)
