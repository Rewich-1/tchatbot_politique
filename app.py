import streamlit as st
import numpy as np
import pandas as pd
import json
import time
from streamlit_cookies_manager import EncryptedCookieManager
import os

# This should be on top of your script
cookies = EncryptedCookieManager(
    prefix="ktosiek/streamlit-cookies-manager/",
    password=os.environ.get("COOKIES_PASSWORD", "lest go"),
)

if not cookies.ready():
    st.stop()
try :
    historical = json.loads(cookies['historical'].replace("'", '"'))
except:
    cookies['historical'] = "[]"
    historical = []

def answer(text):
    return "yes i am bob"

st.title('tchatbot')

tab1, tab2 = st.tabs(["tchat", "tuto"])

with tab1:
    st.header('tchat ')

    st.write('<style>[data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {max-height: 400px;overflow: auto;flex-direction:column-reverse;} </style>', unsafe_allow_html=True)
    container = st.container()

    question = st.text_input(value="",label="Speak")
    if question != "":

        historical.append({'user':1,'text':question})
        historical.append({'user': 0, 'text': answer(question)})

    historical.reverse()

    with container:
        for i in range(len(historical)):
            if historical[i]["user"]==0:
                col1, col2,col3, col4 = st.columns([3,20,20,3])
                if i == 0:
                    placeholder = st.empty()
                    with placeholder:
                        for seconds in range(1):
                            st.write(f"⏳")
                            time.sleep(1)
                    placeholder.empty()
                    col1.image("fille.png")
                    col2.success(historical[i]['text'])
                else:
                    col1.image("fille.png")
                    col2.warning(historical[i]['text'])

            else:

                col1, col2,col3, col4 = st.columns([3,20,20,3])
                col3.info(historical[i]["text"])
                col4.image("homme.png")


    historical.reverse()
    cookies['historical'] = str(historical)
    cookies.save()
   


with tab2:
    st.header('documentation')
    recherche = st.text_input(value="", label="recherche")
    with st.expander("information sur les personnes politiques"):
        st.subheader("le parcours d'une personne politique")
        st.write('doc1')
        st.subheader("sa participation a certain débat")
        st.write('doc1')


    with st.expander("information sur les séances parlementaires"):
        st.subheader("des information en fonction d'une période bien précise")
        st.write('doc1')
        st.subheader("aprofondir certain sujet")
        st.write('doc1')

























