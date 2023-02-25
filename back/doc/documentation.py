import streamlit as st
import numpy as np
import pandas as pd


def documentation():
    with st.expander("Information sur les personnes politiques"):
        st.subheader("Le parcours d'une personne politique")
        st.write('Example de prompt : Qui sont les députés de paris ?')

        st.subheader("Plus d'information sur une personne politique")
        st.write('Example de prompt : Qui est david amiel ?')

    with st.expander("Information sur le planing politique"):
        st.subheader("En savoir plus sur l'agenda de l'assemblée nationale")
        st.write("Example de prompt : Quel est l'agenda de l'assemblé nationale Aujourd'hui/Demain ?")

    with st.expander("Information sur les dossiers traités à l'Assemblée"):
        st.subheader("Connaître les dossier traité à l'assemblée")
        st.write('Example de prompt : Donne moi les dossier traité à l\'assemblée ce mois ci')

        st.subheader("En savoir plus sur un dossier")
        st.write('Example de prompt : Dis moi en plus sur le dossier "Projet de loi de financement rectificative de la sécurité sociale pour 2023"')

