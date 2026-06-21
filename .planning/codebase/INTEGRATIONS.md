# INTEGRATIONS

## Integrações principais
- `win32com.client` para manipular planilhas Excel no Windows.
- `sqlite3` para persistência local via banco de dados SQLite.
- `customtkinter` para construção da interface gráfica.

## Integração de arquivos
- `utils/path_helper.py` oferece caminhos para planilhas e banco de dados.
- `ensaios/ensaio_001/sync_ensaio_001.py` usa `get_planilha_path()` e `get_database_path()` para leitura/escrita de dados.

## Observações
- A integração com Excel depende de planilhas hospedadas em `planilhas/asfalto/Ensaio_001.xlsm`.
- O projeto não usa frameworks web ou serviços externos; é um sistema desktop autônomo.
