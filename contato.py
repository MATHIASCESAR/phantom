import streamlit as st


def contato():
    col1, col2, col3 = st.columns([1, 15, 35])

    with col1:
        st.write("")

    with col2:
        st.write("")

    with col3:
        logo_image = "https://github.com/MATHIASCESAR/phantom/blob/meu_app/contato.png?raw=true"
        st.image(logo_image, width=230)
    
    st.markdown('<h8></h8>', unsafe_allow_html=True)



    col8, col9, col0 = st.columns([35, 15, 35])

    with col8:
        st.markdown('**INCA-Instituto Nacional do Câncer**')
        st.caption('**_PQM-Programa de Qualidade em Mamográfia_**')
        st.markdown('<h8>sonia.silva@inca.gov.br</h8>', unsafe_allow_html=True)
        st.markdown('<h8>leonardo.travassos@inca.gov.br</h8>', unsafe_allow_html=True)

    with col9:
        st.write("")

    with col0:
        st.markdown('**UFG-Universidade Federal de Goiás**')
        st.markdown('<h8>gustavolaureano@ufg.br</h8>', unsafe_allow_html=True)
        st.markdown('<h8>mathiascassis@hotmail.com</h8>', unsafe_allow_html=True)
        st.markdown('<h8>crsaguiar2@gmail.com</h8>', unsafe_allow_html=True)

   
    col4, col5, col6, col7 = st.columns([1, 45, 1, 35])

    with col4:
        logo_image = "https://github.com/MATHIASCESAR/phantom/blob/meu_app/Logo_INCA.jpg?raw=true"
        st.image(logo_image, width=150)

    with col5:
        st.write("")

    with col6:
        st.write("")
    
    with col7:
        logo_image = "https://github.com/MATHIASCESAR/phantom/blob/meu_app/Inf_UFG.png?raw=true"
        st.image(logo_image, width=150)
    
 
if __name__ == '__main__':
    contato()
