# scripts/ensaio_001/config_ensaio_001.py

"""
Configuração de mapeamento entre células da planilha Ensaio_001.xlsm
e os campos da tabela Tbl_Ensaio_001 no SQLite.
Inclui vinculação com Tbl_Procedim e Tbl_Projeto.
"""

from typing import Dict

# --- Nome da tabela correspondente ---
TABELA_ENSAIO = "Tbl_Ensaio_001"

# --- Chaves de relacionamento com outras tabelas ---
RELACIONAMENTOS = {
    "id_projeto": {
        "tabela_referencia": "Tbl_Projeto",
        "campo_referencia": "PROJ",      # Nome do projeto (texto)
        "celula_origem": "B9",           # Célula da planilha onde o usuário escolhe o projeto
    },
    "id_procedimento": {
        "tabela_referencia": "Tbl_Procedim",
        "campo_referencia": "PROC",      # Nome do procedimento (texto)
        "celula_origem": "D11",          # Célula da planilha onde o usuário escolhe o procedimento
    }
}

CELULAS_COM_FORMULAS = [
    "M21", "M22",
    *[f"F{i}" for i in range(15, 36)],
    "M63", "M68",
    "H63", "H65", "H66", "H67", "H68",
    "H72", "H74", "H77"
]

# --- Mapeamento de células e tipos de dados ---
CELULAS_MAPEADAS: dict[str, dict[str, str]] = {
    # --- Cabeçalho ---
    "B7":  {"campo": "Rodovia", "tipo": "TEXT"},
    "D7":  {"campo": "Trecho", "tipo": "TEXT"},
    "H7":  {"campo": "Sub_trecho", "tipo": "TEXT"},
    "J7":  {"campo": "Protocolo", "tipo": "INTEGER"},
    "K7":  {"campo": "id", "tipo": "INTEGER"},
    "L7":  {"campo": "Hora", "tipo": "TEXT"},

    "B9":  {"campo": "Projeto", "tipo": "TEXT"},
    "D9":  {"campo": "Material", "tipo": "TEXT"},
    "F9":  {"campo": "Usina", "tipo": "TEXT"},
    "H9":  {"campo": "Local", "tipo": "TEXT"},
    "J9":  {"campo": "Data_rec", "tipo": "DATE"},
    "L9":  {"campo": "Data_ensaio", "tipo": "DATE"},

    "B11": {"campo": "Placa", "tipo": "TEXT"},
    "D11": {"campo": "Procedimento", "tipo": "TEXT"},
    "G11": {"campo": "Obra", "tipo": "TEXT"},
    "I11": {"campo": "Clima", "tipo": "TEXT"},
    "L11": {"campo": "Operador", "tipo": "TEXT"},
    "K12": {"campo": "Tipo_ext", "tipo": "TEXT"},

    # --- Dados físicos ---
    "M15": {"campo": "Temp", "tipo": "REAL"},
    "M16": {"campo": "Am_ligante", "tipo": "REAL"},
    "M17": {"campo": "Am_Lavada", "tipo": "REAL"},
    "M20": {"campo": "Fator_correção", "tipo": "REAL"},
    "M21": {"campo": "Teor", "tipo": "REAL"},
    "M22": {"campo": "Filler", "tipo": "REAL"},

    # --- Retenção e percentuais das peneiras ---
    **{f"D{linha}": {"campo": f"Ret_Pen{i}", "tipo": "REAL"} for i, linha in enumerate(range(15, 35), start=1)},
    **{f"F{linha}": {"campo": f"Perc_Pen{i}", "tipo": "REAL"} for i, linha in enumerate(range(15, 35), start=1)},

    # --- Ensaio Rice ---
    "M59": {"campo": "Rice_1", "tipo": "REAL"},
    "M60": {"campo": "Rice_2", "tipo": "REAL"},
    "M61": {"campo": "Rice_3", "tipo": "REAL"},
    "M63": {"campo": "Dens_Rice", "tipo": "REAL"},

    # --- Umidade ---
    "M65": {"campo": "Umid_1", "tipo": "REAL"},
    "M66": {"campo": "Umid_2", "tipo": "REAL"},
    "M68": {"campo": "Teor_real", "tipo": "REAL"},

    # --- Corpos de prova ---
    "E59": {"campo": "CpAr_1", "tipo": "REAL"},
    "F59": {"campo": "CpAr_2", "tipo": "REAL"},
    "G59": {"campo": "CpAr_3", "tipo": "REAL"},

    "E60": {"campo": "CpIm_1", "tipo": "REAL"},
    "F60": {"campo": "CpIm_2", "tipo": "REAL"},
    "G60": {"campo": "CpIm_3", "tipo": "REAL"},

    "E61": {"campo": "CpSa_1", "tipo": "REAL"},
    "F61": {"campo": "CpSa_2", "tipo": "REAL"},
    "G61": {"campo": "CpSa_3", "tipo": "REAL"},

    # --- Cálculos ---
    "H63": {"campo": "Dens_Apar", "tipo": "REAL"},
    "H65": {"campo": "Vazios", "tipo": "REAL"},
    "H66": {"campo": "VCB", "tipo": "REAL"},
    "H67": {"campo": "VAM", "tipo": "REAL"},
    "H68": {"campo": "RBV", "tipo": "REAL"},

    # --- Resistência e estabilidade ---
    "E69": {"campo": "Alt_Cp1", "tipo": "REAL"},
    "F69": {"campo": "Alt_Cp2", "tipo": "REAL"},
    "G69": {"campo": "Alt_Cp3", "tipo": "REAL"},
    "E70": {"campo": "Con_Prensa", "tipo": "REAL"},

    "E71": {"campo": "RT_Cp1", "tipo": "INTEGER"},
    "F71": {"campo": "RT_Cp2", "tipo": "INTEGER"},
    "G71": {"campo": "RT_Cp3", "tipo": "INTEGER"},
    "H72": {"campo": "RTCD", "tipo": "REAL"},

    "E73": {"campo": "Est_Cp1", "tipo": "INTEGER"},
    "F73": {"campo": "Est_Cp2", "tipo": "INTEGER"},
    "G73": {"campo": "Est_Cp3", "tipo": "INTEGER"},
    "H74": {"campo": "Estabilidade", "tipo": "REAL"},

    # --- Fluência ---
    "E75": {"campo": "Fl_Cp1", "tipo": "REAL"},
    "F75": {"campo": "Fl_Cp2", "tipo": "REAL"},
    "G75": {"campo": "Fl_Cp3", "tipo": "REAL"},
    "E76": {"campo": "Fl_Cp4", "tipo": "REAL"},
    "F76": {"campo": "Fl_Cp5", "tipo": "REAL"},
    "G76": {"campo": "Fl_Cp6", "tipo": "REAL"},
    "H77": {"campo": "Fluencia", "tipo": "REAL"},

    # --- Assinaturas ---
    "C79": {"campo": "Ass_1", "tipo": "TEXT"},
    "I79": {"campo": "Ass_2", "tipo": "TEXT"},
}

# --- Abas e intervalos ---
ABA_FORM = "Form_001"
ABA_PROC = "Proc_Asfalto"
ABA_PROJ = "Projeto_Asfalto"
#RANGE_VISUALIZACAO = "A1:N81"
