import os
import base64
import argparse
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

"""
Unified file encryption and decryption script via command line arguments.

English documentation:
This script allows users to encrypt or decrypt files using a password. It automatically determines
whether to perform encryption or decryption based on the file extension (.cripto).

Documentação em português:
Este script permite criptografar ou descriptografar arquivos usando uma senha. Ele determina automaticamente
se deve executar a criptografia ou a descriptografia com base na extensão do arquivo (.cripto).
"""

def gerar_chave_da_senha(senha: str, sal: bytes) -> bytes:
    """
    Derives a cryptographic key from a password.

    English documentation:
    Uses PBKDF2HMAC with SHA256 to generate a key compatible with Fernet.

    Documentação em português:
    Usa PBKDF2HMAC com SHA256 para gerar uma chave compatível com Fernet.
    """
    gerador_chave = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=sal,
        iterations=480000,
    )
    return base64.urlsafe_b64encode(gerador_chave.derive(senha.encode()))

def criptografar_arquivo(caminho_arquivo: str, senha: str) -> None:
    """
    Encrypts a file and replaces it with an encrypted version.

    English documentation:
    Reads input data, encrypts it, appends salt, and writes to a new file with .cripto extension.

    Documentação em português:
    Lê os dados de entrada, os criptografa, anexa o sal e grava em um novo arquivo com a extensão .cripto.
    """
    sal = os.urandom(16)
    chave = gerar_chave_da_senha(senha, sal)
    fernet = Fernet(chave)

    with open(caminho_arquivo, "rb") as arquivo_entrada:
        dados_originais = arquivo_entrada.read()

    dados_criptografados = fernet.encrypt(dados_originais)
    caminho_saida = caminho_arquivo + ".cripto"

    with open(caminho_saida, "wb") as arquivo_saida:
        arquivo_saida.write(sal + dados_criptografados)

    os.remove(caminho_arquivo)
    print(f"Arquivo criptografado com sucesso: {caminho_saida}")

def descriptografar_arquivo(caminho_arquivo_criptografado: str, senha: str) -> None:
    """
    Decrypts an encrypted file and restores the original file.

    English documentation:
    Extracts the salt, decrypts the ciphertext, and restores the original file.

    Documentação em português:
    Extrai o sal, descriptografa os dados e restaura o arquivo original.
    """
    with open(caminho_arquivo_criptografado, "rb") as arquivo_entrada:
        conteudo = arquivo_entrada.read()

    sal = conteudo[:16]
    dados_criptografados = conteudo[16:]

    chave = gerar_chave_da_senha(senha, sal)
    fernet = Fernet(chave)

    try:
        dados_descriptografados = fernet.decrypt(dados_criptografados)
        caminho_original = caminho_arquivo_criptografado.replace(".cripto", "")

        with open(caminho_original, "wb") as arquivo_saida:
            arquivo_saida.write(dados_descriptografados)

        os.remove(caminho_arquivo_criptografado)
        print(f"Arquivo descriptografado com sucesso: {caminho_original}")
    except Exception:
        print("Erro: Senha incorreta ou arquivo corrompido.")

def executar_processo() -> None:
    """
    Parses command line arguments and triggers appropriate operation.

    English documentation:
    Handles input flags --arquivo and --senha to execute encryption or decryption.

    Documentação em português:
    Processa os argumentos de linha de comando --arquivo e --senha para executar criptografia ou descriptografia.
    """
    analisador = argparse.ArgumentParser(description="Script para criptografar e descriptografar arquivos.")
    analisador.add_argument("--arquivo", required=True, help="Caminho do arquivo a ser processado")
    analisador.add_argument("--senha", required=True, help="Senha para criptografia ou descriptografia")

    argumentos = analisador.parse_args()

    if not os.path.exists(argumentos.arquivo):
        print(f"Erro: O arquivo '{argumentos.arquivo}' não foi encontrado.")
        return

    if argumentos.arquivo.endswith(".cripto"):
        descriptografar_arquivo(argumentos.arquivo, argumentos.senha)
    else:
        criptografar_arquivo(argumentos.arquivo, argumentos.senha)

if __name__ == "__main__":
    executar_processo()