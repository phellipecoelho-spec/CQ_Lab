# ui/procedim_ui.py
import customtkinter as ctk
from utils.db_manager import inserir_procedim, atualizar_procedim, excluir_procedim, existe_procedim, get_procedim_por_id, get_all_procedim
from typing import Dict, Any

class ProcedimUI:
    def __init__(self, master):
        self.master = master

        self.window = ctk.CTkToplevel(master)
        self.window.title("Cadastro - Tbl_Procedim (Parâmetros Normativos)")
        self.window.geometry("1100x750")

        # Centralizar the window on open
        self.window.update_idletasks()
        width = 1100
        height = 700
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

        # Fazer a janela ficar à frente e receber foco
        try:
            self.window.transient(master)
            self.window.grab_set()
            self.window.focus_force()
        except Exception:
            pass

        self.entries = {}

        # Adiciona um frame rolável para todo o conteúdo
        self.scroll = ctk.CTkScrollableFrame(self.window, width=1080, height=700)
        self.scroll.pack(padx=0, pady=0, fill="both", expand=True)

        # Frame Procedimento (simulando LabelFrame)
        proc_label = ctk.CTkLabel(self.scroll, text="Procedimento", font=("Arial", 14, "bold"))
        proc_label.pack(padx=10, pady=(10, 0), anchor="w")
        frame_proc = ctk.CTkFrame(self.scroll, width=1050, height=70)
        frame_proc.pack(padx=10, pady=(0, 4), fill="x")
        frame_proc.pack_propagate(False)
        self._add_label_entry("PROC", "Procedimento (PROC)", parent=frame_proc)

        # Frame Faixa de Especificação (simulando LabelFrame)
        faixa_label = ctk.CTkLabel(self.scroll, text="Faixa de Especificação", font=("Arial", 14, "bold"))
        faixa_label.pack(padx=10, pady=(4, 0), anchor="w")
        frame_peneiras = ctk.CTkFrame(self.scroll, width=1050, height=420)
        frame_peneiras.pack(padx=10, pady=(0, 4), fill="x")
        frame_peneiras.pack_propagate(False)

        # Cabeçalho da tabela
        headers = ["Peneira", "Peneira (pol.)", "Abertura (mm)", "Faixa mín. (%)", "Faixa máx. (%)"]
        for j, h in enumerate(headers):
            lbl = ctk.CTkLabel(frame_peneiras, text=h, font=("Arial", 12, "bold"), width=110)
            lbl.grid(row=0, column=j, padx=2, pady=2)

        for i in range(1, 21):
            peneira_lbl = ctk.CTkLabel(frame_peneiras, text=f"Peneira {i}", width=110)
            peneira_lbl.grid(row=i, column=0, padx=2, pady=2)
            abert_col = f"Abert_Pen_{i:02d}"
            fxmin_col = f"Fx_min_Pen_{i:02d}"
            fxmax_col = f"Fx_max_Pen_{i:02d}"
            pen_col = f"Pen_{i:02d}"
            self._add_table_entry(pen_col, f"Pen_{i:02d}", frame_peneiras, i, 1)
            self._add_table_entry(abert_col, f"Abertura Pen_{i:02d}", frame_peneiras, i, 2)
            self._add_table_entry(fxmin_col, f"Faixa Mín Pen_{i:02d}", frame_peneiras, i, 3)
            self._add_table_entry(fxmax_col, f"Faixa Máx Pen_{i:02d}", frame_peneiras, i, 4)

        # Frame Parâmetros de Volume e Resistência (simulando LabelFrame)
        param_label = ctk.CTkLabel(self.scroll, text="Parâmetros de Volume e Resistência", font=("Arial", 14, "bold"))
        param_label.pack(padx=10, pady=(4, 0), anchor="w")
        frame_param = ctk.CTkFrame(self.scroll, width=1050, height=180)
        frame_param.pack(padx=10, pady=(0, 4), fill="x")
        frame_param.pack_propagate(False)

        # Cabeçalho
        param_headers = ["", "Vol. Vazios (%)", "RBV (%)", "VAM (%)", "Filler/Asfalto (%)", "RTCD (mpa)", "DUI (%)", "Estabilidade (mpa)", "Fluência (mm)"]
        for j, h in enumerate(param_headers):
            lbl = ctk.CTkLabel(frame_param, text=h, font=("Arial", 12, "bold"), width=110)
            lbl.grid(row=0, column=j, padx=2, pady=2)

        # Linhas: Mínimo e Máximo
        param_map = [
            ("Mínimo", ["VV_min", "RBV_min", "VAM_min", "Filler_Asf_min", "RTCD_min", "DUI_min", "Estab_min", "Fluen_min"]),
            ("Máximo", ["VV_max", "RBV_max", None, "Filler_Asf_max", None, None, None, "Fluen_max"])
        ]
        for i, (rotulo, campos) in enumerate(param_map, 1):
            lbl = ctk.CTkLabel(frame_param, text=rotulo, width=110)
            lbl.grid(row=i, column=0, padx=2, pady=2)
            for j, col in enumerate(campos, 1):
                if col:
                    self._add_table_entry(col, col, frame_param, i, j)
                else:
                    ctk.CTkLabel(frame_param, text="-").grid(row=i, column=j, padx=2, pady=2)

        # Botões
        btn_frame = ctk.CTkFrame(self.scroll)
        btn_frame.pack(pady=8)

        self.btn_salvar = ctk.CTkButton(btn_frame, text="Salvar", command=self.salvar)
        self.btn_salvar.grid(row=0, column=0, padx=6)

        self.btn_limpar = ctk.CTkButton(btn_frame, text="Limpar", command=self.limpar)
        self.btn_limpar.grid(row=0, column=1, padx=6)

        self.btn_editar = ctk.CTkButton(btn_frame, text="Editar", command=self.editar)
        self.btn_editar.grid(row=0, column=2, padx=6)

        self.btn_excluir = ctk.CTkButton(btn_frame, text="Excluir", command=self.excluir)
        self.btn_excluir.grid(row=0, column=3, padx=6)

        self.btn_anterior = ctk.CTkButton(btn_frame, text="←", command=self.anterior)
        self.btn_anterior.grid(row=0, column=4, padx=6)

        self.btn_proximo = ctk.CTkButton(btn_frame, text="→", command=self.proximo)
        self.btn_proximo.grid(row=0, column=5, padx=6)

        self.label_status = ctk.CTkLabel(self.scroll, text="")
        self.label_status.pack(pady=6)

        # gerenciamento interno de navegação/edição
        self._ids = []
        self._pos = -1
        self._editando_id = None
        self._carregar_ids()

    def _add_label_entry(self, col_name: str, label_text: str, parent=None):
        if parent is None:
            parent = self.window
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=3, padx=6)

        lbl = ctk.CTkLabel(frame, text=label_text, width=200, anchor="w")
        lbl.pack(side="left", padx=6)

        entry = ctk.CTkEntry(frame, placeholder_text=label_text)
        entry.pack(side="left", fill="x", expand=True, padx=6)
        self.entries[col_name] = entry

    def _add_table_entry(self, col_name: str, label_text: str, parent, row, col):
        entry = ctk.CTkEntry(parent, width=110, placeholder_text=label_text)
        entry.grid(row=row, column=col, padx=2, pady=2)
        self.entries[col_name] = entry

    def salvar(self):
        # Coletar valores e converter números onde aplicável
        dados: Dict[str, Any] = {}
        for col, widget in self.entries.items():
            val = widget.get().strip()
            if val == "":
                dados[col] = None
            else:
                if col == "PROC":
                    dados[col] = val
                else:
                    try:
                        dados[col] = float(val.replace(",", "."))
                    except Exception:
                        dados[col] = val

        # Verificar duplicidade quando não estiver em modo edição
        if self._editando_id is None and existe_procedim(dados):
            self.label_status.configure(
                text="Registro duplicado – não foi inserido.",
                text_color="orange",
            )
            return

        try:
            if self._editando_id is not None:
                # Atualizar registro existente
                atualizar_procedim(self._editando_id, dados)
                self.label_status.configure(
                    text=f"Registro {self._editando_id} atualizado.", text_color="green"
                )
                self._editando_id = None
            else:
                # Inserir novo registro
                new_id = inserir_procedim(dados)
                self.label_status.configure(
                    text=f"Registro salvo com REG_NORMA = {new_id}", text_color="green"
                )
            # Recarregar lista de IDs e posicionamento
            self._carregar_ids()
        except Exception as e:
            self.label_status.configure(text=f"Erro ao salvar: {e}", text_color="red")

    def limpar(self):
        for widget in self.entries.values():
            widget.delete(0, "end")
        self.label_status.configure(text="")

        # Resetar navegação/edição
        self._pos = -1
        self._editando_id = None

    def editar(self):
        """Carrega o registro atual para edição."""
        if not self._ids or self._pos == -1:
            self.label_status.configure(text="Nenhum registro para editar.", text_color="red")
            return
        reg_id = self._ids[self._pos]
        registro = get_procedim_por_id(reg_id)
        if not registro:
            self.label_status.configure(text="Registro não encontrado.", text_color="red")
            return
        for col, widget in self.entries.items():
            val = registro.get(col)
            widget.delete(0, "end")
            if val is not None:
                widget.insert(0, str(val))
        self._editando_id = reg_id
        self.label_status.configure(text=f"Edição do registro {reg_id}", text_color="blue")

    def excluir(self):
        """Remove o registro atual."""
        if not self._ids or self._pos == -1:
            self.label_status.configure(text="Nenhum registro para excluir.", text_color="red")
            return
        reg_id = self._ids[self._pos]
        excluir_procedim(reg_id)
        self.label_status.configure(text=f"Registro {reg_id} excluído.", text_color="green")
        self._carregar_ids()

    def anterior(self):
        """Navega para o registro anterior."""
        if self._pos > 0:
            self._pos -= 1
            self._carregar_registro(self._ids[self._pos])

    def proximo(self):
        """Navega para o próximo registro."""
        if self._pos + 1 < len(self._ids):
            self._pos += 1
            self._carregar_registro(self._ids[self._pos])

    def _carregar_ids(self):
        """Carrega a lista de IDs existentes."""
        registros = get_all_procedim()
        self._ids = [r["REG_NORMA"] for r in registros]
        if self._ids:
            self._pos = 0
            self._carregar_registro(self._ids[0])
        else:
            self._pos = -1

    def _carregar_registro(self, reg_id: int):
        """Preenche as entrys com os dados do registro especificado."""
        registro = get_procedim_por_id(reg_id)
        if not registro:
            return
        for col, widget in self.entries.items():
            widget.delete(0, "end")
            val = registro.get(col)
            if val is not None:
                widget.insert(0, str(val))
        self.label_status.configure(text=f"Registro {reg_id} carregado.", text_color="green")
