import streamlit as st
import numpy as np
import pandas as pd


def documentation():
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