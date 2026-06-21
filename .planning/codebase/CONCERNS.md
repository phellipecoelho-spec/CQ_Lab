# CONCERNS

## Riscos e pontos fracos

### Dependência do Windows e Excel COM
- A sincronização de planilhas depende de `win32com.client`, o que torna a aplicação restrita ao Windows e a instalações do Microsoft Excel.
- Chamadas COM podem falhar silenciosamente se o Excel não estiver instalado ou se a versão do Windows tiver permissões restritas.

### Arquitetura de persistência
- O uso de um único arquivo `database.db` sem migrações formais pode dificultar futuras alterações de esquema.
- A inicialização do banco é chamada em múltiplos pontos (`app.py`, `utils/auth.py`, `sync_ensaio_001.py`), o que pode mascarar dependências de inicialização.

### Qualidade de código e manutenção
- Alguns módulos UI (`concreto_ui.py`, `solos_ui.py`) são placeholders e não oferecem funcionalidade real.
- Nomes de colunas e tabelas no banco são mistos, o que pode gerar inconsistência e dificultar consultas futuras.
- O arquivo `ui/main_menu.py` contém código comentado e histórico, sugerindo refatoração pendente.

### Segurança e autenticação
- A autenticação é local e baseada em SQLite, adequada para desktop, mas sem proteção adicional contra ataques de força bruta.
- Não há política clara para reset de senha além da interface, e não há registro de tentativas de login.

## Recomendações de mitigação
- Isolar a lógica de Excel em serviços testáveis e adicionar wrappers de erro robustos.
- Adotar esquema de migração versionada em `utils/db_manager.py` ou usar uma biblioteca de migração leve.
- Refatorar a UI para remover código morto e consolidar importações entre módulos.
- Considerar armazenamento de senhas com salt e validação de políticas mais fortes.
