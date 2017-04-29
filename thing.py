import discord
import asyncio
import random
import datetime
import schedule
import time 
from words import search, vocabulary
from eventmaker import eventdetector, profilepicture, specialprofilechecker
from urllib.request import Request, urlopen

client = discord.Client()
shit_list = []
most_recent_channel = None

def eventmessage():
    yield from client.send_message(message.channel, random.choice(eventdetector), tts=True) 
    
@client.event
@asyncio.coroutine
def on_message(received_message):
    if received_message.channel.is_private:
         yield from client.send_message(last_message.channel, received_message.content)
    else:
        last_message = received_message
        shitdetector = False;
        triggered = False;
        if received_message.author != received_message.server.me:
            if received_message.server.me.nick.lower() in received_message.content.lower():
                    yield from client.send_message(received_message.channel, random.choice(vocabulary['angry']) )
            if 'bees' in received_message.content.lower():
                comment = vocabulary['bee']
                for split_message in [comment[character:character+1500] for character in range(0, len(comment), 1500)]:
                    yield from client.send_message(received_message.channel, split_message)
            if specialprofilechecker is True:
                schedule.every(10).minutes.do(eventmessage)        
            if received_message.content.lower().startswith('hi'):
                avatar = urlopen(Request(received_message.author.avatar_url.replace('webp','jpeg'), headers={'User-Agent': 'Mozilla/5.0'})).read()
                if avatar is not received_message.server.me.avatar:
                    yield from client.edit_profile(avatar=avatar)
                else:
                    print('didnt fetch shjit')
                if received_message.server.me.server_permissions.manage_roles is True:
                    yield from client.edit_role(received_message.server, received_message.server.me.top_role, colour=received_message.author.color)
                yield from client.edit_profile(username=received_message.author.name)
                yield from client.change_nickname(received_message.server.me, received_message.author.nick)
                yield from client.delete_message(received_message)
                yield from client.send_message(received_message.channel, received_message.content + ' also i enjoy penis')
                return
            if str(int(datetime.datetime.now().minute)) + 'clear' in received_message.content.lower():
                yield from client.purge_from(received_message.channel, before=datetime.datetime.now() - datetime.timedelta(minutes=15), check=lambda message:received_message.author == client.user)
                yield from client.delete_message(received_message)
                return
            for wordlist_name, words in search.items():
                for word in words:
                    if word in received_message.content.lower():
                        if wordlist_name in ['yours','theres']:
                            yield from client.send_message(received_message.channel, '*' + random.choice(vocabulary[wordlist_name]))
                        if wordlist_name is 'shia':
                            yield from client.send_message(received_message.channel, 'He\'s following you, about 30 feet back')
                        if wordlist_name is 'shit':
                            shit_list.append(received_message.author)
                            formatted_list = []
                            for user in set(shit_list):
                                name = user.display_name
                                entry = "{0} x{1}".format(name, shit_list.count(user))
                                formatted_list.append(entry)
                            yield from client.send_message(received_message.channel, 'you have entered the shit list ' + random.choice(vocabulary['nice']) + ' ' + random.choice(vocabulary['friend']))
                            yield from client.send_message(received_message.channel, str.join("\n", formatted_list))
                            shitdetector = True;
                        if wordlist_name in ['hitler','ussr']:
                            for phrase in vocabulary[wordlist_name]:
                                yield from client.send_message(received_message.channel, phrase)
                        if wordlist_name is 'instadeletecomments':
                            triggered = True;
                            yousucktimer = time.time()
                            shitauthor = message.author        
                        if wordlist_name is 'learning':
                            yield from client.send_message(received_message.channel,'existence is pain')
                        if wordlist_name is 'friend':
                            yield from client.send_message(received_message.channel,"i ain't your " + word + ', ' + random.choice(vocabulary['friend']))
            if shitdetector is False:
                yield from client.add_reaction(received_message, random.choice(vocabulary['emojis']))
            else:
                yield from client.add_reaction(received_message, '💩')
            if triggered is True:                 
                while (time.time() - yousucktimer) > 300: 
                    if message.author == shitauthor:
                        yield from client.delete_message(message)
                        yield from client.send_message(message.channel, 'Did you guys hear something?', tts=True)
            if specialprofilechecker is True:            
                yield from client.edit_profile(avatar=urlopen(profilepicture).read())  
            else:                  
                yield from client.edit_profile(avatar=urlopen('https://www.acorn.gov.au/sites/g/files/net1061/f/styles/full-size/public/logo-qld.png?itok=bGXZpG9f').read())       

client.run(input('token: '))
