# Status do projeto

## Objetivo atual

Esta etapa implementa a massa inicial de dados sintéticos para usuários, rotinas e viagens planejadas da Linha 7–Rubi, preservando o cadastro real de estações em [data/estacoes_linha7.csv](data/estacoes_linha7.csv) e separando as entidades artificiais em [data/simulados](data/simulados).

## Planejado

- Modelagem dimensional simples em estrela para o MVP.
- Dados de três usuários fictícios e cinco rotinas de viagem.
- Registro de premissas e do processo de geração em [docs/dados-simulados.md](docs/dados-simulados.md).

## Em andamento

- Validação de consistência entre tabelas e horários.

## Implementado

- Script reprodutível em [data/simulados/generate_dados_sinteticos.py](data/simulados/generate_dados_sinteticos.py).
- CSVs gerados em [data/simulados](data/simulados): dim_estacao.csv, dim_usuario.csv, dim_tempo.csv, dim_rotina.csv, dim_ocorrencia.csv e fato_viagem_planejada.csv.
- Expansão para 6 usuários fictícios, com 3 perfis novos em horários distintos e um usuário adicional com deficiência informada.
- Cenário operacional de 24 horas para a segunda-feira, 2026-09-01, com registros de 1 em 1 hora.

## Validado

- 6 usuários, 8 rotinas, 16 trechos planejados e 24 ocorrências horárias.
- Chaves primárias e estrangeiras consistentes.
- Idades coerentes com data de referência fixa.
- CPFs sintéticos e claramente fictícios.
- Retorno invertido em relação à ida e horários plausíveis.
- Linha em funcionamento real contemplado: fechado fora do horário oficial e operação normal/pico/queda de energia simulada nas faixas pertinentes.

## Pendências

- Simulador operacional e interface ainda não implementados.
- Futuras ocorrências e cenários operacionais serão adicionados em etapa posterior.
