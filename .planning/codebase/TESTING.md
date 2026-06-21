# TESTING

## Estado atual
- O projeto não inclui testes automatizados.
- A maior parte da lógica está em componentes de UI e scripts de automação de Excel.

## Oportunidades de testes
- Testar funções de utilitários em `utils/`, como `auth.py` e `db_manager.py`.
- Criar testes de integração para a inicialização do banco de dados e criação de tabelas.
- Simular chamadas SQLite para verificar inserção e leitura de `Tbl_Procedim` e `Tbl_Projeto`.

## Recomendações
- Adotar `pytest` para cobertura de utilitários.
- Separar lógica de negócios de UI em funções testáveis.
- Evitar testes dependentes de COM/Excel em primeira etapa; preferir isolar sincronização com mocks.
