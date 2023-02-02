import streamlit as st
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from keras.preprocessing.text import Tokenizer
import re
from nltk.corpus import stopwords
import json
import random


from bs4 import BeautifulSoup
import requests


stop_words = set(stopwords.words('french'))

def good_scrapingg(topic):
    reponse = ['je ne comprend pas', 'non mais ça ne veux rien dire','tu te moque de moi ?','parle moi en français',]
    value = random.choice(reponse)
    if 'sénat' in topic:
        print('sénat')
    elif ('département' in topic) and ('député' in topic):
        with open('depute.json') as json_file:
            data = json.load(json_file)

        if topic['département'] in data['departement']:
            index = [i for i, x in enumerate(data['departement']) if x == topic['département']]
            #index = data['departement'].index(topic['département'])
            value = " les député de "+ str(topic['département'])
            if len(index) > 1:
                value += " sont "
            else:
                value += " est "
            for i in range(len(index)):
                value += str(data['prenom'][index[i]]) +" "+  str(data['nom'][index[i]]) + " "
                if i < len(index)-1:
                    value += " et "
            #st.write(data['nom'][index])
    elif 'nom_député' in topic:
        with open('depute.json') as json_file:
            data = json.load(json_file)
        index = [i for i, x in enumerate(data['nom']) if x == topic['nom_député']]
        lien = data['adresse'][index[0]]
        value = " voici le lien de la page de "+ str(topic['nom_député']) + " : " + lien
    elif 'région' in topic:
        st.write('région')
    elif 'temps' in topic:
        st.write('temps')
    elif 'assemblée' in topic:
        print('assemblée')
    elif 'député' in topic:
        print('député')
    elif 'sénateur' in topic:
        print('sénateur')

    return value

def cleaning(text):

    newString = text.lower()
   # newString = BeautifulSoup(newString, "lxml").text
    newString = re.sub(r"(\w+:\/\/\S+)|^rt|http.+?", "", newString)
    newString = re.sub('"','', newString)
    newString = re.sub(r"'s\b","",newString)
    #newString = re.sub("[^a-zA-Z]", " ", newString)
    tokens = [word for word in newString.split() if word not in (stop_words)]
    newString = ''

    topic_find = []
    for i in tokens:
        if len(i) > 1:
            topic_find.append(i)

    return topic_find


def find_topic(text):

    dic_find = {}
    with open('topic.json') as json_file:
        dict_topic = json.load(json_file)

    #dict_topic = {
        #    'sénat': ['sénat'],
        #    'assemblée': ['assemblée','assemblée nationale'],
        #    'député': ['député','députés','députée','députées'],
        #   'sénateur': ['sénateur','sénateurs','sénatrice','sénatrices'],
        #   'département': ['ain','aisne','allier','alpes-de-haute-provence','hautes-alpes','alpes-maritimes','ardèche','ardennes','ariège','aube','aveyron','bouches-du-rhône','calvados','cantal','charente','charente-maritime','cher','corrèze','corse-du-sud','haute-corse','côte-d\'or','côtes-d\'armor','creuse','dordogne','doubs','drôme','eure','eure-et-loir','finistère','gard','haute-garonne','gers','gironde','hérault','ille-et-vilaine','indre','indre-et-loire','isère','jura','landes','loir-et-cher','loire','haute-loire','loire-atlantique','loiret','lot','lot-et-garonne','lozère','maine-et-loire','manche','marne','haute-marne','mayenne','meurthe-et-moselle','meuse','morbihan','moselle','nièvre','nord','oise','orne','pas-de-calais','puy-de-dôme','pyrénées-atlantiques','hautes-pyrénées','pyrénées-orientales','bas-rhin','haut-rhin','rhône','haute-saône','saône-et-loire','sarthe','savoie','haute-savoie','paris','seine-maritime','seine-et-marne','yvelines','deux-sèvres','somme','tarn','tarn-et-garonne','var','vaucluse','vendée','vienne','haute-vienne','vosges','yonne','territoire de belfort','essonne','hauts-de-seine','seine-saint-denis','val-de-marne','val-d\'oise','guadeloupe','martinique','guyane','la réunion','mayotte'],
        #    'région' : ['auvergne-rhône-alpes','bourgogne-franche-comté','bretagne','centre-val de loire','corse','grand est','hauts-de-france','île-de-france','normandie','nouvelle-aquitaine','occitanie','pays de la loire','provence-alpes-côte d\'azur','guadeloupe','martinique','guyane','la réunion','mayotte'],
    #   'temps' : ['aujourd\'hui','hier','demain','après demain','avant hier','semaine','mois','année','années','semaines','mois','jours','jour']
    #}

    for i in text:
        for key, value in dict_topic.items():
            if i in value:
                dic_find[key] = i

    return dic_find






def answer(text,answer):
    newString = cleaning(text)
    topic = find_topic(newString)
    good_scraping = good_scrapingg(topic)

    if answer:
        return  str(good_scraping)
    else :
        return str(newString) + str(topic) + str(good_scraping)
