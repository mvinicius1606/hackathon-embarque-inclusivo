# Encerramento do projeto

Atualização documental: 02/10/2026.

## 1. Situação final

**Projeto acadêmico concluído.** O Embarque Inclusivo foi desenvolvido no contexto do Hacktown, voltado ao empreendedorismo, por três estudantes da Universidade Presbiteriana Mackenzie.

A equipe foi composta por Marcos Vinicius Vieira dos Santos (Análise e Desenvolvimento de Sistemas), Karla Priscila Oliveira Silva (Matemática) e Gabriela Cristina Vieira (Marketing). As responsabilidades individuais estão registradas no [README](README.md#12-equipe-e-contribuições).

O projeto foi classificado para a segunda fase com nota **7,4**. Dificuldades logísticas impediram a participação do grupo na apresentação presencial dessa etapa.

O ciclo acadêmico está encerrado. O repositório preserva o protótipo, os dados de demonstração e a documentação como registro do trabalho e material de portfólio.

## 2. Entregas concluídas

- Nova interface com identidade visual da equipe, navegação Viagem/Estações/Apoio/Perfil e organização responsiva.
- Entrada por seis usuários fictícios, rotinas existentes com ida/volta e criação de perfil e rotina temporários.
- Busca de estações, diagrama do percurso, recursos publicados e informação desconhecida explícita.
- Quatro cenários selecionáveis, exploração das 24 horas e avisos conforme percurso e necessidades.
- Assistência pendente, confirmada, concluída ou cancelada, com prevenção de duplicidade e reinício ao mudar o contexto.
- Preferências de leitura preservadas durante a navegação.
- Separação entre dados (`data_access.py`), regras (`journey.py`), telas e apresentação (`ui.py`/`style.css`).
- Correção de `TMP-1830`, referenciado por uma viagem e ausente em `dim_tempo.csv`, também no gerador.
- README, metadados dos dados e roteiro atualizados para refletir o app existente.

## 3. Verificações registradas na entrega

- Na revisão técnica de setembro de 2026, 11 testes automatizados foram aprovados com Python 3.12 e Streamlit 1.64.0.
- Fluxos verificados com o AppTest do Streamlit: perfis, navegação, ida/volta, validação de estações, rotina da sessão e estados de apoio.
- Geração comparada em diretório temporário: as seis tabelas reproduzem os CSVs versionados, incluindo o horário corrigido.
- Base: 17 estações, seis usuários, oito rotinas, 16 trechos, 15 horários e 24 registros operacionais.
- Versão publicada na branch `main` e aberta no Streamlit em 26/09/2026.
- Revisão no navegador desktop: entrada, identidade visual, viagem da Maria, cenário de pico com ocorrência, cadastro de estações e pedido pendente → confirmado → concluído.
- A revisão visual em largura de celular não foi concluída na entrega; o navegador de revisão não permitiu abrir a prévia local utilizada para esse teste. Não há validação em celular real registrada no repositório.

## 4. Limites da entrega e preservação

- O app não possui autenticação, persistência permanente, dados operacionais ao vivo ou integração com a operadora.
- A idade usa referência fixa de 15/01/2026. O dia operacional de exemplo é 01/09/2026, uma terça-feira.
- Durações artificiais e integrações do cadastro não são usadas como previsões ou rotas alternativas verificadas.
- Recursos de leitura não equivalem a auditoria de acessibilidade concluída.
- Não há novas etapas de desenvolvimento previstas para este ciclo acadêmico. Eventuais melhorias ou validações adicionais dependeriam de uma nova iniciativa.

O encerramento registra a conclusão do trabalho acadêmico dentro do escopo demonstrativo entregue. As limitações técnicas permanecem documentadas como parte desse registro.

Premissas e estrutura dos dados: [docs/dados-simulados.md](docs/dados-simulados.md). Roteiro: [apresetacao/roteiro_demo.md](apresetacao/roteiro_demo.md).
