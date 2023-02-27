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
import requests
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation
stop_words = set(stopwords.words('french'))

#---- Fonctions utilitaires ----#
def summarize(text, n):
    """
    Résume un texte en n phrases

    Parameters:
    ----------
    text : string
        Le texte à résumer
    n : int
        Le nombre de phrases du résumé
    Returns:
    -------
    string
        Le résumé du texte
    """
    text = text.replace("\n", " ").replace("\r", "").replace("\xa0", " ")
    text = re.sub(r'\.(?! )', '. ', text)
    text = re.sub(r'\!(?! )', '! ', text)
    text = re.sub(r'\?(?! )', '? ', text)
    text = re.sub(r'\s+', ' ', text)

    stop_words = set(stopwords.words('french'))
    stemmer = nltk.stem.PorterStemmer()
    sentences = sent_tokenize(text)
    words = [word_tokenize(sentence.lower()) for sentence in sentences]
    filtered_words = [[stemmer.stem(word) for word in words if word not in stop_words and word not in punctuation] for words in words]

    word_freq = {}
    for sentence in filtered_words:
        for word in sentence:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1

    sentence_scores = {}
    for i, sentence in enumerate(filtered_words):
        score = 0
        for word in sentence:
            score += word_freq[word]
        sentence_scores[i] = score

    summary_sentences = []
    sorted_scores = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    for i in range(n):  # Change the number to control the length of the summary
        summary_sentences.append(sentences[sorted_scores[i][0]])
    summary = ' '.join(summary_sentences)

    return summary

def get_debat_dossier(url):
    """
    Récupère par scrapping tous les débats sur le dossier dont l'url est donné

    Parameters:
    ----------
    url : string
        Lien du dossier
    Returns:
    -------
    dataframe
        Les échanges des députés sur le dossier
    """
    URL_du_dossier = url
    page_dossier = requests.get(URL_du_dossier)

    soup = BeautifulSoup(page_dossier.content, "html.parser")

    sceances = soup.find("div", class_="seances_dossier").find_all("a")

    dataframe = []

    for sceance in sceances:
        URL_sceance = sceance.get("href")
        URL_sceance = "https://www.nosdeputes.fr"+URL_sceance
        page_sceance = requests.get(URL_sceance)

        soup = BeautifulSoup(page_sceance.content, "html.parser")

        #We get every intervention done in the sceance
        interventions = soup.find_all("div", class_="intervention")
        folder_name = ""

        #We filter the first lines of off topic discussions
        for i in range(0, len(interventions)):
            inter = interventions[i]
            if inter.find("div", id="table_1582"):
                folder_name = inter.find("h2", {'class': 'section'}).text
                interventions = interventions[i:]
                break
        
        #And the last lines of off topic discussions
        for i in range(0, len(interventions)):
            inter = interventions[i]
            if not inter.find("div", {'class': 'intervenant'}):
                if inter.find("h2", {'class': 'section'}).text != folder_name:
                    interventions = interventions[:i]
                    break
        
        #Now based on what remains we build our dataframe of interventions
        for inter in interventions:
            intervenant = inter.find("div", {'class': 'intervenant'})
            #We filter the interventions that are not from a person
            if intervenant and not intervenant.find("div", {'class': 'didascalie'}) \
            and intervenant.find('img', {'class': 'jstitle'}):
                text = intervenant.find('img', {'class': 'jstitle'})['title']
                name, group = text.split(' -- ')[0], text.split(' -- ')[1]
                group = group.strip('()')
                group_name, group_parlementaire = group.split(':')
                dataframe.append({
                    "intervenant" : name,
                    "parti" : group_parlementaire.strip(),
                    "intervention" : intervenant.find("div", {'class': 'texte_intervention'}).text
                })

    df = pd.DataFrame(dataframe)
    df["parti"] = df["parti"].apply(lambda x: x.replace('app. ', ''))
    df["intervenant"] = df["intervenant"].apply(lambda x: x.split(' ')[-1].lower())
    return df

#---- Fonctions réponses ----#
def resume_parti_debat_depute(url, topic):
    """
    Génère le résumé des débats de l'assemblée nationale d'un delegue

    Parameters:
    ----------

    Returns:
    -------
    string
        Une réponse formatée avec le résumé de l'opinion d'un député sur un dossier
    """
    print(topic)
    df = get_debat_dossier(url)
    concat = df.groupby('intervenant')['intervention'].apply(lambda x: ' '.join(x))

    answer = "Voici un résumé de ce que "+ topic['nom_député'] +" a dit lors de ce débat : \n\n" + summarize(concat[topic['nom_député']], n=5)
    return answer

def resume_parti_debat(url):
    """
    Génère le résumé des débats de l'assemblée nationale par parti

    Parameters:
    ----------

    Returns:
    -------
    string
        Une réponse formaté avec le résumé des débats de l'assemblée nationale
    """

    df = get_debat_dossier(url)
    concat = df.groupby('parti')['intervention'].apply(lambda x: ' '.join(x))

    answer = "Voici un résumé de ce que les députés de chaque parti ont dit lors de ce débat : \n\n"
    for key, value in concat.apply(summarize, n=1).items():
        answer = answer + "- Parti " + key + "\n\n    " + value + "\n\n"
    
    return answer

def resume_parti_debat_parti(url, topic):
    """
    Génère le résumé des débats de l'assemblée nationale pour un parti

    Parameters:
    ----------

    Returns:
    -------
    string
        Une réponse formaté avec le résumé des débats de l'assemblée nationale pour un parti
    """

    df = get_debat_dossier(url)
    concat = df.groupby('parti')['intervention'].apply(lambda x: ' '.join(x))
    
    return "Voici un résumé de ce que les députés du parti '" + topic['parti_politique'].upper() + "' ont dit lors de ce débat : \n\n" + summarize(concat[topic['parti_politique'].upper()], n=3)

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
        value = " les député de " + str(topic['département']) + " sont/est :\n "
        for i in range(len(index)):
            prenom = str(data['prenom'][index[i]])
            nom = str(data['nom'][index[i]])
            value += " - " + prenom.capitalize() + " " + nom.upper() + "\n "

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

    page = requests.get(lien)
    soup = BeautifulSoup(page.content, "html.parser")

    return soup.find("h1", class_="h1 _mt-small").text + " est un député du parti **" + soup.find("a", class_="h4 _colored link").text.strip() + \
    "**.\n\n Il représente : "+ soup.find("div", class_="_mb-small _centered-text").find("span").text + \
    ".\n\n Voici sa biographie : " + soup.find("div", class_="_gutter-xxs _vertical").find("p").text

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


#---- Fonctions Traitement ----#
def good_scrapingg(topic, text):
    reponse = ['Je n\'ai pas compris votre demande', 'Pouvez vous reformuler votre question ?']
    value = random.choice(reponse)
    if 'sénat' in topic:
        print('sénat')

    elif ('département' in topic) and ('député' in topic):
        value = departement_depute(topic)

    elif  ("agenda" in topic) and ("assemblée" in topic):
        value = agenda_assemblee(topic)

    elif ("dossier" in topic) and '"' in text and "résumé" in topic and ('nom_député' in topic):
        value = dossier_assemblee_select(topic, text)
        value = resume_parti_debat_depute(value, topic)
    
    elif ("dossier" in topic) and '"' in text and "résumé" in topic and "parti_politique" in topic:
        value = dossier_assemblee_select(topic, text)
        value = resume_parti_debat_parti(value, topic)
    
    elif ("dossier" in topic) and '"' in text and "résumé" in topic:
        value = dossier_assemblee_select(topic, text)
        value = resume_parti_debat(value)
    
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
