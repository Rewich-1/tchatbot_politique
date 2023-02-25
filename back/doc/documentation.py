import streamlit as st
import numpy as np
import pandas as pd


def documentation():
    with st.expander("information sur les personnes politiques"):
        st.subheader("le parcours d'une personne politique")
        st.write('qui sont les députés  de paris ?')
        st.subheader("demander des information sur une personne politique")
        st.write('qui est david amiel ?')

    with st.expander("information sur le planing politique"):
        st.subheader("en savoir plus sur l'agenda de l'assemblée nationale")
        st.write("quel est l'agenda de l'assemblé nationale ?")

    with st.expander("information sur les dossiers traités à l'Assemblée"):
        st.subheader("savoir les dossier traité à l'assemblée")
        st.write('donne moi les dossier traité à l\'assemblée ce mois ci')
        st.subheader("approfondir sur un dossier")
        st.write('dis moi en plus sur le dossier "Projet de loi de financement rectificative de la sécurité sociale pour 2023"')

