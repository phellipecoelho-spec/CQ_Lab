# CONVENTIONS

## Estilo de código
- Uso misto de `snake_case` para funções e variáveis.
- Classes em `PascalCase` para componentes de UI.
- Arquivos Python seguem uma organização simples em diretórios temáticos.

## Persistência de dados
- O banco local é um arquivo SQLite (`database.db`) no root do projeto.
- A inicialização do banco é centralizada em `utils/db_manager.py`.
- Tabelas são criadas dinamicamente com `CREATE TABLE IF NOT EXISTS`.

## Interface do usuário
- A UI é construída com `customtkinter` e telas baseadas em classes.
- O menu principal redireciona para módulos temáticos.
- Algumas telas ainda são placeholders (`concreto_ui.py`, `solos_ui.py`).

## Observações de convenção
- Há comentários de migração e compatibilidade dentro do `db_manager.py`.
- Alguns módulos carregam `customtkinter` e `win32com.client` apenas quando necessário.
- Os nomes de tabelas no banco seguem convenções misturadas de `Tbl_` e minúsculas simples.
