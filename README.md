# hackathon-embarque-inclusivo

## Visão geral

Este repositório documenta um MVP de aplicativo de mobilidade inclusiva para a Linha 7–Rubi, em São Paulo, pensado para apresentação em hackathon e como material de portfólio.

O objetivo do projeto é facilitar a viagem de pessoas que precisam de apoio, ajudando a relacionar informações de acessibilidade com as condições reais do percurso e com necessidades específicas da pessoa. A proposta não assume parceria com a operadora nem promete atendimento real ou percurso garantido.

## Estado real do repositório

O repositório ainda está em fase de documentação e planejamento. Não há implementação do protótipo, nem infraestrutura, nem dados persistentes configurados.

O único arquivo de código presente é [ingestao-bronze/src/api.py](ingestao-bronze/src/api.py), que se configura como um placeholder de uma proposta anterior e não deve ser interpretado como funcionalidade atual do MVP.

## Problema a ser mostrado

As pessoas que viajam por transporte público muitas vezes encontram dificuldade para responder perguntas simples e essenciais:

- qual estação oferece acessibilidade relevante para o meu caso;
- o percurso tem algum ponto problemático;
- o equipamento necessário está disponível;
- como solicitar apoio durante a viagem;
- qual é o estado real da assistência solicitada.

O MVP tem como diferencial explicar por que uma condição do percurso afeta a viagem de uma pessoa específica, e não apenas apresentar um resumo genérico de acessibilidade.

## Solução proposta

A solução é um protótipo em Streamlit para celular, com jornada guiada de usuário fictício. O app reúne:

- informações de acessibilidade conhecidas das estações;
- o perfil e as necessidades do usuário;
- a rotina habitual de deslocamento;
- o percurso selecionado;
- condições operacionais simuladas e alertas relevantes;
- a solicitação de assistência e o acompanhamento do estado.

A experiência é pensada para demonstrar a decisão do usuário em cenas diferentes, sem afirmar que o atendimento foi confirmado por uma operadora real.

## Funcionalidades planejadas

### Entrada e perfil

- Conta de demonstração com usuário fictício.
- Identificação clara de que não há autenticação real.
- Preferências e necessidades de acessibilidade.
- Informação sobre deficiência opcional, editável e sem exigência de diagnóstico.
- Pergunta direta sobre o apoio necessário durante a viagem.
- Suporte também para necessidades temporárias.

### Rotina e viagem

- Origem, destino, dias e horário habitual.
- Possibilidade de selecionar ou alterar a rotina.
- Consulta ao percurso e à acessibilidade conhecidas.
- Condições simuladas e alertas relevantes.
- Alternativas somente quando verificadas.
- Limitação explicitada quando não houver alternativa confirmada.

### Assistência

- Solicitar apoio.
- Acompanhar estados como pendente, confirmado e concluído.
- Mostrar responsável e ponto de encontro fictícios quando houver confirmação simulada.
- Evitar pedidos duplicados por repetição de clique ou atualização da interface.

### Controles da demonstração

- Selecionar cenário.
- Avançar eventos.
- Reiniciar a demonstração.
- Manter esses controles separados da jornada do passageiro.

## Arquitetura simplificada

A estrutura abaixo é uma proposta para implementação futura e não representa código já implementado.

```text
app.py
requirements.txt
dados/
    estacoes.json
    usuario_demo.json
    cenarios.json
src/
    dados.py
    simulacao.py
    viagem.py
    assistencia.py
    telas/
        entrada.py
        perfil.py
        inicio.py
        viagem.py
docs/
    roteiro_demo.md
```

Responsabilidades previstas:

- app.py: início e navegação.
- dados.py: carregamento e validação dos arquivos.
- simulacao.py: cenários, avanço de eventos e reinício.
- viagem.py: percurso e impacto das condições nas necessidades do usuário.
- assistencia.py: estados e transições do atendimento.
- telas/: apresentação e interação, sem concentrar regras de negócio.

## Dados reais e simulados

### Dados reais

- Identificador e nome da estação.
- Ordem da estação na linha.
- Endereço e integrações, quando confirmados.
- Recursos de acessibilidade publicados pela fonte.
- URL da fonte e data da consulta.

Esses dados devem ser tratados como cadastro estático real e não devem ser inventados nesta tarefa.

### Dados simulados

- Usuário fictício e suas preferências.
- Movimento nas estações.
- Condições operacionais.
- Ocorrências.
- Solicitações e confirmações de assistência.
- Funcionários e pontos de encontro usados na demonstração.

O aplicativo deve distinguir claramente entre informações reais e simulações, sem atribuir dados sintéticos à operadora como se fossem medições reais.

## Quatro cenários do MVP

Os cenários abaixo usam horários ilustrativos para a demonstração e não representam medição real de demanda da Linha 7.

1. Baixo movimento: 22h, sem ocorrências.
2. Movimento moderado: 14h, sem ocorrências.
3. Horário de pico: 7h30, movimento intenso, sem ocorrências.
4. Horário de pico com ocorrência: 7h30, movimento intenso e uma ocorrência programada.

O horário não determina sozinho a existência de uma ocorrência. Os dois cenários de pico usam o mesmo horário para demonstrar o efeito do problema.

No cenário 4, uma indisponibilidade simulada de elevador pode afetar um acesso necessário à viagem do usuário. O aplicativo explica esse impacto e permite solicitar orientação. Só oferece alternativa de percurso se houver uma verificada.

## Regras e limitações atuais

- O protótipo usa login e assistência simulados.
- Não há autenticação real, nem coleta de senhas.
- Não há persistência permanente na primeira versão.
- Não há integração com a operadora e não há promessa de atendimento real.
- Dados ausentes na fonte são tratados como “não informado”, não como “inexistente”.
- Acessibilidade deve ser avaliada em relação ao percurso e ao apoio necessário.
- Novas funcionalidades só entram por decisão explícita.

## Estado do projeto

Este projeto está em fase de planejamento e documentação para apresentação em hackathon. O documento de roteiro de demonstração em [docs/roteiro_demo.md](docs/roteiro_demo.md) detalha a jornada, os cenários e os critérios de prontidão.

A implementação do MVP ainda não foi iniciada, e o trabalho documental deve continuar confirmando o escopo e evitando promessas que extrapolam o estado real do repositório.
