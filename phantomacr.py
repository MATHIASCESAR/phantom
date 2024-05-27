import os
import streamlit as st
import pydicom
import sqlalchemy
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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

def phantomacr():
    col1, col2 = st.columns([1, 35])

    with col1:
        st.write("")

    with col2:
        logo_image = "phantomACR.jpg"
        st.image(logo_image, width=500)

    st.markdown('<h3>Informações do Serviço</h3>', unsafe_allow_html=True)
    

    with st.form(key='cliente_form', clear_on_submit=True):
        nome = st.text_input('Nome')
        st.markdown('<h3>Upload da Imagem Phantom:</h3>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader('Escolha o arquivo da imagem .DCM', type=['dcm'])

        submit_button = st.form_submit_button('Confirmar')

        if submit_button:
            if nome and uploaded_file is not None:
                # Salvar informações do cliente no banco de dados
                novo_cliente = Cliente(nome=nome)
                session.add(novo_cliente)
                session.commit()
                st.success(f'Cliente {nome} cadastrado com sucesso!')

                # Criar pasta com o nome do cliente
                client_folder = os.path.join('Phantom ACR', nome)
                os.makedirs(client_folder, exist_ok=True)

                # Salvar o arquivo na pasta do cliente
                file_path = os.path.join(client_folder, uploaded_file.name)
                with open(file_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f'Arquivo {uploaded_file.name} salvo na pasta {client_folder} com sucesso!')

                # Exibir algumas informações do arquivo DICOM
                try:
                    dicom_data = pydicom.dcmread(file_path)
                    st.subheader('Informações do Arquivo DICOM')
                    st.text(f'Patient Name: {dicom_data.PatientName}')
                    st.text(f'Modality: {dicom_data.Modality}')
                    st.text(f'Study Date: {dicom_data.StudyDate}')
                except Exception as e:
                    st.error(f'Erro ao ler o arquivo DICOM: {e}')
            else:
                st.error('Por favor, preencha todos os campos e faça o upload de um arquivo DICOM.')

if __name__ == '__main__':
    phantomacr()
