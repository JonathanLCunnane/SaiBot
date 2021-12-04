#imports
#region
from operator import ge
import discord
from discord.embeds import Embed
from discord.enums import ActivityType, ChannelType
from discord.http import HTTPException
from discord.ext import tasks
from discord import Spotify
from discord_slash import SlashCommand, SlashContext
import os
from dotenv import load_dotenv
from datetime import date, datetime, timedelta
from random import choice, randrange, randint
import sqlite3
from re import search
from asyncio import sleep
import asyncio
import psutil
from math import ceil

import time
timeone = time.time()
from SaiClasses import Character, usercooldown, Characters
timetwo = time.time()
print(f"Character Import Time: {timetwo - timeone}\n\n")
#endregion


#gets client token and creates client
load_dotenv()
TOKEN = os.getenv("TOKEN")
client = discord.Client(intents=discord.Intents.all(), command_prefix="s.", help_command=False)
slash = SlashCommand(client, sync_commands=True)

#variables
#region
alltimezones = {"GMT":0, 
                "UTC":0, 
                "ECT":1, 
                "BST":1, 
                "EET":2, 
                "ART":2, 
                "EAT":3, 
                "MET":3.5, 
                "NET":4, 
                "PLT":5, 
                "IST":5.5, 
                "VST":7, 
                "CTT":8, 
                "JST":9, 
                "ACT":9.5, 
                "AET":10, 
                "SST":11, 
                "NST":12, 
                "MIT":-11, 
                "HST":-10, 
                "AST":-9, 
                "PST":-8, 
                "PNT":-7, 
                "MST":-7, 
                "CST":-6, 
                "EST":-5, 
                "IET":-5, 
                "PRT":-4, 
                "CNT":-3.5, 
                "AGT":-3, 
                "BET":-3, 
                "CAT":-1}
embedcolour = 0xd6d6d6
database = r".\SaiDatabase.db"
saigifs = ["https://c.tenor.com/iRVQxndqnLUAAAAC/kenjutsu-cool.gif",
           "https://tenor.com/view/naruto-akatsuki-sai-ninja-draw-gif-16739112   ",
           "https://tenor.com/view/naruto-slap-sai-smack-gif-11514561",
           "https://media.giphy.com/media/w3QZlygasHD0Y/giphy.gif",
           "https://media.giphy.com/media/13k3zHhaIPkK52/giphy.gif",
           "https://media.giphy.com/media/1qHu77EWk5ji/giphy.gif",
           "https://media.giphy.com/media/bMEmctNEi7GI8/giphy.gif",
           "https://media.giphy.com/media/3orHABymmb3vG/giphy.gif",
           "https://media.giphy.com/media/uvnPNosvJ7f4k/giphy.gif",
           "https://media.giphy.com/media/gO3dpclzdwSLm/giphy.gif",
           "https://media.giphy.com/media/mdeHUb6tosRBS/giphy.gif",
           "https://media.tenor.com/images/54c3178c436e952648d9ad16b44e0902/tenor.gif",
           "https://media.tenor.com/images/12b53fdec9367f1f4a5d532ce58567c7/tenor.gif",
           "https://media.tenor.com/images/23a1592736664ef1e55caeeb964436ce/tenor.gif",
           "https://media.tenor.com/images/8106ae241cf535e05e68d96ce59911d1/tenor.gif",
           "https://media.tenor.com/images/59a225d12675eaa88437c6ed3e61b99a/tenor.gif",
           "https://media.tenor.com/images/8fe4470402cc963550e78fc317b6df7f/tenor.gif",
           "https://media.tenor.com/images/43e5c5d6b4869817ef3fb07527478d97/tenor.gif",
           "https://media.tenor.com/images/8bd691ac934f6bb2aa1453580153b166/tenor.gif",
           "https://media.tenor.com/images/f3ec69991ec2785bf6a3bf40d6dd788d/tenor.gif",
           "https://media.tenor.com/images/102956c55d8d4ba6af587ced0f8fd755/tenor.gif",
           "https://media.tenor.com/images/18dc193b9440bd6ae1f3745d968167f9/tenor.gif"]
saistatuses = [[discord.ActivityType.watching, "naruto shippuden"],
    [discord.ActivityType.competing, "a calligraphy contest"],
    [discord.ActivityType.listening, "blue bird"],
    [discord.ActivityType.listening, "naruto complain"],
    [discord.ActivityType.listening, "naruto scream dattebayo"],
    [discord.ActivityType.watching, "sexy jutsu"],
    [discord.ActivityType.playing, "with calligraphy sets"]
    ]
starttime = datetime.now()
commandsrun = 0
snipedict = {}
editsnipedict = {}
allcooldowns = []

### UPDATE THESE BEFORE BOT UPDATE ###+
commandnumber = 31
version = "1.11.0"
linesofcode = "8467"
libraries = "os, dotenv, datetime, random, sqlite3, re, asyncio, psutil, math"
### UPDATE THESE BEFORE BOT UPDATE ###

weeklytulaiigif = "https://tenor.com/view/death-note-hey-can-i-have-autograph-sign-it-gif-18164531"
eightballreplies = ["It is Certain.",
                    "It is decidedly so.",
                    "Without a doubt.",
                    "Yes definitely.",
                    "You may rely on it.",
                    "As I see it, yes.",
                    "Most likely.",
                    "Outlook good.",
                    "Yes.",
                    "Signs point to yes.",
                    "Reply hazy, try again.",
                    "Ask again later.",
                    "Better not tell you now.",
                    "Cannot predict now.",
                    "Concentrate and ask again.",
                    "Don't count on it.",
                    "My reply is no.",
                    "My sources say no.",
                    "Outlook not so good.",
                    "Very doubtful."]
customisationquestions = ["What is your name?",
                          "What are your pronouns?",
                          "What is your age?",
                          "What nickname(s) do you prefer?",
                          "What is your favourite colour?",
                          "Name a few things you like:",
                          "Name a few things you dislike:",
                          "What hobbies do you have?"]
saiquotes = [
    "The manual said that the first way to appeal to someone is with a smiling face. I've practiced but I'm still unable to make this facial expression.",
    "You're... pretty weak. The way you fight, are you a boy or a girl?",
    "A smile is the best way to get oneself out of a tight spot, even if it is a fake one. Surprisingly enough, everyone takes it at face value. I read that in a book.",
    "[to Naruto, who is mentally comparing Sai's appearance to Sasuke's] If you keep staring at me, I'll hit you.",
    "[to Naruto in a hot springs] Well gee... You actually do have one after all.",
    "I’ve drawn hundreds, maybe thousands of pictures so far… none of them have titles.",
    "[to Naruto] Please don’t lay the blame on others for your own minimal amount of ability.",
    "I have none of what you’d call “emotions”.",
    "[To Sakura after being told to nickname people after comes to mind] Thanks for the advice... ugly.",
    "[thinking] If I use female's true characteristics, they get scary. I might avoid it if I say the opposite of what I think. [to Ino] Pleased to meet you... um, Gorgeous.",
    "[talking to Sakura] I like everyone. Even you, ugly.",
    "||[About Sasuke] He betrayed the Leaf and ran off to serve Orochimaru... I don't want to be lumped together with a cockroach along the same lines... as Orochimaru.||",
    "[to Naruto] Oh, geez… You two are so alike… you and my brother, I mean. He was loud, impatient, unrefined, and his peni... Well, it doesn't really matter. But still... Yeah... Just like you, he took on anything he did with everything he had. Watching you somehow brings back memories of...",
    "||[to Sasuke] I'm here... to take you back to the Leaf Village. Although my original intention was to assassinate you.||",
    "[Sees Naruto clones training simultaneously] Naruto? [Begins to read] When your friends are working unusually hard on the job or doing their hobbies, it's nice to casually bring them a snack or drink. [Looks back at the hundreds of training Naruto clones] Working unusually hard.. Seems normal to me. [Takes out an apple originally intended for Naruto and takes a bite]",
    "I wonder if this is what you'd call 'gross'.",
    "||[to Sakura] I only became part of your team recently when I replaced Sasuke, so I don't know everything that's going on.|| I don't really understand people either. But even I can tell that Naruto really loves you. Naruto's been shouldering that promise for a long time...I think he means to shoulder it for the rest of his life. I don't know what you said to him, but it's just like what's been done to me - it feels like a curse. Sasuke causes Naruto pain, but I think you do too.",
    "||Sakura didn't come out here to confess her love. She was supposed to tell you the collective decision made by all your former Academy classmates...Konoha is going to dispose of Sasuke itself. Your ex-classmates are preparing to ask as we speak.||",
    "||Sasuke is only helping spread his darkness across the world. Letting him live will only sow the seeds of another war. He's just another criminal now. Sasuke lost all hope of coming back when his group, Akatsuki, attacked our village. Your fellow Konoha shinobi would never accept him now. Sakura's not stupid, either. She understands the position he's put us all in. That's why she came out here, to tell you herself.||",
    "||It's because Sakura loves Sasuke that she doesn't want him to sink any lower. It's because she loves him that she wants to rescue him from the evil path he currently walks. Even if the only way to do it is to kill him with her own two hands, I believe she's prepared to do it because she loves him. Which also means she's willing to let you hate her forever, Naruto. I think it's her way of atoning for saddling you with the burden of that promise that you held for so many years. She's asked too much of you, so she's trying to end this all herself.||",
    "[In his mind while coming to Naruto's aid during ||the war||] This...is what it means to have friends. I understand it perfectly...Naruto."]

#cooldown timers in seconds

temp = usercooldown(0)
### NARUTO ###
charactercooldown = temp.get_cooldown_length("character")
informationcooldown = temp.get_cooldown_length("character")

### INFO ###
aboutcooldown = temp.get_cooldown_length("about")
helpcooldown = temp.get_cooldown_length("help")
linkscooldown = temp.get_cooldown_length("links")
patreoncooldown = temp.get_cooldown_length("patreon")
profilecooldown = temp.get_cooldown_length("profile")
statisticscooldown = temp.get_cooldown_length("statistics")
testcountcooldown = temp.get_cooldown_length("testcount")

### UTILITY ###
cooldownscooldown = temp.get_cooldown_length("cooldowns")
editsnipecooldown = temp.get_cooldown_length("editsnipe")
eventcooldown = temp.get_cooldown_length("event")
nicknamecooldown = temp.get_cooldown_length("nickname")
pingcooldown = temp.get_cooldown_length("ping")
rescuecooldown = temp.get_cooldown_length("rescue")
snipecooldown = temp.get_cooldown_length("snipe")
timecooldown = temp.get_cooldown_length("time")
voteremindercooldown = temp.get_cooldown_length("votereminder")

### MODERATION AND ADMIN ###
bancooldown = temp.get_cooldown_length("ban")
kickcooldown = temp.get_cooldown_length("kick")
lockdowncooldown = temp.get_cooldown_length("lockdown")
messagecooldown = temp.get_cooldown_length("message")
purgecooldown = temp.get_cooldown_length("purge")
rolecooldown = temp.get_cooldown_length("role")
slowmodecooldown = temp.get_cooldown_length("slowmode")
unlockdowncooldown = temp.get_cooldown_length("unlockdown")

### FUN ###
decidecooldown = temp.get_cooldown_length("decide")
eightballcooldown = temp.get_cooldown_length("eightball")
gifcooldown = temp.get_cooldown_length("gif")
quotecooldown = temp.get_cooldown_length("quote")
tulaiiisabigmancooldown = temp.get_cooldown_length("tulaiiisabigman")
#endregion

#functions
#region
def createparamlist(commandname, parametersstring, delimiter):
    """returns a list of all parameters for a command with a specific delimiter"""
    length = len(commandname)
    parameterslist = parametersstring[length:].strip().split(delimiter)
    parameterslist = [parameter.strip() for parameter in parameterslist]
    return parameterslist
def updateeventembed(previousembed, attending, unsure, notattending):
    """updates the event embed with the new attending, unsure, and not attending list, returning an embed to show this new data to the user"""
    neweventembed=discord.Embed(title=previousembed.title, description=previousembed.description, color=embedcolour)
    neweventembed.set_thumbnail(url=previousembed.thumbnail.url)
    neweventembed.add_field(name="­\n  :white_check_mark: Attending", value=">>> ­{0}".format("\n".join(attending.split(",")).strip("\n")), inline=False)
    neweventembed.add_field(name="­\n  :grey_question: Unsure", value=">>> ­{0}".format("\n".join(unsure.split(",")).strip("\n")), inline=False)
    neweventembed.add_field(name="­\n  :x:Not Attending", value=">>> ­{0}".format("\n".join(notattending.split(",")).strip("\n")), inline=False)
    neweventembed.add_field(name="­­\n\nHow to choose preference/status­: ", value="Simply react to the message below with the corresponding emoji, and if you want to change your choice, make sure you are only reacted to one choice.", inline=False)
    neweventembed.set_footer(text=previousembed.footer.text, icon_url=previousembed.footer.icon_url)
    return neweventembed
def getcooldownembed(commandname, timeleft, user):
    """returns a cooldown embed that can be used by the bot to ouput onto a channel"""
    cooldownembed = discord.Embed(title = "Cooldown triggered", description = "Slow down, you still have {0} before you can run the `{1}` command again.".format(timeleft, commandname), color=embedcolour)
    cooldownembed.set_footer(text="Command run by {0}#{1}".format(user.name, user.discriminator), icon_url=user.avatar_url)
    return cooldownembed
def formattimedelta(timedelta):
    """returns a formatted timedelta in the format D days, H hours, M minutes, S seconds"""
    days = timedelta.days
    seconds = timedelta.seconds
    
    hours = seconds//3600
    minutes = (seconds//60)%60
    seconds = seconds - (hours*3600 + minutes*60)
    if seconds == 1 and minutes == 0 and hours == 0 and days == 0:
        return f"`{seconds}` second"
    elif minutes == 0 and hours == 0 and days == 0:
        return f"`{seconds}` seconds"
    elif minutes == 1 and hours == 0 and days == 0:
        return f"`{minutes}` minute, `{seconds}` seconds"
    elif hours == 0 and days == 0:
        return f"`{minutes}` minutes, `{seconds}` seconds"
    elif days == 0:
        return f"`{hours}` hours, `{minutes}` minutes, `{seconds}` seconds"
    elif days == 1:
        return f"`{days}` day, `{hours}` hours, `{minutes}` minutes, `{seconds}` seconds"    
    else:
        return f"`{days}` days, `{hours}` hours, `{minutes}` minutes, `{seconds}` seconds"    
def isint(number):
    """returns true if number is an int, otherwise returns false"""
    try:
        number = int(number)
        return True
    except:
        return False
def isuserID(string):
    """retruns true if string is a user ID, otherwise returns false"""
    string  = str(string)
    return ((search("<@.+>", string) and len(string) == 21) or (search("<@!.+>", string) and len(string) == 22) or (isint(string) and len(string) == 18))
def isroleID(string):
    """retruns true if string is a role ID, otherwise returns false"""
    string  = str(string)
    return ((search("<@\&.+>", string) and len(string) == 22) or (isint(string) and len(string) == 18))
def ischannelID(string):
    """retruns true if string is a role ID, otherwise returns false"""
    string  = str(string)
    return ((search("<#.+>", string) and len(string) == 21) or (isint(string) and len(string) == 18))
def getuserID(string):
    """returns a user ID from a mention string or from a user ID string if the string has an accepted user ID format"""
    string  = str(string)
    try:
        if (search("<@.+>", string) and len(string) == 21):
            userID = string[2:20]
        elif (search("<@!.+>", string) and len(string) == 22):
            userID = string[3:21]
        else:
            userID = string
        return int(userID)
    except:
        return None
def getroleID(string):
    """returns a role ID from a mention string or from a role ID string if the string has an accepted role ID format"""
    string  = str(string)
    try:
        if search("<@\&.+>", string):
            roleID = string[3:21]
        else:
            roleID = string
        return int(roleID)
    except:
        return None
def getchannelID(string):
    """returns a channel ID from a mention string or from a channel ID string if the string has an accepted channel ID format"""
    string  = str(string)
    try:
        if search("<#.+>", string):
            channelID = string[2:20]
        else:
            channelID = string
        return int(channelID)
    except:
        return None
def parsetimestring(string):
    """returns an amount of seconds depending on what is entered, or returns None if no format is recognised"""
    string = string.lower()
    string.replace(" ", "")
    try:
        time = datetime.strptime(string, "%H:%M:%S")
    except:
        try:
            time = datetime.strptime(string, "%M:%S")
        except:
            try:
                time = datetime.strptime(string, "%Hh%Mm%Ss")
            except:
                try:
                    time = datetime.strptime(string, "%Hh%Mm")
                except:
                    try:
                        time = datetime.strptime(string, "%Hh%Ss")
                    except:
                        try:
                            time = datetime.strptime(string, "%Hh")
                        except:
                            try:
                                time = datetime.strptime(string, "%Mm%Ss")
                            except:
                                try:
                                    time = datetime.strptime(string, "%Mm")
                                except:
                                    try:
                                        time = datetime.strptime(string, "%Ss")
                                    except:
                                        try:
                                            time = datetime.strptime(string, "%S")
                                        except:
                                            return None
    time = time - datetime(1900, 1, 1)
    time = time.total_seconds()
    return time
#endregion

#tasks
#region

@tasks.loop(minutes=randrange(10,30))
#switches status
async def switchstatus():
    #sets random status
    status = choice(saistatuses)
    await client.change_presence(activity=discord.Activity(type=status[0], name=status[1]))
@switchstatus.before_loop
async def beforeswitchstatus():
    await client.wait_until_ready()

#endregion

#old events
#region


@client.event
async def on_ready():

    #returns login message to console
    print("Logged in as {0.user}".format(client))  
    print("Bot created on {0}".format(client.user.created_at))
    global starttime
    starttime = datetime.now()
    return


@client.event
async def on_connect():

    #sets random status
    status = choice(saistatuses)
    await client.change_presence(activity=discord.Activity(type=status[0], name=status[1]))
    return


@client.event
async def on_message(message):

    #precommand stuff
    #region
    
    #processes message
    content = message.content

    #if message is from Sai Bot or any Bot no action is taken
    if message.author == client.user or message.author.bot:
        return

    #endregion
    #if message is sent in Sai server's tester-recruitment, delete it and send me a dm
    if message.channel.id == 865877072131784724:
        if message.content.strip().startswith("s."):
            await message.delete()
            await message.channel.send(f"{message.author.mention} You can't run commands here!", delete_after=10)
            return
        if len(message.content) > 2048:
            await message.channel.send(f"{message.author.mention} Make sure your application is under or equal to 2048 characters!", delete_after=10)
            await message.delete(delay=10)
            return
        await message.delete()
        applicationembed = discord.Embed(title="New Application!", description=message.content, color=embedcolour)
        applicationembed.set_footer(text=f"Application is from {str(message.author)}")
        owner = await client.fetch_user(457517248786202625)
        await owner.send(embed=applicationembed)
        await message.channel.send(f"{message.author.mention} Your application was successful, please be patient while it is reviewed!", delete_after=10)

    #else if prefix is recognised
    elif content.startswith("s.") or content.startswith("S.") or (client.user.mentioned_in(message) and content.strip() == "<@!858663143931641857>"):

        #if in a DM channel, send a friendly embed message with an invite
        if isinstance(message.channel, discord.channel.DMChannel):
            dmembed=discord.Embed(title="Hello there user! <:info:881883500515590144>", description="You can't give me commands in DM's! Make sure to [invite Sai to your own server by clicking here](https://discord.com/oauth2/authorize?client_id=858663143931641857&permissions=120729185406&scope=bot) to run the commands for yourself! Also, join the [official discord server for Sai](https://discord.gg/BSFCCFKK7f) for any other support, questions, or suggestions for the bot!", color=embedcolour)
            dmembed.set_thumbnail(url=client.user.avatar_url)
            dmembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
            try:
                await message.channel.send(embed=dmembed)
            except:
                pass
            return
        
        
        #adds user to allcooldowns if they are not already in it
        adduser = True
        for user in allcooldowns:
            if int(user.userID) == int(message.author.id):
                adduser = False
                currentuser = allcooldowns[allcooldowns.index(user)]
                break
                
        if adduser:
            newuser = usercooldown(int(message.author.id)) 
            allcooldowns.append(newuser)
            currentuser = allcooldowns[-1]

        #get variables
        global commandsrun
        global starttime

        #increments commandsrun
        commandsrun += 1

        #processes the command entered
        if client.user.mentioned_in(message) and content.strip() == "<@!858663143931641857>":
            command = "help"
        else:
            command = content[2:].strip()

        
        #code for logging the command
        loggingtime = datetime.utcnow().strftime("%#A, %#d %#B\n%H:%M:%S:%f")

        loggingembed=discord.Embed(title="Command Executed", colour=embedcolour)
        loggingembed.add_field(name="Command", value=f"```{message.content}```", inline=True)
        loggingembed.add_field(name="Server", value=f"```{message.guild.name} (id:{message.guild.id})```", inline=True)
        loggingembed.add_field(name="Channel", value=f"```{message.channel.name} (id:{message.channel.id})```", inline=True)
        loggingembed.add_field(name="Time", value=f"```{loggingtime}```", inline=True)
        loggingembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
        await client.get_guild(859934506159833178).get_channel(881913733532758036).send(embed=loggingembed)
        
        #naruto
        #region

        if command[0:10] == "character " or command[0:5] == "char " or command[0:4] == "chr ":
            
            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.character + timedelta(seconds=charactercooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.character = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.character + timedelta(seconds=charactercooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("character", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return

            if command[0:10] == "character ":
                charactername = command[10:]
            elif command[0:5] == "char ":
                charactername = command[5:]
            else:
                charactername = command[4:]

            character = Characters.find(charactername)
            
            #if no character found
            if character == None:
                await message.channel.send("Make sure you enter the character correctly with no typos! Capitalisation does not matter. To check all supported characters, run `s.help characterlist`")
                return

            #get character info and post the embed 
            if len(character.aliases) >= 8:
                aliaslist = "\n".join(["*" + alias + "*" for alias in character.aliases[0:7]])
            else:
                aliaslist = ["*" + alias + "*" for alias in character.aliases[0:len(character.aliases)]]
                missingaliases = 8 - len(character.aliases)
                aliasfillerlines = missingaliases // 2
                for fillerline in range(aliasfillerlines):
                    aliaslist.insert(0, "­")
                    aliaslist.append("­")
                aliaslist = "\n".join(aliaslist)

            
            characterembed=discord.Embed(color=embedcolour)
            characterembed.add_field(name=f"{character.name}  {character.sexemoji}", value=f"""­\n{aliaslist}""", inline=True)
            characterembed.add_field(name="­", value=f"""­\n**Episode #{character.debut}**\n\n{character.rankemoji}\n{character.clanemoji}\n{"".join(character.naturetypeemojis)}\n{"".join(character.kekkeigenkaiemojis)}\n­""", inline=True)
            characterembed.set_image(url=character.image)
            characterembed.set_footer(text="Command run by {0}#{1} | Run 's.help character' for more info on how to understand all the information here!".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
            await message.channel.send(embed=characterembed)

        elif command[0:5] == "info " or command[0:12] == "information ":
            
            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.information + timedelta(seconds=informationcooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.information = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.information + timedelta(seconds=informationcooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("information", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return

            #find character and then
            if command[0:5] == "info ":
                charactername = command[5:]
            else:
                charactername = command[12:]

            character = Characters.find(charactername)
            
            #if no character found
            if character == None:
                await message.channel.send("Make sure you enter the character correctly with no typos! Capitalisation does not matter. To check all supported characters, run `s.help characterlist`")
                return
            
            #send first page
            pagenum = 1

            informationembed = discord.Embed(title=f"Information for {character.name}", color=embedcolour)
            informationembed.add_field(name="Name:", value=character.name, inline=False)
            informationembed.add_field(name="Aliases:", value=", ".join(character.aliases), inline=False)
            informationembed.add_field(name="Debut:", value=str(character.debut), inline=False)
            informationembed.set_image(url=character.image)
            informationembed.set_footer(text="Command run by {0}#{1} | Page {2} of 5 | Run 's.help information' for more info on how this command functions!".format(message.author.name, message.author.discriminator, pagenum), icon_url=message.author.avatar_url)

            informationmessage = await message.channel.send(embed=informationembed)
            
            #add reactions for pages
            await informationmessage.add_reaction("⬅️")
            await informationmessage.add_reaction("➡️")

            def check(reaction, user):
                return (user.id != 858663143931641857 and str(reaction.emoji) in ["⬅️", "➡️"])
            
            #try to wait for user reactions
            while True:
                
                try:
                    reaction, user = await client.wait_for("reaction_add", check=check, timeout=60)

                    #increment or decrement page number
                    if reaction.emoji == "⬅️":
                        if pagenum <= 1:
                            continue
                        else:
                            pagenum -= 1

                    elif reaction.emoji == "➡️":
                        if pagenum >= 5:
                            continue
                        else:
                            pagenum += 1


                    
                    #create and edit embed
                    informationembed = discord.Embed(title=f"Information for {character.name}", color=embedcolour)
                    
                    #get fields per page
                    if pagenum <= 1:
                        pagenum = 1
                        informationembed.add_field(name="Name:", value=character.name, inline=False)
                        informationembed.add_field(name="Aliases:", value=", ".join(character.aliases), inline=False)
                        informationembed.add_field(name="Debut:", value=str(character.debut), inline=False)
                    elif pagenum == 2:
                        informationembed.add_field(name="Kekkei Genkai:", value=("\n".join([character.kekkeigenkaiemojis[index] + " - " + character.kekkeigenkai[index] for index in range(len(character.kekkeigenkai))])), inline=False)
                        informationembed.add_field(name="Nature Types:", value=("\n".join([character.naturetypeemojis[index] + " - " + character.naturetypes[index] for index in range(len(character.naturetypes))])), inline=False)
                        informationembed.add_field(name="Clan:", value=(character.clanemoji + " - " + character.clan), inline=False)
                        informationembed.add_field(name="Affiliations:", value=("\n".join([character.affiliationemojis[index] + " - " + character.affiliations[index] for index in range(len(character.affiliations))])), inline=False)
                    elif pagenum == 3:
                        informationembed.add_field(name="Rank:", value=(character.rankemoji + " - " + character.rank), inline=False)
                        informationembed.add_field(name="Birth Date:", value=character.dob, inline=False)
                        informationembed.add_field(name="Sex:", value=(character.sexemoji + " - " + character.sex), inline=False)
                        informationembed.add_field(name="Height:", value=character.height, inline=False)
                        informationembed.add_field(name="Weight:", value=character.weight, inline=False)
                    elif pagenum == 4:
                        jutsustringnumber = 1
                        jutsustring = ""
                        jutsustringtwo = ""
                        jutsustringthree = ""
                        for jutsu in character.jutsu:
                            #choose which string to add to
                            if len(jutsustring) + len("*" + jutsu + "*,\n") > 1024 and jutsustringnumber == 1:
                                jutsustringnumber = 2
                            elif len(jutsustringtwo) + len("*" + jutsu + "*,\n") > 1024 and jutsustringnumber == 2:
                                jutsustringnumber = 3
                            
                            #add to correct string
                            if jutsustringnumber == 1:
                                if jutsu != character.jutsu[-1]:
                                    jutsustring += ("*" + jutsu + "*,\n")
                                else:
                                    jutsustring += ("*" + jutsu + "*")
                            elif jutsustringnumber == 2:
                                if jutsu != character.jutsu[-1]:
                                    jutsustringtwo += ("*" + jutsu + "*,\n")
                                else:
                                    jutsustringtwo += ("*" + jutsu + "*")
                            elif jutsustringnumber == 3:
                                if jutsu != character.jutsu[-1]:
                                    jutsustringthree += ("*" + jutsu + "*,\n")
                                else:
                                    jutsustringthree += ("*" + jutsu + "*")
                        
                        informationembed.add_field(name="Jutsu:", value=jutsustring, inline=False)
                        if jutsustringtwo != "":
                            informationembed.add_field(name="­", value=jutsustringtwo, inline=False)
                        if jutsustringthree != "":
                            informationembed.add_field(name="­", value=jutsustringthree, inline=False)

                    elif pagenum >= 5:
                        pagenum = 5
                        informationembed.add_field(name="Teams:", value=(",\n".join(character.team.split(","))), inline=False)
                        informationembed.add_field(name="Family:", value=(",\n".join(["**" + member + "**" for member in character.familymembers])), inline=False)

                    informationembed.set_image(url=character.image)
                    informationembed.set_footer(text="Command run by {0}#{1} | Page {2} of 5 | Run 's.help information' for more info on how this command functions!".format(message.author.name, message.author.discriminator, pagenum), icon_url=message.author.avatar_url)

                    await informationmessage.edit(embed=informationembed)
                    await reaction.remove(user)


                except asyncio.TimeoutError:
                    await informationmessage.clear_reactions()

        elif command == "naruto":
            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.character + timedelta(seconds=charactercooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.character = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.character + timedelta(seconds=charactercooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("character", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return

            #send prompt to run the command correctly
            await message.channel.send("Try running `s.character Naruto`!\nRun `s.help character` for more information.")

        #endregion
               
        #info
        #region

        #code for help command
        elif command[0:5] == "help " or command[0:2] == "h " or command == "help" or command == "h":

            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.help + timedelta(seconds=helpcooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.help = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.help + timedelta(seconds=helpcooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("help", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return

            #finds the command that is being asked for help
            if command[0:4] == "help":
                helpcommand = command[4:].strip()
            else:
                helpcommand = command[1:].strip()

            #if 's.help' is run return list of commands
            if helpcommand == "":
                helpembed=discord.Embed(title="Help <:help:881883309142077470>", description="\n**Prefix - **`s.`\n\nHere is a list of all of Sai's commands.\nIf you would like a feature to be implemented, join the [official discord server for Sai](https://discord.gg/BSFCCFKK7f).\n\nTo get help for a specific command, run **`s.help <command>`**", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="<:naruto:886208833393938452> Naruto", value="```character, information```", inline=False)
                helpembed.add_field(name="<:info:881883500515590144> Info", value="```about, help, links (/vote/server/invite), patreon (/donate/premium), profile, statistics, testcount```", inline=False)
                helpembed.add_field(name="<:utility:881883277424746546> Utility", value="```editsnipe, event, nickname, ping, rescue, snipe, time, vote reminder```", inline=False)
                helpembed.add_field(name="<:moderation_and_admin:881897640948826133> Moderation and Admin", value="```ban, kick, lockdown, message, purge, role, slowmode, unlockdown```", inline=False)
                helpembed.add_field(name="<:fun:881899126286061609> Fun", value="```decide, gif, quote, tulaiiisabigman, 8ball```", inline=False)
                helpembed.set_footer(text="Command run by {0}#{1} | If you want me to make a private version of the bot for your server, or add custom commands, or you simply want to make suggestions, get in contact with the owner of the bot, jlc, by joining the official Sai Support server.".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)

            
            #naruto
            #region

            #if 's.help character' is run
            elif helpcommand == "character" or helpcommand == "char" or helpcommand == "chr":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `character` <:naruto:886208833393938452>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `character` command is used to get general information and an image of any Naruto character! **BEWARE OF SPOILERS** For a list of all characters available, run 's.help characterlist'", inline=False)
                helpembed.add_field(name="How to use it", value="```s.character [character name] or [character alias]```For Example:```s.character Sai```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Naruto\n**Aliases:** ```character, char, chr```\n**Cooldown**: `{0}` seconds\n**Delimiter:** None".format(charactercooldown), inline=False)
                helpembed.add_field(name="How to read the information!", value=" - On the top left of the message will be a list of aliases, which are in *italics*\n - On the top right of the message will be the debut episode, which is in **bold**. If the debut is in Naruto Shippuden or Boruto, the episode number will be the episode number plus the number of episodes in the preceding titles. e.g. A debut in episode 3 of Naruto Shippuden, will have the debut listed as **Episode #223**, since `220 + 3 = 223`.\n - Below the debut will be a list of emojis, of which there are four rows:\n­       + The first row denotes the character's highest achieved rank.\n­       + The second row denotes the character's clan\n­       + The third row denotes the character's nature types\n­       + The fourth and last row denotes the character's kekkei genkai.", inline=False)
                helpembed.add_field(name="Extra Info", value="This command uses material from the [“Characters”](https://naruto.fandom.com/wiki/Category:Characters) articles on the [Naruto wiki](https://naruto.fandom.com) at [Fandom](https://www.fandom.com) and is licensed under the [Creative Commons Attribution-Share Alike License](https://creativecommons.org/licenses/by-sa/3.0/).", inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)

            elif helpcommand == "info" or helpcommand == "information":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `information` <:naruto:886208833393938452>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `information` command is used to get very specific information and an image of any Naruto character! **BEWARE OF SPOILERS** For a list of all characters available, run 's.help characterlist'", inline=False)
                helpembed.add_field(name="How to use it", value="```s.information [character name] or [character alias]```For Example:```s.information Sai```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Naruto\n**Aliases:** ```information, info```\n**Cooldown**: `{0}` seconds\n**Delimiter:** None".format(informationcooldown), inline=False)
                helpembed.add_field(name="How to read the information!", value="On the 1st page:\n­ - Full Name\n­ - Aliases\n­ - Debut\nOn the 2nd page:\n­ - Kekkei Genkai and Emojis\n­ - Nature Types and Emojis\n­ - Clan and Emoji\n­ - Affiliations and Emojis\nOn the 3rd page:\n­ - Rank\n­ - Birth Date\n­ - Sex and Emoji\n­ - Height\n­ - Weight\nOn the 4th page:\n­ - Jutsu List\nOn the 5th page:\n­ - Team List\n­ - Family Members List", inline=False)
                helpembed.add_field(name="Extra Info", value="This command uses material from the [“Characters”](https://naruto.fandom.com/wiki/Category:Characters) articles on the [Naruto wiki](https://naruto.fandom.com) at [Fandom](https://www.fandom.com) and is licensed under the [Creative Commons Attribution-Share Alike License](https://creativecommons.org/licenses/by-sa/3.0/).", inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)
            #endregion
            
            #info
            #region

            #if 's.help about' is run
            elif helpcommand == "about" or helpcommand == "abt":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `about` <:info:881883500515590144>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `about` command is used to get general information about the bot.", inline=False)
                helpembed.add_field(name="How to use it", value="```s.about```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Info\n**Aliases:** ```about, abt```\n**Cooldown**: `{0}` seconds\n**Delimiter:** None".format(aboutcooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)
            
            #if 's.help help' is run
            elif helpcommand == "help" or helpcommand == "h":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `help` <:help:881883309142077470>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `help` command is useful for new users to discover all of Sai's commands, and how to use them.", inline=False)
                helpembed.add_field(name="How to use it", value="```s.help (command)```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Info\n**Aliases:** ```help, h```\n**Cooldown**: `{0}` seconds\n**Delimiter:** ` `".format(helpcooldown), inline=False)
                helpembed.add_field(name="Extra Info", value="When running the `help` command on a specific command, the 'How to use it' field may seem confusing at first. There are three types of brackets which may show up here:\n`()` means this parameter is optional\n`[]` means this paramter is necessary\n`{}` means the value inside is the default paramter passed into the command if there are no user-passed paramters", inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)

            #if 's.help links' is run
            elif helpcommand == "links" or helpcommand == "server" or helpcommand == "invite" or helpcommand == "vote":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `links` <:info:881883500515590144>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `links` command is useful for voting for Sai, inviting Sai to your own server, getting an invite to the Official Support Server for Sai, and more.", inline=False)
                helpembed.add_field(name="How to use it", value="```s.links```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Info\n**Aliases:** ```links, server, invite, vote```\n**Cooldown**: `{0}` seconds\n**Delimiter:** None".format(linkscooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)
            
            #if 's.help patreon' is run
            elif helpcommand == "patreon" or helpcommand == "donate" or helpcommand == "premium":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `patreon` <:info:881883500515590144>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `patreon` command is used to get information on supporting Sai through Patreon!", inline=False)
                helpembed.add_field(name="How to use it", value="```s.patreon```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Info\n**Aliases:** ```patreon, donate, premium```\n**Cooldown**: `{0}` seconds\n**Delimiter:** None".format(patreoncooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)

            #if 's.help profile' is run
            elif helpcommand == "profile" or helpcommand == "p" or helpcommand == "userinfo":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `profile` <:info:881883500515590144>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `profile` command returns a list of information about mentioned user*, or by default, the user that ran the command. You can also use this command to customise† your own profile!", inline=False)
                helpembed.add_field(name="How to use it", value="To look at a certain user's profile:```s.profile {Command user} or (Mentioned user)```To customise your own profile:```s.profile customise/cust```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Info\n**Aliases:** ```profile, p, userinfo```\n**Cooldown**: `{0}` seconds\n**Delimiter:** ` `".format(profilecooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1} | *If multiple users are mentioned then there is no guarantee that the first mentioned member's profile will be shown. This is a limitation with discord itself, and there is nothing that can be done about this sadly. (Just mention who's profile you want to see!) | †Each answer of the custom profile has to have 115 or less characters due to resrictions in discord's embeds! If you think this should be changed, put it in bot-suggestions on the official discord server. To join the server click the link in `s.help`!".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)
            
            #if 's.help statistics' is run
            elif helpcommand == "statistics" or helpcommand == "stats" or helpcommand == "status":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `statistics` <:info:881883500515590144>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `statistics` command is used to get much more specific information about the bot, including its number of channels, and its CPU and RAM usage, for anyone who is interested.", inline=False)
                helpembed.add_field(name="How to use it", value="```s.statistics```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Info\n**Aliases:** ```statistics, stats, status```\n**Cooldown**: `{0}` seconds\n**Delimiter:** None".format(statisticscooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)

            #if 's.help testcount' is run
            elif helpcommand == "testcount" or helpcommand == "tc":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `testcount` <:info:881883500515590144>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `testcount` command is used to get the amount of times a user/users have tested in the Sai Support Server. It can only be used here because of the fact that testing goes on in this server. [Click here to join the Sai Support Server.](https://top.gg/servers/859934506159833178)", inline=False)
                helpembed.add_field(name="How to use it", value="To get the testcount for one members:```s.testcount {Command Member} or (Mentioned Member or Member ID)```To get the testcount for all members:```s.testcount all/list```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Info\n**Aliases:** ```testcount, tc```\n**Cooldown**: `{0}` seconds\n**Delimiter:** ` `".format(testcountcooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)
            
            #endregion

            #utility
            #region
            
            #if 's.help editsnipe' is run
            elif helpcommand == "editsnipe" or helpcommand == "es":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `editsnipe` <:utility:881883277424746546>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `editsnipe` command returns the latest edited message.", inline=False)
                helpembed.add_field(name="How to use it", value="```s.editsnipe```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Utility\n**Aliases:** ```editsnipe, es```\n**Cooldown**: `{0}` seconds\n**Delimiter:** None".format(editsnipecooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)
            
            #if 's.help event' is run
            elif helpcommand == "event" or helpcommand == "evt" or helpcommand == "ev":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `event` <:utility:881883277424746546>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `event` command is used for finding attendance to an event, by sending a member reactable message to the desired channel with the user-defined title and description. Available to members with admin perms or higher only.", inline=False)
                helpembed.add_field(name="How to use it", value="```s.event [channel ID] or [channel mention] | [Event Title] | (Event Description)```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Utility\n**Aliases:** ```event, evt, ev```\n**Cooldown**: `{0}` seconds\n**Delimiter:** `|`".format(eventcooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)  
        
            #if 's.help nickname' is run
            elif helpcommand == "nickname" or helpcommand == "nick":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `nickname` <:utility:881883277424746546>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `nickname` command is used to set or reset your own nickame.", inline=False)
                helpembed.add_field(name="How to use it", value="To set your nickname:```s.nickname (new nickname)```To reset your nickname:```s.nickname reset/default```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Utility\n**Aliases:** ```nickname, nick```\n**Cooldown**: `{0}` seconds\n**Delimiter:** None".format(nicknamecooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)

            #if 's.help ping' is run
            elif helpcommand == "ping":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `ping` <:utility:881883277424746546>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `ping` command is used to find your latency in `ms` to the Sai bot.", inline=False)
                helpembed.add_field(name="How to use it", value="```s.ping```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Utility\n**Aliases:** ```ping```\n**Cooldown**: `{0}` seconds\n**Delimiter:** None".format(pingcooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)
            
            #if 's.help rescue' is run
            elif helpcommand == "rescue" or helpcommand == "resc" or helpcommand == "r":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `rescue` <:utility:881883277424746546>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `rescue` nulls the effects of the `snipe` and `editsnipe` commands easily, if you need a quick rescue without manually deleting/editing another message respectively ;)", inline=False)
                helpembed.add_field(name="How to use it", value="```s.rescue```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Utility\n**Aliases:** ```rescue, resc, r```\n**Cooldown**: `{0}` seconds\n**Delimiter:** None".format(rescuecooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)
            
            #if 's.help snipe' is run
            elif helpcommand == "snipe" or helpcommand == "s":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `snipe` <:utility:881883277424746546>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `snipe` command returns the latest edited message.", inline=False)
                helpembed.add_field(name="How to use it", value="```s.snipe```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Utility\n**Aliases:** ```snipe, s```\n**Cooldown**: `{0}` seconds\n**Delimiter:** None".format(snipecooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)
            
            #if 's.help time' is run
            elif helpcommand == "time" or helpcommand == "t":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `time` <:utility:881883277424746546>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `time` command is used for finding the time in one or a variety of timezones.", inline=False)
                helpembed.add_field(name="How to use it", value="To display desired timezone:```s.time {UTC}, (timezone#1), (timezone#2), ... , (timezone#n)```To display all timezones:```s.time all/ALL```Get timezones wikipedia page for more info:```s.time wiki/wikipedia```\n*Note: timezones should be written in their shortened form (e.g. IST, BST, GMT, est, pst, ast)*", inline=False)
                helpembed.add_field(name="About", value="**Category:** Utility\n**Aliases:** ```time, t```\n**Cooldown**: `{0}` seconds\n**Delimiter:** `,`".format(timecooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1} | For Sai's accepted timezones, run 's.help timezones'".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)

            #if 's.help vote reminder' is run
            elif helpcommand == "vote reminder" or helpcommand == "remind" or helpcommand == "vote remind" or helpcommand == "votereminder":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `vote reminder` <:utility:881883277424746546>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `vote reminder` command is used for notifying the user when they can vote again, DMing the user after 12 hours of the command being run.", inline=False)
                helpembed.add_field(name="How to use it", value="```s.vote reminder```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Utility\n**Aliases:** ```vote reminder, remind, vote remind, votereminder```\n**Cooldown**: `{0}` seconds\n**Delimiter:** None".format(voteremindercooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1} | Note that DMs have to be open for this command to work, this is to stop channels potentially being clogged due to reminders.".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)
            
            #endregion 
        
            #moderation and admin
            #region

            #if 's.help ban' is run
            elif helpcommand == "ban":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `ban` <:moderation_and_admin:881897640948826133>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `ban` command is used to ban a specified user. Note that to run this command you need to have user banning perms.", inline=False)
                helpembed.add_field(name="How to use it", value="```s.ban [user ID] or [user mention] | (reason)```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Moderation and Admin\n**Aliases:** ```ban```\n**Cooldown**: `{0}` seconds\n**Delimiter:** `|`".format(bancooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)

            #if 's.help kick' is run
            elif helpcommand == "kick":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `kick` <:moderation_and_admin:881897640948826133>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `kick` command is used to kick a specific user. Note that to run this command you need to have user kicking perms.", inline=False)
                helpembed.add_field(name="How to use it", value="```s.kick [user ID] or [user mention] | (reason)```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Moderation and Admin\n**Aliases:** ```kick```\n**Cooldown**: `{0}` seconds\n**Delimiter:** `|`".format(kickcooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)
            
            #if 's.help lockdown' is run
            elif helpcommand == "lockdown" or helpcommand == "lock" or helpcommand == "shush" or helpcommand == "shutup":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `lockdown` <:moderation_and_admin:881897640948826133>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `lockdown` command is used to prevent users from sending messages on a channel, essentially muting them on the specified channel. Note that to run this command you need to have manage permission permissions.", inline=False)
                helpembed.add_field(name="How to use it", value="```s.lockdown {current channel} (channel ID or channel mention)```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Moderation and Admin\n**Aliases:** ```lockdown, lock, shush, shutup```\n**Cooldown**: `{0}` seconds\n**Delimiter:** ` `".format(lockdowncooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)
            
            #if 's.help message' is run
            elif helpcommand == "message" or helpcommand == "msg":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `message` <:moderation_and_admin:881897640948826133>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `message` command is used to make Sai send a message to a specific channel. Note that to run this command you need to have admin perms or higher.", inline=False)
                helpembed.add_field(name="How to use it", value="```s.message [channel ID] or [channel mention] | [message]```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Moderation and Admin\n**Aliases:** ```message, msg```\n**Cooldown**: `{0}` seconds\n**Delimiter:** `|`".format(messagecooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)

            #if 's.help purge' is run
            elif helpcommand == "purge" or helpcommand == "finesse" or helpcommand == "annihilate":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `purge` <:moderation_and_admin:881897640948826133>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `purge` command is used to bulk delete a range of messages. Note that to run this command you need to have manage messages perms.", inline=False)
                helpembed.add_field(name="How to use it", value="```s.purge [number of messages to delete]```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Moderation and Admin\n**Aliases:** ```purge, finesse, annihilate```\n**Cooldown**: `{0}` seconds\n**Delimiter:** None".format(purgecooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)

            #if 's.help role' is run
            elif helpcommand == "role":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `role` <:moderation_and_admin:881897640948826133>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `role` command is a very powerful command which has multiple uses. \n  -  Firstly, it can add or remove roles from a user.\n  -  Secondly, it can display information about a specific role.\n  -  Thirdly, it can display information about all roles. \n  -  Lastly, it can display information about all the roles of a specific user.\nNote that to run this command you need to have manage roles perms.", inline=False)
                helpembed.add_field(name="How to use it", value="To add/remove a role: ```s.role add/give [user mention] or [user ID] [role mention] or [role ID]``````s.role remove/take [user mention] or [user ID] [role mention] or [role ID]```To get info about all roles: ```s.role information/info list/all```To get info about a singular role: ```s.role information/info [role mention] or [role ID]```To get all role info about a singular user: ```s.role information/info {command user} or [user mention] or [user ID]```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Moderation and Admin\n**Aliases:** ```role, r```\n**Cooldown**: `{0}` seconds\n**Delimiter:** ` `".format(rolecooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1} | This command is experimental, so if any bugs occur ping me on the Sai bot official server.".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)
            
            #if 's.help slowmode' is run
            elif helpcommand == "slowmode" or helpcommand == "slow" or helpcommand == "sm":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `slowmode` <:moderation_and_admin:881897640948826133>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `slowmode` command allows a user to toggle on and off slowmode for channels, and set a desired duration. Note that to run this command you need to have manage channel perms.", inline=False)
                helpembed.add_field(name="How to use it", value="General command notation for turning on slowmode:```s.slowmode {current channel} or (desired channel mention or ID) {30seconds} or (desired slowmode time <MAX 6 HOURS>)```General command notation for turning off slowmode:```s.slowmode {current channel} or (channel mention or ID) off / false```\nExamples:\nSlowmode current channel for certain time -```s.slowmode hours:minutes:seconds```Slowmode certain channel for default time -```s.slowmode #channel-name```Slowmode certain channel for certain time -```s.slowmode channelID minutes:seconds```Slowmode current channel for default time -```s.slowmode```Turn off slowmode for current channel -```s.slowmode off```Turn off slowmode for certain channel -```s.slowmode #channel-name false```\n (This list of examples is not exhaustive, so experiment!!)", inline=False)
                helpembed.add_field(name="About", value="**Category:** Moderation and Admin\n**Aliases:** ```slowmode, slow, sm```\n**Cooldown**: `{0}` seconds\n**Delimiter:** ` `".format(slowmodecooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1} | For accepted time formats, run 's.help timeformats'".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)

            #if 's.help unlockdown' is run
            elif helpcommand == "unlockdown" or helpcommand == "unlock" or helpcommand == "unshush" or helpcommand == "antishutup":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `lockdown` <:moderation_and_admin:881897640948826133>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `unlockdown` command is used to reverse the effects of the `lockdown` command. Note that to run this command you need to have the manage permissions permission.", inline=False)
                helpembed.add_field(name="How to use it", value="```s.unlockdown {current channel} (channel ID or channel mention)```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Moderation and Admin\n**Aliases:** ```unlockdown, unlock, unshush, antishutup```\n**Cooldown**: `{0}` seconds\n**Delimiter:** ` `".format(unlockdowncooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)
            
            #endregion

            #fun
            #region

            #if 's.help decide' is run
            elif helpcommand == "decide" or helpcommand == "choose" or helpcommand == "roll":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `decide` <:fun:881899126286061609>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `decide` command returns a random choice from the entered choices.", inline=False)
                helpembed.add_field(name="How to use it", value="```s.decide (choice#1), (choice#2), ... , (choice#n)```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Fun\n**Aliases:** ```decide, choose, roll```\n**Cooldown**: `{0}` seconds\n**Delimiter:** `,`".format(decidecooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)

            #if 's.help gif' is run
            elif helpcommand == "gif":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `gif` <:fun:881899126286061609>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `gif` command returns a random Sai gif.", inline=False)
                helpembed.add_field(name="How to use it", value="```s.gif```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Fun\n**Aliases:** ```gif```\n**Cooldown**: `{0}` seconds\n**Delimiter:** None".format(gifcooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)

            #if 's.help quote' is run
            elif helpcommand == "quote":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `quote` <:fun:881899126286061609>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `quote` command returns a random Sai quote.\n**Note: If you havent finished Naruto and Naruto Shippuden be wary when clicking on spoilers :)**", inline=False)
                helpembed.add_field(name="How to use it", value="```s.quote```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Fun\n**Aliases:** ```quote```\n**Cooldown**: `{0}` seconds\n**Delimiter:** None".format(quotecooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)
                  
            #if 's.help tulaiiisabigman' is run
            elif helpcommand == "tulaiiisabigman":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `tulaiiisabigman` <:fun:881899126286061609>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `tulaiiisabigman` command gives the spiciest gif of the week, found by my specialist gif curator: tulaii✿#6598", inline=False)
                helpembed.add_field(name="How to use it", value="```s.tulaiiisabigman```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Fun\n**Aliases:** ```tulaiiisabigman```\n**Cooldown**: `{0}` seconds\n**Delimiter:** None".format(tulaiiisabigmancooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)

            #if 's.help 8ball' is run
            elif helpcommand == "8ball":
                helpembed=discord.Embed(title="Help", description="Command specific help for: `8ball` <:fun:881899126286061609>", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="Description", value="The `8ball` command lets Sai give a response to your yes/no question", inline=False)
                helpembed.add_field(name="How to use it", value="```s.8ball (question)```", inline=False)
                helpembed.add_field(name="About", value="**Category:** Fun\n**Aliases:** ```8ball```\n**Cooldown**: `{0}` seconds\n**Delimiter:** None".format(eightballcooldown), inline=False)
                helpembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)

            #endregion

            #other
            #region

            #if 's.help timeformats' is run
            elif helpcommand == "timeformats":
                helpembed=discord.Embed(title="Help", description="List of all accepted timeformats for Sai bot. If you want to request one to be added, ping me on the official Sai bot server.", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="<:clock:881899619364253706> Timeformats: ", value="`H:M:S` -> e.g. 12:15:34 means *12 hours 15 minutes and 34 seconds*\n`M:S` -> e.g. 15:34 means *15 minutes and 34 seconds*\n`S` -> e.g. 34 means *34 seconds*\n`HhMmSs` -> e.g. 8h56m23s means *8 hours 56 minutes and 23 seconds*\n`HhMm` -> e.g. 8h56m means *8 hours and 56 minutes*\n`HhSs` -> e.g. 8h23s means *8 hours and 23 seconds*\n`Hh` -> e.g. 8h means *8 hours*\n`MmSs` -> e.g. 56m23s means *56 minutes and 23 seconds*\n`MmSs` -> e.g. 56m23s means *56 minutes and 23 seconds*\n`Mm` -> e.g. 56m means *56 minutes*\n`Ss` -> e.g. 23s means *23 seconds*", inline=False)
                helpembed.set_footer(text="Command run by {0}#{1} | Note, any spaces or changes of case will not affect the parsing of your entered time string.".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)

            #if 's.help timezones'
            elif helpcommand == "timezones":
                helpembed=discord.Embed(title="Help", description="List of all accepted timezones for Sai bot. If you want to request one to be added, ping me on the official Sai bot server.", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="<:clock:881899619364253706> Timezones: ", value="`GMT` -> UTC + 0\n`UTC` -> UTC + 0\n`ECT` -> UTC + 1\n`BST` -> UTC + 1\n`EET` -> UTC + 2\n`ART` -> UTC + 2\n`EAT` -> UTC + 3\n`MET` -> UTC + 3.5\n`NET` -> UTC + 4\n`PLT` -> UTC + 5\n`IST` -> UTC + 5.5\n`VST` -> UTC + 7\n`CTT` -> UTC + 8\n`JST` -> UTC + 9\n`ACT` -> UTC + 9.5\n`AET` -> UTC + 10\n`SST` -> UTC + 11\n`NST` -> UTC + 12\n`MIT` -> UTC - 11\n`HST` -> UTC - 10\n`AST` -> UTC - 9\n`PST` -> UTC - 8\n`PNT` -> UTC - 7\n`MST` -> UTC - 7\n`CST` -> UTC - 6\n`EST` -> UTC - 5\n`IET` -> UTC - 5\n`PRT` -> UTC - 4\n`CNT` -> UTC - 3.5\n`AGT` -> UTC - 3\n`BET` -> UTC - 3\n`CAT` -> UTC - 1", inline=False)
                helpembed.set_footer(text="Command run by {0}#{1} | Note, any changes of case will not affect the parsing of your entered timezone.".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed)

            #if 's.help characterlist'
            elif helpcommand == "characterlist":
                characterlist = Characters.list()
                charactercount = characterlist[0]
                characterlist = characterlist[1:]

                #open SaiCharacterlist.txt files, write the Characters.list() list to the file and then add it to the embed as a text file.
                characterlistfile = open("SaiCharacterlist.txt", "w")
                with characterlistfile as f: 
                    for character in characterlist:
                        f.write(str(characterlist.index(character) + 1) + ". " + character + ",\n")

                helpembed=discord.Embed(title="Help", description="List of all accepted characters for Sai bot. If you want to request one to be added, ping me on the official Sai bot server.", color=embedcolour)
                helpembed.set_thumbnail(url=client.user.avatar_url)
                helpembed.add_field(name="<:naruto:886208833393938452> Characters:", value=f"**# of Characters: {charactercount}**\n\nFor the list of characters look into the attached .txt file named SaiCharacterlist.txt\n\nMake sure to dowload the full file to see all lines.\n\nHappy Sai'ing! <:sai:881902408786120715> ", inline=False)
                helpembed.set_footer(text="Command run by {0}#{1} | Note, any changes of case will not affect the parsing of your entered character.".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=helpembed, file=discord.File(r".\SaiCharacterlist.txt"))

            #endregion
        
        #code for about command
        elif command == "about" or command == "abt":

            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.about + timedelta(seconds=aboutcooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.about = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.about + timedelta(seconds=aboutcooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("about", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return

            uptime = datetime.now() - starttime
            uptime = str(uptime).split(".")[0]
            guilds = client.guilds
            servernum = len(guilds)
            usernum = len(client.users)

            owner = await client.fetch_user(457517248786202625)
            ownername = "{}#{}".format(owner.name, owner.discriminator)
            owneravatar = owner.avatar_url 
        
            aboutembed=discord.Embed(title="About <:info:881883500515590144>", colour=embedcolour)
            aboutembed.set_author(name="Bot created by {0}".format(ownername), icon_url=owneravatar)
            aboutembed.set_thumbnail(url=client.user.avatar_url)
            aboutembed.add_field(name="Name", value="Sai", inline=True)
            aboutembed.add_field(name="Time", value="Uptime: `{0}`\nCreated: `Sunday, 27 June 2021`".format(uptime), inline=True)
            aboutembed.add_field(name="Servers", value="Sai is in `{0}` servers".format(servernum), inline=False)
            aboutembed.add_field(name="Users", value="Sai can see `{0}` users".format(usernum), inline=True)
            aboutembed.add_field(name="Version", value="<:sai:881902408786120715> Sai ({0})\n<:python:881906567325302844> Python (3.9.7)\n<:discordpy:881907255639941151> discord.py (1.7.3)".format(version), inline=True)
            aboutembed.add_field(name="Libraries", value="```{0}```".format(libraries), inline=False)
            aboutembed.add_field(name="Invite the bot", value="[Invite Here!](https://discord.com/api/oauth2/authorize?client_id=858663143931641857&permissions=8&scope=bot)", inline=True)
            aboutembed.add_field(name="Colour", value="Hex - #d6d6d6\nRGB - 214, 214, 214", inline=True)
            aboutembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
            await message.channel.send(embed=aboutembed)
                       
        #code for links command
        elif command == "links" or command == "server" or command == "invite" or command == "vote":

            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.links + timedelta(seconds=linkscooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.links = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.links + timedelta(seconds=linkscooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("links", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return
        
            owner = await client.fetch_user(457517248786202625)
            ownername = "{}#{}".format(owner.name, owner.discriminator)
            owneravatar = owner.avatar_url
            
            linksembed=discord.Embed(title="Links <:info:881883500515590144>", colour=embedcolour)
            linksembed.set_author(name="Bot created by {0}".format(ownername), icon_url=owneravatar)
            linksembed.set_thumbnail(url=client.user.avatar_url)
            linksembed.add_field(name="Invite Sai to your server:", value="[Click here to invite.](https://discord.com/api/oauth2/authorize?client_id=858663143931641857&permissions=8&scope=bot)", inline=True)
            linksembed.add_field(name="Get support on Sai's official server:", value="[Click here to join.](https://discord.com/invite/BSFCCFKK7f)", inline=True)
            linksembed.add_field(name="Support me by voting for Sai on top.gg:", value="[Click here to vote.](https://top.gg/bot/858663143931641857)", inline=True)
            linksembed.add_field(name="Other links:", value="<:python:881906567325302844> [Python](https://www.python.org)\n<:discordpy:881907255639941151> [Discord.py](https://discordpy.readthedocs.io/en/stable/#getting-started)", inline=False)
            linksembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
            await message.channel.send(embed=linksembed)

        #code for patreon command
        elif command == "patreon" or command == "donate" or command == "premium":
            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.patreon + timedelta(seconds=patreoncooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.patreon = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.patreon + timedelta(seconds=patreoncooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("patreon", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return

            #creates embed and sends
            patreonembed=discord.Embed(title="The best way to support Sai", description=f"If you are looking for a way to customise Sai for your server, or simply want to show your support for the bot, we have opened a Patreon page to do so, adding to the many ways you can support the bot! If you want other tiers to be included or anything along those lines, feel free to ping the owner ({str(client.get_user(457517248786202625))}) in [The Official Sai Support Server](https://discord.com/invite/BSFCCFKK7f).", color=0xd6d6d6)
            patreonembed.set_author(name="Support Sai on Patreon:\nhttps://www.patreon.com/officialsaibot", icon_url=client.get_user(216303189073461248).avatar_url)
            patreonembed.set_thumbnail(url=client.user.avatar_url)
            patreonembed.add_field(name="Tier Ⅰ - Rasengan", value="- Advisor role\n- Tier Ⅰ Supporter role", inline=True)
            patreonembed.add_field(name="Tier Ⅱ - Tailed Beast Ball", value="\n- Advisor role\n- Custom Bot Avatar\n- Custom Bot Name\n- Tier Ⅱ Supporter role", inline=True)
            patreonembed.add_field(name="Tier Ⅲ - Tailed Beast Ball Rasenshuriken", value="- Advisor role\n- Custom Bot Avatar\n- Custom Bot Name\n- Up to 5 Server\n Specific Commands\n- Tier Ⅲ Supporter role", inline=True)
            patreonembed.add_field(name="Become a Patron Now:", value="[Click here](https://www.patreon.com/officialsaibot) for the official Patreon page for Sai. (Note the roles refer to ones within the Official Sai Support Server)", inline=False)
            patreonembed.set_footer(text="Command run by {0}#{1} | Have a great day!".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
            await message.channel.send(embed=patreonembed)
        
        #code for profile command
        elif command == "profile" or command[0:8] == "profile " or command == "p" or command[0:2] == "p " or command == "userinfo" or command[0:9] == "userinfo ":

            ### THE PROFILEID COLUMN IN THE DB IS CREATED BY APPENDING THE USERID TO THE GUILDID ###
            
            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.profile + timedelta(seconds=profilecooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.profile = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.profile + timedelta(seconds=profilecooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("profile", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return
            
            #gets user

            profilementionuser = ""
            #if noone mentioned the user is the sender
            if command == "profile" or command == "p" or command == "userinfo":
                profilementionuser = message.author
            #if there are any mentions then show the profile and it is not customisation
            if (message.mentions and (not (command == "profile customise" or command == "p customise" or command == "userinfo customise" or command == "profile customize" or command == "p customize" or command == "userinfo customize" or command == "p cust"or command == "profile cust" or command == "userinfo cust")))  or profilementionuser != "":
                #if the command was s.profile @user get the user
                if profilementionuser == "":
                    try:
                        profilementionuser = message.mentions[0]
                    except:
                        profileembed = discord.Embed(title="Profile Cmd Error: ", color=embedcolour)
                        profileembed.add_field(name="Mention Error: ", value = "Make sure you have mentioned a valid user.")
                        profileembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                        await message.channel.send(embed=profileembed)
                        return     
        
                #gets roles
                rolelist = profilementionuser.roles
                rolementions = [role.mention for role in rolelist if role != message.guild.default_role]
                rolementions = " ".join(rolementions)
                
                #get activity
                profileactivity = profilementionuser.activity
                if profileactivity is None:
                    profileactivitymsg = "Nothing!"
                elif isinstance(profileactivity, Spotify):
                    profileactivitymsg = "Listening to **{0}** by **{1}**".format(profileactivity.title, profileactivity.artist)
                elif profileactivity.type == ActivityType.competing:
                    profileactivitymsg = "Competing in **{0}**".format(profileactivity.name)
                elif profileactivity.type == ActivityType.custom:
                    profileactivitymsg = "Custom activity (Sai cannot show this because of custom emojis that could be used in this type of activity!)"
                elif profileactivity.type == ActivityType.listening:
                    profileactivitymsg = "Listening to **{0}**".format(profileactivity.name)
                elif profileactivity.type == ActivityType.playing:
                    profileactivitymsg = "Playing **{0}**".format(profileactivity.name)
                elif profileactivity.type == ActivityType.streaming:
                    profileactivitymsg = "Streaming **{0}**".format(profileactivity.name)
                elif profileactivity.type == ActivityType.watching:
                    profileactivitymsg = "Watching **{0}**".format(profileactivity.name)
                elif profileactivity.type == ActivityType.unknown:
                    profileactivitymsg = "Sai doesn't know : ("
                else:
                    profileactivitymsg = "Sai doesn't know : ("

                #get custom data from db
                if profilementionuser.id == 858663143931641857:
                    profileid = "858663143931641857"
                else:
                    profileid = str(message.guild.id) + str(profilementionuser.id)

                dbconnection = sqlite3.connect(database)
                cursor = dbconnection.cursor()
                cursor.execute(f"""SELECT * FROM profiles WHERE profileid="{profileid}" """)

                customprofile = cursor.fetchall()
                if customprofile == []:
                    customprofile = [["Not customised!"] * 9]

                customprofile = [option for option in customprofile[0]]
                for option in customprofile:
                    if str(option).lower() == "skip":
                        customprofile[customprofile.index(option)] = ""
                
                profileembed=discord.Embed(title="Profile <:info:881883500515590144>", description="Information on requested user below: ", color=embedcolour)
                profileembed.set_thumbnail(url=profilementionuser.avatar_url)
                profileembed.add_field(name="­Name: ", value="User nickname: `{0}` \nUsername: `{1}#{2}`".format(profilementionuser.nick, profilementionuser.name, profilementionuser.discriminator), inline=False)
                profileembed.add_field(name="Timings: ", value="Joined this server: <t:{0}:R> \nJoined discord: <t:{1}:R>".format(int(profilementionuser.joined_at.timestamp()//1), int(profilementionuser.created_at.timestamp()//1)), inline=False)
                profileembed.add_field(name="Roles: ", value="Role number: `{0}`\nRoles: {1}".format(len(profilementionuser.roles) - 1, rolementions), inline=False)
                profileembed.add_field(name="Activity: ", value=profileactivitymsg, inline=False)
                profileembed.add_field(name="Custom: ", value=f"**Name:** {customprofile[1]}\n**Pronouns:** {customprofile[2]}\n**Age:** {customprofile[3]}\n**Nickname(s):** {customprofile[4]}\n**Favourite colour:** {customprofile[5]}\n**Likes:** {customprofile[6]}\n**Dislikes:** {customprofile[7]}\n**Hobbies:** {customprofile[8]}", inline=False)
                profileembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=profileembed)

            #else if the command run is s.profile customize/customise, or s.p cust, then make Sai ask questions, and then write to database
            elif command == "profile customise" or command == "p customise" or command == "profile customize" or command == "p customize" or command == "p cust"or command == "profile cust":

                def check(waitformsg):
                    return ((waitformsg.author == message.author) and (waitformsg.channel == message.channel))
                
                #ask questions and gather answers
                questionnumber = 0
                profileid = str(message.guild.id) + str(message.author.id)

                profileembed=discord.Embed(title="Profile Customisation", color=embedcolour)
                profileembed.add_field(name="Important info", value="When responding to the questions, whatever you put in will be displayed on your profile, so keep it readable and understandable. You can use discord markdown symbols and put in whatever format you wish. If you do not want to have a certain field on your profile, type 'skip' as a response to the question Sai asks. That's all for now, have a great day :) ", inline=False)
                profileembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=profileembed)
                
                responses = []

                while True:
                    currentquestion = customisationquestions[questionnumber]

                    try:
                        await message.channel.send(currentquestion)
                        waitformsg = await client.wait_for("message", check=check, timeout=300)
                        responses.append(waitformsg.content)

                        questionnumber += 1
                        if questionnumber >= len(customisationquestions):
                            await message.channel.send("Profile customisation finished!")
                            break
                        elif len(waitformsg.content) > 115:
                            await message.channel.send("Each of your answers have to be below 115 characters, run `s.help profile` for more information. Run the customisation command again to retry.")
                            return

                    except asyncio.TimeoutError:
                        await message.channel.send("You did not send your answer fast enough!")
                        break
                
                #write to db
                dbconnection = sqlite3.connect(database)
                cursor = dbconnection.cursor()

                cursor.execute(f"""INSERT OR REPLACE INTO profiles VALUES ("{profileid}", 
                                                                         "{responses[0]}",
                                                                         "{responses[1]}",
                                                                         "{responses[2]}",
                                                                         "{responses[3]}",
                                                                         "{responses[4]}",
                                                                         "{responses[5]}",
                                                                         "{responses[6]}",
                                                                         "{responses[7]}")""")

                dbconnection.commit()
                dbconnection.close()

                await message.channel.send("All done! Run `s.profile` to see the results.")
      
        #code for statistics command
        elif command == "stats" or command == "statistics" or command == "status":

            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.statistics + timedelta(seconds=statisticscooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.statistics = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.statistics + timedelta(seconds=statisticscooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("statistics", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return

            #gets bot info
            
            uptime = datetime.now() - starttime
            uptime = str(uptime).split(".")[0]
            start = starttime.strftime("%#A, %#d %#B\n%H:%M:%S")
            guilds = client.guilds
            servernum = len(guilds)
            usernum = len(client.users)
            allchannels = list(client.get_all_channels())
            channelnum = len(allchannels)
            textchannelnum = len([channel for channel in allchannels if channel.type == ChannelType.text])
            voicechannelnum = len([channel for channel in allchannels if channel.type == ChannelType.voice])

            #get bot resource info
            pid = os.getpid()
            saibotprocess = psutil.Process(pid)

            ramusagemb = ((saibotprocess.memory_info()[0] / 10000) // 1) / 100
            cpupercent = (((saibotprocess.cpu_percent() / psutil.cpu_count()) * 100) // 1) / 100

            owner = await client.fetch_user(457517248786202625)
            ownername = "{}#{}".format(owner.name, owner.discriminator)
            owneravatar = owner.avatar_url 
        
            statusembed=discord.Embed(title="Statistics <:info:881883500515590144>", colour=embedcolour)
            statusembed.set_author(name="Bot created by {0}".format(ownername), icon_url=owneravatar)
            statusembed.set_thumbnail(url=client.user.avatar_url)
            statusembed.add_field(name="Version", value="<:sai:881902408786120715> Sai v{0}".format(version), inline=False)
            statusembed.add_field(name="Time", value="Uptime: `{0}`\nTime Started: `{1}`\nCreated: `Sunday, 27 June 2021`".format(uptime, start), inline=True)
            statusembed.add_field(name="Channels", value="Sai is in a total of `{0}` channels*\n<:text_channel:881903452207341629> Text Channels: `{1}`\n<:voice_channel:881904408319897600> Voice Channels: `{2}`".format(channelnum, textchannelnum, voicechannelnum), inline=True)
            statusembed.add_field(name="Servers", value="Sai is in `{0}` servers".format(servernum), inline=False)
            statusembed.add_field(name="Users", value="Sai can see `{0}` users".format(usernum), inline=True)
            statusembed.add_field(name="Resources", value="CPU Usage: `{0}%`\nRAM Usage: `{1} MB`".format(cpupercent, ramusagemb), inline=True)
            statusembed.add_field(name="Commands", value="# of cmds: `{0}`\n# of cmds run since restart: `{1}`".format(commandnumber, commandsrun), inline=False)
            statusembed.add_field(name="Coding", value="Lines of code: `{0}`\n Libraries used: `{1}`".format(linesofcode, libraries))
            statusembed.set_footer(text="Command run by {0}#{1}  |  *The total number of channels also counts stage channels, private channels, etc.".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
            await message.channel.send(embed=statusembed)
        
        #code for testcount command
        elif command == "testcount" or command == "tc" or command[0:10] == "testcount " or command[0:3] == "tc ":

            #first check that the user is in the Sai Support guild

            #if the user is not in the guild send a message to join the Sai Support Server
            if message.guild.id != 859934506159833178:

                testcountembed=discord.Embed(title="Test Count Command <:info:881883500515590144>", colour=embedcolour)
                testcountembed.set_thumbnail(url=client.user.avatar_url)
                testcountembed.add_field(name="You can't run this command here!", value="This command shows the amount of times a user has tested on the [Sai Support Server](https://top.gg/servers/859934506159833178). This command is only available there for this reason. [Click here to join Sai's Official Support Server](https://top.gg/servers/859934506159833178)".format(version), inline=False)
                testcountembed.set_footer(text="Command run by {0}#{1} | Run 's.help testcount' for more information on this command.".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=testcountembed)

            #else the guild is correct, run the command
            else:

                #firstly checks if the cooldown has been met
                if (currentuser.cooldowns.testcount + timedelta(seconds=testcountcooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                    currentuser.cooldowns.testcount = datetime.now()
                else:
                    timeleft = (currentuser.cooldowns.testcount + timedelta(seconds=testcountcooldown)) - datetime.now()
                    timeleft = formattimedelta(timeleft)
                    cooldownembed = getcooldownembed("testcount", timeleft, message.author)
                    await message.channel.send(embed=cooldownembed)
                    return

                selectall = False
                #if no user is entered, assume the user is the user that ran the command
                if command == "testcount" or command == "tc":
                    testcountmemberid = message.author.id
                
                #else try to find the mentioned user or the 'all'/'list' parameter
                else:
                    if command[0:10] == "testcount ":
                        testcountparam = command[10:].strip()
                    else:
                        testcountparam = command[3:].strip()

                    if testcountparam == "all" or testcountparam == "list":
                        selectall = True

                    else:
                        #try to get the memberid
                        if isuserID(testcountparam):
                            testcountmemberid = getuserID(testcountparam)
                        
                        #if there is no memberid then send error embed
                        else:
                            testcountembed=discord.Embed(title="Testcount Command Error", colour=embedcolour)
                            testcountembed.add_field(name="Parameter Error", value="Make sure to mention one member or include the ID of one member.".format(version), inline=False)
                            testcountembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                            try:
                                await message.author.send(embed=testcountembed)
                            except:
                                try:
                                    await message.channel.send(embed=testcountembed)
                                except:
                                    pass
                            return
                
                #start database conection
                dbconnection = sqlite3.connect(database)
                cursor = dbconnection.cursor()

                if selectall:
                    fetchtestcountpermember = "SELECT * FROM saisupportstats ORDER BY testcount DESC"
                else:
                    fetchtestcountpermember = "SELECT * FROM saisupportstats WHERE memberid={0}".format(testcountmemberid)
                cursor.execute(fetchtestcountpermember)
                saisupportstatslist = cursor.fetchall()

                #create and send embed      
                testcountembed=discord.Embed(title="Test Counter:", colour=embedcolour)
                testcountembedfieldvalue = ""

                for member in saisupportstatslist:

                    #if member who has a test score has exited the guild, i.e. the get_member returns None, do not display the user test count
                    if message.guild.get_member(member[0]) == None:
                        continue
                    testcountembedfieldvalue += (str(message.guild.get_member(member[0])) + " - " + str(member[1]) + "\n")

                testcountembedfieldvalue.strip("\n")

                #if there are no tests
                if testcountembedfieldvalue == "":
                    testcountembedfieldvalue = "Quite a lot of nothing."

                testcountembed.add_field(name="# of tests per user: ", value=testcountembedfieldvalue, inline=False)
                testcountembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=testcountembed)
                
                #close database connection
                dbconnection.commit()
                dbconnection.close()

        #code for add test command (BOT OWNER ONLY)
        elif command[0:9] == "add test " and message.author.id == 457517248786202625:
            addtestparam = command[9:]
            if isuserID(addtestparam):
                addtestmemberID = getuserID(addtestparam)
                addtestmember = message.guild.get_member(addtestmemberID)
            else:
                await message.author.send("smh actually mention someone LOL")
                return   

            if addtestmember == None:
                await message.author.send("smh actually mention someone LOL")
            
            #get db connection and add testcount to current user, or add user to saisupportstats
            
            #start database connection
            dbconnection = sqlite3.connect(database)
            cursor = dbconnection.cursor()

            # first check if memberid is currently in db
            indb = False
            cursor.execute("SELECT * FROM saisupportstats")
            saisupportstatslist = cursor.fetchall()

            for member in saisupportstatslist:
                if member[0] == addtestmemberID:
                    indb = True
                    indbmember = member
                    break

            #if user is in db already add to the current testcount
            if indb:
                testcount = indbmember[1]
                testcount += 1
                cursor.execute(f"UPDATE saisupportstats SET testcount={int(testcount)} WHERE memberid={int(indbmember[0])}")
            #else create a new record in the table
            else:
                cursor.execute(f"INSERT INTO saisupportstats (memberid, testcount) VALUES ({addtestmemberID}, 1)")


            #close database connection
            dbconnection.commit()
            dbconnection.close()

            #send conformation message
            await message.channel.send("Added test to: {0} !".format(str(addtestmember)))

        #code for owner Sai info
        elif command == "admin info" and message.author.id == 457517248786202625:
            #compile info 
            informationfile = open("AdminInformation.txt", "w+")
            with informationfile as file:
                file.write("================================================================================================================================\n\t\t\t\t\t\tGUILD INFORMATION\n================================================================================================================================\n")
                file.write("{: ^50} {: ^50}\n".format(*["Guild Name:", "Member Count:"]))
                for guild in client.guilds:
                    data = [guild.name, str(guild.member_count)]
                    try:
                        file.write("{: ^50} {: ^50}\n".format(*data))
                    except:
                        data = ["Cannot Display", str(guild.member_count)]
                        file.write("{: ^50} {: ^50}\n".format(*data))
                file.close()
                await message.channel.send(content="See Attachment:", file=discord.File(r".\AdminInformation.txt"))
                

        #endregion
        
        #utility
        #region

        #code for the cooldowns command
        elif command == "cooldowns" or command == "cooldown" or command == "cd":
            # firstly check if the cooldown has been met (ironic lmfao)
            if (currentuser.cooldowns.cooldowns + timedelta(seconds=cooldownscooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.cooldowns = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.cooldowns + timedelta(seconds=cooldownscooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("cooldowns", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return
            
            # create and then attempt to return an embed
            cooldownsembed = discord.Embed(title=f"Cooldowns", description="Below is a table of your cooldowns for each of the commands. The first column shows the command in question, and the columns show, in order the cooldown left for a certain user, the generic cooldown length, the time the command was last run, and if the command is runnable now.", color=embedcolour)
            # fetch cooldowns for the user
            column_name_one = "Command"
            column_name_two = "Cooldown"
            column_name_three = "General Cooldown"
            column_name_four = "Last Run"
            column_name_five = "Runnable"
            empty = ""
            table = f"{column_name_one:^15}|{column_name_two:^20}|{column_name_three:^20}|{column_name_four:^10}|{column_name_five:^10}\n{empty:_^15} {empty:_^20} {empty:_^20} {empty:_^10} {empty:_^10}\n"
            small_table = f"{column_name_one:^15}|{column_name_two:^20}|{column_name_five:^10}\n{empty:_^15} {empty:_^20} {empty:_^10}\n"
            zero_timedelta = timedelta(0)
            for cooldown, time in currentuser:
                time_last_run = time.strftime("%H:%M:%S")
                cooldown_command = "s." + cooldown
                cooldown_length = currentuser.get_cooldown_length(cooldown)
                if time == datetime.utcfromtimestamp(0):
                    cooldown_left = formattimedelta(zero_timedelta)
                else:
                    cooldown_left = (time + timedelta(seconds=cooldown_length)) - datetime.now()
                    if cooldown_left < zero_timedelta:
                        cooldown_left = formattimedelta(zero_timedelta)
                    else:
                        cooldown_left = formattimedelta(cooldown_left)
                if cooldown_left == formattimedelta(zero_timedelta):
                    runnable = "Yes"
                else:
                    runnable = "No"                
                table += f"{cooldown_command:^15}|{cooldown_left:^20}|{formattimedelta(timedelta(seconds=cooldown_length)):^20}|{time_last_run:^10}|{runnable:^10}\n"
                small_table += f"{cooldown_command:^15}|{cooldown_left:^20}|{runnable:^10}\n"
            # add table to field
            cooldownsembed.add_field(name=f"Cooldowns for {str(message.author)}:", value=small_table)
            
            try:
                await message.channel.send(embed=cooldownsembed)
            except Exception as e:
                print(e)

        #code for edit snipe command
        elif command == "editsnipe" or command == "es":

            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.editsnipe + timedelta(seconds=editsnipecooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.editsnipe = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.editsnipe + timedelta(seconds=editsnipecooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("editsnipe", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return

            try:
                #get edited msg
                editsnipedmsg = editsnipedict[message.channel.id]

                #send before edited msg
                editsnipeembed=discord.Embed(description=editsnipedmsg.content, color=embedcolour)
                editsnipeembed.set_author(name=str(editsnipedmsg.author), icon_url=editsnipedmsg.author.avatar_url)
                editsnipeembed.set_footer(text="Sniped by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=editsnipeembed)

            except KeyError:
                #send msg if ther eis nothing to snipe
                editsnipedmsg = "There is nothing to snipe 🤔"
                await message.channel.send(editsnipedmsg)
        
        #code for event command
        elif (command[0:6] == "event " or command[0:4] == "evt " or command[0:3] == "ev ") and message.author.guild_permissions.administrator:
            
            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.event + timedelta(seconds=eventcooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.event = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.event + timedelta(seconds=eventcooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("event", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return            
            
            #create event param list
            if command[0:6] == "event ":
                eventparams = createparamlist("event", command, "|")
            elif command[0:4] == "evt ":
                eventparams = createparamlist("evt", command, "|")
            else:
                eventparams = createparamlist("ev", command, "|")

            
           #split up the params and add more variables
            try:
                #gets event channel, depdending on whether the channel was mentioned or the id was entered
                eventchannel = client.get_channel(getchannelID(eventparams[0]))
            except IndexError:
                #if no channel entered
                eventembed = discord.Embed(title="Event Cmd Error: ", color=embedcolour)
                eventembed.add_field(name="Format Error: ", value = "Make sure you include a channel ID for your event to be in.")
                eventembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                try:
                    await message.author.send(embed=eventembed)
                except:
                    await message.channel.send(embed=eventembed)
                return
            except:
                eventembed = discord.Embed(title="Event Cmd Error: ", color=embedcolour)
                eventembed.add_field(name="Channel Error: ", value = "The channel you want to create the event in might not exist, or cannot be seen by Sai")
                eventembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                try:    
                    await message.author.send(embed=eventembed)
                except:
                    await message.channel.send(embed=eventembed)
                return
            
            try:
                eventtitle = eventparams[1]
                #make event description optional
                if len(eventparams) >= 3:
                    eventdescription = eventparams[2]
                else:
                    eventdescription = ""
            except IndexError:
                #if no title and/or no description are entered
                eventembed = discord.Embed(title="Event Cmd Error: ", color=embedcolour)
                eventembed.add_field(name="Format Error: ", value = "Make sure you include a title to your event")
                eventembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                try:
                    await message.author.send(embed=eventembed)
                except:
                    await message.channel.send(embed=eventembed)
                return

            eventguildicon = message.guild.icon_url

            #send dm to command sender if channel is not in guild
            if eventchannel.guild != message.guild:
                eventembed = discord.Embed(title="Event Cmd Error: ", color=embedcolour)
                eventembed.add_field(name="Channel Error: ", value = "\nMake sure that the `<channelid>` is in the same guild that you are running the command.\n*(You cannot create events via Sai cross-guild.)*")
                eventembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                try:
                    await message.author.send(embed=eventembed)
                except:
                    await message.channel.send(embed=eventembed)
                return

            #create event embed
            eventembed=discord.Embed(title=eventtitle, description=eventdescription, color=embedcolour)
            eventembed.set_thumbnail(url=eventguildicon)
            eventembed.add_field(name="­\n  :white_check_mark: Attending", value=">>> ­", inline=False)
            eventembed.add_field(name="­\n  :grey_question: Unsure", value=">>> ­­­­­­­", inline=False)
            eventembed.add_field(name="­\n  :x: Not Attending", value=">>> ­", inline=False)
            eventembed.add_field(name="­­\n\nHow to choose preference/status­: ", value="Simply react to the message below with the corresponding emoji, and if you want to change your choice, make sure you are only reacted to one choice.", inline=False)
            eventembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
            eventmsg = await eventchannel.send(embed=eventembed)
            await message.add_reaction("\N{White Heavy Check Mark}")
            await eventmsg.add_reaction("\N{White Heavy Check Mark}")
            await eventmsg.add_reaction("\N{White Question Mark Ornament}")
            await eventmsg.add_reaction("\N{Cross Mark}")

            #add eventid to database in events table
            dbconnection = sqlite3.connect(database)
            cursor = dbconnection.cursor()
            addeventtodb = """INSERT INTO events VALUES ({0}, "", "", "")""".format(eventmsg.id)
            cursor.execute(addeventtodb)
            dbconnection.commit()
            dbconnection.close()
        
        #code for nick command
        elif (command[0:5] == "nick " or command[0:9] == "nickname ") and message.author.guild_permissions.change_nickname:
            
            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.nickname + timedelta(seconds=nicknamecooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.nickname = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.nickname + timedelta(seconds=nicknamecooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("nickname", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return 
            
            
            if command[0:5] == "nick ":
                newnick = command.replace("nick ", "").strip()
            else:
                newnick = command.replace("nickname ", "").strip()

            if newnick == "reset" or newnick == "default":
                newnick = message.author.name

            #if no nick entered
            if newnick == message.author.nick or (newnick == message.author.name and message.author.nick == None):
                nickchannel = await client.fetch_channel(int(message.channel.id))
                await nickchannel.trigger_typing()
                await message.channel.send("https://tenor.com/view/naruto-ninja-confused-da-fuq-gif-14325384")
                await nickchannel.trigger_typing()
                await sleep(3)
                await message.channel.send("uh...")               
                await nickchannel.trigger_typing()
                await sleep(3)
                await message.channel.send("what :kissing:")
                return

            try:
                #changes nickname
                await message.author.edit(nick=newnick, reason="Sai changed this users nickname using the s.nickname command.")
            except:
                #if the nickname is not valid
                nickembed = discord.Embed(title="Nickname Cmd Error: ", color=embedcolour)
                nickembed.add_field(name="User Error/Permissions Error: ", value="You cannot choose this as your nickname. Make sure your nickname only includes valid unicode characters and are between 1 and 32 characters. \nThis error could also occur if Sai's top role is below yours in the role hierarchy.")
                nickembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                try:
                    await message.author.send(embed=nickembed)
                except:
                    await message.channel.send(embed=nickembed)
                return
        
        #code for ping command
        elif command == "ping":

            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.ping + timedelta(seconds=pingcooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.ping = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.ping + timedelta(seconds=pingcooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("ping", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return 
            
            response = await message.channel.send("Currently Pinging... ")

            latencytimedelta = response.created_at - message.created_at
            latency = latencytimedelta.days * 24 * 60 * 60 * 1000
            latency += latencytimedelta.seconds * 1000
            latency += latencytimedelta.microseconds / 1000

            pingembed = discord.Embed(title="Pong!", description="Your current ping to Sai bot is: {0} ms".format(latency), color=embedcolour)
            pingembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
            await response.edit(content=None, embed=pingembed)
   
        #code for rescure command
        elif command == "rescue" or command == "resc" or command == "r":

            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.rescue + timedelta(seconds=rescuecooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.rescue = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.rescue + timedelta(seconds=rescuecooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("rescue", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return 

            #send a message, edit it, and then delete both messages
            await message.delete()
            rescuemessage = await message.channel.send("­")
            await rescuemessage.edit(content = "rescued, better luck next time")
            await rescuemessage.delete()

        #code for snipe command
        elif command == "snipe" or command == "s":

            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.snipe + timedelta(seconds=snipecooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.snipe = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.snipe + timedelta(seconds=snipecooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("snipe", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return

            try:
                #get sniped msg
                snipedmsg = snipedict[message.channel.id]

                #send sniped msg
                snipeembed=discord.Embed(description=snipedmsg.content, color=embedcolour)
                snipeembed.set_author(name=str(snipedmsg.author), icon_url=snipedmsg.author.avatar_url)
                snipeembed.set_footer(text="Sniped by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=snipeembed)

            except KeyError:
                #send msg if ther eis nothing to snipe
                snipedmsg = "There is nothing to snipe 🤔"
                await message.channel.send(snipedmsg)
        
        #code for time command
        elif command[0:5] == "time " or command[0:2] == "t " or command == "time" or command == "t":

            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.time + timedelta(seconds=timecooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.time = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.time + timedelta(seconds=timecooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("time", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return 
            
            #creating list of params
            if command[0:4] == "time":
                timezones = createparamlist("time", command, ",")
            else:
                timezones = createparamlist("t", command, ",")

            #checking for special params and user errors
            if timezones == [""]:
                timezones = ["UTC"]
            elif timezones[0].lower().startswith("wiki") or timezones[0].lower().startswith("wikipedia"):
                await message.channel.send("<@{0}> Here is the link to the a list of timezones by country: https://en.wikipedia.org/wiki/List_of_time_zones_by_country".format(message.author.id))
                return 
            elif timezones[0].upper() == "ALL":
                timezones = [timezone for timezone in alltimezones]
            for timezone in timezones:
                if timezone.upper() not in alltimezones:
                    await message.channel.send("<@{0}>, make sure the timezones are in the correct format or are in the bot's timezone list.".format(message.author.id), delete_after=10)
                    return

            #create embed for time command
            timeembed=discord.Embed(title="Time <:clock:881899619364253706>", color=embedcolour)
            for timezone in timezones:
                nowtime = datetime.utcnow() + timedelta(hours = alltimezones[timezone.upper()])
                nowtime = nowtime.strftime("%#A, %#d %#B\n%H:%M:%S")
                timeembed.add_field(name=timezone.upper(), value="`{0}`".format(nowtime), inline=True)
            timeembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
            await message.channel.send(embed=timeembed)
      
        #code for vote reminder command
        elif command == "vote reminder" or command == "remind" or command == "vote remind" or command == "votereminder":
            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.votereminder + timedelta(seconds=voteremindercooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.votereminder = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.votereminder + timedelta(seconds=voteremindercooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("vote reminder", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return 
            try:
                voteremindembed = discord.Embed(title="Reminder Set.", description="A reminder has been set for 12 hours from now! A DM will be sent to you at the time, to prevent clogging up channels, so make sure you have your DMs open! If you want to vote now, you can do that here:\nhttps://top.gg/bot/858663143931641857", color=embedcolour)
                voteremindembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.channel.send(embed=voteremindembed)
            except Exception as e:
                await message.channel.send(content=f"An error occured!\n```Send this error message to the bot developer\n{e}```")
                return
            await sleep(43200)
            try:
                await message.author.send("You can vote!")
            except:
                print("The user's DM's were closed, so could not be reminded to vote!")
        
        #endregion

        #moderation and admin
        #region

        #code for ban command
        elif command[0:4] == "ban " and message.author.guild_permissions.ban_members:

            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.ban + timedelta(seconds=bancooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.ban = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.ban + timedelta(seconds=bancooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("ban", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return 

            #get ban params
            banparams = createparamlist("ban", command, "|")

            #check if user has been inputted correctly
            try:
                if search("<@.+>", banparams[0]) and len(banparams[0]) == 21:
                    banuser = message.guild.get_member(int(banparams[0][2:20]))
                elif search("<@!.+>", banparams[0]) and len(banparams[0]) == 22:
                    banuser = message.guild.get_member(int(banparams[0][3:21]))
                else:
                    banuser = message.guild.get_member(int(banparams[0]))
            except IndexError:
                #if no user is entered
                banembed = discord.Embed(title="Ban Cmd Error: ", color=embedcolour)
                banembed.add_field(name="Format Error: ", value = "Make sure you include a user")
                banembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                try:
                    await message.author.send(embed=banembed)
                except:
                    await message.channel.send(embed=banembed)
                return
            except:
                #if no user is entered
                banembed = discord.Embed(title="Ban Cmd Error: ", color=embedcolour)
                banembed.add_field(name="Syntax Error: ", value = "Make sure you include a correct user ID or mention, and that the user is in the same server.")
                banembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                try:
                    await message.author.send(embed=banembed)
                except:
                    await message.channel.send(embed=banembed)
                return
            
            #gets server owner who can ban or kick anyone
            owner = message.guild.get_member(int(message.guild.owner.id))
            
            #firstly check if Sai can ban
            sai = message.guild.get_member(int(client.user.id))

            if sai.top_role <= banuser.top_role:
                banmessage = "Sai cant ban users above or at the same level as himself!"
                await message.channel.send(banmessage)
                await message.add_reaction("❌")
                return
            
            #check that the user is above in heirarchy and not owner (owner can ban anyone)
            if banuser.top_role >= message.author.top_role and (not (message.author == owner)):
                if randint(1,1000) == 1:
                    banmessage = "Your sexy jutsu is not powerful enough to ban this user"
                else:
                    banmessage = "You cant ban users above or at the same level as you!"
                await message.channel.send(banmessage)
                await message.add_reaction("❌")
                return

            if len(banparams) >= 2:
                banembed = discord.Embed(title="You were banned from {0}.".format(str(message.guild)), colour=embedcolour)
                banembed.add_field(name="Reason: ", value=banparams[1])
                banembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                try:
                    await banuser.send(embed=banembed)
                except:
                    pass
                await message.channel.send("{0} was banned. Reason: {1}".format(str(banuser), banparams[1]))
            else:
                banembed = discord.Embed(title="You were banned from {0}.".format(str(message.guild)), colour=embedcolour)
                banembed.add_field(name="Reason: ", value="No reason given.")
                banembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                try:
                    await banuser.send(embed=banembed)
                except:
                    pass
                await message.channel.send("{0} was banned. Reason: No reason given.".format(str(banuser)))
            
            #ban the user and react to message
            try:
                banreason = banparams[1]
            except IndexError:
                banreason = "No reason given :("
            await banuser.ban(reason=banreason)
            await message.add_reaction("✅")
       
        #code for kick command
        elif command[0:5] == "kick " and message.author.guild_permissions.kick_members:

            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.kick + timedelta(seconds=kickcooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.kick = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.kick + timedelta(seconds=kickcooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("kick", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return 

            #get kick params
            kickparams = createparamlist("kick", command, "|")

            #check if user has been inputted correctly
            try:
                if search("<@.+>", kickparams[0]) and len(kickparams[0]) == 21:
                    kickuser = message.guild.get_member(int(kickparams[0][2:20]))
                elif search("<@!.+>", kickparams[0]) and len(kickparams[0]) == 22:
                    kickuser = message.guild.get_member(int(kickparams[0][3:21]))
                else:
                    kickuser = message.guild.get_member(int(kickparams[0]))
            except IndexError:
                #if no user is entered
                kickembed = discord.Embed(title="Kick Cmd Error: ", color=embedcolour)
                kickembed.add_field(name="Format Error: ", value = "Make sure you include a user")
                kickembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                try:
                    await message.author.send(embed=kickembed)
                except:
                    await message.channel.send(embed=kickembed)
                return
            except:
                #if no user is entered
                kickembed = discord.Embed(title="Kick Cmd Error: ", color=embedcolour)
                kickembed.add_field(name="Syntax Error: ", value = "Make sure you include a correct user ID or mention, and the user is in the same server.")
                kickembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                try:
                    await message.author.send(embed=kickembed)
                except:
                    await message.channel.send(embed=kickembed)
                return

            #gets server owner who can ban or kick anyone
            owner = message.guild.get_member(int(message.guild.owner.id))
            
            #firstly check if Sai can kick
            sai = message.guild.get_member(int(client.user.id))

            if sai.top_role <= kickuser.top_role:
                banmessage = "Sai cant kick users above or at the same level as himself!"
                await message.channel.send(banmessage)
                await message.add_reaction("❌")
                return
            
            
            #check that the user is above in heirarchy and not the owner (owner can ban anyone)
            if kickuser.top_role >= message.author.top_role and (not (message.author == owner)):
                if randint(1,1000) == 1:
                    kickmessage = "Your sexy jutsu is not powerful enough to kick this user"
                else:
                    kickmessage = "You cant kick users above or at the same level as you!"
                await message.channel.send(kickmessage)
                await message.add_reaction("❌")
                return

            if len(kickparams) >= 2:
                kickembed = discord.Embed(title="You were kicked from {0}.".format(str(message.guild)), colour=embedcolour)
                kickembed.add_field(name="Reason: ", value=kickparams[1])
                kickembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                try:
                    await kickuser.send(embed=kickembed)
                except:
                    pass
                await message.channel.send("{0} was kicked. Reason: {1}".format(str(kickuser), kickparams[1]))
            else:
                kickembed = discord.Embed(title="You were kicked from {0}.".format(str(message.guild)), colour=embedcolour)
                kickembed.add_field(name="Reason: ", value="No reason given.")
                kickembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                try:
                    await kickuser.send(embed=kickembed)
                except:
                    pass
                await message.channel.send("{0} was kicked. Reason: No reason given.".format(str(kickuser)))
            
            #kick the user
            await kickuser.kick()
            await message.add_reaction("✅")
        
        #code for lockdown command
        elif (command[0:9] == "lockdown " or command[0:5] == "lock " or command[0:6] == "shush " or command[0:7] == "shutup " or command == "lockdown" or command == "lock" or command == "shush" or command == "shutup") and message.author.guild_permissions.manage_permissions:
        
            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.lockdown + timedelta(seconds=lockdowncooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.lockdown = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.lockdown + timedelta(seconds=lockdowncooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("lockdown", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return

            #if 's.lockdown' on its own is run, set the channel to be lockdowned to the current channel
            if command == "lockdown" or command == "lock" or command == "shush" or command == "shutup":
                channel = message.channel
            else:
                #trim down command to only the channel
                if command[0:9] == "lockdown ":
                    param = command[9:]
                elif command[0:5] == "lock ":
                    param = command[5:]
                elif command[0:6] == "shush ":
                    param = command[6:]
                else:
                    param = command[7:]
                
                #if the channel entered is in the correct format
                if ischannelID(param):
                    try:
                        channel = message.guild.get_channel(getchannelID(param))
                    except:
                        #if the channel entered is not real or doesnt exist output an error message
                        lockdownembed = discord.Embed(title="Lockdown Cmd Error: ", color=embedcolour)
                        lockdownembed.add_field(name="Channel Error: ", value = "\nMake sure that the channel entered exists and is in the same guild that you are running the command.")
                        lockdownembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                        try:
                            await message.author.send(embed=lockdownembed)
                        except:
                            await message.channel.send(embed=lockdownembed)
                        await message.add_reaction("❌")
                        return     
                
                #else if the entered text is not a channel
                else:
                    #if the channel entered is not real or doesnt exist output an error message
                    lockdownembed = discord.Embed(title="Lockdown Cmd Error: ", color=embedcolour)
                    lockdownembed.add_field(name="Channel Error: ", value = "\nMake sure that you enter an actual channel.")
                    lockdownembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                    try:
                        await message.author.send(embed=lockdownembed)
                    except:
                        await message.channel.send(embed=lockdownembed)
                    await message.add_reaction("❌")
                    return

            #lockdown the channel and provide conformation by a reaction
            lockdownoverwrite = channel.overwrites_for(message.guild.default_role)

            #if the channel is not locked
            if lockdownoverwrite.send_messages == False:
                await message.add_reaction("❌")
                await message.channel.send("This channel is already locked!")
                return

            lockdownoverwrite.send_messages = False
            await channel.set_permissions(message.guild.default_role, overwrite=lockdownoverwrite)
            await message.add_reaction("✅")

        #code for msg command
        elif (command[0:4] == "msg " or command[0:8] == "message ") and message.author.guild_permissions.administrator:
            
            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.message + timedelta(seconds=messagecooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.message = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.message + timedelta(seconds=messagecooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("message", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return 
            
            #create list of params
            if command[0:3] == "msg":
                msgparams = createparamlist("msg", command, "|")
            else:
                msgparams = createparamlist("message", command, "|")

            #send msg to channel
            try:
                msgchannel = client.get_channel(getchannelID(msgparams[0]))

                #if channel in same guild send message, otherwise dm the message sender that the channel has to be in the same guild
                if message.channel.guild == msgchannel.guild or message.author.id == 457517248786202625:
                    await msgchannel.send(msgparams[1])
                else:
                    msgembed = discord.Embed(title="Msg Cmd Error: ", color=embedcolour)
                    msgembed.add_field(name="Channel Error: ", value = "\nMake sure that the `<channelid>` is in the same guild that you are running the command.\n*(You cannot send messages via Sai cross-guild.)*")
                    msgembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                    try:
                        await message.author.send(embed=msgembed)
                    except:
                        await message.channel.send(embed=msgembed)
            except IndexError:
                #if no channel entered
                msgembed = discord.Embed(title="Msg Cmd Error: ", color=embedcolour)
                msgembed.add_field(name="Format Error: ", value = "Make sure you include a message and/or correct channel")
                msgembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                try:
                    await message.author.send(embed=msgembed)
                except:
                    await message.channel.send(embed=msgembed)
            except:
                msgembed = discord.Embed(title="Msg Cmd Error: ", color=embedcolour)
                msgembed.add_field(name="Format Error: ", value = "\nCheck that the following format has been followed\n\n`s.message <channelid> | <message>`")
                msgembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                try:
                    await message.author.send(embed=msgembed)
                except:
                    await message.channel.send(embed=msgembed)

        #code for purge command
        elif (command[0:6] == "purge " or command[0:8] == "finesse " or command[0:11] == "annihilate ") and message.author.guild_permissions.manage_messages:

            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.purge + timedelta(seconds=purgecooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.purge = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.purge + timedelta(seconds=purgecooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("purge", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return
            
            #get number of msgs to purge
            purgeparams = command.split(" ")
            if command[0:6] == "purge ":
                purgeparams.remove("purge")
                purgenum = purgeparams[0]
                purgeword = "Purged"
            elif command[0:8] == "finesse ":
                purgeparams.remove("finesse")
                purgenum = purgeparams[0]
                purgeword = "Finessed"
            else:              
                purgeparams.remove("annihilate")
                purgenum = purgeparams[0]
                purgeword = "Annihilated"

            #make sure a correct number has been added
            if len(purgeparams) > 1:
                await message.channel.send("<@{0}> Enter a correct number of messages to delete.".format(int(message.author.id)), delete_after=3)
                return
            if (not isint(purgenum)):
                await message.channel.send("<@{0}> Enter a correct number of messages to delete.".format(int(message.author.id)), delete_after=3)
                return

            purgenum = int(purgenum)

            #purges messages
            await message.channel.purge(limit=(purgenum + 1))
            await message.channel.send("{0} {1} messages.".format(purgeword, purgenum), delete_after=1)

        #code for role command
        elif (command[0:5] == "role ") and message.author.guild_permissions.manage_roles:

            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.role + timedelta(seconds=rolecooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.role = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.role + timedelta(seconds=rolecooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("role", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return

            if command[0:5] == "role ":
                roleparams = createparamlist("role", command, " ")
            else:
                roleparams = createparamlist("r", command, " ")

            #remove blank params
            for roleparam in roleparams:
                if roleparam == "":
                    roleparams.remove(roleparam)

            if len(roleparams) == 0:
                await message.channel.send("<@{0}> Need help with the `role` command? Run `s.help role` for more...")
                return

            #if s.role give [user] [role] is run or s.role remove [user] [role]
            if roleparams[0] == "give" or roleparams[0] == "add" or roleparams[0] == "remove" or roleparams[0] == "take":

                #if there are not two parameters (user and role) then give error message
                if len(roleparams) != 3:
                    roleembed = discord.Embed(title="Role Cmd Error: ", color=embedcolour)
                    roleembed.add_field(name="Syntax Error: ", value = "\nMake sure that you have inputted both the user and the role to give in the format `s.role give [user mention] or [user ID] [role mention] or [role ID]`. Also do not add extra parameters.")
                    roleembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                    try:
                        await message.author.send(embed=roleembed)
                    except:
                        await message.channel.send(embed=roleembed)
                    return
                
                #if first param is a userID 
                isinputuserID = isuserID(roleparams[1])
                isinputroleID = isroleID(roleparams[2])
                if isinputuserID and isinputroleID:
                    try:
                        #get users
                        userchanging = await message.guild.fetch_member(int(message.author.id))
                        usertochange = await message.guild.fetch_member(getuserID(roleparams[1]))
                        
                        #get role
                        roletochange = message.guild.get_role(getroleID(roleparams[2]))
                    except:
                        roleembed = discord.Embed(title="Role Cmd Error: ", color=embedcolour)
                        roleembed.add_field(name="User/Role Error: ", value = "\nMake sure that you have given the real / correct role and user mention or ID. The user must also be in the guild you are running the command.")
                        roleembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                        try:
                            await message.author.send(embed=roleembed)
                        except:
                            await message.channel.send(embed=roleembed)
                        return

                    saiuser = await message.guild.fetch_member(858663143931641857)

                    #get owner who can give or take any role
                    owner = message.guild.get_member(int(message.guild.owner.id))
                    
                    #give role if the command is give
                    if roleparams[0] == "give" or roleparams[0] == "add":
                        #if Sai's top role is not above the role to give, react with an appropriate message
                        if userchanging.top_role <= roletochange and (not (message.author == owner)):
                            await message.channel.send("You cant give this role to anyone!")
                            await message.add_reaction("❌")
                            return
                        if saiuser.top_role <= roletochange:
                            await message.channel.send("Sai cant give this role to anyone! Make sure Sai is above this role in the Hierarchy...")
                            await message.add_reaction("❌")
                            return

                        #check if the user already has the role
                        if roletochange in usertochange.roles:
                            await message.channel.send("The user already has this role!")
                            await message.add_reaction("❌")
                            return
                        
                        #give specified role to specified user
                        await usertochange.add_roles(roletochange, reason="Sai gave the role as per {0}'s request".format(str(userchanging)))
                        await message.add_reaction("✅")

                    #remove role if the command is remove
                    if roleparams[0] == "remove" or roleparams[0] == "take":
                        #if Sai's top role is not above the role to give, react with an appropriate message
                        if userchanging.top_role <= roletochange and (not (message.author == owner)):
                            #if the user running command is not the same as the user to change and the role is the same level, they cannot change the role so send this message
                            if userchanging == usertochange and userchanging.top_role == roletochange:
                                pass
                            else:
                                await message.channel.send("You cant remove this role!")
                                await message.add_reaction("❌")
                                return
                        if saiuser.top_role <= roletochange:
                            if saiuser == userchanging and saiuser.top_role == roletochange:
                                pass
                            await message.channel.send("Sai cant remove this role from anyone! Make sure Sai is above this role in the Hierarchy...")
                            await message.add_reaction("❌")
                            return

                        #check if the user doesnt have the role
                        if not (roletochange in usertochange.roles):
                            await message.channel.send("The user does not have this role!")
                            await message.add_reaction("❌")
                            return
                        
                        #give specified role to specified user
                        await usertochange.remove_roles(roletochange, reason="Sai removed the role as per {0}'s request".format(str(userchanging)))
                        await message.add_reaction("✅")
                
                else:
                    roleembed = discord.Embed(title="Role Cmd Error: ", color=embedcolour)
                    roleembed.add_field(name="User/Role Error: ", value = "\nMake sure that you have given the real / correct role and user mention or ID. The user must also be in the guild you are running the command.")
                    roleembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                    try:
                        await message.author.send(embed=roleembed)
                    except:
                        await message.channel.send(embed=roleembed)
                    return

            #if s.role info 'params' is run
            elif roleparams[0] == "information" or roleparams[0] == "info":

                #if nothing is entered as roleparams[1] then set it to the userID of the user who called the command, since this is the default parameter
                if len(roleparams) == 1:
                    roleparams.append(message.author.id)

                #if the command is s.role info list/all
                if roleparams[1] == "list" or roleparams[1] == "all":

                    #list all role info for the selected server
                    roleembed = discord.Embed(title="Role Information: ", color=embedcolour)

                    await message.channel.trigger_typing()
                    #if there will be less that 25 fields:
                    if len(message.guild.roles) <= 25:
                        for role in message.guild.roles:
                            if not role.is_default():
                                roleembed.add_field(name=str(role), value="{0}\n# of users: `{1}`\ncreated at: `{2}`\nmentionable: `{3}`".format(role.mention, len(role.members), role.created_at.strftime("%#x"), role.mentionable))
                        roleembed.set_footer(text="Command run by {0}#{1} | Page 1 of 1".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                        await message.channel.send(embed=roleembed)
                        return
                    #if there is more than 25 fields create a menu where you can react to change the page number
                    else:
                        
                        pagenum = 0
                        pages = ceil(len(message.guild.roles) / 25) - 1
                        
                        for role in message.guild.roles[0:25]:
                            if not role.is_default():
                                roleembed.add_field(name=str(role), value="{0}\n# of users: `{1}`\ncreated at: `{2}`\nmentionable: `{3}`".format(role.mention, len(role.members), role.created_at.strftime("%#x"), role.mentionable))
                            else:
                                roleembed.add_field(name=str(role), value="{0}\n# of users: `{1}`\ncreated at: `{2}`\nmentionable: `{3}`".format("@everyone", len(role.members), role.created_at.strftime("%#x"), role.mentionable))
                        roleembed.set_footer(text="Command run by {0}#{1} | Page {2} of {3}".format(message.author.name, message.author.discriminator, (pagenum + 1), (pages + 1)), icon_url=message.author.avatar_url)
                        roleembedmsg = await message.channel.send(embed=roleembed)
                        await roleembedmsg.add_reaction("⬅️")
                        await roleembedmsg.add_reaction("➡️")

                        def check(reaction, user):
                            return (user.id != 858663143931641857 and str(reaction.emoji) in ["⬅️", "➡️"])

                        while True:
                            try:                     
                                reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)

                                #if reacted with next page
                                if reaction.emoji == "➡️" and (not (pagenum >= pages)):
                                    pagenum += 1
                                    roleembed = discord.Embed(title="Role Information: ", color=embedcolour)
                                    roleembed.set_footer(text="Command run by {0}#{1} | Page {2} of {3}".format(message.author.name, message.author.discriminator, (pagenum + 1), (pages + 1)), icon_url=message.author.avatar_url)

                                    startroleindex = pagenum*25
                                    endroleindex = (pagenum*25)+25
                                    if endroleindex > len(message.guild.roles):
                                        endroleindex = ((pagenum*25)+25) - (len(message.guild.roles) - endroleindex)

                                    for role in message.guild.roles[startroleindex:endroleindex]:
                                        if not role.is_default():
                                            roleembed.add_field(name=str(role), value="{0}\n# of users: `{1}`\ncreated at: `{2}`\nmentionable: `{3}`".format(role.mention, len(role.members), role.created_at.strftime("%#x"), role.mentionable))
                                        else:
                                            roleembed.add_field(name=str(role), value="{0}\n# of users: `{1}`\ncreated at: `{2}`\nmentionable: `{3}`".format("@everyone", len(role.members), role.created_at.strftime("%#x"), role.mentionable))
                                    await roleembedmsg.edit(embed=roleembed)
                                    await roleembedmsg.remove_reaction(reaction, user)

                                #if reacted with prev page
                                elif reaction.emoji == "⬅️" and (not (pagenum <= 0)):
                                    pagenum -= 1
                                    roleembed = discord.Embed(title="Role Information: ", color=embedcolour)
                                    roleembed.set_footer(text="Command run by {0}#{1} | Page {2} of {3}".format(message.author.name, message.author.discriminator, (pagenum + 1), (pages + 1)), icon_url=message.author.avatar_url)

                                    startroleindex = pagenum*25
                                    endroleindex = (pagenum*25)+25

                                    for role in message.guild.roles[startroleindex:endroleindex]:
                                        if not role.is_default():
                                            roleembed.add_field(name=str(role), value="{0}\n# of users: `{1}`\ncreated at: `{2}`\nmentionable: `{3}`".format(role.mention, len(role.members), role.created_at.strftime("%#x"), role.mentionable))
                                        else:
                                            roleembed.add_field(name=str(role), value="{0}\n# of users: `{1}`\ncreated at: `{2}`\nmentionable: `{3}`".format("@everyone", len(role.members), role.created_at.strftime("%#x"), role.mentionable))
                                    await roleembedmsg.edit(embed=roleembed)
                                    await roleembedmsg.remove_reaction(reaction, user)

                                #otherwise delete reaction
                                else:
                                    await roleembedmsg.remove_reaction(reaction, user)

                            except asyncio.TimeoutError:
                                await roleembedmsg.clear_reactions()
                                return

                #if the command is s.role info rolemention/roleid
                if isroleID(roleparams[1]):
                    try:
                        #list info for the specified role 
                        role = message.guild.get_role(getroleID(roleparams[1]))

                        roleembed = discord.Embed(title="Role Information: ", color=embedcolour)
                        roleembed.add_field(name=str(role), value="{0}\n# of users: `{1}`\ncreated at: `{2}`\nmentionable: `{3}`".format(role.mention, len(role.members), role.created_at.strftime("%#x"), role.mentionable))
                        roleembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)     

                        await message.channel.send(embed=roleembed)
                        return
                    except:
                        pass

                #if the command is s.user info usermention/userid
                if isuserID(roleparams[1]):
                    try:
                        #list all role info for the selected user
                        usertoget = await message.guild.fetch_member(getuserID(roleparams[1]))

                        roleembed = discord.Embed(title="Role Information: ", color=embedcolour)

                        await message.channel.trigger_typing()
                        #if there will be less that 25 fields:
                        if len(usertoget.roles) <= 25:
                            for role in usertoget.roles:
                                if not role.is_default():
                                    roleembed.add_field(name=str(role), value="{0}\n# of users: `{1}`\ncreated at: `{2}`\nmentionable: `{3}`".format(role.mention, len(role.members), role.created_at.strftime("%#x"), role.mentionable))
                            roleembed.set_footer(text="Command run by {0}#{1} | Page 1 of 1".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                            await message.channel.send(embed=roleembed)
                            return
                        #if there is more than 25 fields create a menu where you can react to change the page number
                        else:
                            
                            pagenum = 0
                            pages = ceil(len(usertoget.roles) / 25) - 1
                            
                            for role in usertoget.roles[0:25]:
                                if not role.is_default():
                                    roleembed.add_field(name=str(role), value="{0}\n# of users: `{1}`\ncreated at: `{2}`\nmentionable: `{3}`".format(role.mention, len(role.members), role.created_at.strftime("%#x"), role.mentionable))
                                else:
                                    roleembed.add_field(name=str(role), value="{0}\n# of users: `{1}`\ncreated at: `{2}`\nmentionable: `{3}`".format("@everyone", len(role.members), role.created_at.strftime("%#x"), role.mentionable))
                            roleembed.set_footer(text="Command run by {0}#{1} | Page {2} of {3}".format(message.author.name, message.author.discriminator, (pagenum + 1), (pages + 1)), icon_url=message.author.avatar_url)
                            roleembedmsg = await message.channel.send(embed=roleembed)
                            await roleembedmsg.add_reaction("⬅️")
                            await roleembedmsg.add_reaction("➡️")

                            def check(reaction, user):
                                return (user.id != 858663143931641857 and str(reaction.emoji) in ["⬅️", "➡️"])

                            while True:
                                try:                     
                                    reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)

                                    #if reacted with next page
                                    if reaction.emoji == "➡️" and (not (pagenum >= pages)):
                                        pagenum += 1
                                        roleembed = discord.Embed(title="Role Information: ", color=embedcolour)
                                        roleembed.set_footer(text="Command run by {0}#{1} | Page {2} of {3}".format(message.author.name, message.author.discriminator, (pagenum + 1), (pages + 1)), icon_url=message.author.avatar_url)

                                        startroleindex = pagenum*25
                                        endroleindex = (pagenum*25)+25
                                        if endroleindex > len(usertoget.roles):
                                            endroleindex = ((pagenum*25)+25) - (len(usertoget.roles) - endroleindex)

                                        for role in usertoget.roles[startroleindex:endroleindex]:
                                            if not role.is_default():
                                                roleembed.add_field(name=str(role), value="{0}\n# of users: `{1}`\ncreated at: `{2}`\nmentionable: `{3}`".format(role.mention, len(role.members), role.created_at.strftime("%#x"), role.mentionable))
                                            else:
                                                roleembed.add_field(name=str(role), value="{0}\n# of users: `{1}`\ncreated at: `{2}`\nmentionable: `{3}`".format("@everyone", len(role.members), role.created_at.strftime("%#x"), role.mentionable))
                                        await roleembedmsg.edit(embed=roleembed)
                                        await roleembedmsg.remove_reaction(reaction, user)

                                    #if reacted with prev page
                                    elif reaction.emoji == "⬅️" and (not (pagenum <= 0)):
                                        pagenum -= 1
                                        roleembed = discord.Embed(title="Role Information: ", color=embedcolour)
                                        roleembed.set_footer(text="Command run by {0}#{1} | Page {2} of {3}".format(message.author.name, message.author.discriminator, (pagenum + 1), (pages + 1)), icon_url=message.author.avatar_url)

                                        startroleindex = pagenum*25
                                        endroleindex = (pagenum*25)+25

                                        for role in usertoget.roles[startroleindex:endroleindex]:
                                            if not role.is_default():
                                                roleembed.add_field(name=str(role), value="{0}\n# of users: `{1}`\ncreated at: `{2}`\nmentionable: `{3}`".format(role.mention, len(role.members), role.created_at.strftime("%#x"), role.mentionable))
                                            else:
                                                roleembed.add_field(name=str(role), value="{0}\n# of users: `{1}`\ncreated at: `{2}`\nmentionable: `{3}`".format("@everyone", len(role.members), role.created_at.strftime("%#x"), role.mentionable))
                                        
                                        await roleembedmsg.edit(embed=roleembed)
                                        await roleembedmsg.remove_reaction(reaction, user)

                                    #otherwise delete reaction
                                    else:
                                        await roleembedmsg.remove_reaction(reaction, user)

                                except asyncio.TimeoutError:
                                    await roleembedmsg.clear_reactions()
                                    break
                    except:
                        pass

                roleembed = discord.Embed(title="Role Cmd Error: ", color=embedcolour)
                roleembed.add_field(name="Parameter Error:", value="Make sure the role/user/parameter entered exists/is accepted and is in the same server. The role/user must be in the same guild as where the command is being run.")
                roleembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                try:
                    await message.author.send(embed=roleembed)
                except:
                    await message.channel.send(embed=roleembed)
                        
            #if s.role reaction 'params' is run
            elif roleparams[0] == "reaction" and message.author.id == 457517248786202625:

                roleembed = discord.Embed(title="Tester Role: ", description="React with the <:tester:865963914721886248> emoji to get the tester role! If you are a tester you will be able to help with the development of the bot throughout by bug testing. Helping multiple times will give you different roles, from <@&863846948870815778> to <@&863847318625583154>\n\n", color=embedcolour)
                roleembed.add_field(name="­", value="<:tester:865963914721886248> <@&865877112282808371>\n­")
                roleembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)

                reactionrole = await message.channel.send(embed=roleembed)
                await reactionrole.add_reaction("<:tester:865963914721886248>")

        #code for slowmode command
        elif (command[0:9] == "slowmode " or command[0:5] == "slow " or command[0:3] == "sm " or command == "slowmode" or command == "slow" or command == "sm") and message.author.guild_permissions.manage_channels:

            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.slowmode + timedelta(seconds=slowmodecooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.slowmode = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.slowmode + timedelta(seconds=slowmodecooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("slowmode", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return

            #if command run is 's.slowmode' on its own
            if command == "slowmode" or command == "slow" or command == "sm":
                #trigger slowmode
                await message.channel.edit(slowmode_delay=30)
                await message.add_reaction("✅")
                return
            
            if command[0:9] == "slowmode ":
                slowmodeparams = createparamlist("slowmode", command, " ")
            elif command[0:5] == "slow ":
                slowmodeparams = createparamlist("slow", command, " ")
            else:
                slowmodeparams = createparamlist("sm", command, " ")

            slowmodetoggle = True
            
            #if channel specified
            if ischannelID(slowmodeparams[0]):

                #if no time specified, use default value of 30 seconds
                if len(slowmodeparams) == 1:

                    seconds = 30
                    slowmodechannel = message.author.guild.get_channel(getchannelID(slowmodeparams[0]))
                
                #else find time specified
                else:    

                    #if slowmode should be turned off  
                    if slowmodeparams[1].lower() == "off" or slowmodeparams[1].lower() == "false":
                        slowmodetoggle = False

                    else:
                        #join parts of the time specified
                        slowmodetimestring = ""
                        for i in range(len(slowmodeparams[1:])):
                            slowmodetimestring += slowmodeparams[1:][i]

                        seconds = parsetimestring(slowmodetimestring)
                    slowmodechannel = message.author.guild.get_channel(getchannelID(slowmodeparams[0]))

            #else channel not specified
            else:
                
                #if slowmode should be turned off  
                if slowmodeparams[0].lower() == "off" or slowmodeparams[0].lower() == "false":
                    slowmodetoggle = False
                
                else:
                    #join parts of the time specified
                    slowmodetimestring = ""
                    for i in range(len(slowmodeparams)):
                        slowmodetimestring += slowmodeparams[i]

                    seconds = parsetimestring(slowmodetimestring)
                slowmodechannel = message.channel

            #if slowmode is to be turned off
            if not slowmodetoggle:
                await slowmodechannel.edit(slowmode_delay=0)
                await message.add_reaction("✅")
                return
            
            #if channel doesnt exist in guild
            elif slowmodechannel == None:
                slowmodeembed = discord.Embed(title="Slowmode Cmd Error: ", color=embedcolour)
                slowmodeembed.add_field(name="Parameter Error:", value="Make sure the channel exists and is in the same guild as the server where this command was run.")
                slowmodeembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                try:
                    await message.author.send(embed=slowmodeembed)
                except:
                    await message.channel.send(embed=slowmodeembed)

            #if the time format was incorrect
            elif seconds == None:
                slowmodeembed = discord.Embed(title="Slowmode Cmd Error: ", color=embedcolour)
                slowmodeembed.add_field(name="Parameter Error:", value="Make sure the time specified is in an accepted format. Run `s.help timeformats` for accepted formats.")
                slowmodeembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                try:
                    await message.author.send(embed=slowmodeembed)
                except:
                    await message.channel.send(embed=slowmodeembed)

            #if the time is over 6 hours
            elif seconds > 21600:
                slowmodeembed = discord.Embed(title="Slowmode Cmd Error: ", color=embedcolour)
                slowmodeembed.add_field(name="Parameter Error:", value="Make sure the time specified is below six hours*.")
                slowmodeembed.set_footer(text="Error Triggered by {0}#{1} | *The max time for slowmode in discord is six hours.".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                try:
                    await message.author.send(embed=slowmodeembed)
                except:
                    await message.channel.send(embed=slowmodeembed)

            #trigger slowmode
            else:
                await slowmodechannel.edit(slowmode_delay=seconds)
                await message.add_reaction("✅")
        
        #code for unlockdown command
        elif (command[0:11] == "unlockdown " or command[0:7] == "unlock " or command[0:8] == "unshush " or command[0:11] == "antishutup " or command == "unlockdown" or command == "unlock" or command == "unshush" or command == "antishutup") and message.author.guild_permissions.manage_permissions:
        
            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.unlockdown + timedelta(seconds=unlockdowncooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.unlockdown = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.unlockdown + timedelta(seconds=unlockdowncooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("unlockdown", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return

            #if 's.lockdown' on its own is run, set the channel to be lockdowned to the current channel
            if command == "unlockdown" or command == "unlock" or command == "unshush" or command == "antishutup":
                channel = message.channel
            else:
                #trim down command to only the channel
                if command[0:11] == "unlockdown ":
                    param = command[11:]
                elif command[0:7] == "unlock ":
                    param = command[7:]
                elif command[0:8] == "unshush ":
                    param = command[8:]
                else:
                    param = command[11:]
                
                #if the channel entered is in the correct format
                if ischannelID(param):
                    try:
                        channel = message.guild.get_channel(getchannelID(param))
                    except:
                        #if the channel entered is not real or doesnt exist output an error message
                        unlockdownembed = discord.Embed(title="Unlockdown Cmd Error: ", color=embedcolour)
                        unlockdownembed.add_field(name="Channel Error: ", value = "\nMake sure that the channel entered exists and is in the same guild that you are running the command.")
                        unlockdownembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                        try:
                            await message.author.send(embed=unlockdownembed)
                        except:
                            await message.channel.send(embed=unlockdownembed)
                        await message.add_reaction("❌")
                        return

                #else if the entered text is not a channel
                else:
                    #if the channel entered is not real or doesnt exist output an error message
                    unlockdownembed = discord.Embed(title="Unockdown Cmd Error: ", color=embedcolour)
                    unlockdownembed.add_field(name="Channel Error: ", value = "\nMake sure that you enter an actual channel.")
                    unlockdownembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                    try:
                        await message.author.send(embed=unlockdownembed)
                    except:
                        await message.channel.send(embed=unlockdownembed)
                    await message.add_reaction("❌")
                    return

            #lockdown the channel and provide conformation by a reaction
            unlockdownoverwrite = channel.overwrites_for(message.guild.default_role)

            #if the channel is not locked
            if unlockdownoverwrite.send_messages == None or unlockdownoverwrite.send_messages == True:
                await message.add_reaction("❌")
                await message.channel.send("This channel is not locked!")
                return

            unlockdownoverwrite.send_messages = None
            await channel.set_permissions(message.guild.default_role, overwrite=unlockdownoverwrite)
            await message.add_reaction("✅")
        
        #code for get tester command (BOT OWNER ONLY) INACTIVE COMMAND
        elif command == "get tester" and message.author.id == 457517248786202625 and False:
            await message.delete()
            testermsg = await message.channel.send("<@&865877112282808371> a tester is required, react to this message to become a tester this time!", delete_after=600)
            
            try:
                testerreaction = await client.wait_for("reaction_add", timeout=600)
            except asyncio.TimeoutError:
                await message.channel.send("A tester did not react quick enough!", delete_after=600)
            else:
                testeruser = message.guild.get_member(testerreaction[1].id)
                await testeruser.add_roles(message.guild.get_role(865515162122584085), reason="Wanted to be a tester.")
                await message.channel.send("{0} Was selected to be a tester!".format(testeruser.mention), delete_after=600)

        #code for create tester application embed
        elif command == "tester application information" and message.author.id == 457517248786202625:

            await message.delete()
            applicationembed = discord.Embed(title="Tester Applications", description="To become a tester, all that is required is to convince me that you should be a tester for the bot. This is intentionally very open ended, and no advice will be given on how to go about this, since I want to see how all of you who actually want to be a tester can convince me! Tester applications will be constantly running, until specified otherwise.", color=embedcolour)
            applicationembed.add_field(name="Expectations of a Tester:", value="Testers are required to be relatively active on discord, so that you can provide an appreciable amount of testing help with the bot, and if a tester cannot meet the required expectations, their role will be removed. Also, when new features come out, make sure to try and break them as much as you can! (However odd this sounds, I encourage anyone who wants to be a tester regardless of if they have the role or not to try and do this, who knows, you might end up becoming a tester anyway.)", inline=False)
            applicationembed.add_field(name="Tester Rewards:", value="As well as receiving the <@&865877112282808371> role, becoming a tester will:\n - Provide you access to the <#865515102265933854> channel where I will be carrying out testing for the bot, and so can you! Any issues raised here by testers will be more private and noted more easily by me.\n - Any suggestions put into <#859939744199606272> will be more weighted, almost like the <@&860112148964704259> role.\n - Testers with more than 5 contributions/bugs spotted/times tested when requested will get the <@&863847233878622219> role.", inline=False)
            applicationembed.add_field(name="How to Submit Applications:", value="Simply send the application in this channel, and I will action your application soon. Do not send your application more than once, unless it was not accepted, in which case wait for the bot the start running again. Your application has been accepted if you see a prompt after you sent your message saying the application succeeded! (Note: Any spamming of this will result in a mute or ban). **The application has to be under 2048 characters in size or it will not be accepted**")
            applicationembed.set_footer(text="Happy testing! Sai art by: Dingier on Deviant Art - https://www.deviantart.com/dingier", icon_url=client.user.avatar_url)
            applicationembed.set_image(url="https://cdn.discordapp.com/attachments/886205213420191795/889121596244103178/saitesterapplication.png")
            await message.channel.send(embed=applicationembed)
        
        
        #endregion

        #fun
        #region

        #code for decide command
        elif command[0:7] == "decide " or command[0:7] == "choose " or command[0:5] == "roll " or command == "decide" or command == "choose" or command == "roll":

            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.decide + timedelta(seconds=decidecooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.decide = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.decide + timedelta(seconds=decidecooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("decide", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return
            
            #create list of params
            if command[0:6] == "decide":
                decideparams = createparamlist("decide", command, ",")
            elif command[0:6] == "choose":
                decideparams = createparamlist("choose", command, ",")
            else:
                decideparams = createparamlist("roll", command, ",")

            #if 0 or 1 choice(s) is entered send a message 
            if decideparams == [""]:
                await message.channel.send("<@{0}> You need to enter at least 2 choices <:facepalm:860913056040747088>".format(message.author.id))
                return
            elif len(decideparams) == 1:
                await message.channel.send("<@{0}> I'm not sure what to choose, seems too hard 😗".format(message.author.id))
                return

            #create and send embed
            decideembed = discord.Embed(title="The Decision: ", color=embedcolour)
            decideembed.add_field(name="Sai's decision was: ", value="­\n\n{0}\n\n­".format(choice(decideparams)))
            decideembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
            await message.channel.send(embed=decideembed)
        
        #code for sai gif command
        elif command == "gif":

            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.gif + timedelta(seconds=gifcooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.gif = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.gif + timedelta(seconds=gifcooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("gif", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return

            randomgif = choice(saigifs)
            await message.channel.send(randomgif)

        #code for quote command
        elif command == "quote":
            
            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.quote + timedelta(seconds=quotecooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.quote = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.quote + timedelta(seconds=quotecooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("quote", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return

            #sends a random Sai quote
            await message.channel.send(f"\"{choice(saiquotes)}\"")

        #code for tulaii weekly gif command
        elif command == "tulaiiisabigman":

            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.tulaiiisabigman + timedelta(seconds=tulaiiisabigmancooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.tulaiiisabigman = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.tulaiiisabigman + timedelta(seconds=tulaiiisabigmancooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("tulaiiisabigman", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return
            
            #sends gif
            await message.channel.send(weeklytulaiigif)
        
        #code for 8ball command
        elif command == "8ball" or command[0:6] == "8ball ":
            #firstly checks if the cooldown has been met
            if (currentuser.cooldowns.eightball + timedelta(seconds=eightballcooldown) <= datetime.now()) or message.author.id == 457517248786202625:
                currentuser.cooldowns.eightball = datetime.now()
            else:
                timeleft = (currentuser.cooldowns.eightball + timedelta(seconds=eightballcooldown)) - datetime.now()
                timeleft = formattimedelta(timeleft)
                cooldownembed = getcooldownembed("8ball", timeleft, message.author)
                await message.channel.send(embed=cooldownembed)
                return

            #if no question asked
            if command == "8ball":
                await message.channel.send("<@{0}> You need to enter a question for me <:facepalm:860913056040747088>".format(message.author.id))
                return
            #otherwise return answer
            else:
                question = command[6:]
                await message.channel.send("<@{0}> {1}".format(message.author.id, choice(eightballreplies)))
        

        #endregion
       
    
    #if message is sent in Sai server's bot-suggestions, react to it
    if message.channel.id == 859939744199606272:

        #if the message is in the correct format then add up and downvotes
        if search("[S].+\n.+[R].+", message.content):
            await message.add_reaction("\N{White Heavy Check Mark}")
            await message.add_reaction("\N{Upwards Black Arrow}")
            await message.add_reaction("\N{Downwards Black Arrow}")
            await sleep(5)
            await message.remove_reaction("\N{White Heavy Check Mark}", client.user)

        #else delete the message and send dm to the user
        else:
            await message.delete()
            suggembed = discord.Embed(title="Suggestion Error: ", color=embedcolour)
            suggembed.add_field(name="Format Error: ", value = "Check pinned messages in `bot-suggestions` to make sure your message is in the correct format.")
            suggembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
            try:
                await message.author.send(embed=suggembed)
            except:
                pass


@client.event
async def on_message_delete(message):

    #add message to the snipe dictionary if the message is not from a bot
    if not message.author.bot:
        snipedict[message.channel.id] = message


@client.event
async def on_message_edit(before, after):

    #add message to the edit snipe dictionary if the message is not from a bot
    if not before.author.bot:
        editsnipedict[before.channel.id] = before


@client.event
async def on_raw_reaction_add(payload):
    #get message from payload
    try:
        message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    except:
        print("Message could not be fetched when reaction added!")
        return

    #if reaction is from Sai, or another bot no action is taken
    try:
        if payload.member.bot:
            return
    except:
        print("Bot-or-not status could not be fetched when reaction removed!")
        return
    try:
        if payload.member == client.user:
            return
    except:
        print("Member could not be fetched when reaction added!")
        return

    #start database conection
    dbconnection = sqlite3.connect(database)
    cursor = dbconnection.cursor()

    #retrieve tables' information
    cursor.execute("SELECT * FROM events")
    eventsdb = cursor.fetchall()    
    
    #what type of message was reacted to
    iseventmessage = False
    istesterreactionrolemessage = False
    try:
        for event in eventsdb:
            if event[0] == int(message.id):
                iseventmessage = True
                break
        testeremoji = client.get_emoji(865963914721886248)
        if message.id == 880778807219470346 and payload.emoji == testeremoji:
            istesterreactionrolemessage = True
    except:
        print("Type of message could not be fetched!")

    if iseventmessage:
        previouseventembed = message.embeds[0]

        #get event from Sai db
        geteventcommand = """SELECT * FROM events WHERE eventid={0}""".format(int(message.id))
        cursor.execute(geteventcommand)
        event = cursor.fetchall()
        attending = event[0][1]
        unsure = event[0][2]
        notattending = event[0][3]
        reactorguild = await client.fetch_guild(payload.guild_id)
        reactormember = await reactorguild.fetch_member(payload.user_id)
        eventreactor = "{0}#{1}".format(reactormember.name, reactormember.discriminator) 

        #get reactions
        eventreactions = message.reactions
        attendingusers = []
        unsureusers = []
        notattendingusers = []
        for reaction in eventreactions:
            try:
                if reaction.emoji == "✅":
                    async for user in reaction.users():
                        attendingusers.append(user)
                elif reaction.emoji == "❔":
                    async for user in reaction.users():
                        unsureusers.append(user)
                elif reaction.emoji == "❌":
                    async for user in reaction.users():
                        notattendingusers.append(user)
            except:
                pass

        #if user reacted as attending
        if str(payload.emoji) == "✅":            

            #add user who reacted to attending in Sai db if not reacted elsewhere
            if (not (eventreactor in attending.split(",") or eventreactor in unsure.split(",") or eventreactor in notattending.split(",")) and ((not (reactormember in unsureusers)) or (not (reactormember in notattendingusers)))):
                attending += "{0},".format(eventreactor)
                updateattendingcommand = """UPDATE events SET attending="{0}" WHERE eventid={1}""".format(attending, int(message.id))
                cursor.execute(updateattendingcommand)

                #update embed
                neweventembed = updateeventembed(previouseventembed, attending, unsure, notattending)
                await message.edit(embed=neweventembed)

        #else if user reacted as unsure
        elif str(payload.emoji) == "❔":

            #add user who reacted to unsure in Sai db if not reacted elsewhere
            if (not (eventreactor in attending.split(",") or eventreactor in unsure.split(",") or eventreactor in notattending.split(",")) and ((not (reactormember in attendingusers)) or (not (reactormember in notattendingusers)))):
                unsure += "{0},".format(eventreactor)
                updateunsurecommand = """UPDATE events SET unsure="{0}" WHERE eventid={1}""".format(unsure, int(message.id))
                cursor.execute(updateunsurecommand)

                #update embed
                neweventembed = updateeventembed(previouseventembed, attending, unsure, notattending)
                await message.edit(embed=neweventembed)

        #else if user reacted as notattending
        elif str(payload.emoji) == "❌":

            #add user who reacted to notattending in Sai db if not reacted elsewhere
            if (not (eventreactor in attending.split(",") or eventreactor in unsure.split(",") or eventreactor in notattending.split(",")) and ((not (reactormember in attendingusers)) or (not (reactormember in unsureusers)))):
                notattending += "{0},".format(eventreactor)
                updatenotattendingcommand = """UPDATE events SET notattending="{0}" WHERE eventid={1}""".format(notattending, int(message.id))
                cursor.execute(updatenotattendingcommand)

                #update embed
                neweventembed = updateeventembed(previouseventembed, attending, unsure, notattending)
                await message.edit(embed=neweventembed)
            
    elif istesterreactionrolemessage:
        reactor = await message.guild.fetch_member(payload.user_id)
        await reactor.add_roles(message.guild.get_role(865877112282808371), reason="Reacted to the tester reaction role")


    #close database connection
    dbconnection.commit()
    dbconnection.close()


@client.event
async def on_raw_reaction_remove(payload):
    #get message from payload
    try:
        message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    except:
        print(f"Message could not be fetched when reaction removed!")
        return

    #if reaction is from Sai, or anothre bot, no action is taken
    try:
        if payload.member.bot:
            return
    except:
        print("Bot-or-not status could not be fetched when reaction removed!")
        return
    try:
        if payload.member == client.user:
            return
    except:
        print("Member could not be fetched when reaction removed!")
        return

    #start database conection
    dbconnection = sqlite3.connect(database)
    cursor = dbconnection.cursor()

    #retrieve tables' information
    cursor.execute("SELECT * FROM events")
    eventsdb = cursor.fetchall()    
    
    #what type of message was reacted to
    iseventmessage = False
    istesterreactionrolemessage = False
    try:
        for event in eventsdb:
            if event[0] == int(message.id):
                iseventmessage = True
                break
        testeremoji = client.get_emoji(865963914721886248)
        if message.id == 880778807219470346 and payload.emoji == testeremoji:
            istesterreactionrolemessage = True
    except:
        print("Type of message could not be fetched!")

    if iseventmessage:
        previouseventembed = message.embeds[0]

        #get event from Sai db
        geteventcommand = """SELECT * FROM events WHERE eventid={0}""".format(int(message.id))
        cursor.execute(geteventcommand)
        event = cursor.fetchall()
        attending = event[0][1]
        unsure = event[0][2]
        notattending = event[0][3]
        unreactorguild = await client.fetch_guild(payload.guild_id)
        unreactormember = await unreactorguild.fetch_member(payload.user_id)
        eventunreactor = "{0}#{1}".format(unreactormember.name, unreactormember.discriminator) 

        #loop through reactions and get a list of 
        eventreactions = message.reactions
        attendingusers = []
        unsureusers = []
        notattendingusers = []
        for reaction in eventreactions:
            try:
                if reaction.emoji == "✅":
                    async for user in reaction.users():
                        attendingusers.append(user)
                elif reaction.emoji == "❔":
                    async for user in reaction.users():
                        unsureusers.append(user)
                elif reaction.emoji == "❌":
                    async for user in reaction.users():
                        notattendingusers.append(user)
            except:
                pass


        #if the user unreacted with attending and they are attending
        if str(payload.emoji) == "✅":
            
            if eventunreactor in attending.split(","):
                #remove the reactor from attending list in Sai db
                attending = attending.replace("{0},".format(eventunreactor), "")
                updateattendingcommand = """UPDATE events SET attending="{0}" WHERE eventid={1}""".format(attending, int(message.id))
                cursor.execute(updateattendingcommand)

            #if user is reacted as also unsure
            if (unreactormember in unsureusers and (not (unreactormember in notattendingusers)) and (not (eventunreactor in unsure.split(",")))):

                #add user who is also reacted as unsure in Sai db if not reacted elsewhere
                unsure += "{0},".format(eventunreactor)
                updateunsurecommand = """UPDATE events SET unsure="{0}" WHERE eventid={1}""".format(unsure, int(message.id))
                cursor.execute(updateunsurecommand)

            #if user is reacted as also not attending
            elif (unreactormember in notattendingusers and (not (unreactormember in unsureusers)) and (not (eventunreactor in notattending.split(",")))):

                #add user who is also reacted as unsure in Sai db if not reacted elsewhere
                notattending += "{0},".format(eventunreactor)
                updatenotattendingcommand = """UPDATE events SET notattending="{0}" WHERE eventid={1}""".format(notattending, int(message.id))
                cursor.execute(updatenotattendingcommand)

            #update embed
            neweventembed = updateeventembed(previouseventembed, attending, unsure, notattending)
            await message.edit(embed=neweventembed)

        #else if the user unreacted with unsure and they are unsure
        elif str(payload.emoji) == "❔":

            if eventunreactor in unsure.split(","):
                #remove the reactor from unsure list in Sai db
                unsure = unsure.replace("{0},".format(eventunreactor), "")
                updateunsurecommand = """UPDATE events SET unsure="{0}" WHERE eventid={1}""".format(unsure, int(message.id))
                cursor.execute(updateunsurecommand)

            #if user is reacted as also attending
            if (unreactormember in attendingusers and (not (unreactormember in notattendingusers)) and (not (eventunreactor in attending.split(",")))):

                #add user who is also reacted as unsure in Sai db if not reacted elsewhere
                attending += "{0},".format(eventunreactor)
                updateattendingcommand = """UPDATE events SET attending="{0}" WHERE eventid={1}""".format(attending, int(message.id))
                cursor.execute(updateattendingcommand)

            #if user is reacted as also not attending
            elif (unreactormember in notattendingusers and (not (unreactormember in attendingusers)) and (not (eventunreactor in notattending.split(",")))):

                #add user who is also reacted as unsure in Sai db if not reacted elsewhere
                notattending += "{0},".format(eventunreactor)
                updatenotattendingcommand = """UPDATE events SET notattending="{0}" WHERE eventid={1}""".format(notattending, int(message.id))
                cursor.execute(updatenotattendingcommand)

            #update embed
            neweventembed = updateeventembed(previouseventembed, attending, unsure, notattending)
            await message.edit(embed=neweventembed)

        #else if the user unreacted with attending and they are attending
        elif str(payload.emoji) == "❌":

            if eventunreactor in notattending.split(","):
                #remove the reactor from attending list in Sai db
                notattending = notattending.replace("{0},".format(eventunreactor), "")
                updatenotattendingcommand = """UPDATE events SET notattending="{0}" WHERE eventid={1}""".format(notattending, int(message.id))
                cursor.execute(updatenotattendingcommand)

            #if user is reacted as also attending
            if (unreactormember in attendingusers and (not (unreactormember in unsureusers)) and (not (eventunreactor in attending.split(",")))):

                #add user who is also reacted as unsure in Sai db if not reacted elsewhere
                attending += "{0},".format(eventunreactor)
                updateattendingcommand = """UPDATE events SET attending="{0}" WHERE eventid={1}""".format(attending, int(message.id))
                cursor.execute(updateattendingcommand)

            #if user is reacted as also unsure
            elif (unreactormember in unsureusers and (not (unreactormember in attendingusers)) and (not (eventunreactor in unsure.split(",")))):

                #add user who is also reacted as unsure in Sai db if not reacted elsewhere
                unsure += "{0},".format(eventunreactor)
                updateunsurecommand = """UPDATE events SET unsure="{0}" WHERE eventid={1}""".format(unsure, int(message.id))
                cursor.execute(updateunsurecommand)

            #update embed
            neweventembed = updateeventembed(previouseventembed, attending, unsure, notattending)
            await message.edit(embed=neweventembed)

    elif istesterreactionrolemessage:
        reactor = await message.guild.fetch_member(payload.user_id)
        await reactor.remove_roles(message.guild.get_role(865877112282808371), reason="Reacted to the tester reaction role")
    
    #close database connection
    dbconnection.commit()
    dbconnection.close()


@client.event
async def on_member_join(member):

    #if the server joined is the Sai bot server then send a dm
    if member.guild.id == 859934506159833178:
        joinembed = discord.Embed(title="Welcome to my server!", description="I hope you enjoy your time here, make sure you read the rules under **'Welcome & Info'**. If you have any queries, feel free to ask!", color=embedcolour)
        joinembed.set_thumbnail(url=member.guild.icon_url)
        joinembed.set_footer(text="Welcome {0}#{1}".format(member.name, member.discriminator), icon_url=member.avatar_url)
        try:
            await member.send(embed=joinembed)
        except:
            pass


@client.event
async def on_guild_join(guild):

    #send the guild join welcome message
    general = False
    for text_channel in guild.text_channels:
        if "general" in text_channel.name.lower():
            general = text_channel
    owner = await client.fetch_user(457517248786202625)
    ownername = "{}#{}".format(owner.name, owner.discriminator)
    owneravatar = owner.avatar_url 
    welcomeembed = discord.Embed(title="Thank you for inviting Sai!", description="I hope you will enjoy using my bot, and if you ever need help with anything to do with the bot, run `s.help`, or simply ping sai with @Sai#9289. If you need more help, you can join the official Sai Support server." , colour=embedcolour)
    welcomeembed.set_author(name="Bot created by {0}".format(ownername), icon_url=owneravatar)
    welcomeembed.set_thumbnail(url=client.user.avatar_url)
    welcomeembed.set_image(url="https://cdn.discordapp.com/attachments/777130317815349258/911657189712740443/tumblr_a5c8249773e4e4cdcf83eef4fd7ca917_ae2bc31f_500.gif")
    welcomeembed.add_field(name=f"First time commands <:info:881883500515590144>:", value="```s.help\ns.links\ns.about\ns.patreon```",inline=True)
    welcomeembed.add_field(name=f"Naruto commands <:naruto:886208833393938452>:", value="```s.character\ns.info\ns.gif\ns.quote```",inline=True)
    welcomeembed.add_field(name=f"Moderation and Utility commands <:moderation_and_admin:881897640948826133>:",value="```s.ban\ns.kick\ns.event\ns.time```", inline=True)
    welcomeembed.add_field(name=f"Additional information:",value="Thanks for supporting Sai by inviting this bot to your server! For more support options, you can run `s.links` and `s.patreon`. To get command specific help, run `s.help` followed by the command, as shown here: `s.help character`.", inline=False)
    welcomeembed.set_footer(text="Have an amazing day, and I hope you enjoy your time while Sai is on your server! If you need a custom version of the bot, do not hesitate to contact the owner. | Welcome image taken from here: https://gfycat.com/leafycoolisabellineshrike", icon_url=guild.icon_url)
    if general: 
        try:
            await general.send(embed=welcomeembed)
        except:
            try:
                await guild.owner.send(embed=welcomeembed)
            except:
                print("Guild Owner's DMs are closed, could not send welcome message.")
    else:
        try:
            await guild.owner.send(embed=welcomeembed)
        except:
            print("Guild Owner's DMs are closed, could not send welcome message.")



    #code for logging the guild join
    loggingtime = datetime.utcnow().strftime("%#A, %#d %#B\n%H:%M:%S:%f")

    loggingembed=discord.Embed(title="Guild Joined", colour=embedcolour)
    loggingembed.add_field(name="Server", value=f"```{guild.name} (id:{guild.id})```", inline=True)
    loggingembed.add_field(name="Time", value=f"```{loggingtime}```", inline=True)
    loggingembed.set_footer(text="Owner {0}#{1}".format(guild.owner.name, guild.owner.discriminator), icon_url=guild.owner.avatar_url)
    await client.get_guild(859934506159833178).get_channel(881913733532758036).send(embed=loggingembed)

@client.event
async def on_guild_remove(guild):
    try:
        #code for logging the guild leave
        loggingtime = datetime.utcnow().strftime("%#A, %#d %#B\n%H:%M:%S:%f")

        loggingembed=discord.Embed(title="Guild Left", colour=embedcolour)
        loggingembed.add_field(name="Server", value=f"```{guild.name} (id:{guild.id})```", inline=True)
        loggingembed.add_field(name="Time", value=f"```{loggingtime}```", inline=True)
        loggingembed.set_footer(text="Owner {0}#{1}".format(guild.owner.name, guild.owner.discriminator), icon_url=guild.owner.avatar_url)
        await client.get_guild(859934506159833178).get_channel(881913733532758036).send(embed=loggingembed)
    except:
        pass

@client.event
async def on_error(event, *args, **kwargs):
    message = args[0]  
    print(f"error at {datetime.now()} with {message}")
    try:       
        errorembed = discord.Embed(title="Permissions Error:", description="Error in running the command: {0} ```{1}```".format(message.content, message), color=embedcolour)
        errorembed.add_field(name="Why?", value="Most likely the bot did not have the required permissions in the server to carry out your request. Please join the [official Sai Support server](https://discord.gg/BSFCCFKK7f) to report this if you think the error was not caused by permission errors!")
        errorembed.set_footer(text="Error Triggered")
        await message.author.send(embed=errorembed)
        await client.get_guild(859934506159833178).get_channel(881913733532758036).send(embed=errorembed)
    except:
        try:
            await message.channel.send(embed=errorembed)
        except:
            print("FATAL ERROR")
    

#endregion

#new events i.e. slash commands
#region

def get_current_user(author):
    adduser = True
    for user in allcooldowns:
        if int(user.userID) == int(author.id):
            adduser = False
            currentuser = allcooldowns[allcooldowns.index(user)]
            break
            
    if adduser:
        newuser = usercooldown(int(author.id)) 
        allcooldowns.append(newuser)
        currentuser = allcooldowns[-1]
    return currentuser

@slash.slash(name="voteReminder", description="This is a command that will remind after twelve hours to vote for Sai on top.gg!", guild_ids=[729672504662294669])
async def test(ctx: SlashContext):
    #firstly checks if the cooldown has been met
    try:
        currentuser = get_current_user(ctx.author)
        if (currentuser.cooldowns.votereminder + timedelta(seconds=voteremindercooldown) <= datetime.now()) or ctx.author.id == 457517248786202625:
            currentuser.cooldowns.votereminder = datetime.now()
        else:
            timeleft = (currentuser.cooldowns.votereminder + timedelta(seconds=voteremindercooldown)) - datetime.now()
            timeleft = formattimedelta(timeleft)
            cooldownembed = getcooldownembed("/votereminder", timeleft, ctx.author)
            await ctx.send(embed=cooldownembed)
            return
        voteremindembed = discord.Embed(title="Reminder Set.", description="A reminder has been set for 12 hours from now! A DM will be sent to you at the time, to prevent clogging up channels, so make sure you have your DMs open! If you want to vote now, you can do that here:\nhttps://top.gg/bot/858663143931641857", color=embedcolour)
        voteremindembed.set_footer(text="Command run by {0}#{1}".format(ctx.author.name, ctx.author.discriminator), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=voteremindembed)
    except Exception as e:
        await ctx.send(content=f"An error occured!\n```Send this error message to the bot developer\n{e}```")
        return
    await sleep(43200)
    await ctx.author.send("You can vote!")


#endregion
if __name__ == "__main__":
    #start the bot if run from the file not imported
    switchstatus.start()
    client.run(TOKEN)
