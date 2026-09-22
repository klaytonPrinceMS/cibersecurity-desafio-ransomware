# Encriptador e Descriptador de Arquivos CLI

Uma ferramenta de linha de comando simples e segura desenvolvida em Python para criptografia e descriptografia de arquivos usando criptografia simétrica com chave derivada por senha.

## 🚀 Funcionalidades

- **Criptografia Segura**: Utiliza a cifra Fernet (AES-128 em modo CBC com HMAC-SHA256 para verificação de integridade).
- **Derivação de Chave Forte**: Derivação de chaves a partir de senhas de texto puro utilizando **PBKDF2HMAC** com SHA256 e sal aleatório.
- **Detecção Automática**: O script identifica automaticamente se deve criptografar ou descriptografar com base na extensão do arquivo (`.cripto`).
- **Interface CLI**: Operação via argumentos diretos na linha de comando.

---

## 📋 Pré-requisitos

- **Python 3.8+** instalado.
- Gerenciador de pacotes **pip**.

---

## 📦 Instalação

1. **Clone o repositório:**
   ```bash
   mkdir cripto
   git clone https://github.com/klaytonPrinceMS/cibersecurity-desafio-ransomware
   cd cripto
   ```

2. **Crie e ative um ambiente virtual (recomendado):**
   - **Windows:**
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```
   - **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Como Usar

O script `klayton.py` aceita dois parâmetros obrigatórios:
- `--arquivo`: Caminho para o arquivo que será processado.
- `--senha`: Senha combinada para criptografia ou descriptografia.

### 🔒 Criptografar um arquivo
Para criptografar um arquivo comum (ex: `documento.pdf` ou `mensagem.txt`):

```bash
python criptografia.py --arquivo arquivoParaCriptografar.txt --senha MinhaSenhaSegura123
```
* **Resultado:** O arquivo original será substituído pelo arquivo criptografado `arquivoParaCriptografar.txt.cripto`.

---

### 🔓 Descriptografar um arquivo
Para descriptografar um arquivo `.cripto` recebido:

```bash
python criptografia.py --arquivo mensagem.txt.cripto --senha MinhaSenhaSegura123
```
* **Resultado:** O arquivo `.cripto` será removido e o arquivo original `mensagem.txt` será restaurado.

---

## 🛡️ Segurança

- O arquivo criptografado armazena um **sal (salt)** aleatório de 16 bytes no seu cabeçalho, garantindo que senhas iguais gerem criptografias totalmente diferentes a cada execução.
- Em caso de senha incorreta ou arquivo corrompido, o script interrompe o processo e exibe um erro de autenticação sem alterar o arquivo original.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.