import discord
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from random import choice
import sqlite3
from re import search
from asyncio import sleep


#gets client token and creates client
load_dotenv()
TOKEN = os.getenv("TOKEN")
client = discord.Client()

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
database = r"C:\Users\Jonathan\Personal OneDrive\OneDrive\GameDev\SaiBot\SaiDatabase.db"
#endregion

#functions
#region
def createparamlist(commandname, parametersstring, delimiter):
    parameterslist = parametersstring.replace(commandname, "").split(delimiter)
    parameterslist = [parameter.strip() for parameter in parameterslist]
    return parameterslist
def updateeventembed(previousembed, attending, unsure, notattending):
    neweventembed=discord.Embed(title=previousembed.title, description=previousembed.description, color=embedcolour)
    neweventembed.set_thumbnail(url=previousembed.thumbnail.url)
    neweventembed.add_field(name="­\n  :white_check_mark: Attending", value=">>> ­{0}".format("\n".join(attending.split(",")).strip("\n")), inline=False)
    neweventembed.add_field(name="­\n  :grey_question: Unsure", value=">>> ­{0}".format("\n".join(unsure.split(",")).strip("\n")), inline=False)
    neweventembed.add_field(name="­\n  :x:Not Attending", value=">>> ­{0}".format("\n".join(notattending.split(",")).strip("\n")), inline=False)
    neweventembed.add_field(name="­­\n\nHow to choose preference/status­: ", value="Simply react to the message below with the corresponding emoji, and if you want to change your choice, make sure you unreact to the first choice.", inline=False)
    neweventembed.set_footer(text=previousembed.footer.text, icon_url=previousembed.footer.icon_url)
    return neweventembed
#endregion

#events
#region

@client.event
async def on_ready():

    #returns login message to console
    print("Logged in as {0.user}".format(client))  
    print("Bot created on {0}".format(client.user.created_at))

    return


@client.event
async def on_connect():

    #sets status
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with calligraphy sets"))

    return


@client.event
async def on_message(message):

    #processes message
    content = message.content

    #if message is from Sai Bot no action is taken
    if message.author == client.user:
        return

    #else if prefix is recognised
    elif content.startswith("s."):

        #processes the command entered
        command = message.content[2:].strip()

        #code for help command
        if command.startswith("help"):
            await message.channel.send("<@{0}> Help command coming soon...".format(message.author.id))

        #code for time command
        elif command.startswith("time"):

            #creating list of params
            timezones = createparamlist("time", command, ",")

            #checking for special params and user errors
            if timezones == [""]:
                timezones = ["UTC"]
            elif timezones[0].upper() == "ALL":
                timezones = [timezone for timezone in alltimezones]
            for timezone in timezones:
                if timezone.upper() not in alltimezones:
                    await message.channel.send("<@{0}>, make sure the timezones are in the correct format or are in the bot's timezone list.".format(message.author.id), delete_after=10)
                    return

            #create embed for time command
            timeembed=discord.Embed(title="Time :clock9:", color=embedcolour)
            for timezone in timezones:
                time = datetime.utcnow() + timedelta(hours = alltimezones[timezone.upper()])
                time = time.strftime("%#A, %#d %#B\n%#H:%#M:%#S")
                timeembed.add_field(name=timezone.upper(), value="`{0}`".format(time), inline=True)
            timeembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
            await message.channel.send(embed=timeembed)

        #code for msg command
        elif (command.startswith("msg") or command.startswith("message")) and message.author.guild_permissions.administrator:
            
            #create list of params
            if command.startswith("msg"):
                msgparams = createparamlist("msg", command, "|")
            else:
                msgparams = createparamlist("message", command, "|")

            #send msg to channel
            try:
                msgchannel = client.get_channel(int(msgparams[0]))

                #if channel in same guild send message, otherwise dm the message sender that the channel has to be in the same guild
                if message.channel.guild == msgchannel.guild or message.author.id == 457517248786202625:
                    await msgchannel.send(msgparams[1])
                else:
                    msgembed = discord.Embed(title="Msg Cmd Error: ", color=embedcolour)
                    msgembed.add_field(name="Channel Error: ", value = "\nMake sure that the `<channelid>` is in the same guild that you are running the command.\n*(You cannot send messages via Sai cross-guild.)*")
                    msgembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                    await message.author.send(embed=msgembed)
            except:
                msgembed = discord.Embed(title="Msg Cmd Error: ", color=embedcolour)
                msgembed.add_field(name="Format Error: ", value = "\nCheck that the following format has been followed\n\n`s.dm <channelid>, <message>`")
                msgembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.author.send(embed=msgembed)

        #code for decide command
        elif command.startswith("decide"):

            #create list of params
            decideparams = createparamlist("decide", command, ",")

            #create and send embed
            decideembed = discord.Embed(title="The Decision: ", color=embedcolour)
            decideembed.add_field(name="Sai's decision was: ", value="­\n\n{0}\n\n­".format(choice(decideparams)))
            decideembed.set_footer(text="Command run by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
            await message.channel.send(embed=decideembed)

        #code for event command
        elif command.startswith("event") and message.author.guild_permissions.administrator:

            #create event param list
            eventparams = createparamlist("event", command, "|")

            #split up the params and add more variables
            try:
                eventchannel = client.get_channel(int(eventparams[0]))
            except:
                msgembed = discord.Embed(title="Event Cmd Error: ", color=embedcolour)
                msgembed.add_field(name="Channel Error: ", value = "The channel you want to create the event in might not exist, or cannot be seen by Sai")
                msgembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.author.send(embed=msgembed)
                return
            eventtitle = eventparams[1]
            eventdescription = eventparams[2]
            eventguildicon = message.guild.icon_url

            #send dm to command sender if channel is not in guild
            if eventchannel.guild != message.guild:
                eventembed = discord.Embed(title="Event Cmd Error: ", color=embedcolour)
                eventembed.add_field(name="Syntax Error: ", value = "The channel you want to create the event in has to be within the same guild.")
                eventembed.set_footer(text="Error Triggered by {0}#{1}".format(message.author.name, message.author.discriminator), icon_url=message.author.avatar_url)
                await message.author.send(embed=eventembed)
                return

            #create event embed
            eventembed=discord.Embed(title=eventtitle, description=eventdescription, color=embedcolour)
            eventembed.set_thumbnail(url=eventguildicon)
            eventembed.add_field(name="­  :white_check_mark: Attending", value=">>> ­", inline=True)
            eventembed.add_field(name="­  :grey_question: Unsure", value=">>> ­­­­­­­", inline=True)
            eventembed.add_field(name="­  :x: Not Attending", value=">>> ­", inline=True)
            eventembed.add_field(name="­­\n\nHow to choose preference/status­: ", value="Simply react to the message below with the corresponding emoji, and if you want to change your choice, make sure you unreact to the first choice.", inline=False)
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
            await message.author.send(embed=suggembed)

@client.event
async def on_raw_reaction_add(payload):
    #get message from payload
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)

    #if reaction is from Sai, no action is taken
    if payload.member == client.user:
        return

    #start database conection
    dbconnection = sqlite3.connect(database)
    cursor = dbconnection.cursor()

    #retrieve tables' information
    cursor.execute("SELECT * FROM events")
    eventsdb = cursor.fetchall()    
    
    #what type of message was reacted to
    iseventmessage = False
    for event in eventsdb:
        if event[0] == int(message.id):
            iseventmessage = True
            break
    if iseventmessage:
        previouseventembed = message.embeds[0]

        #get event from Sai db
        geteventcommand = """SELECT * FROM events WHERE eventid={0}""".format(int(message.id))
        cursor.execute(geteventcommand)
        event = cursor.fetchall()
        attending = event[0][1]
        unsure = event[0][2]
        notattending = event[0][3]
        eventreactor = "{0}#{1}".format(payload.member.name, payload.member.discriminator)

        #if user reacted as attending
        if str(payload.emoji) == "✅":            

            #add user who reacted to attending in Sai db if not reacted elsewhere
            if not (eventreactor in attending.split(",") or eventreactor in unsure.split(",") or eventreactor in notattending.split(",")):
                attending += "{0},".format(eventreactor)
                updateattendingcommand = """UPDATE events SET attending="{0}" WHERE eventid={1}""".format(attending, int(message.id))
                cursor.execute(updateattendingcommand)

                #update embed
                neweventembed = updateeventembed(previouseventembed, attending, unsure, notattending)
                await message.edit(embed=neweventembed)

        #else if user reacted as unsure
        elif str(payload.emoji) == "❔":

            #add user who reacted to unsure in Sai db if not reacted elsewhere
            if not (eventreactor in attending.split(",") or eventreactor in unsure.split(",") or eventreactor in notattending.split(",")):
                unsure += "{0},".format(eventreactor)
                updateunsurecommand = """UPDATE events SET unsure="{0}" WHERE eventid={1}""".format(unsure, int(message.id))
                cursor.execute(updateunsurecommand)

                #update embed
                neweventembed = updateeventembed(previouseventembed, attending, unsure, notattending)
                await message.edit(embed=neweventembed)

        #else if user reacted as notattending
        elif str(payload.emoji) == "❌":

            #add user who reacted to notattending in Sai db if not reacted elsewhere
            if not (eventreactor in attending.split(",") or eventreactor in unsure.split(",") or eventreactor in notattending.split(",")):
                notattending += "{0},".format(eventreactor)
                updatenotattendingcommand = """UPDATE events SET notattending="{0}" WHERE eventid={1}""".format(notattending, int(message.id))
                cursor.execute(updatenotattendingcommand)

                #update embed
                neweventembed = updateeventembed(previouseventembed, attending, unsure, notattending)
                await message.edit(embed=neweventembed)
            

    #close database connection
    dbconnection.commit()
    dbconnection.close()


@client.event
async def on_raw_reaction_remove(payload):
    #get message from payload
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)

    #if reaction is from Sai, no action is taken
    if payload.member == client.user:
        return

    #start database conection
    dbconnection = sqlite3.connect(database)
    cursor = dbconnection.cursor()

    #retrieve tables' information
    cursor.execute("SELECT * FROM events")
    eventsdb = cursor.fetchall()    
    
    #what type of message was reacted to
    iseventmessage = False
    for event in eventsdb:
        if event[0] == int(message.id):
            iseventmessage = True
            break
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
        #if the user unreacted with attending and they are attending
        if str(payload.emoji) == "✅" and (eventunreactor in attending.split(",")):
            #remove the reactor from attending list in Sai db
            attending = attending.replace("{0},".format(eventunreactor), "")
            updateattendingcommand = """UPDATE events SET attending="{0}" WHERE eventid={1}""".format(attending, int(message.id))
            cursor.execute(updateattendingcommand)

            #update embed
            neweventembed = updateeventembed(previouseventembed, attending, unsure, notattending)
            await message.edit(embed=neweventembed)

        #else if the user unreacted with unsure and they are unsure
        elif str(payload.emoji) == "❔" and (eventunreactor in unsure.split(",")):

            #remove the reactor from unsure list in Sai db
            unsure = unsure.replace("{0},".format(eventunreactor), "")
            updateunsurecommand = """UPDATE events SET unsure="{0}" WHERE eventid={1}""".format(unsure, int(message.id))
            cursor.execute(updateunsurecommand)

            #update embed
            neweventembed = updateeventembed(previouseventembed, attending, unsure, notattending)
            await message.edit(embed=neweventembed)

        #else if the user unreacted with attending and they are attending
        elif str(payload.emoji) == "❌" and (eventunreactor in notattending.split(",")):

            #remove the reactor from attending list in Sai db
            notattending = notattending.replace("{0},".format(eventunreactor), "")
            updatenotattendingcommand = """UPDATE events SET notattending="{0}" WHERE eventid={1}""".format(notattending, int(message.id))
            cursor.execute(updatenotattendingcommand)

            #update embed
            neweventembed = updateeventembed(previouseventembed, attending, unsure, notattending)
            await message.edit(embed=neweventembed)

    #close database connection
    dbconnection.commit()
    dbconnection.close()


@client.event
async def on_member_join(member):

    #if the server joined is the Sai bot server then send a dm
    if member.guild.id == 859934506159833178:
        joinembed = discord.Embed(title="Welcome to my server!", description="I hope you enjoy your time here, make sure you read the rules under **'Welcome & Info'**. If you have any queries, feel free to ask!", color=embedcolour)
        joinembed.set_thumbnail(member.guild.icon_url)
        joinembed.set_footer(text="Welcome {0}#{1}".format(member.name, member.discriminator), icon_url=member.avatar_url)

#endregion



client.run(TOKEN)