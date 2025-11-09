# ensaios/ensaio_001/sync_ensaio_001.py

import sqlite3
import win32com.client
from utils.path_helper import get_planilha_path, get_database_path
from ensaios.ensaio_001.config_ensaio_001 import CELULAS_MAPEADAS, RELACIONAMENTOS, TABELA_ENSAIO, CELULAS_COM_FORMULAS


# --------------------------
# 🔹 Funções auxiliares
# --------------------------

def abrir_excel(visivel=True):
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = visivel
    caminho = get_planilha_path("Ensaio_001.xlsm")
    wb = excel.Workbooks.Open(caminho)
    return excel, wb


def obter_id_por_nome(tabela, campo_nome, valor_nome):
    if not valor_nome:
        return None
    conn = sqlite3.connect(get_database_path())
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM {tabela} WHERE {campo_nome} = ?", (valor_nome,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def carregar_aba_procedimentos(ws):
    """Sincroniza Tbl_Procedim → aba Proc_Asfalto"""
    conn = sqlite3.connect(get_database_path())
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tbl_Procedim")
    colunas = [desc[0] for desc in cur.description]
    dados = cur.fetchall()
    ws.Cells.ClearContents()

    # Cabeçalho
    for j, col in enumerate(colunas, start=1):
        ws.Cells(1, j).Value = col

    # Dados
    for i, linha in enumerate(dados, start=2):
        for j, valor in enumerate(linha, start=1):
            ws.Cells(i, j).Value = valor
    conn.close()


def carregar_aba_projetos(ws):
    """Sincroniza Tbl_Projeto → aba Projeto_Asfalto"""
    conn = sqlite3.connect(get_database_path())
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tbl_Projeto")
    colunas = [desc[0] for desc in cur.description]
    dados = cur.fetchall()
    ws.Cells.ClearContents()

    for j, col in enumerate(colunas, start=1):
        ws.Cells(1, j).Value = col

    for i, linha in enumerate(dados, start=2):
        for j, valor in enumerate(linha, start=1):
            ws.Cells(i, j).Value = valor
    conn.close()


def sincronizar_tabelas_normativas():
    """Sincroniza Tbl_Procedim e Tbl_Projeto nas abas correspondentes"""
    excel, wb = abrir_excel(visivel=False)
    try:
        carregar_aba_procedimentos(wb.Worksheets("Proc_Asfalto"))
        carregar_aba_projetos(wb.Worksheets("Projeto_Asfalto"))
        wb.Save()
    finally:
        wb.Close(SaveChanges=True)
        excel.Quit()


# --------------------------
# 🔹 CRUD principal
# --------------------------

def ler_dados_planilha(ws):
    """Lê os dados digitados na aba Form_001 (ignora células de fórmula)."""
    dados = {}
    for celula, info in CELULAS_MAPEADAS.items():
        if celula in CELULAS_COM_FORMULAS:
            continue  # não salvar fórmulas
        valor = ws.Range(celula).Value
        dados[info["campo"]] = valor
    return dados


def salvar_registro():
    """Insere novo registro em Tbl_Ensaio_001"""
    excel, wb = abrir_excel(visivel=False)
    ws = wb.Worksheets("Form_001")
    dados = ler_dados_planilha(ws)

    # Relacionamentos automáticos
    id_projeto = obter_id_por_nome(
        RELACIONAMENTOS["id_projeto"]["tabela_referencia"],
        RELACIONAMENTOS["id_projeto"]["campo_referencia"],
        ws.Range(RELACIONAMENTOS["id_projeto"]["celula_origem"]).Value
    )
    id_procedimento = obter_id_por_nome(
        RELACIONAMENTOS["id_procedimento"]["tabela_referencia"],
        RELACIONAMENTOS["id_procedimento"]["campo_referencia"],
        ws.Range(RELACIONAMENTOS["id_procedimento"]["celula_origem"]).Value
    )

    dados["id_projeto"] = id_projeto
    dados["id_procedimento"] = id_procedimento

    conn = sqlite3.connect(get_database_path())
    cur = conn.cursor()

    campos = ", ".join(dados.keys())
    placeholders = ", ".join(["?" for _ in dados])
    cur.execute(f"INSERT INTO {TABELA_ENSAIO} ({campos}) VALUES ({placeholders})", tuple(dados.values()))
    conn.commit()
    conn.close()
    wb.Close(SaveChanges=False)
    excel.Quit()


def editar_registro(id_registro):
    """Atualiza um registro existente"""
    excel, wb = abrir_excel(visivel=False)
    ws = wb.Worksheets("Form_001")
    dados = ler_dados_planilha(ws)

    conn = sqlite3.connect(get_database_path())
    cur = conn.cursor()

    set_clause = ", ".join([f"{campo} = ?" for campo in dados.keys()])
    valores = list(dados.values()) + [id_registro]
    cur.execute(f"UPDATE {TABELA_ENSAIO} SET {set_clause} WHERE id = ?", valores)
    conn.commit()
    conn.close()
    wb.Close(SaveChanges=False)
    excel.Quit()


def excluir_registro(id_registro):
    """Remove um registro pelo ID"""
    conn = sqlite3.connect(get_database_path())
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {TABELA_ENSAIO} WHERE id = ?", (id_registro,))
    conn.commit()
    conn.close()

def carregar_registro(id_registro):
    """Carrega um registro do banco para a planilha, sem sobrescrever células com fórmulas."""
    excel, wb = abrir_excel(visivel=False)
    ws = wb.Worksheets("Form_001")

    conn = sqlite3.connect(get_database_path())
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {TABELA_ENSAIO} WHERE id = ?", (id_registro,))
    row = cur.fetchone()
    if not row:
        print("Registro não encontrado.")
        wb.Close(SaveChanges=False)
        excel.Quit()
        return

    colunas = [desc[0] for desc in cur.description]
    dados = dict(zip(colunas, row))

    for celula, info in CELULAS_MAPEADAS.items():
        if celula in CELULAS_COM_FORMULAS:
            continue  # não sobrescrever células com fórmulas
        campo = info["campo"]
        if campo in dados:
            ws.Range(celula).Value = dados[campo]

    wb.Save()
    wb.Close()
    excel.Quit()
    conn.close()

def proximo_registro(id_atual):
    conn = sqlite3.connect(get_database_path())
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM {TABELA_ENSAIO} WHERE id > ? ORDER BY id ASC LIMIT 1", (id_atual,))
    row = cur.fetchone()
    conn.close()
    if row:
        carregar_registro(row[0])
    else:
        print("⚠️ Já está no último registro.")

def registro_anterior(id_atual):
    conn = sqlite3.connect(get_database_path())
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM {TABELA_ENSAIO} WHERE id < ? ORDER BY id DESC LIMIT 1", (id_atual,))
    row = cur.fetchone()
    conn.close()
    if row:
        carregar_registro(row[0])
    else:
        print("⚠️ Já está no primeiro registro.")


# --------------------------
# 🔹 Execução direta via VBA
# --------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python sync_ensaio_001.py [acao] [id]")
        sys.exit(1)

    acao = sys.argv[1]

    if acao == "sincronizar":
        sincronizar_tabelas_normativas()
    elif acao == "salvar":
        salvar_registro()
    elif acao == "editar" and len(sys.argv) > 2:
        editar_registro(int(sys.argv[2]))
    elif acao == "excluir" and len(sys.argv) > 2:
        excluir_registro(int(sys.argv[2]))
    elif acao == "carregar" and len(sys.argv) > 2:
        carregar_registro(int(sys.argv[2]))
    elif acao == "proximo" and len(sys.argv) > 2:
        proximo_registro(int(sys.argv[2]))
    elif acao == "anterior" and len(sys.argv) > 2:
        registro_anterior(int(sys.argv[2]))