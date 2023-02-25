import streamlit as st
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from keras.preprocessing.text import Tokenizer
import re
from nltk.corpus import stopwords
import json
import random
import datetime as dt

from bs4 import BeautifulSoup
import requests
stop_words = set(stopwords.words('french'))


def departement_depute(topic):
    """
    Présente les différents députés d'une région

    Parameters:
    ----------
    topic : dictionnaire
        Contient le département dont on veut les députés
        clées : 
            - 'département' : string

    Returns:
    -------
    string
        Une réponse formaté avec les députés du département
    """
    value = ""
    with open('data/depute.json') as json_file:
        data = json.load(json_file)

    if topic['département'] in data['departement']:
        index = [i for i, x in enumerate(data['departement']) if x == topic['département']]
        # index = data['departement'].index(topic['département'])
        value = " les député de " + str(topic['département'])
        if len(index) > 1:
            value += " sont "
        else:
            value += " est "
        for i in range(len(index)):
            value += str(data['prenom'][index[i]]) + " " + str(data['nom'][index[i]]) + " "
            if i < len(index) - 1:
                value += " et "

    return value


def nom_depute(topic):
    """
    Donne le lien de la page d'un député

    Parameters:
    ----------
    topic : dictionnaire
        Contient le nom du député dont on veut la page
        clées : 
            - 'nom_député' : string

    Returns:
    -------
    string
        Une réponse formaté avec le lien de la page du député
    """
    value = ""
    with open('data/depute.json') as json_file:
        data = json.load(json_file)

    index = [i for i, x in enumerate(data['nom']) if x == topic['nom_député']]
    lien = data['adresse'][index[0]]
    value = "Voici le lien de la page de " + str(topic['nom_député']) + " : " + lien

    return value

def agenda_assemblee(topic):
    """
    Donne l'agenda de l'assemblée nationale pour une date donnée

    Parameters:
    ----------
    topic : dictionnaire
        Contient la date de l'agenda
        clées : 
            - 'temps' : string

    Returns:
    -------
    string
        Une réponse formaté avec le lien de l'agenda pour la journée concernée
    """
    value = ""
    if topic['temps'] != "":
        if topic['temps'] == "aujourhui":
            url = 'https://www2.assemblee-nationale.fr/agendas/les-agendas/'
            value = "Voici le lien de la page de l'agenda pour aujourd'hui : " + url
        elif topic['temps'] == "demain":
            today = dt.date.today()
            tomorrow = today + dt.timedelta(days=1)
            url = 'https://www2.assemblee-nationale.fr/agendas/les-agendas/' + str(tomorrow)
            value = "Voici le lien de la page de l'agenda pour demain : " + url
    else:
        url = 'https://www2.assemblee-nationale.fr/agendas/les-agendas/'
        value = "Voici le lien de la page de l'agenda pour aujourd'hui " + url

    return value

def dossier_assemblee(topic):
    """
    Donne la liste des dossier discuté à l'assemblée nationale pour le mois en cours

    Parameters:
    ----------
    topic : ?

    Returns:
    -------
    string
        Une réponse formaté avec la liste des dossier
    """
    url = "https://www.nosdeputes.fr/dossiers/date"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find('div', class_='travaux_parlementaires')
    lis = table.find('li')
    date = table.find('h3')
    print(date.text)
    liss = lis.find_all('li')

    list_dossiers = []

    for i in liss:
        dossier = {}
        oui = i.find('a')
        dossier["date"] = date.text
        dossier["link"] = oui['href']
        dossier["text"] = oui.text
        list_dossiers.append(dossier)

    value = "Voici la liste des dossiers de ce mois-ci : \n"
    for i in list_dossiers:
        value += " - " + i['text'] + "\n"

    return value

def dossier_assemblee_select(topic, text):
    target = re.findall(r'"(.*?)"', text)
    target = target[0]

    url = "https://www.nosdeputes.fr/dossiers/date"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find('div', class_='travaux_parlementaires')
    lis = table.find('li')
    date = table.find('h3')
    print(date.text)
    liss = lis.find_all('li')

    list_dossiers = []

    for i in liss:
        dossier = {}
        oui = i.find('a')
        dossier["date"] = date.text
        dossier["link"] = oui['href']
        dossier["text"] = oui.text
        list_dossiers.append(dossier)

    value = "voici la liste des dossiers de ce mois-ci :"
    for i in list_dossiers:
        if i["text"] == target:
            value = i["link"]
            break

    value = "https://www.nosdeputes.fr/" + value

    return value


def good_scrapingg(topic, text):
    reponse = ['Je n\'ai pas compris votre demande', 'Pouvez vous reformuler votre question ?']
    value = random.choice(reponse)
    if 'sénat' in topic:
        print('sénat')

    elif ('département' in topic) and ('député' in topic):
        value = departement_depute(topic)

    elif  ("agenda" in topic) and ("assemblée" in topic):
        value = agenda_assemblee(topic)

    elif ("dossier" in topic) and '"' in text :
        value = dossier_assemblee_select(topic, text)

    elif  ("dossier" in topic) and ("assemblée" in topic):
        value = dossier_assemblee(topic)

    elif 'nom_député' in topic:
        value = nom_depute(topic)

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
    newString = re.sub(r"d'", "", newString)
    newString = re.sub(r"l'", "", newString)
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
    with open('data/topic.json') as json_file:
        dict_topic = json.load(json_file)

    for i in text:
        for key, value in dict_topic.items():
            if i in value:
                dic_find[key] = i

    return dic_find

def answer(text, answer):
    """
    Entrée de l'algorithme de réponse

    Parameters:
    ----------
    text : string
        Demande de l'utilisateur

    Returns:
    -------
    string
        Une réponse formaté avec la liste des dossier
    """
    newString = cleaning(text)
    topic = find_topic(newString)
    good_scraping = good_scrapingg(topic, text)

    if answer:
        return  str(good_scraping)
    else :
        return str(newString) + str(topic) + str(good_scraping)
