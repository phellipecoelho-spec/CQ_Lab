# ui/asfalto_ui.py
import customtkinter as ctk
from ui.procedim_ui import ProcedimUI
from ui.projeto_ui import ProjetoUI
from utils.path_helper import get_planilha_path
import os


class AsfaltoUI:
    def __init__(self, master, usuario):
        self.master = master
        self.usuario = usuario

        # Frame principal centralizado
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(expand=True, fill="both")

        # Frame central para botões e label
        self.center_frame = ctk.CTkFrame(
            self.frame, width=380, height=320, corner_radius=16)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.center_frame.pack_propagate(False)

        self.label = ctk.CTkLabel(
            self.center_frame, text="Módulo Asfalto", font=("Arial", 18))
        self.label.pack(pady=(30, 20))

        self.btn_parametros = ctk.CTkButton(
            self.center_frame, text="Parâmetros Normativos", command=self.abrir_parametros, width=220)
        self.btn_parametros.pack(pady=8, padx=30)

        self.btn_parametros_projeto = ctk.CTkButton(
            self.center_frame, text="Parâmetros de Projeto", command=self.abrir_parametros_projeto, width=220)
        self.btn_parametros_projeto.pack(pady=8, padx=30)

        self.btn_ensaio001 = ctk.CTkButton(
            self.center_frame, text="Marshall Completo", command=self.abrir_ensaio_001, width=220)
        self.btn_ensaio001.pack(pady=8, padx=30)

        self.btn_voltar = ctk.CTkButton(
            self.center_frame, text="Voltar", command=self.voltar_menu, width=220)
        self.btn_voltar.pack(pady=18, padx=30)

        # Centralizar a janela principal ao abrir (caso seja uma janela Toplevel)
        if hasattr(master, 'geometry') and hasattr(master, 'winfo_screenwidth'):
            master.update_idletasks()
            width = 800
            height = 600
            x = (master.winfo_screenwidth() // 2) - (width // 2)
            y = (master.winfo_screenheight() // 2) - (height // 2)
            master.geometry(f"{width}x{height}+{x}+{y}")

    def abrir_parametros(self):
        ProcedimUI(self.master)

    def abrir_parametros_projeto(self):
        ProjetoUI(self.master)

    def abrir_ensaio_001(self):
        """
        Abre a planilha Ensaio_001.xlsm diretamente no Microsoft Excel.
        Corrige o problema de abertura duplicada e bloqueio.
        """
        caminho = get_planilha_path("Ensaio_001.xlsm", categoria="asfalto")

        if os.path.exists(caminho):
            try:
                import win32com.client

                # Preferimos criar uma nova instância isolada para controlar opções
                excel = None
                workbook = None
                try:
                    # Tentar reutilizar instância existente para evitar múltiplas janelas
                    excel = win32com.client.GetActiveObject(
                        "Excel.Application")
                except Exception:
                    excel = None

                # Configurar política de automação para permitir macros (definir antes de abrir)
                # msoAutomationSecurityLow = 1
                def _set_automation_low(app):
                    try:
                        app.AutomationSecurity = 1
                    except Exception:
                        pass

                # If no active Excel, create a new one
                if excel is None:
                    excel = win32com.client.DispatchEx('Excel.Application')
                    excel.Visible = True
                    _set_automation_low(excel)

                else:
                    # even for existing instance, try to lower AutomationSecurity temporarily
                    _set_automation_low(excel)

                # Suppress alerts while opening/adjusting
                try:
                    excel.DisplayAlerts = False
                except Exception:
                    pass

                # Antes de abrir, verificar se o workbook já está presente na instância do Excel
                workbook = None
                try:
                    for wb in excel.Workbooks:
                        try:
                            if os.path.abspath(getattr(wb, 'FullName', '')).lower() == os.path.abspath(caminho).lower():
                                workbook = wb
                                break
                        except Exception:
                            continue
                except Exception:
                    # Não conseguiu iterar Workbooks; continue para tentar abrir
                    workbook = None

                # Open workbook explicitly allowing edit and ignoring read-only recommended
                if workbook is None:
                    try:
                        workbook = excel.Workbooks.Open(os.path.abspath(
                            caminho), ReadOnly=False, IgnoreReadOnlyRecommended=True)
                    except Exception as open_err:
                        # If open fails, try to recover from Protected View windows
                        try:
                            # Attempt to see if the file is in Protected View and edit it
                            pv_count = 0
                            try:
                                pv_count = excel.ProtectedViewWindows.Count
                            except Exception:
                                pv_count = 0

                            edited = False
                            for i in range(1, pv_count + 1):
                                try:
                                    pv = excel.ProtectedViewWindows(i)
                                    src = getattr(pv, 'SourceName', '')
                                    if os.path.abspath(src).lower() == os.path.abspath(caminho).lower():
                                        # convert Protected View to normal workbook
                                        wb = pv.Edit()
                                        workbook = wb
                                        edited = True
                                        break
                                except Exception:
                                    continue

                            if not edited:
                                # As a last resort, try opening with fewer flags
                                workbook = excel.Workbooks.Open(
                                    os.path.abspath(caminho))
                        except Exception:
                            raise open_err

                # Garantir que o workbook não está marcado como somente leitura
                try:
                    if getattr(workbook, 'ReadOnly', False):
                        # tentar reabrir em modo editável
                        workbook.Close(SaveChanges=False)
                        workbook = excel.Workbooks.Open(os.path.abspath(
                            caminho), ReadOnly=False, IgnoreReadOnlyRecommended=True)
                except Exception:
                    pass

                # Desproteger workbook e worksheets de forma segura
                # NÃO reproteger após abertura para evitar bloqueios futuros
                try:
                    self.desproteger_planilha_seguro(
                        excel, workbook, reproteger=False)
                except Exception:
                    pass

                # Restaurar comportamento e interface
                try:
                    excel.ScreenUpdating = True
                except Exception:
                    pass
                try:
                    excel.EnableEvents = True
                except Exception:
                    pass
                try:
                    excel.Interactive = True
                except Exception:
                    pass

                # Interface: maximizar e trazer para frente
                try:
                    excel.WindowState = -4137  # xlMaximized
                except Exception:
                    pass
                try:
                    excel.DisplayFullScreen = True
                except Exception:
                    pass
                try:
                    excel.Visible = True
                except Exception:
                    pass

                try:
                    workbook.Activate()
                    if workbook.Worksheets.Count > 0:
                        workbook.Worksheets(4).Activate()
                except Exception:
                    pass

                # Ocultar a visualização das guias (sheet tabs) na janela do workbook
                try:
                    try:
                        windows_count = workbook.Windows.Count
                    except Exception:
                        windows_count = 0

                    if windows_count > 0:
                        for i in range(1, windows_count + 1):
                            try:
                                workbook.Windows(i).DisplayWorkbookTabs = False
                            except Exception:
                                # fallback: tentar no ActiveWindow
                                try:
                                    excel.ActiveWindow.DisplayWorkbookTabs = False
                                except Exception:
                                    pass
                    else:
                        try:
                            excel.ActiveWindow.DisplayWorkbookTabs = False
                        except Exception:
                            pass
                except Exception:
                    # não crítico
                    pass

                print("Planilha aberta com sucesso!")

            except Exception as e:
                # Fallback: se tudo falhar, abrir com app padrão do SO
                print(f"Erro ao abrir com Excel COM: {e}")
                try:
                    os.startfile(os.path.abspath(caminho))
                except Exception as fallback_error:
                    self.mostrar_erro(
                        f"Falha ao abrir planilha: {fallback_error}")
        else:
            self.mostrar_erro(f"Planilha não encontrada: {caminho}")

    def desproteger_planilha_seguro(self, excel_app, workbook, reproteger: bool = True):
        """
        Desprotege planilhas de forma segura sem causar reabertura
        """
        try:
            # **SALVA O ESTADO ORIGINAL DA PROTEÇÃO**
            estado_original = {}
            for worksheet in workbook.Worksheets:
                estado_original[worksheet.Name] = worksheet.ProtectContents

            # **DESPROTEGE WORKBOOK**
            try:
                if workbook.ProtectStructure:
                    workbook.Unprotect()  # Tenta sem senha
                    print("Workbook desprotegido")
            except Exception as e:
                print(f"Aviso: Não foi possível desproteger workbook: {e}")

            # **DESPROTEGE WORKSHEETS**
            for worksheet in workbook.Worksheets:
                try:
                    if worksheet.ProtectContents:
                        worksheet.Unprotect()  # Tenta sem senha
                        print(f"Worksheet {worksheet.Name} desprotegido")
                except Exception as e:
                    print(
                        f"Aviso: Não foi possível desproteger {worksheet.Name}: {e}")

            # **APLICA PROTEÇÃO APENAS SE NECESSÁRIO (UserInterfaceOnly)**
            # Isso permite macros mesmo com proteção
            if reproteger:
                for worksheet in workbook.Worksheets:
                    if estado_original.get(worksheet.Name, False):
                        try:
                            worksheet.Protect(
                                Password="",
                                DrawingObjects=True,
                                Contents=True,
                                Scenarios=True,
                                UserInterfaceOnly=True  # **PERMITE MACROS**
                            )
                            print(
                                f"Worksheet {worksheet.Name} reprotegido com UserInterfaceOnly")
                        except Exception as e:
                            print(
                                f"Aviso: Não foi possível reproteger {worksheet.Name}: {e}")

        except Exception as e:
            print(f"Erro no processo de desproteção: {e}")

    def mostrar_erro(self, mensagem):
        """Exibe mensagem de erro na interface"""
        # Limpa mensagens anteriores
        for widget in self.center_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget.cget("text_color") == "red":
                widget.destroy()

        ctk.CTkLabel(
            self.center_frame,
            text=mensagem,
            text_color="red"
        ).pack(pady=10)

    def voltar_menu(self):
        from ui.main_menu import MainMenu
        self.frame.destroy()
        MainMenu(self.master, self.usuario)
