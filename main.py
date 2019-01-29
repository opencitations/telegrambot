
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

                obj_command = all_commands[module]['commands'][command]

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

    bot.sendMessage(chat_id, msg)


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
