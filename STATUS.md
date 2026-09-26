# Status do projeto

Atualização: 26/09/2026.

## 1. Objetivo atual

Melhorar a interface e os fluxos do protótipo Streamlit para apresentar a jornada inclusiva na Linha 7–Rubi. O escopo permanece em cadastro estático, cenários artificiais e assistência simulada, sem infraestrutura adicional.

## 2. Implementado

- Nova interface com identidade visual da equipe, navegação Viagem/Estações/Apoio/Perfil e organização responsiva.
- Entrada por seis usuários fictícios, rotinas existentes com ida/volta e criação de perfil e rotina temporários.
- Busca de estações, diagrama do percurso, recursos publicados e informação desconhecida explícita.
- Quatro cenários selecionáveis, exploração das 24 horas e avisos conforme percurso e necessidades.
- Assistência pendente, confirmada, concluída ou cancelada, com prevenção de duplicidade e reinício ao mudar o contexto.
- Preferências de leitura preservadas durante a navegação.
- Separação entre dados (`data_access.py`), regras (`journey.py`), telas e apresentação (`ui.py`/`style.css`).
- Correção de `TMP-1830`, referenciado por uma viagem e ausente em `dim_tempo.csv`, também no gerador.
- README, metadados dos dados e roteiro atualizados para refletir o app existente.

## 3. Validação

- 11 testes automatizados aprovados com Python 3.12 e Streamlit 1.64.0.
- Fluxos verificados com o AppTest do Streamlit: perfis, navegação, ida/volta, validação de estações, rotina da sessão e estados de apoio.
- Geração comparada em diretório temporário: as seis tabelas reproduzem os CSVs versionados, incluindo o horário corrigido.
- Base: 17 estações, seis usuários, oito rotinas, 16 trechos, 15 horários e 24 registros operacionais.
- Versão publicada na branch `main` e aberta no Streamlit em 26/09/2026.
- Revisão no navegador desktop: entrada, identidade visual, viagem da Maria, cenário de pico com ocorrência, cadastro de estações e pedido pendente → confirmado → concluído.
- A revisão visual em largura de celular não foi concluída: o navegador de revisão não permite abrir a prévia local utilizada para esse teste. A validação em celular real permanece pendente.

## 4. Limitações e próximo passo

- O app não possui autenticação, persistência permanente, dados operacionais ao vivo ou integração com a operadora.
- A idade usa referência fixa de 15/01/2026. O dia operacional de exemplo é 01/09/2026, uma terça-feira.
- Durações artificiais e integrações do cadastro não são usadas como previsões ou rotas alternativas verificadas.
- Recursos de leitura não equivalem a auditoria de acessibilidade concluída.
- Próximo passo recomendado: validar a compreensão da jornada com usuários PCD e representantes da operação. Isso depende de uma nova tarefa.

Premissas e estrutura dos dados: [docs/dados-simulados.md](docs/dados-simulados.md). Roteiro: [apresetacao/roteiro_demo.md](apresetacao/roteiro_demo.md).
