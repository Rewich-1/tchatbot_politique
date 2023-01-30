import streamlit as st
import numpy as np
import pandas as pd
import json
import time

historical = open("historical.txt", "r")
#st.write(historical)
historical = str(historical.read())
#st.write(historical)
#st.write(len(historical))
if len(historical) == 0:
    historical = []
else :
    historical = json.loads(historical.replace("'", '"'))

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
                if historical[i]["user"]==1:
                    col1, col2,col3, col4 = st.columns([3,20,20,3])

                    col1.image("homme.png")
                    col2.info(historical[i]['text'])
                else:

                    col1, col2,col3, col4 = st.columns([3,20,20,3])
                    if i == 0:
                        placeholder = st.empty()
                        with placeholder:
                            for seconds in range(1):
                                st.write(f"⏳")
                                time.sleep(1)
                        placeholder.empty()
                        col3.success(historical[i]["text"])
                        col4.image("fille.png")

                    else:
                        col3.warning(historical[i]["text"])
                        col4.image("fille.png")

        historical.reverse()
        with open("historical.txt", "w") as file:
            file.write(str(historical))


with tab2:
    st.header('documentation')
    with st.expander("doc1"):
        st.write('doc1')

    with st.expander("doc2"):
        st.write('doc2')

























