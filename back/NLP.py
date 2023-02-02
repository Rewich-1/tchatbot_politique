import streamlit as st
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from keras.preprocessing.text import Tokenizer
import re
from nltk.corpus import stopwords
import json

from bs4 import BeautifulSoup
import requests


stop_words = set(stopwords.words('french'))

def good_scrapingg(topic):
    index = 0
    if 'sénat' in topic:
        st.write('sénat')
    if 'assemblée' in topic:
        st.write('assemblée')
    if 'député' in topic:
        st.write('député')
    if 'sénateur' in topic:
        st.write('sénateur')
    if ('département' in topic) and ('député' in topic):

        with open('depute.json') as json_file:
            data = json.load(json_file)

        if topic['département'] in data['departement']:
            print('OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK')
            index = data['departement'].index(topic['département'])
            value = " le député de "+ str(topic['département']) + " est " +str(data['prenom'][index]) +" "+  str(data['nom'][index])
            #st.write(data['nom'][index])



    if 'région' in topic:
        st.write('région')
    if 'temps' in topic:
        st.write('temps')

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
    dict_topic = {

        'sénat': ['sénat'],
        'assemblée': ['assemblée','assemblée nationale'],
        'député': ['député','députés','députée','députées'],
        'sénateur': ['sénateur','sénateurs','sénatrice','sénatrices'],
        'département': ['ain','aisne','allier','alpes-de-haute-provence','hautes-alpes','alpes-maritimes','ardèche','ardennes','ariège','aube','aveyron','bouches-du-rhône','calvados','cantal','charente','charente-maritime','cher','corrèze','corse-du-sud','haute-corse','côte-d\'or','côtes-d\'armor','creuse','dordogne','doubs','drôme','eure','eure-et-loir','finistère','gard','haute-garonne','gers','gironde','hérault','ille-et-vilaine','indre','indre-et-loire','isère','jura','landes','loir-et-cher','loire','haute-loire','loire-atlantique','loiret','lot','lot-et-garonne','lozère','maine-et-loire','manche','marne','haute-marne','mayenne','meurthe-et-moselle','meuse','morbihan','moselle','nièvre','nord','oise','orne','pas-de-calais','puy-de-dôme','pyrénées-atlantiques','hautes-pyrénées','pyrénées-orientales','bas-rhin','haut-rhin','rhône','haute-saône','saône-et-loire','sarthe','savoie','haute-savoie','paris','seine-maritime','seine-et-marne','yvelines','deux-sèvres','somme','tarn','tarn-et-garonne','var','vaucluse','vendée','vienne','haute-vienne','vosges','yonne','territoire de belfort','essonne','hauts-de-seine','seine-saint-denis','val-de-marne','val-d\'oise','guadeloupe','martinique','guyane','la réunion','mayotte'],
        'région' : ['auvergne-rhône-alpes','bourgogne-franche-comté','bretagne','centre-val de loire','corse','grand est','hauts-de-france','île-de-france','normandie','nouvelle-aquitaine','occitanie','pays de la loire','provence-alpes-côte d\'azur','guadeloupe','martinique','guyane','la réunion','mayotte'],
        'temps' : ['aujourd\'hui','hier','demain','après demain','avant hier','semaine','mois','année','années','semaines','mois','jours','jour']

    }

    for i in text:
        for key, value in dict_topic.items():
            if i in value:
                dic_find[key] = i


    return dic_find






def answer(text):

    newString = cleaning(text)
    topic = find_topic(newString)
    good_scraping = good_scrapingg(topic)

    return  str(good_scraping)
