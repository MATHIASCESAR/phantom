import os
import streamlit as st
from streamlit_option_menu import option_menu

from phantomacr import phantomacr
from phantomcbr import phantomcbr


st.set_page_config(
    page_title='Seja Bem-Vindo'
)

# Centralizando as imagens
col1, col2, col3 = st.sidebar.columns([1, 1, 3])

with col1:
    st.write("")

with col2:
    logo_image = "https://github.com/MATHIASCESAR/phantom/Logo_INCA.jpg?raw=true"
    st.image(logo_image, width=150)

with col3:
    st.write("")


class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        with st.sidebar:
            selected = option_menu(
                menu_title='Menu',
                options=['Home Page', 'Phantom ACR', 'Phantom CBR', 'Contato'],
                icons=['house-fill', 'cloud-upload-fill', 'cloud-upload-fill', 'envelope-heart-fill'],
                menu_icon='menu-app-fill',
                default_index=0,
            )

        # Criar diretório com o nome da página selecionada
        if not os.path.exists(selected):
            os.makedirs(selected)

        for app in self.apps:
            if app['title'] == selected:
                app['function']()


def main():
    st.markdown("<h2 style='text-align: center; color: bold;'> Coleta das Imagens Phantom </h2>", unsafe_allow_html=True)

    st.markdown('#### Instruções para envio e armazenamento da imagem')
    st.write('''
        1) Posicione o objeto simulador no mamógrafo, de forma que fique centralizado no detector;
        2) Abaixe a bandeja de compressão para que ela apenas toque a parte superior do *phantom*;
        3) Verifique se o sensor do Controle Automático de Exposição (CAE) está abaixo do centro do *phantom* e no mesmo posicionamento de aquisição anteriores;
        4) Faça uma exposição usando os parâmetros clinicamente utilizados conforme o modelo do Phantom (ACR ou CBR);
        5) Informar o nome do Serviço;
        6) Selecionar a imagem e fazer o *UPLOAD*, conforme instruções;
    ''')

    st.write('---')


# Inicializar o aplicativo
app = MultiApp()
app.add_app("Home Page", main)
app.add_app("Phantom ACR", phantomacr)
app.add_app("Phantom CBR", phantomcbr)

app.run()
