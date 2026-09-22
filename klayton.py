import os
import base64
import argparse
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

"""
Unified file and folder encryption/decryption script via command line arguments.

English documentation:
This script allows users to encrypt or decrypt individual files or entire folders using a password.
It automatically determines whether to perform encryption or decryption based on the file extension (.cripto).

Documentação em português:
Este script permite criptografar ou descriptografar arquivos individuais ou pastas inteiras usando uma senha.
Ele determina automaticamente se deve executar a criptografia ou a descriptografia com base na extensão (.cripto).
"""


def gerar_chave_da_senha(senha: str, sal: bytes) -> bytes:
    """
    Derives a cryptographic key from a password using PBKDF2HMAC with SHA256.
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
    Encrypts a single file and replaces it with an encrypted version (.cripto).
    """
    try:
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
        print(f"[Criptografado] {caminho_saida}")
    except Exception as e:
        print(f"Erro ao criptografar '{caminho_arquivo}': {e}")


def descriptografar_arquivo(caminho_arquivo_criptografado: str, senha: str) -> None:
    """
    Decrypts an encrypted file and restores the original file.
    """
    try:
        with open(caminho_arquivo_criptografado, "rb") as arquivo_entrada:
            conteudo = arquivo_entrada.read()

        sal = conteudo[:16]
        dados_criptografados = conteudo[16:]

        chave = gerar_chave_da_senha(senha, sal)
        fernet = Fernet(chave)

        dados_descriptografados = fernet.decrypt(dados_criptografados)
        caminho_original = caminho_arquivo_criptografado.replace(".cripto", "")

        with open(caminho_original, "wb") as arquivo_saida:
            arquivo_saida.write(dados_descriptografados)

        os.remove(caminho_arquivo_criptografado)
        print(f"[Descriptografado] {caminho_original}")
    except Exception:
        print(f"Erro ao descriptografar '{caminho_arquivo_criptografado}': Senha incorreta ou arquivo corrompido.")


def processar_pasta(caminho_pasta: str, senha: str) -> None:
    """
    Recursively processes all files inside a folder for encryption or decryption.
    """
    print(f"Processando a pasta: {caminho_pasta}\n")

    arquivos_encontrados = 0
    for raiz, _, arquivos in os.walk(caminho_pasta):
        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)
            arquivos_encontrados += 1

            if arquivo.endswith(".cripto"):
                descriptografar_arquivo(caminho_completo, senha)
            else:
                criptografar_arquivo(caminho_completo, senha)

    if arquivos_encontrados == 0:
        print("A pasta está vazia.")
    else:
        print("\nProcessamento da pasta concluído!")


def executar_processo() -> None:
    """
    Parses command line arguments and triggers appropriate operation for file or folder.
    """
    analisador = argparse.ArgumentParser(description="Script para criptografar e descriptografar arquivos e pastas.")

    # Grupo para garantir que o usuário informe --arquivo OU --pasta (mas não ambos ao mesmo tempo)
    grupo = analisador.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--arquivo", help="Caminho do arquivo a ser processado")
    grupo.add_argument("--pasta", help="Caminho da pasta a ser processada recursivamente")

    analisador.add_argument("--senha", required=True, help="Senha para criptografia ou descriptografia")

    argumentos = analisador.parse_args()

    if argumentos.arquivo:
        if not os.path.exists(argumentos.arquivo):
            print(f"Erro: O arquivo '{argumentos.arquivo}' não foi encontrado.")
            return
        if argumentos.arquivo.endswith(".cripto"):
            descriptografar_arquivo(argumentos.arquivo, argumentos.senha)
        else:
            criptografar_arquivo(argumentos.arquivo, argumentos.senha)

    elif argumentos.pasta:
        if not os.path.exists(argumentos.pasta):
            print(f"Erro: A pasta '{argumentos.pasta}' não foi encontrada.")
            return
        processar_pasta(argumentos.pasta, argumentos.senha)


if __name__ == "__main__":
    executar_processo()