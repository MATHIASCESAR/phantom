import os
import streamlit as st
from streamlit_option_menu import option_menu

from phantomacr import phantomacr
from phantomcbr import phantomcbr
from contato import contato

st.set_page_config(
    page_title='Seja Bem-Vindo'
)

# Centralizando as imagens
col1, col2, col3 = st.sidebar.columns([1, 1, 3])

with col1:
    st.write("")

with col2:
    logo_image = "https://github.com/MATHIASCESAR/phantom//blob/meu_app/Logo_INCA.jpg?raw=true"
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
                options=['Home Page', 'Phantom ACR', 'Phantom MAMA', 'Contato'],
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

    st.markdown('#### Instruções para Preenchimento e Envio da(s) imagem(s)')
    st.write('''
        1) No :red[**MENU**] ao lado, selecione o modelo de Phantom desejado, :red[**ACR**] (Americano) ou :red[**MAMA**] (Nacional);
        2) No formulário, informe a :red[**Razão Social**] e a :red[**Identificação do CNES**];
        3) Selecione o Tipo de Equipamento, entre :red[**CR**] (Radiografia Convencional) ou :red[**DR**] (Radiografia Digital);
        4) Em caso de Equipamentos :red[**CR**], informar as métricas da **Exposição** (:red[**KV, mAs e Combinação Alvo/Filtro**]);
        5) Clique em :red[**Browe Files**] ou em :red[**Drag and drop files here**], para selecionar o(s) arquivo(s) DICOM;
        6) Após selecionar o(s) arquivo(s), clique em :red[**ENVIAR**] e aguarde a Confirmação;
        7) Em caso de dúvidas, use a opção :red[**CONTATO**];
        8) Os campos :red[**_CNES, KV, mAs_**] aceitam apenas números!
    ''')

    st.write('---')


# Inicializar o aplicativo
app = MultiApp()
app.add_app("Home Page", main)
app.add_app("Phantom ACR", phantomacr)
app.add_app("Phantom MAMA", phantomcbr)
app.add_app("Contato", contato)

app.run()
