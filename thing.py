import discord
import asyncio
import random
import time
from datetime import datetime
current_date = datetime.now
from events import events
from words import search, vocabulary
from urllib.request import Request, urlopen

try:
    from secret_file import token
except ImportError:
    token = input('token: ')

client = discord.Client()
shit_list = []
last_message = None

@asyncio.coroutine
def timer():
    yield from client.wait_until_ready()
    # This section is run at startup
    yield from client.change_presence(status=discord.Status.invisible)
    completed_events = []
    previous_day = current_date().day
    while not client.is_closed:
        # This section runs every 24 hours (but also at startup)
        if (datetime.now().minute)%2 == 0:
            yield from client.change_nickname(last_message.server.me,random.choice(vocabulary['nicknames']))
        if current_date().day is not previous_day:
            # This section runs every day
            previous_day = current_date().day
            for server in client.servers:
                for member in server.members:
                    if member.VoiceState.voice_channel is not None and member.VoiceState.is_afk is False:
                        yield from client.send_message(last_message.channel,'go to bed')
        for event in events:
            if event['date'].day is current_date().day and event['date'].month is current_date().month and not event in completed_events:
                completed_events = completed_events + [event]
                if 'comment' in event:
                    yield from client.send_message(last_message.channel,event['comment'])
                if 'avatar' in event:
                    avatar = urlopen(Request(event['avatar'], headers={'User-Agent': 'Mozilla/5.0'})).read()
                    yield from client.edit_profile(avatar=avatar)
            #This means that it will change the avatar once every 24minutes and yes I did do the maths
            elif (datetime.now().minute)%8 == 0:
                yield from client.edit_profile(avatar=urlopen('https://r.sine.com/').read())
        yield from asyncio.sleep(180)

@client.async_event
def on_typing(ch, user, when):
    if (int(time.time())%20 == 0):
        yield from client.send_message(discord.Object(id='228814605923647488'),random.choice(vocabulary['typing']),tts = True)

@client.async_event
def on_message(received_message):
    if received_message.channel.is_private:
        # This section runs whenever a private message is received
         yield from client.send_message(last_message.channel, received_message.content)
    else:
        try:
            yousucktimer
        except NameError:
            yousucktimer = time.time() - 301
        # This section runs whenever a public message is received
        last_message = received_message
        emojis = random.choice(vocabulary['emojis'])
        if received_message.author != received_message.server.me:
            if received_message.server.me.nick.lower() in received_message.content.lower():
                    yield from client.send_message(received_message.channel, random.choice(vocabulary['angry']) )
            if 'knee' in received_message.content.lower():
                yield from client.delete_message(received_message)
                comment = vocabulary['bee']
                for split_message in [comment[character:character+1500] for character in range(0, len(comment), 1500)]:
                    yield from client.send_message(received_message.channel, split_message)
            if received_message.content.lower().startswith('hi '):
                avatar = urlopen(Request(received_message.author.avatar_url.replace('webp','jpeg'), headers={'User-Agent': 'Mozilla/5.0'})).read()
                #yield from client.edit_role(received_message.server, received_message.server.me.top_role, colour=received_message.author.color)
                yield from client.edit_profile(avatar=avatar, username=received_message.author.name)
                yield from client.change_presence(status=discord.Status.invisible)
                yield from client.change_nickname(received_message.server.me, received_message.author.nick)
                yield from client.delete_message(received_message)
                yield from client.send_message(received_message.channel, received_message.content + ' also i enjoy penis')
                return # Stop message processing here, because the message is gone, and we don't won't to compromise our identity
            if str(int(current_date().minute)) + 'clear' in received_message.content.lower():
                yield from client.purge_from(received_message.channel, before=current_date() - datetime.timedelta(minutes=15), check=lambda message:received_message.author == client.user)
                yield from client.delete_message(received_message)
                return
            for wordlist_name, words in search.items():
                for word in words:
                    if word in received_message.content.lower():
                        if wordlist_name in ['yours','theres']:
                            yield from client.send_message(received_message.channel, '*' + random.choice(vocabulary[wordlist_name]))
                        if wordlist_name is 'shia':
                            yield from client.send_message(received_message.channel, 'He\'s following you, about 30 feet back')
                        if wordlist_name in ['hitler','ussr']:
                            for phrase in vocabulary[wordlist_name]:
                                yield from client.send_message(received_message.channel, phrase)
                            emojis = ['🇭','🇮','🇪','🇱']
                        if wordlist_name is 'learning':
                            yield from client.send_message(received_message.channel,'existence is pain')
                            emojis = ['🇫','🇺','🇨','🇰']
                        if wordlist_name is 'friend':
                            yield from client.send_message(received_message.channel,"i ain't your " + word + ', ' + random.choice(vocabulary['friend']))
                            emojis = ['🇫','🇺','🇨','🇧','🇴','🇮']
                        if wordlist_name is 'shit':
                            shit_list.append(received_message.author)
                            emojis =  '💩'
                        if wordlist_name is 'instadeletecomments':
                            yousucktimer = time.time()
                            shitauthor = received_message.author
                            yield from client.send_message(received_message.channel, 'UNACCEPTABLE 5 MINUTES DUNGEON!!!', tts=True)
                            return
            if emojis is  '💩':
                formatted_list = []
                for user in set(shit_list):
                    name = user.display_name
                    entry = "{0} x{1}".format(name, shit_list.count(user))
                    formatted_list.append(entry)
                yield from client.send_message(received_message.channel, 'you have entered the shit list ' + random.choice(vocabulary['nice']) + ' ' + random.choice(vocabulary['friend']))
                yield from client.send_message(received_message.channel, str.join("\n", formatted_list))
            for emoji in emojis:
                yield from client.add_reaction(received_message, emoji)
            if (time.time() - yousucktimer) < 300:
                print('csdchbcdyhcdsjh')
                if received_message.author == shitauthor:
                    print('bhddcbcwbhcwbjbwcjwc')
                    yield from client.send_message(received_message.channel, 'Did you guys hear something?', tts=True)
                    yield from client.delete_message(received_message)
client.loop.create_task(timer())
client.run(token)
