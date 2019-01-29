##NOTE: Always leave this variable
my_commands = {
    #Add all the commands that you want the bot to handle from this module
    #e.g:  [[COMMAND-NAME]] : {"notes":[[COMMAND-DESCRIPTION]]}

    #EXAMPLE
    #"/howToContactYou" : {"notes":" Check how you can contact me!"},
}

##NOTE: Always leave this method
#Always leave this method inside the module written as following
def get_my_commands():
    return my_commands

##NOTE: Always leave this method
#For each different command name associate the corresponding defined method
def exec_my_commands(command,param):
    #e.g: /howToContactYou
    if command == "/howToContactYou":
        return how_to_contact_you(param)
    #elif ... All other commands




#ADD all the methods you want to use
####################################

import csv
import urllib.request
#this method is called once the command '/howToContactYou' arrives
def how_to_contact_you(a_text):
    str_to_return = ""
    api_call = "https://ivanhb.github.io/data/contacts.csv"
    csv_matrix = get_csv_file(api_call)

    for i in range(1,len(csv_matrix)):
        str_to_return = str_to_return + "\n"+csv_matrix[i][0]+": "+csv_matrix[i][1]
    return str_to_return
