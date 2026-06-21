# STRUCTURE

## Estrutura de diretórios

- `app.py` — entrada da aplicação
- `ui/` — pacotes de interface do usuário
  - `login_ui.py` — tela de login, cadastro e reset de senha
  - `main_menu.py` — menu principal e navegação entre módulos
  - `asfalto_ui.py` — módulo Asfalto com controle de planilhas e sincronização
  - `concreto_ui.py` — módulo Concreto (placeholder de UI)
  - `solos_ui.py` — módulo Solos (placeholder de UI)
  - `projeto_ui.py` — tela de parâmetros de Projeto
  - `procedim_ui.py` — tela de parâmetros Normativos
- `utils/` — utilitários e helpers
  - `db_manager.py` — conexão e inicialização de banco de dados SQLite
  - `auth.py` — autenticação, hashing de senha e gerenciamento de usuários
  - `path_helper.py` — resolução de caminhos de arquivos e planilhas
- `ensaios/ensaio_001/` — integração de ensaio específico com Excel
  - `config_ensaio_001.py` — mapeamento de campos e referências de planilha
  - `sync_ensaio_001.py` — sincronização entre Excel e SQLite
- `planilhas/` — diretório de planilhas Excel usadas pela aplicação
- `database.db` — banco de dados local
