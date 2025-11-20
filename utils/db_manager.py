# utils/db_manager.py
import sqlite3
import os
from typing import Dict, Any, List, Optional

# Place the database file in the project root (one level above this utils package)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "database.db")

def conectar():
    # Garantir que o diretório do DB exista
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir, exist_ok=True)
        except Exception:
            pass

    # Garantir que o arquivo do DB exista (modo seguro)
    if not os.path.exists(DB_PATH):
        try:
            open(DB_PATH, "a").close()
        except Exception:
            # deixamos a chamada a sqlite lançar erro se não for possível criar
            pass

    return sqlite3.connect(DB_PATH)

def inicializar_db():
    conn = conectar()
    cur = conn.cursor()

    # Tabela usuarios (mantém compatibilidade)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        senha_hash TEXT NOT NULL
    )
    """)

    # Se a tabela já existia e não possui a coluna senha_hash, adicioná-la (migração segura - opção A)
    try:
        cur.execute("PRAGMA table_info(usuarios)")
        cols_info = cur.fetchall()
        col_names = [c[1] for c in cols_info]
        if 'senha_hash' not in col_names:
            # adicionar coluna sem alterar dados existentes
            cur.execute("ALTER TABLE usuarios ADD COLUMN senha_hash TEXT")
            # não removemos coluna antiga (se existir) aqui - política segura
    except Exception:
        # se qualquer erro ocorrer, não interromper a inicialização
        pass

    # Tabela Tbl_Procedim (parâmetros normativos) - conforme especificado
    # Construímos dinamicamente o SQL para evitar um bloco enorme de texto
    campos = [
        "REG_NORMA INTEGER PRIMARY KEY AUTOINCREMENT",
        "PROC TEXT"
    ]

    # Pen_01..Pen_20
    campos += [f"Pen_{i:02d} REAL" for i in range(1, 21)]
    # Abert_Pen_01..Abert_Pen_20
    campos += [f"Abert_Pen_{i:02d} REAL" for i in range(1, 21)]
    # Fx_min_Pen_01..Fx_min_Pen_20
    campos += [f"Fx_min_Pen_{i:02d} REAL" for i in range(1, 21)]
    # Fx_max_Pen_01..Fx_max_Pen_20
    campos += [f"Fx_max_Pen_{i:02d} REAL" for i in range(1, 21)]

    # Campos adicionais
    campos += [
        "VV_min REAL", "VV_max REAL",
        "RBV_min REAL", "RBV_max REAL",
        "VAM_min REAL",
        "Filler_Asf_min REAL", "Filler_Asf_max REAL",
        "RTCD_min REAL",
        "DUI_min REAL",
        "Estab_min REAL",
        "Fluen_min REAL", "Fluen_max REAL"
    ]

    sql_proc = f"CREATE TABLE IF NOT EXISTS Tbl_Procedim ({', '.join(campos)})"
    cur.execute(sql_proc)

    # Tabela Tbl_Projeto (parâmetros de estudo/projeto)
    campos_proj = [
        "ID_PROJ INTEGER PRIMARY KEY AUTOINCREMENT",
        "PROJ TEXT",
        "Teor_otimo REAL",
        "Fx_gran_trabalho TEXT",
        "VAM REAL",
        "RBV REAL",
        "VV REAL",
        "Estabilidade REAL",
        "Fluencia REAL",
        "Densidade_aparente REAL",
        "DUI REAL",
        "Observacoes TEXT"
    ]
    # Pen_01..Pen_20
    campos_proj += [f"Pen_{i:02d} REAL" for i in range(1, 21)]
    # Abert_Pen_01..Abert_Pen_20
    campos_proj += [f"Abert_Pen_{i:02d} REAL" for i in range(1, 21)]
    # Fx_min_Pen_01..Fx_min_Pen_20
    campos_proj += [f"Fx_min_Pen_{i:02d} REAL" for i in range(1, 21)]
    # Fx_max_Pen_01..Fx_max_Pen_20
    campos_proj += [f"Fx_max_Pen_{i:02d} REAL" for i in range(1, 21)]
    sql_proj = f"CREATE TABLE IF NOT EXISTS Tbl_Projeto ({', '.join(campos_proj)})"
    cur.execute(sql_proj)
    # Migração segura: se a tabela já existir mas não possuir novas colunas, adicioná-las
    try:
        cur.execute("PRAGMA table_info(Tbl_Projeto)")
        cols_info = cur.fetchall()
        existing_cols = {c[1] for c in cols_info}
        # colunas que adicionamos recentemente
        needed = ["Teor_minimo", "Teor_maximo"]
        for col in needed:
            if col not in existing_cols:
                try:
                    cur.execute(f"ALTER TABLE Tbl_Projeto ADD COLUMN {col} REAL")
                except Exception:
                    pass
    except Exception:
        pass

    # Tabela de registros gerais (mantida se já existia)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS registros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        categoria TEXT,
        ensaio TEXT,
        dados_digitados TEXT,
        resultados TEXT,
        data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

#Função que cria a tabela do Ensaio_001
def criar_tabela_ensaio_001(table_name: str = "Tbl_Ensaio_001"):
    """Cria a tabela para o Ensaio 001. `table_name` pode ser alterado para criar tabelas com nomes diferentes."""
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Rodovia TEXT,
                Trecho TEXT,
                Sub_trecho TEXT,
                Protocolo INTEGER,
                Hora TEXT,
                Projeto TEXT,
                Material TEXT,
                Usina TEXT,
                Local TEXT,
                Data_rec TEXT,
                Data_ensaio TEXT,
                Placa TEXT,
                Faixa TEXT,
                Obra TEXT,
                Clima TEXT,
                Operador TEXT,
                Temp REAL,
                Am_ligante REAL,
                Am_Lavada REAL,
                Fat_corr REAL,
                Teor REAL,
                Filler REAL,
                -- Retenção e percentuais de peneiras
                Ret_Pen1 REAL, Ret_Pen2 REAL, Ret_Pen3 REAL, Ret_Pen4 REAL, Ret_Pen5 REAL,
                Ret_Pen6 REAL, Ret_Pen7 REAL, Ret_Pen8 REAL, Ret_Pen9 REAL, Ret_Pen10 REAL,
                Ret_Pen11 REAL, Ret_Pen12 REAL, Ret_Pen13 REAL, Ret_Pen14 REAL, Ret_Pen15 REAL,
                Ret_Pen16 REAL, Ret_Pen17 REAL, Ret_Pen18 REAL, Ret_Pen19 REAL, Ret_Pen20 REAL,
                Perc_Pen1 REAL, Perc_Pen2 REAL, Perc_Pen3 REAL, Perc_Pen4 REAL, Perc_Pen5 REAL,
                Perc_Pen6 REAL, Perc_Pen7 REAL, Perc_Pen8 REAL, Perc_Pen9 REAL, Perc_Pen10 REAL,
                Perc_Pen11 REAL, Perc_Pen12 REAL, Perc_Pen13 REAL, Perc_Pen14 REAL, Perc_Pen15 REAL,
                Perc_Pen16 REAL, Perc_Pen17 REAL, Perc_Pen18 REAL, Perc_Pen19 REAL, Perc_Pen20 REAL,
                Rice_1 REAL, Rice_2 REAL, Rice_3 REAL, Dens_Rice REAL,
                Umid_1 REAL, Umid_2 REAL, Teor_real REAL,
                CpAr_1 REAL, CpAr_2 REAL, CpAr_3 REAL,
                CpIm_1 REAL, CpIm_2 REAL, CpIm_3 REAL,
                CpSa_1 REAL, CpSa_2 REAL, CpSa_3 REAL,
                Dens_Apar REAL, Vazios REAL, VCB REAL, VAM REAL, RBV REAL,
                Alt_Cp1 REAL, Alt_Cp2 REAL, Alt_Cp3 REAL,
                Con_Prensa REAL,
                RT_Cp1 INTEGER, RT_Cp2 INTEGER, RT_Cp3 INTEGER, RTCD REAL,
                Est_Cp1 INTEGER, Est_Cp2 INTEGER, Est_Cp3 INTEGER, Estabilidade REAL,
                Fl_Cp1 REAL, Fl_Cp2 REAL, Fl_Cp3 REAL,
                Fl_Cp4 REAL, Fl_Cp5 REAL, Fl_Cp6 REAL, Fluencia REAL,
                Ass_1 TEXT, Ass_2 TEXT
            )
        """)
        conn.commit()

# --- Funções de CRUD --- #

def inserir_procedim(dados: Dict[str, Any]) -> int:
    """
    Insere um registro em Tbl_Procedim.
    `dados` é um dict cujas chaves são os nomes das colunas (ex: "PROC","Pen_01", ...).
    Retorna o REG_NORMA (id) do registro inserido.
    """
    inicializar_db()
    conn = conectar()
    cur = conn.cursor()

    # remover chaves vazias que não existem como colunas (defensivo)
    # construir lista de colunas e placeholders
    cols = []
    vals = []
    for k, v in dados.items():
        # aceite apenas chaves não-nulas e que não sejam REG_NORMA
        if k and k != "REG_NORMA":
            cols.append(k)
            vals.append(v)

    if not cols:
        conn.close()
        raise ValueError("Nenhum campo para inserir em Tbl_Procedim")

    placeholders = ", ".join(["?"] * len(cols))
    sql = f"INSERT INTO Tbl_Procedim ({', '.join(cols)}) VALUES ({placeholders})"
    cur.execute(sql, vals)
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id

def atualizar_procedim(reg_id: int, dados: Dict[str, Any]) -> None:
    """
    Atualiza registro existente em Tbl_Procedim pelo REG_NORMA.
    """
    inicializar_db()
    conn = conectar()
    cur = conn.cursor()
    set_clause = ", ".join([f"{k}=?" for k in dados.keys()])
    values = list(dados.values())
    values.append(reg_id)
    sql = f"UPDATE Tbl_Procedim SET {set_clause} WHERE REG_NORMA = ?"
    cur.execute(sql, values)
    conn.commit()
    conn.close()


def excluir_procedim(reg_id: int) -> None:
    """
    Remove registro de Tbl_Procedim pelo REG_NORMA.
    """
    inicializar_db()
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM Tbl_Procedim WHERE REG_NORMA = ?", (reg_id,))
    conn.commit()
    conn.close()


def existe_procedim(dados: Dict[str, Any]) -> bool:
    """
    Verifica se já existe um registro com os mesmos valores das colunas especificadas (exclui REG_NORMA).
    Retorna True se houver duplicata.
    """
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    conditions = " AND ".join([f"{k}=?" for k in dados.keys() if k != "REG_NORMA"])
    values = [v for k, v in dados.items() if k != "REG_NORMA"]
    sql = f"SELECT 1 FROM Tbl_Procedim WHERE {conditions} LIMIT 1"
    cur.execute(sql, values)
    exists = cur.fetchone() is not None
    conn.close()
    return exists

def inserir_projeto(dados: Dict[str, Any]) -> int:
    """
    Insere um registro em Tbl_Projeto.
    Retorna o ID_PROJ inserido.
    """
    inicializar_db()
    conn = conectar()
    cur = conn.cursor()

    cols = []
    vals = []
    for k, v in dados.items():
        if k and k != "ID_PROJ":
            cols.append(k)
            vals.append(v)

    if not cols:
        conn.close()
        raise ValueError("Nenhum campo para inserir em Tbl_Projeto")

    placeholders = ", ".join(["?"] * len(cols))
    sql = f"INSERT INTO Tbl_Projeto ({', '.join(cols)}) VALUES ({placeholders})"
    cur.execute(sql, vals)
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id

def get_ultimo_procedim() -> Optional[Dict[str, Any]]:
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tbl_Procedim ORDER BY REG_NORMA DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return dict(row)

def get_procedim_por_id(reg_id: int) -> Optional[Dict[str, Any]]:
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tbl_Procedim WHERE REG_NORMA = ?", (reg_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return dict(row)

def get_all_procedim() -> List[Dict[str, Any]]:
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tbl_Procedim ORDER BY REG_NORMA ASC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_projetos() -> List[Dict[str, Any]]:
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tbl_Projeto ORDER BY ID_PROJ ASC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Execução direta para criar DB ao importar rodando como script
if __name__ == "__main__":
    inicializar_db()
    print("Banco inicializado em", DB_PATH)
