
import os
import streamlit as st
import pydicom
import sqlite3
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do banco de dados
DATABASE_URL = "sqlite:///clientes.db"

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telefone = Column(String, nullable=False)

# Criar a engine do banco de dados
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

# Criar a sessão do banco de dados
Session = sessionmaker(bind=engine)
session = Session()

def main():
    st.title('Cadastro de Clientes')

    # Formulário de Cadastro de Cliente
    st.header('Informações do Cliente')
    nome = st.text_input('Nome')
    email = st.text_input('Email')
    telefone = st.text_input('Telefone')

    # Upload de Arquivo DICOM
    st.header('Upload de Arquivo DICOM')
    uploaded_file = st.file_uploader('Escolha um arquivo DICOM', type=['dcm'])

    if st.button('Cadastrar Cliente e Carregar Arquivo'):
        if nome and email and telefone and uploaded_file is not None:
            # Salvar informações do cliente no banco de dados
            novo_cliente = Cliente(nome=nome, email=email, telefone=telefone)
            session.add(novo_cliente)
            session.commit()
            st.success(f'Cliente {nome} cadastrado com sucesso!')

            # Criar pasta com o nome do cliente
            client_folder = os.path.join('clientes', nome)
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

    # Exibir dados da tabela clientes
    st.header('Clientes Cadastrados')
    if st.button('Ver Clientes Cadastrados'):
        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        conn.close()

        for cliente in clientes:
            st.text(f'ID: {cliente[0]}, Nome: {cliente[1]}, Email: {cliente[2]}, Telefone: {cliente[3]}')

if __name__ == '__main__':
    main()
