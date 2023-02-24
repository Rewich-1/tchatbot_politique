import streamlit as st
import time

def tchat(historical):
    for i in range(len(historical)):
        if historical[i]["user"] == 0:
            col1, col2, col3, col4 = st.columns([3, 20, 20, 3])
            if i == 0:
                placeholder = st.empty()
                with placeholder:
                    for seconds in range(1):
                        st.write(f"⏳")
                        time.sleep(1)
                placeholder.empty()
                col1.image("img/fille.png")
                col2.success(historical[i]['text'])
            else:
                col1.image("img/fille.png")
                col2.warning(historical[i]['text'])

        else:
            col1, col2, col3, col4 = st.columns([3, 20, 20, 3])
            col3.info(historical[i]["text"])
            col4.image("img/homme.png")