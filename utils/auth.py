import sqlite3
import hashlib
import os
import sys
import shutil

def resource_path(relative_path: str) -> str:
    """
    Retorna o caminho absoluto de um recurso, compatível com execução empacotada (PyInstaller).
    """
    try:
        # Quando o app é empacotado, PyInstaller cria uma pasta temporária em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Em modo de desenvolvimento, usa o diretório atual do projeto
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def garantir_db_local() -> str:
    """
    Garante que o banco de dados SQLite esteja disponível para escrita na pasta atual.
    Se estiver empacotado, copia o arquivo embutido para a pasta onde o .exe está.
    """
    # Caminho do banco na pasta atual
    db_local = os.path.join(os.getcwd(), "database.db")

    # Caminho do banco dentro do pacote (ou no modo dev)
    db_origem = resource_path("database.db")

    # Copia o banco do pacote caso ainda não exista
    if not os.path.exists(db_local):
        try:
            shutil.copy(db_origem, db_local)
        except Exception as e:
            print(f"Erro ao copiar o banco de dados: {e}")

    return db_local

# Define o caminho global do banco de dados
DB_PATH = garantir_db_local()

def conectar():
    """Abre conexão com o banco SQLite local."""
    return sqlite3.connect(DB_PATH)

def criar_tabela_usuarios():
    """Cria tabela de usuários caso não exista."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL
            )
        """)
        conn.commit()

def hash_senha(senha: str) -> str:
    """Cria o hash SHA-256 da senha informada."""
    return hashlib.sha256(senha.encode()).hexdigest()

def criar_usuario(usuario: str, senha: str) -> bool:
    """Cria um novo usuário no banco (retorna False se já existir)."""
    criar_tabela_usuarios()
    # Normalizar o nome de usuário
    usuario_norm = normalize_user(usuario)

    # Validar senha de acordo com a política
    if not validar_senha(senha):
        raise ValueError("A senha não atende à política: 8 caracteres, letras e números.")

    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (usuario, senha_hash) VALUES (?, ?)",
                (usuario_norm, hash_senha(senha))
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

def autenticar_usuario(usuario: str, senha: str) -> bool:
    """Valida usuário e senha."""
    criar_tabela_usuarios()
    usuario_norm = normalize_user(usuario)
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT senha_hash FROM usuarios WHERE usuario = ?", (usuario_norm,))
        row = cursor.fetchone()
        if row and row[0] == hash_senha(senha):
            return True
    return False


def normalize_user(usuario: str) -> str:
    """Normaliza o nome de usuário: primeira letra maiúscula e o restante minúsculas."""
    if not usuario:
        return usuario
    usuario = usuario.strip()
    return usuario[:1].upper() + usuario[1:].lower()


def validar_senha(senha: str) -> bool:
    """Valida política de senha: mínimo 8 caracteres, contém letras e números."""
    if not senha or len(senha) < 8:
        return False
    has_digit = any(c.isdigit() for c in senha)
    has_alpha = any(c.isalpha() for c in senha)
    return has_digit and has_alpha


def resetar_senha(usuario: str, nova_senha: str) -> bool:
    """Reseta a senha do usuário (necessita que o usuário exista). Retorna True se atualizado."""
    criar_tabela_usuarios()
    usuario_norm = normalize_user(usuario)
    if not validar_senha(nova_senha):
        raise ValueError("A senha não atende à política: 8 caracteres, letras e números.")

    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE usuario = ?", (usuario_norm,))
        row = cursor.fetchone()
        if not row:
            return False
        cursor.execute("UPDATE usuarios SET senha_hash = ? WHERE usuario = ?", (hash_senha(nova_senha), usuario_norm))
        conn.commit()
        return True


# from utils.db_manager import conectar, inicializar_db Modificado em 12/10/2025

# def autenticar_usuario(usuario, senha):
#     inicializar_db()
#     conn = conectar()
#     cur = conn.cursor()

#     cur.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha))
#     user = cur.fetchone()
#     conn.close()

#     return user is not None

# def criar_usuario(usuario, senha):
#     inicializar_db()
#     conn = conectar()
#     cur = conn.cursor()
#     try:
#         cur.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
#         conn.commit()
#     except Exception as e:
#         print("Erro ao criar usuário:", e)
#     finally:
#         conn.close()
