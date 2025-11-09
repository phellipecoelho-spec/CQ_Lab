# ui/projeto_ui.py
import customtkinter as ctk
from utils.db_manager import inserir_projeto
from typing import Dict, Any

class ProjetoUI:
    def __init__(self, master):
        self.master = master
        self.window = ctk.CTkToplevel(master)
        self.window.title("Cadastro - Tbl_Projeto (Parâmetros de Projeto)")
        # definir tamanho e centralizar
        width = 850
        height = 700
        self.window.geometry(f"{width}x{height}")
        self.window.update_idletasks()
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

        # Usar um frame rolável para conteúdos longos
        self.entries = {}
        self.scroll = ctk.CTkScrollableFrame(self.window, width=680, height=680)
        self.scroll.pack(padx=10, pady=10, fill="both", expand=True)

        # Frame Dados do Projeto
        proj_label = ctk.CTkLabel(self.scroll, text="Dados do Projeto", font=("Arial", 14, "bold"))
        proj_label.pack(padx=6, pady=(6, 0), anchor="w")
        frame_proj = ctk.CTkFrame(self.scroll, width=660, height=400)
        frame_proj.pack(padx=6, pady=(0, 6), fill="x")
        frame_proj.pack_propagate(False)

        # Campo adicional: Nome do Projeto (coluna PROJ)
        self._add_label_entry("PROJ", "Nome do Projeto", parent=frame_proj)

        # Colocar três campos de teor lado a lado: ótimo, mínimo e máximo
        frame_teores = ctk.CTkFrame(frame_proj)
        frame_teores.pack(fill="x", pady=4, padx=6)

        # Rótulo alinhado lateralmente como os demais campos
        lbl_teor = ctk.CTkLabel(frame_teores, text="Teor (Ótimo / Mín / Máx)", width=220, anchor="w")
        lbl_teor.pack(side="left", padx=6)

        # Container para as três entradas — ocupará o espaço restante e distribuirá igualmente
        entries_container = ctk.CTkFrame(frame_teores)
        entries_container.pack(side="left", fill="x", expand=True, padx=6)

        # Usar grid dentro do container e configurar pesos iguais para colunas
        entries_container.grid_columnconfigure(0, weight=1)
        entries_container.grid_columnconfigure(1, weight=1)
        entries_container.grid_columnconfigure(2, weight=1)

        entry_teor_otimo = ctk.CTkEntry(entries_container, placeholder_text="Ótimo (%)")
        entry_teor_otimo.grid(row=0, column=0, sticky="ew", padx=(0,6))
        self.entries["Teor_otimo"] = entry_teor_otimo

        entry_teor_min = ctk.CTkEntry(entries_container, placeholder_text="Mínimo (%)")
        entry_teor_min.grid(row=0, column=1, sticky="ew", padx=(0,6))
        self.entries["Teor_minimo"] = entry_teor_min

        entry_teor_max = ctk.CTkEntry(entries_container, placeholder_text="Máximo (%)")
        entry_teor_max.grid(row=0, column=2, sticky="ew")
        self.entries["Teor_maximo"] = entry_teor_max

        campos = [
            ("Fx_gran_trabalho", "Faixa granulométrica de trabalho"),
            ("VAM", "VAM (%)"),
            ("RBV", "RBV"),
            ("VV", "VV"),
            ("Estabilidade", "Estabilidade"),
            ("Fluencia", "Fluência"),
            ("Densidade_aparente", "Densidade aparente"),
            ("DUI", "DUI"),
            ("Observacoes", "Observações")
        ]

        for col, label in campos:
            self._add_label_entry(col, label, parent=frame_proj)

        # Frame Faixa de Especificação (peneiras)
        faixa_label = ctk.CTkLabel(self.scroll, text="Faixa de Trabalho de Projeto", font=("Arial", 14, "bold"))
        faixa_label.pack(padx=6, pady=(6, 0), anchor="w")
        frame_peneiras = ctk.CTkFrame(self.scroll, width=640, height=320)
        frame_peneiras.pack(padx=6, pady=(0, 6), fill="x")
        frame_peneiras.pack_propagate(False)

        headers = ["Peneira", "Peneira (pol.)", "Abertura (mm)", "Faixa mín. (%)", "Faixa máx. (%)"]
        for j, h in enumerate(headers):
            lbl = ctk.CTkLabel(frame_peneiras, text=h, width=110)
            lbl.grid(row=0, column=j, padx=4, pady=2)

        for i in range(1, 21):
            ctk.CTkLabel(frame_peneiras, text=f"Peneira {i}").grid(row=i, column=0, padx=4, pady=2)
            self._add_table_entry(f"Pen_{i:02d}", f"Pen_{i:02d}", frame_peneiras, i, 1)
            self._add_table_entry(f"Abert_Pen_{i:02d}", f"Abert_Pen_{i:02d}", frame_peneiras, i, 2)
            self._add_table_entry(f"Fx_min_Pen_{i:02d}", f"Fx_min_Pen_{i:02d}", frame_peneiras, i, 3)
            self._add_table_entry(f"Fx_max_Pen_{i:02d}", f"Fx_max_Pen_{i:02d}", frame_peneiras, i, 4)

        # Botões
        btn_frame = ctk.CTkFrame(self.scroll)
        btn_frame.pack(pady=8)

        self.btn_salvar = ctk.CTkButton(btn_frame, text="Salvar Projeto", command=self.salvar)
        self.btn_salvar.grid(row=0, column=0, padx=6)

        self.btn_limpar = ctk.CTkButton(btn_frame, text="Limpar", command=self.limpar)
        self.btn_limpar.grid(row=0, column=1, padx=6)

        self.label_status = ctk.CTkLabel(self.scroll, text="")
        self.label_status.pack(pady=6)

    def _add_label_entry(self, col_name: str, label_text: str):
        # backward-compatible: accept parent via keyword if passed
        # new signature: _add_label_entry(col_name, label_text, parent=None)
        # But keep this wrapper for older code paths
        parent = getattr(self, 'frame', None)
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=4)

        lbl = ctk.CTkLabel(frame, text=label_text, width=220, anchor="w")
        lbl.pack(side="left", padx=6)

        entry = ctk.CTkEntry(frame, placeholder_text=label_text)
        entry.pack(side="left", fill="x", expand=True, padx=6)
        self.entries[col_name] = entry

    def _add_label_entry(self, col_name: str, label_text: str, parent=None):
        # new implementation that accepts parent; keeps compatibility
        if parent is None:
            parent = getattr(self, 'scroll', None) or self.window
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=4, padx=6)

        lbl = ctk.CTkLabel(frame, text=label_text, width=220, anchor="w")
        lbl.pack(side="left", padx=6)

        entry = ctk.CTkEntry(frame, placeholder_text=label_text)
        entry.pack(side="left", fill="x", expand=True, padx=6)
        self.entries[col_name] = entry

    def _add_table_entry(self, col_name: str, label_text: str, parent, row, col):
        entry = ctk.CTkEntry(parent, width=110, placeholder_text=label_text)
        entry.grid(row=row, column=col, padx=4, pady=2)
        self.entries[col_name] = entry

    def salvar(self):
        dados: Dict[str, Any] = {}
        for col, widget in self.entries.items():
            val = widget.get().strip()
            if val == "":
                dados[col] = None
            else:
                # converter onde apropriado
                if col in ("Fx_gran_trabalho", "Observacoes"):
                    dados[col] = val
                else:
                    try:
                        dados[col] = float(val.replace(",", "."))
                    except Exception:
                        dados[col] = val

        try:
            new_id = inserir_projeto(dados)
            self.label_status.configure(text=f"Projeto salvo com ID_PROJ = {new_id}", text_color="green")
        except Exception as e:
            self.label_status.configure(text=f"Erro ao salvar: {e}", text_color="red")

    def limpar(self):
        for widget in self.entries.values():
            widget.delete(0, "end")
        self.label_status.configure(text="")
