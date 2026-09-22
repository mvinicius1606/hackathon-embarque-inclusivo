# hackathon-embarque-inclusivo

MVP de mobilidade inclusiva para a Linha 7–Rubi, com foco em facilitar o acesso à informação e o planejamento de viagens de pessoas com deficiência (PCD).

## Objetivo

Reunir informações sobre estações, acessibilidade e condições operacionais em uma interface simples, permitindo ao passageiro consultar seu percurso, solicitar assistência e acompanhar o atendimento. O projeto também pretende transformar relatos dos usuários em dados estruturados que possam apoiar melhorias no serviço.

## Problemas que queremos resolver

| Problema | Solução proposta |
| --- | --- |
| Dificuldade para encontrar informações de acessibilidade relevantes para a viagem | Centralizar os recursos das estações de origem e destino, de acordo com o apoio necessário ao passageiro |
| Incerteza sobre as condições do percurso | Apresentar informações disponíveis com fonte, horário de atualização e indicação de dados ainda não confirmados |
| Falta de previsibilidade sobre a assistência | Permitir solicitar apoio e acompanhar confirmação, responsável e ponto de encontro |
| Relatos dispersos em mensagens de texto | Registrar e classificar relatos por estação, assunto, problema e sentimento |

O atendimento PCD será o principal caso de uso do MVP. Consultas de informações e envio de relatos também poderão atender ao público geral.

## Como será desenvolvido

A interface inicial será construída em **Streamlit**, com **FastAPI** para disponibilizar consultas e gerenciar solicitações. A coleta utilizará APIs REST quando disponíveis e requisições HTTP com BeautifulSoup para informações publicadas em páginas web.

Os dados serão armazenados em um **data lake no Amazon S3**, organizados em dois domínios: **estações e operação** e **interações e atendimentos**. Cada domínio seguirá a arquitetura medallion:

- **Bronze:** dados brutos das fontes, textos dos relatos e eventos de atendimento, com identificação da origem e do momento do registro.
- **Silver:** limpeza e padronização em Python, tratamento de duplicidades e extração de informações dos textos, incluindo intenção, estação, assunto e sentimento.
- **Gold:** dados consolidados para consulta pela aplicação, acompanhamento da assistência e síntese dos feedbacks.

O cadastro físico das estações será separado de sua condição operacional: a existência de um elevador não comprova que ele esteja funcionando naquele momento. A fonte para monitoramento em tempo real ainda será definida; a frequência de coleta respeitará a disponibilidade e a atualização de cada fonte.

## Demonstração do MVP

1. O passageiro informa origem, destino, horário e necessidade de apoio.
2. A aplicação apresenta as informações conhecidas sobre o percurso.
3. O passageiro solicita assistência e acompanha seu estado.
4. Um operador de demonstração atribui o responsável e confirma o ponto de encontro.
5. O passageiro registra um relato, que é armazenado na Bronze e processado nas camadas seguintes.

Um simulador fornecerá ocorrências e eventos de atendimento para testar situações como assistência confirmada, indisponibilidade de equipamento e solicitação pendente. Dados oficiais, relatos não verificados e dados simulados serão identificados separadamente.

A retroalimentação inicial ficará limitada ao registro e à análise das interações. Relatos não alterarão automaticamente o status oficial ou as orientações de viagem. O uso gerencial dos dados pela operadora será uma possibilidade de evolução, sem ser o foco da primeira entrega.

## Status e alcance

Projeto em fase de concepção e desenvolvimento para hackathon e portfólio. As funcionalidades descritas representam o escopo planejado.

O MVP é independente e não pressupõe vínculo ou integração com a TIC Trens. Confirmações de assistência na demonstração serão simuladas; atendimento real dependerá de integração e participação da operadora.
