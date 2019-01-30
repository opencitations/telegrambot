
# coding: utf-8

# In[31]:

import time
import random
import datetime
import telepot
from telepot.loop import MessageLoop
import sys
import glob
import importlib.util
import re

#TELEGRAM BOT PARAMS
TOKEN = '552169683:AAFSmGVWFDxJlL3xp1v2ABw8xU_nkRaUhbA'
BOTNAME = '/OpenCitationsBot'

# Get file paths of all modules.
MODULES_PATH = glob.glob('modules/*.py')


def handle(msg):
    parse_mode = None
    chat_id = msg['chat']['id']

    #print msg['text']
    a_text = msg['text'].split(" ")
    command = a_text[0]
    if a_text[0] == BOTNAME:
        a_text.pop(0)
        if len(a_text) > 0:
            command = a_text[0]

    print('Got command: %s' % command)

    msg = ""
    found_bool = False
    #check command name
    for module in all_commands.keys():
        if all_commands[module]['commands'] != None:
            if command in all_commands[module]['commands'].keys():
                a_text.pop(0)

                if 'parse_mode' in all_commands[module]['commands'][command]:
                    parse_mode = all_commands[module]['commands'][command]['parse_mode']
                else:
                    parse_mode = None

                spec = importlib.util.spec_from_file_location(all_commands[module]['path'],module)
                foo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(foo)

                msg = foo.exec_my_commands(command,a_text)

                found_bool = True
                break

    if(not found_bool):
        msg = "You can ask me:\n"
        for module in all_commands.keys():
            if all_commands[module]['commands'] != None:
                for command in all_commands[module]['commands'].keys():
                    msg = str(msg) + str(command)+": "+ all_commands[module]['commands'][command]["notes"]+ "\n"

                if len(all_commands[module]['commands'].keys()) != 0:
                    msg = msg + "\n"

    list_msgs = []
    original_length = len(msg)
    while len(msg) > 3000:
        index = 3000
        while True:
            if (msg[index:index+1] == "\n"):
                break
            else:
                index -= 1

        list_msgs.append(msg[0:index])
        msg = msg[index:original_length-1]
    list_msgs.append(msg)
    print("send back: "+str(len(list_msgs))+" msgs.")
    #print(list_msgs[len(list_msgs)-1])

    count_msgs = 0
    for m in list_msgs:
        #print(m[0:10].encode())
        #print(m[-1].encode())
        if count_msgs >= 3:
            bot.sendMessage(chat_id,'Too many messages to send !',parse_mode= None,disable_web_page_preview=True)
            break
        bot.sendMessage(chat_id,m,parse_mode= parse_mode,disable_web_page_preview=True)
        count_msgs += 1
        time.sleep(0.5)


all_commands = {}
for m in MODULES_PATH:
    url = 'modules/'
    m_name = re.sub('modules/', '', m)
    m_name = re.sub('.py','', m_name)
    spec = importlib.util.spec_from_file_location(m_name, m)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    all_commands[m] = {}
    all_commands[m]['path'] = m_name
    all_commands[m]['commands'] = foo.get_my_commands()

bot = telepot.Bot(TOKEN)

MessageLoop(bot, handle).run_as_thread()
print('I am listening ...')

while 1:
    time.sleep(10)


# In[ ]:
