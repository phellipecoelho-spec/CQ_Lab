# ARCHITECTURE

## Visão geral
Este projeto é uma aplicação desktop Python que combina interface gráfica com persistência local e automação de planilhas Excel.

## Camadas
- `ui/`: interface do usuário com telas para login, menu principal e módulos de Solos, Concreto e Asfalto.
- `utils/`: lógica de suporte para banco de dados, autenticação e caminhos de arquivo.
- `ensaios/`: módulo de integração com planilhas Excel e sincronização de dados de ensaio.

## Fluxo principal
1. `app.py` inicializa o banco e carrega `LoginUI`.
2. Usuário realiza login e é direcionado ao `MainMenu`.
3. `MainMenu` roteia para módulos especializados, por exemplo `AsfaltoUI`.
4. `AsfaltoUI` pode abrir planilhas Excel ou sincronizar tabelas normativas com o SQLite.

## Dependências entre componentes
- `ui/login_ui.py` depende de `utils/auth.py` e `ui/main_menu.py`.
- `ui/main_menu.py` carrega os módulos de domínio (`SolosUI`, `ConcretoUI`, `AsfaltoUI`).
- `utils/db_manager.py` expõe `conectar()` e `inicializar_db()` para todo o sistema.
- `ensaios/ensaio_001/sync_ensaio_001.py` depende de `utils/path_helper.py` e `win32com.client`.
