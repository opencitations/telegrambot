
my_commands = {
    "/contact" : {"notes":" Retrieve all the accounts (email, Twitter, GitHub, etc.) to contact the OpenCitations folks"},
    "/ask" : {"notes":"Params: <DOI>. Retrieve information about the entity identified by the input DOI (source: COCI)"},
    "/citations" : {"notes":"Params: <DOI>. Retrieve all the entities that cite the one identified by the input DOI (source: COCI)"},
    "/references" : {"notes":"Params: <DOI>. Retrieve all the entities that are cited by the one identified by the input DOI (source: COCI)"}
}

def get_my_commands():
    return my_commands

def exec_my_commands(command,param):
    if command == "/contact":
        return how_to_contact_you(param)
    if command == "/ask":
        return ask_coci(param)
    if command == "/citations":
        return who_cite_me_in_coci(param)
    if command == "/references":
        return what_are_my_ref_in_coci(param)





#ADD all the methods you want to use
####################################

import csv
import urllib.request
import json
import re

contact = {
    'Website':'http://opencitations.net/',
    'Email':'contact@opencitations.net',
    'Twitter':'https://twitter.com/opencitations',
    'Github': 'https://github.com/essepuntato/opencitations',
    'Wordpress': 'https://opencitations.wordpress.com/'
}

def how_to_contact_you(a_text):
    str_to_return = ""
    for c in contact:
        str_to_return = str_to_return + "\n"+c+": "+contact[c]
    return str_to_return


#'http://opencitations.net/index/coci/api/v1/metadata/10.1108/jd-12-2013-0166'
def ask_coci(a_text):
    str_to_return = ""

    try:
        a_text = a_text[0]
    except:
        return "You must text me a DOI !"

    find_list = re.findall(r"(10.\d{4,9}\/\S*)",a_text)
    if len(find_list) == 0:
        return "Please, text me a correct DOI format"

    res = find_list[0]

    api_call = 'http://opencitations.net/index/coci/api/v1/metadata/'
    input = res
    api_call = api_call+input
    #call API
    try:

        contents = urllib.request.urlopen(api_call).read().decode('utf-8')
        json_output = json.loads(contents)
        if len(json_output) == 0:
            return "No data found for: "+ input
        else:
            rc_data = json_output[0]

            #Title
            str_title = "\n\n Title: "+rc_data['title']
            if str_title != "\n\n Title: ":
                str_to_return = str_to_return + str_title

            #Authors
            str_authors = "\n\n Author(s): "
            list_authors = rc_data['author'].split(';')
            for an_author in list_authors:
                str_authors = str_authors + "\n" + str(an_author)
            if str_authors != "\n\n Author(s): ":
                str_to_return = str_to_return + str_authors

            #Publication year
            str_year = "\n\n Publication year: " + rc_data['year']
            if str_year != "\n\n Publication year: ":
                str_to_return = str_to_return + str_year

            #DOI
            str_to_return = str_to_return + "\n DOI: "+'https://www.doi.org/'+input

            #OA URL
            str_cit = "\n\n OA URL: "+rc_data['oa_link']
            if str_cit != "\n\n OA URL: ":
                str_to_return = str_to_return + str_cit

            #Citations
            str_cit = "\n\n Cited by: "+rc_data['citation_count']
            if str_cit != "\n\n Cited by: ":
                str_to_return = str_to_return + str_cit

    except:
        return "Sorry, the connection went wrong!"

    return str_to_return


def who_cite_me_in_coci(a_text):
    str_to_return = ""

    try:
        a_text = a_text[0]
    except:
        return "You must text me a DOI !"

    find_list = re.findall(r"(10.\d{4,9}\/\S*)",a_text)
    if len(find_list) == 0:
        return "Please, text me a correct DOI format"

    res = find_list[0]
    api_call = 'http://opencitations.net/index/coci/api/v1/citations/'
    input = res
    api_call = api_call+input
    #call API
    try:
        contents = urllib.request.urlopen(api_call).read().decode('utf-8')
        json_output = json.loads(contents)
        if len(json_output) == 0:
            return "No citations found for: "+ input
        else:
            str_to_return = str_to_return + "\n Cited by: "+str(len(json_output))+ "\n\n"
            for c_elem in json_output:

                #OCI
                str_to_return = str_to_return + "\n OCI: "+str(c_elem['oci'])

                #DOI
                str_to_return = str_to_return + "\n Citing DOI: "+'https://www.doi.org/'+c_elem['citing']

                #Citation Creation date
                creation_str = ""
                list_date = c_elem['oci'].split("-")
                if len(list_date) > 0:
                    creation_str = str(list_date[0])
                    if len(list_date) > 1:
                        creation_str = get_month_name(str(list_date[1])) +" "+ creation_str
                        if len(list_date) > 2:
                            creation_str = str(list_date[2]) + " "+ creation_str
                if creation_str != "":
                    str_to_return = str_to_return + "\n Citation creation date: "+creation_str

                #Timespan
                tspan_str = ""
                result_y = re.search(r"(\d{1,})Y",c_elem['timespan'])
                if result_y:
                    tspan_str += str(result_y.groups(0)[0]) + " Years"
                    result_y = re.search(r"(\d{1,})M",c_elem['timespan'])
                    if result_y:
                        tspan_str += ", "+str(result_y.groups(0)[0]) + " Months"
                        result_y = re.search(r"(\d{1,})D",c_elem['timespan'])
                        if result_y:
                            tspan_str += ", "+str(result_y.groups(0)[0]) + " Days"
                if tspan_str != "":
                    str_to_return = str_to_return + "\n Timespan: "+tspan_str

                ##New item
                str_to_return = str_to_return + "\n\n"
    except:
        return "Sorry, the connection went wrong!"

    return str_to_return


def what_are_my_ref_in_coci(a_text):
    str_to_return = ""

    try:
        a_text = a_text[0]
    except:
        return "You must text me a DOI !"

    find_list = re.findall(r"(10.\d{4,9}\/\S*)",a_text)
    if len(find_list) == 0:
        return "Please, text me a correct DOI format"

    res = find_list[0]
    api_call = 'https://w3id.org/oc/index/coci/api/v1/references/'
    input = res
    api_call = api_call+input
    #call API
    try:
        contents = urllib.request.urlopen(api_call).read().decode('utf-8')
        json_output = json.loads(contents)
        if len(json_output) == 0:
            return "No references found for: "+ input
        else:
            str_to_return = str_to_return + "\n References: "+str(len(json_output))+ "\n\n"
            for c_elem in json_output:
                str_to_return = str_to_return + "\n Cited: "+c_elem['cited']

                pub_date = ""
                result_y = re.search(r"(\d{1,})Y",c_elem['timespan'])
                if result_y:
                    pub_date += str(result_y.groups(0)[0]) + " Years"
                    result_y = re.search(r"(\d{1,})M",c_elem['timespan'])
                    if result_y:
                        pub_date += ", "+str(result_y.groups(0)[0]) + " Months"
                        result_y = re.search(r"(\d{1,})D",c_elem['timespan'])
                        if result_y:
                            pub_date += ", "+str(result_y.groups(0)[0]) + " Days"

                str_to_return = str_to_return + "\n Timespan: "+pub_date


                str_to_return = str_to_return + "\n Resource: "+"http://opencitations.net/index/coci/browser/ci/"+c_elem['oci']
                str_to_return = str_to_return + "\n\n"
    except:
        return "Sorry, the connection went wrong!"

    return str_to_return


def get_month_name(month_num):
    monthDict={'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}
    return monthDict[month_num]
