import os
import sys

# --- Garantir importação funcional em qualquer contexto ---
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def base_path() -> str:
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    else:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def resource_path(relative_path: str) -> str:
    return os.path.join(base_path(), relative_path)

def get_database_path() -> str:
    """Retorna o caminho absoluto do banco de dados SQLite"""
    return resource_path("database.db")

def get_planilha_path(nome_ensaio: str, categoria: str = "asfalto") -> str:
    return resource_path(os.path.join("planilhas", categoria, nome_ensaio))

def get_ui_path(nome_tela: str) -> str:
    return resource_path(os.path.join("ui", nome_tela))

def get_utils_path(nome_script: str) -> str:
    return resource_path(os.path.join("utils", nome_script))

def garantir_pastas_essenciais():
    pastas = [
        os.path.join(base_path(), "planilhas", "asfalto"),
        os.path.join(base_path(), "planilhas", "concreto"),
        os.path.join(base_path(), "planilhas", "solos"),
        os.path.join(base_path(), "ui"),
        os.path.join(base_path(), "utils"),
    ]
    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)

if __name__ == "__main__":
    print("Base path:", base_path())
    print("Database path:", get_database_path())
    print("Planilha Asfalto:", get_planilha_path("Ensaio_001.xlsm"))
