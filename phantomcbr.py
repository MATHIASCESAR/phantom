import os
import zipfile
import streamlit as st
import time
import pydicom
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from b2sdk.v2 import B2Api, InMemoryAccountInfo, UploadSourceBytes
import streamlit.components.v1 as components
from streamlit_modal import Modal

# Configuração do banco de dados
DATABASE_URL = 'sqlite:///clientes.db'

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    cnes = Column(String, nullable=False)
    kv = Column(String, nullable=False)
    mas = Column(String, nullable=False)
    alvo_filtro = Column(String, nullable=False)

def recreate_database():
    # Exclui a tabela existente, se houver
    Base.metadata.drop_all(engine)
    # Cria a tabela novamente
    Base.metadata.create_all(engine)

# Criar a engine do banco de dados
engine = create_engine(DATABASE_URL)
recreate_database()

# Criar a sessão do banco de dados
Session = sessionmaker(bind=engine)
session = Session()


def mensagem(message, blinking=False):
    css = """
    @keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0; }
    100% { opacity: 1; }
    }

    .blink {
    animation: blink 1s infinite;
    font-weight: bold;
    color: green;
    }
    """
    if blinking:
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
        st.markdown(f'<div class="blink">{message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="font-weight: bold; color: green;">{message}</div>', unsafe_allow_html=True)

def authenticate_b2(account_id, application_key):
    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    b2_api.authorize_account("production", account_id, application_key)
    return b2_api

def upload_to_b2_chunked(account_id, application_key, bucket_name, file_path, folder_name, progress_callback):
    b2_api = authenticate_b2(account_id, application_key)
    bucket = b2_api.get_bucket_by_name(bucket_name)
    sanitized_file_name = sanitize_filename(os.path.basename(file_path))
    b2_file_path = os.path.join(folder_name, sanitized_file_name).replace('\\', '/')
    
    file_size = os.path.getsize(file_path)
    chunk_size = 1024 * 1024 * 10  # 10MB chunks

    with open(file_path, 'rb') as f:
        bytes_read = f.read()
        upload_source = UploadSourceBytes(bytes_read)
        bucket.upload(upload_source, b2_file_path)
        
        progress_callback(file_size, file_size)

def sanitize_filename(filename):
    # Remove caracteres especiais e substitui espaços por underscores
    return ''.join(c if c.isalnum() or c in ('.', '_') else '_' for c in filename)

def compress_files(file_paths, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in file_paths:
            zipf.write(file, os.path.basename(file))

def options():
    st.markdown(
    """
    <style>
        div[data-baseweb="input"] input {
        background-color:  #d3d3d3;
        color: #333333;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    

    with col1:
        kv = st.text_input('**KV:**', placeholder="Digite apenas números", key='kv_text', help='Medida da tensão elétrica utilizada no tubo de raios-X (Kilovolt)')
        if any(not char.isdigit() for char in kv):
            st.write(':blue[**Digite apenas números!**]')

    with col2:
        mas = st.text_input('**mAs:**', placeholder="Digite apenas números", key='mas_text', help='Medida da quantidade de radiação usada para obter uma imagem(miliAmpere-segundo)')
        if any(not char.isdigit() for char in mas):
            st.write(':blue[**Digite apenas números!**]')
    
    with col3:
            options = ['Mo/Mo', 'Rh/Rh', 'Mo/Rh', 'W/Rh']
            selected_option = st.radio("Combinação Alvo/Filtro:", options, horizontal=True, index=None)

 
            # Display the selected option
            alvo_filtro = selected_option
            
            #alvo_filtro = st.text_input('**Combinação Alvo/Filtro:**', key='alvo_text', help='Informar a combinação do material do alvo e do filtro usados no tubo de raios-X')

    return kv, mas, alvo_filtro





def limpar_text():
    st.session_state["nome_text"] = ""
    st.session_state["cnes_text"] = ""
    st.session_state["kv_text"] = ""
    st.session_state["mas_text"] = ""
    #st.session_state["alvo_text"] = ""

    st.session_state["file_uploader_key"] += 1




def phantomcbr():

    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0

    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = []


    if "nome" not in st.session_state:
        st.session_state["nome"] = True

    col1, col2, col3 = st.columns([4, 1, 7])

    with col1:
        st.write('')
    with col2:
        logo_image = "https://github.com/MATHIASCESAR/phantom//blob/meu_app/phantomMAMA.png?raw=true"
        st.image(logo_image, width=50)
    with col3:
        st.markdown('<h4>Phantom ACR</h4>', unsafe_allow_html=True)
       
    st.markdown('<h4>Informações do Serviço</h4>', unsafe_allow_html=True)
    nome = st.text_input('**Razão Social:**', key='nome_text')
    cnes = st.text_input('**Identificação CNES:**', placeholder="Digite apenas números", key='cnes_text', help='Favor informar o número do Cadastro Nacional de Estabelecimentos em Saúde')
    if any(not char.isdigit() for char in cnes):
        st.write(':blue[**Digite apenas números!**]')

    st.markdown('---', unsafe_allow_html=True)


    option = st.radio('**Selecione o Tipo de Equipamento:**', ['CR', 'DR'], horizontal=True, help='Selecione entre Mamográfica Convencional(CR) ou Mamografica Digital(DR)')

    st.markdown('---', unsafe_allow_html=True)
    st.write('**Avaliação da Qualidade da Imagem do Simulador**', help='Informar a combinação do material do alvo e do filtro usados no tubo de raios-X')

    kv, mas, alvo_filtro = '', '', ''
    if option == 'CR':
        kv, mas, alvo_filtro = options()
    elif option == 'DR':
        kv, mas, alvo_filtro = '0', '0', '0'  # Atribuir valores zerados para DR

    st.markdown('---', unsafe_allow_html=True)
    st.markdown('<h4>Upload da Imagem Phantom:</h4>', unsafe_allow_html=True)


   
    uploaded_files = st.file_uploader('Escolha os arquivos de imagem .DCM', type=['dcm'], accept_multiple_files=True, help='Selecione um ou mais arquivos de Imagem .DCM', key=st.session_state["file_uploader_key"])
    submit_button = st.button('Enviar', type='primary')
    
   
    if submit_button:
        alerta = st.warning('Favor Aguardar a **CONFIRMAÇÃO** do envio! Em andamento...', icon='⚠️')

        if nome and cnes and kv and mas and alvo_filtro and uploaded_files:
            novo_cliente = Cliente(nome=nome, cnes=cnes, kv=kv, mas=mas, alvo_filtro=alvo_filtro)
            session.add(novo_cliente)
            session.commit()

            sanitized_name = sanitize_filename(nome)
            client_folder = os.path.join('Phantom_ACR', sanitized_name)
            os.makedirs(client_folder, exist_ok=True)

            progress_text = st.empty()
            progress_bar = st.progress(0)
            total_files = len(uploaded_files)
            overall_progress = 0.0

            def update_progress(uploaded_size, file_size):
                nonlocal overall_progress
                progress = min(uploaded_size / file_size, 1.0)
                overall_progress += progress / total_files
                overall_progress = min(overall_progress, 1.0)
                progress_bar.progress(overall_progress)
                progress_text.text(f'Progresso do upload: {int(overall_progress * 100)}%')

            dcm_files = []
            for uploaded_file in uploaded_files:
                sanitized_filename = sanitize_filename(uploaded_file.name)
                file_path = os.path.join(client_folder, sanitized_filename)
                with open(file_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                dcm_files.append(file_path)

                try:
                    dicom_data = pydicom.dcmread(file_path)
                    #st.subheader(f'Informações do Arquivo DICOM: {sanitized_filename}')
                    #st.text(f'Patient Name: {dicom_data.PatientName}')
                    #st.text(f'Modality: {dicom_data.Modality}')
                    #st.text(f'Study Date: {dicom_data.StudyDate}')
                except Exception as e:
                    st.error(f'Erro ao ler o arquivo DICOM: {e}')
            
            zip_path = os.path.join(client_folder, f'{sanitized_name}.zip')
            compress_files(dcm_files, zip_path)
                        
            try:
                upload_to_b2_chunked('0023525a40197c60000000001', 'K002lukJuxRdegDgWgkfo6Uws0BZ9LM', 'macesar', zip_path, sanitized_name, update_progress)
                alerta.empty()
                #mensagem(f'Arquivo(s) ENVIADO(s) com sucesso!', blinking=True)
                
            except Exception as e:
                alerta.empty()
                st.error(f'Erro ao fazer upload para a NUVEM B2: {e}')
                
            try:
                upload_to_b2_chunked('0023525a40197c60000000001', 'K002lukJuxRdegDgWgkfo6Uws0BZ9LM', 'macesar', 'clientes.db', 'database_backup', update_progress)
            except Exception as e:
                st.error(f'Erro ao fazer upload do banco de dados para a Nuvem B2: {e}')

            progress_text.text('')
            progress_bar.empty()
            mensagem(f'Arquivo(s) ENVIADO(s) com sucesso!', blinking=True)
            #mycode = "<script>alert('Arquivo(s) ENVIADO(s) com sucesso!')</script>"
            #components.html(mycode, height=0, width=0)        
            #st.session_state["file_uploader_key"] += 1
            #st.experimental_rerun()
            st.markdown('---', unsafe_allow_html=True)

            if progress_bar.empty():
                col3, col4 = st.columns([3,1])
                with col3:                          
                    st.markdown('<h4>Clique em SIM se deseja enviar mais arquivos!</h4>', unsafe_allow_html=True)
                with col4:
                    st.button('SIM', on_click=limpar_text, type='primary')
            

        else:
            st.error('Por favor, preencha todos os campos e faça o upload de pelo menos um arquivo DICOM.')


if __name__ == '__main__':
    phantomcbr()
