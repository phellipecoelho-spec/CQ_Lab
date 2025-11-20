# ui/projeto_ui.py
import customtkinter as ctk
import tkinter as tk
from utils.db_manager import (
    inserir_projeto,
    existe_projeto,
    get_projeto_por_id,
    atualizar_projeto,
    excluir_projeto,
    get_all_projetos,
    get_all_procedim,
    get_procedim_por_proc,
)
from typing import Dict, Any

class ProjetoUI:
    def __init__(self, master):
        self.master = master
        self.window = ctk.CTkToplevel(master)
        self.window.title("Cadastro - Tbl_Projeto (Parâmetros de Projeto)")
        # definir tamanho e centralizar
        width = 1100
        height = 750
        self.window.geometry(f"{width}x{height}")
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

        # Dar foco à janela
        try:
            self.window.transient(master)
            self.window.grab_set()
            self.window.focus_force()
        except Exception:
            pass

        # Frame rolável
        self.entries = {}
        self.scroll = ctk.CTkScrollableFrame(self.window, width=680, height=680)
        self.scroll.pack(padx=10, pady=10, fill="both", expand=True)

        # Dados do Projeto
        proj_label = ctk.CTkLabel(self.scroll, text="Dados do Projeto", font=("Arial", 14, "bold"))
        proj_label.pack(padx=6, pady=(6, 0), anchor="w")
        frame_proj = ctk.CTkFrame(self.scroll, width=660, height=400)
        frame_proj.pack(padx=6, pady=(0, 6), fill="x")
        frame_proj.pack_propagate(False)

        # Campo Nome do Projeto
        self._add_label_entry("PROJ", "Nome do Projeto", parent=frame_proj)

        # Campos de Teor
        frame_teores = ctk.CTkFrame(frame_proj)
        frame_teores.pack(fill="x", pady=4, padx=6)

        lbl_teor = ctk.CTkLabel(frame_teores, text="Teor (Ótimo / Mín / Máx)", width=220, anchor="w")
        lbl_teor.pack(side="left", padx=6)

        entries_container = ctk.CTkFrame(frame_teores)
        entries_container.pack(side="left", fill="x", expand=True, padx=6)

        entries_container.grid_columnconfigure(0, weight=1)
        entries_container.grid_columnconfigure(1, weight=1)
        entries_container.grid_columnconfigure(2, weight=1)

        entry_teor_otimo = ctk.CTkEntry(entries_container, placeholder_text="Ótimo (%)")
        entry_teor_otimo.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.entries["Teor_otimo"] = entry_teor_otimo

        entry_teor_min = ctk.CTkEntry(entries_container, placeholder_text="Mínimo (%)")
        entry_teor_min.grid(row=0, column=1, sticky="ew", padx=(0, 6))
        self.entries["Teor_minimo"] = entry_teor_min

        entry_teor_max = ctk.CTkEntry(entries_container, placeholder_text="Máximo (%)")
        entry_teor_max.grid(row=0, column=2, sticky="ew")
        self.entries["Teor_maximo"] = entry_teor_max

        # Demais campos
        campos = [
            ("Fx_gran_trabalho", "Faixa granulométrica de trabalho"),
            ("VAM", "VAM (%)"),
            ("RBV", "RBV"),
            ("VV", "VV"),
            ("Estabilidade", "Estabilidade"),
            ("Fluencia", "Fluência"),
            ("Densidade_aparente", "Densidade aparente"),
            ("DUI", "DUI"),
            ("Observacoes", "Observações"),
        ]

        for col, label in campos:
            self._add_label_entry(col, label, parent=frame_proj)

        # Faixa de Especificação (peneiras)
        faixa_label = ctk.CTkLabel(self.scroll, text="Faixa de Trabalho de Projeto", font=("Arial", 14, "bold"))
        faixa_label.pack(padx=6, pady=(6, 0), anchor="w")
        # Contêiner que agrupa a listbox de procedimentos e a tabela de peneiras
        container_proc = ctk.CTkFrame(self.scroll)
        container_proc.pack(padx=6, pady=(0, 6), fill="x")

        # Listbox de procedimentos (PROC) - usando tkinter.Listbox (CTk não tem Listbox)
        listbox_frame = ctk.CTkFrame(container_proc)
        listbox_frame.pack(side="left", padx=6, pady=6)

        self.listbox_procedim = tk.Listbox(
            listbox_frame,
            width=20,
            height=2,
            exportselection=False,
            font=("Arial", 12)
        )
        self.listbox_procedim.pack(side="left", fill="y")

        # Scrollbar lateral
        scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Vincular scrollbar
        self.listbox_procedim.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox_procedim.yview)

        # Bind de seleção
        self.listbox_procedim.bind("<<ListboxSelect>>", self._on_select_procedim)

        # Frame das peneiras (lado direito)
        frame_peneiras = ctk.CTkFrame(container_proc, width=640, height=320)
        frame_peneiras.pack(side="right", fill="both", expand=True, padx=6, pady=6)
        frame_peneiras.pack_propagate(False)

        # Carrega procedimentos na listbox
        self._carregar_procedimentos()

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

        # Botões de ação
        btn_frame = ctk.CTkFrame(self.scroll)
        btn_frame.pack(pady=8)

        self.btn_salvar = ctk.CTkButton(btn_frame, text="Salvar Projeto", command=self.salvar)
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

        # Expandir colunas para distribuir uniformemente e garantir que todos os botões estejam visíveis
        for i in range(6):
            btn_frame.grid_columnconfigure(i, weight=1)
        # Controle interno
        self._ids = []
        self._pos = -1
        self._editando_id = None
        self._ultimo_salvo = None
        # Armazena o REG_NORMA do procedimento selecionado
        self._selected_reg_norma = None
        self._carregar_ids()

        self.label_status = ctk.CTkLabel(self.scroll, text="")
        self.label_status.pack(pady=6)

    # ---------- Helper methods ----------
    def _add_label_entry(self, col_name: str, label_text: str, parent=None):
        if parent is None:
            parent = getattr(self, "scroll", None) or self.window
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

    # ---------- Procedimento handling ----------
    def _carregar_procedimentos(self):
        """Carrega todos os procedimentos (PROC) na listbox."""
        procedimentos = get_all_procedim()
        self.listbox_procedim.delete(0, "end")
        for proc in procedimentos:
            self.listbox_procedim.insert("end", proc.get("PROC"))

    def _on_select_procedim(self, event=None):
        """Preenche as colunas de peneira com valores do procedimento selecionado."""
        # Para compatibilidade com tk.Listbox: usar curselection()
        selection = self.listbox_procedim.curselection()
        if not selection:
            return
        idx = selection[0]
        try:
            proc = self.listbox_procedim.get(idx)
        except Exception:
            return
        registro = get_procedim_por_proc(proc)
        if not registro:
            return
        # Armazena REG_NORMA do procedimento selecionado
        self._selected_reg_norma = registro.get("REG_NORMA")
        # Preencher campo Fx_gran_trabalho com o valor do PROC
        if "Fx_gran_trabalho" in self.entries:
            self.entries["Fx_gran_trabalho"].delete(0, "end")
            self.entries["Fx_gran_trabalho"].insert(0, str(registro.get("PROC", "")))
        # Preencher Pen_XX e Abert_Pen_XX
        for i in range(1, 21):
            pen_key = f"Pen_{i:02d}"
            abrir_key = f"Abert_Pen_{i:02d}"
            pen_val = registro.get(pen_key)
            abrir_val = registro.get(abrir_key)
            if pen_val is not None:
                self.entries[pen_key].delete(0, "end")
                self.entries[pen_key].insert(0, str(pen_val))
            if abrir_val is not None:
                self.entries[abrir_key].delete(0, "end")
                self.entries[abrir_key].insert(0, str(abrir_val))

    def _carregar_ids(self):
        """Carrega todos os IDs de projetos e define a posição atual."""
        projetos = get_all_projetos()
        self._ids = [p["ID_PROJ"] for p in projetos]
        self._pos = 0 if self._ids else -1

    def _carregar_registro(self, proj_id):
        """Carrega os dados de um projeto nas entry widgets."""
        registro = get_projeto_por_id(proj_id)
        if not registro:
            return
        # Carrega REG_NORMA para uso ao salvar
        self._selected_reg_norma = registro.get("REG_NORMA")
        for col, widget in self.entries.items():
            valor = registro.get(col)
            widget.delete(0, "end")
            if valor is not None:
                widget.insert(0, str(valor))

    # ---------- CRUD actions ----------
    def salvar(self):
        """Salva o registro atual, evitando duplicação imediata."""
        dados: Dict[str, Any] = {}
        for col, widget in self.entries.items():
            val = widget.get().strip()
            if val == "":
                dados[col] = None
            else:
                if col in ("Fx_gran_trabalho", "Observacoes"):
                    dados[col] = val
                else:
                    try:
                        dados[col] = float(val.replace(",", "."))
                    except Exception:
                        dados[col] = val

        # Checa duplicação do último registro salvo
        if self._ultimo_salvo is not None and dados == self._ultimo_salvo:
            self.label_status.configure(
                text="Registro já salvo recentemente – nenhuma nova inserção.", text_color="orange"
            )
            return

        # Verificar se já existe registro idêntico no banco
        if existe_projeto(dados):
            self.label_status.configure(
                text="Registro já existente – nenhuma inserção.", text_color="orange"
            )
            return
        # Inserir REG_NORMA associado ao procedimento selecionado, se houver
        dados["REG_NORMA"] = self._selected_reg_norma
        try:
            new_id = inserir_projeto(dados)
            self._ultimo_salvo = dados.copy()
            self.label_status.configure(
                text=f"Projeto salvo com ID_PROJ = {new_id}", text_color="green"
            )
            # Recarrega IDs para navegação
            self._carregar_ids()
            # Desabilita o botão Salvar até que haja nova alteração
            self.btn_salvar.configure(state="disabled")
        except Exception as e:
            self.label_status.configure(text=f"Erro ao salvar: {e}", text_color="red")

    def limpar(self):
        for widget in self.entries.values():
            widget.delete(0, "end")
        self.label_status.configure(text="")
        self._editando_id = None
        self._pos = -1
        # Reabilita o botão Salvar após limpeza
        self.btn_salvar.configure(state="normal")

    def editar(self):
        """Entra em modo edição para o registro atual."""
        if self._pos == -1 or not self._ids:
            self.label_status.configure(text="Nenhum registro para editar", text_color="orange")
            return
        proj_id = self._ids[self._pos]
        self._carregar_registro(proj_id)
        self._editando_id = proj_id
        self.label_status.configure(text=f"Edição do registro ID {proj_id}", text_color="blue")
        # Reabilita o botão Salvar para permitir gravação da edição
        self.btn_salvar.configure(state="normal")

    def excluir(self):
        """Remove o registro atual do banco de dados."""
        if self._pos == -1 or not self._ids:
            self.label_status.configure(text="Nenhum registro para excluir", text_color="orange")
            return
        proj_id = self._ids[self._pos]
        excluir_projeto(proj_id)
        self.label_status.configure(text=f"Registro ID {proj_id} excluído", text_color="green")
        self._carregar_ids()
        self.limpar()
        # Reabilita o botão Salvar após exclusão
        self.btn_salvar.configure(state="normal")

    def anterior(self):
        """Navega para o registro anterior."""
        if not self._ids:
            return
        self._pos = (self._pos - 1) % len(self._ids)
        self._carregar_registro(self._ids[self._pos])
        # Reabilita o botão Salvar ao navegar
        self.btn_salvar.configure(state="normal")

    def proximo(self):
        """Navega para o próximo registro."""
        if not self._ids:
            return
        self._pos = (self._pos + 1) % len(self._ids)
        self._carregar_registro(self._ids[self._pos])
        # Reabilita o botão Salvar ao navegar
        self.btn_salvar.configure(state="normal")
