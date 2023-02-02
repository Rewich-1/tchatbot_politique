import streamlit as st
import numpy as np
import pandas as pd
import json
import time
from streamlit_cookies_manager import EncryptedCookieManager
import os
from back.NLP import answer
from back.doc.documentation import documentation
from tchat import tchat

# This should be on top of your script
cookies = EncryptedCookieManager(
    prefix="ktosiek/streamlit-cookies-manager/",
    password=os.environ.get("COOKIES_PASSWORD", "lest go"),
)

#cookies['historical'] = "[]"
#cookies.save()

if not cookies.ready():
    st.stop()

historical = json.loads(cookies['historical'])

try :
    historical = json.loads(cookies['historical'])
    st.write('cookies Find !')
    #st.title(historical)
except:
    st.write('cookies NOT find !')
    #cookies['historical'] = "[]"
    historical = []

st.title('tchatbot')

tab1, tab2 = st.tabs(["tchat", "tuto"])

with tab1:
    st.header('tchat')

    st.write('<style>[data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {max-height: 400px;overflow: auto;flex-direction:column-reverse;} </style>', unsafe_allow_html=True)
    container = st.container()

    question = st.text_input(value="",label="Speak")

    if st.button('cut the cookies 🍪' ):
        cookies['historical'] = "[]"
        cookies.save()
        historical = []
    else:
        pass


    if question != "":

        historical.append({"user":1,"text":question})
        historical.append({"user": 0, "text": answer(question)})

    historical.reverse()

    with container:
        tchat(historical)

    historical.reverse()

    cookies['historical'] = str(historical).replace("'", '"')
    cookies.save()


with tab2:
    st.header('documentation')
    recherche = st.text_input(value="", label="recherche")
    documentation()

























