import os
import streamlit as st
import pydicom
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from b2sdk.v2 import B2Api

# Configuração do banco de dados
DATABASE_URL = 'sqlite:///clientes.db'

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)

# Criar a engine do banco de dados
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

# Criar a sessão do banco de dados
Session = sessionmaker(bind=engine)
session = Session()

def authenticate_b2(account_id, application_key):
    b2_api = B2Api()
    b2_api.authorize_account("production", account_id, application_key)
    return b2_api

def upload_to_b2(account_id, application_key, bucket_name, file_path, folder_name):
    b2_api = authenticate_b2(account_id, application_key)
    bucket = b2_api.get_bucket_by_name(bucket_name)
    sanitized_file_name = sanitize_filename(os.path.basename(file_path))
    b2_file_path = os.path.join(folder_name, sanitized_file_name).replace('\\', '/')
    with open(file_path, 'rb') as f:
        bucket.upload_local_file(local_file=file_path, file_name=b2_file_path)

def sanitize_filename(filename):
    # Remove caracteres especiais e substitui espaços por underscores
    return ''.join(c if c.isalnum() or c in ('.', '_') else '_' for c in filename)

def phantomacr():
    col1, col2 = st.columns([1, 35])

    with col1:
        st.write("")

    with col2:
        logo_image = "https://github.com/MATHIASCESAR/phantom/blob/meu_app/phantomACR.jpg?raw=true"
        st.image(logo_image, width=500)

    st.markdown('<h4>Informações do Serviço</h4>', unsafe_allow_html=True)
    
    with st.form(key='cliente_form', clear_on_submit=True):
        nome = st.text_input('Nome')
        st.markdown('<h4>Upload da Imagem Phantom:</h4>', unsafe_allow_html=True)
        uploaded_files = st.file_uploader('Escolha os arquivos de imagem .DCM', type=['dcm'], accept_multiple_files=True)

        submit_button = st.form_submit_button('Confirmar')

        if submit_button:
            if nome and uploaded_files:
                # Salvar informações do cliente no banco de dados
                novo_cliente = Cliente(nome=nome)
                session.add(novo_cliente)
                session.commit()
                st.success(f'Favor Aguardar a CONFIRMAÇÃO do envio! Em andamento.....')

                # Criar pasta com o nome do cliente localmente
                sanitized_name = sanitize_filename(nome)
                client_folder = os.path.join('Phantom_ACR', sanitized_name)
                os.makedirs(client_folder, exist_ok=True)

                for uploaded_file in uploaded_files:
                    # Salvar o arquivo na pasta do cliente localmente
                    sanitized_filename = sanitize_filename(uploaded_file.name)
                    file_path = os.path.join(client_folder, sanitized_filename)
                    with open(file_path, 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    #st.success(f'Arquivo {sanitized_filename} salvo na pasta {client_folder} com sucesso!')

                    # Autenticação e upload para o Backblaze B2
                    try:
                        upload_to_b2('0023525a40197c60000000001', 'K002lukJuxRdegDgWgkfo6Uws0BZ9LM', 'macesar', file_path, sanitized_name)
                        st.success(f'Arquivo {sanitized_filename} ENVIADO com sucesso!')
                    except Exception as e:
                        st.error(f'Erro ao fazer upload para o Backblaze B2: {e}')

                    # Exibir algumas informações do arquivo DICOM
                    try:
                        dicom_data = pydicom.dcmread(file_path)
                        st.subheader(f'Informações do Arquivo DICOM: {sanitized_filename}')
                        st.text(f'Patient Name: {dicom_data.PatientName}')
                        st.text(f'Modality: {dicom_data.Modality}')
                        st.text(f'Study Date: {dicom_data.StudyDate}')
                    except Exception as e:
                        st.error(f'Erro ao ler o arquivo DICOM: {e}')
            else:
                st.error('Por favor, preencha todos os campos e faça o upload de pelo menos um arquivo DICOM.')

if __name__ == '__main__':
    phantomacr()
