# STACK

## Linguagens
- Python 3.x
- SQL (SQLite)

## Frameworks/Bibliotecas
- customtkinter
- pywin32 (`win32com.client`)
- sqlite3 (módulo padrão do Python)

## Principais componentes
- `app.py` – ponto de entrada da aplicação
- `ui/` – telas de interface gráfica
- `utils/` – helpers de caminho, autenticação e banco de dados
- `ensaios/` – automação de planilhas Excel e sincronização de ensaios

## Observações
- A interface é desktop, construída com `customtkinter`.
- Existe integração com arquivos Excel via COM/`win32com.client`.
- O banco de dados local é um arquivo SQLite (`database.db`).
