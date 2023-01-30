import streamlit as st
import numpy as np
import pandas as pd



import json

st.title('tchatbot')



tab1, tab2 = st.tabs(["tchat", "tuto"])

with tab1:
    st.header('tchat ')

    st.text_input(value="hello",label="Speak")


    for i in range(10):

        if i%2==0:

            col1, col2,col3, col4 = st.columns([3,20,20,3])
            col1.image("homme.png")
            col2.write('hello col1')
        else:
            col1, col2,col3, col4 = st.columns([3,20,20,3])
            col3.write('hello col2')
            col4.image("fille.png")



with tab2:
    st.header('documentation')
    with st.expander("doc1"):
        st.write('doc1')

    with st.expander("doc2"):
        st.write('doc2')























