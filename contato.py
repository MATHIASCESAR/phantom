import streamlit as st


def contato():
    col1, col2, col3 = st.columns([1, 15, 35])

    with col1:
        st.write("")

    with col2:
        st.write("")

    with col3:
        logo_image = "https://github.com/MATHIASCESAR/phantom/blob/meu_app/contato.png?raw=true"
        st.image(logo_image, width=250)

    st.markdown('<h2></h2>', unsafe_allow_html=True)
    st.markdown('<h7>mathiascassis@hotmail.com</h7>', unsafe_allow_html=True)
    st.markdown('<h7>leonardo.travassos@inca.gov.br</h7>', unsafe_allow_html=True)
    st.markdown('<h7>crsaguiar2@gmail.com</h7>', unsafe_allow_html=True)
   

    col4, col5, col6, col7 = st.columns([1, 15, 15, 35])

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
