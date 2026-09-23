# AGENTS.md

## 1. Escopo e autonomia

- A solicitação atual do autor define o escopo, a autonomia e os entregáveis.
- Trabalhar em mudanças pequenas e revisáveis.
- Ler o estado real do repositório antes de editar qualquer documentação ou implementação.
- Esse projeto é um trabalho em grupo mas apenas eu trabalhara nesse repositório.
- Não transformar sugestões ou ideias em requisitos obrigatórios sem autorização explícita.
- Não iniciar etapas adicionais sem autorização.

## 3. Objetivo do projeto

Nome: hackathon-embarque-inclusivo.

Recorte: Linha 7–Rubi, em São Paulo.

Proposta: um protótipo de aplicativo para mobilidade inclusiva que reúne informações de acessibilidade, considera necessidades e rotinas do passageiro e facilita a solicitação de assistência durante a viagem.

O foco do hackathon é demonstrar a jornada de um usuário fictício em diferentes situações e mostrar como o aplicativo reage. O projeto também serve como portfólio, mas a arquitetura de dados não deve ampliar desnecessariamente o escopo.

## 4. Decisões de arquitetura atuais

- Projeto atualmente foca em experiência de usuário e desenvolvimento web mobile.
- Dados serão puramente artificiais para exemplificar casos de uso do aplicativo.
- Unico dado oficial é a estrutura da linha 7 Rubi com suas estações e o que tem nelas.
- Streamlit via python sera o motor de simulação de um aplicativo, usarei outra plataforma para costomização e fazer a integração com o Streamlit.

Manter separação simples entre dados, regras da aplicação e telas. Evitar abstrações ou serviços sem necessidade concreta.

## 5. Dados reais e dados simulados

### Cadastro real

O arquivo `data/estacoes_linha7.csv` é a referência para as estações da Linha 7–Rubi utilizadas no projeto.

O cadastro pode incluir:

- Identificador e nome da estação.
- Ordem da estação na linha.
- Endereço e integrações, quando confirmados.
- Recursos de acessibilidade publicados pela fonte.
- URL da fonte e data da consulta.

Usar apenas os campos e informações efetivamente disponíveis. Informação ausente significa “não informado”, não que o recurso inexiste. A existência de um equipamento não comprova seu funcionamento atual.

Não inventar estações, integrações ou equipamentos para acomodar uma simulação. Se o cadastro tiver lacunas ou inconsistências relevantes, registrar a limitação antes de utilizá-lo.

### Regras para criação de dados simulados

- Antes de criar ou alterar dados, ler `dados-simulados.md`, o cadastro de estações e os arquivos envolvidos na tarefa. Se a documentação ainda não existir, criá-la com a primeira entrega de dados simulados.
- O prompt de cada tarefa define quais dados devem ser criados, sua estrutura e seu objetivo. Não ampliar a massa de dados ou o schema sem necessidade para a tarefa.
- Usar `data/estacoes_linha7.csv` como referência para nomes, identificadores, ordem das estações e demais informações disponíveis.
- Manter os dados coerentes entre si e com os relacionamentos do schema. Não gerar registros aleatórios e desconectados apenas para preencher tabelas.
- Reutilizar identificadores existentes. Preservar chaves primárias únicas e chaves estrangeiras válidas.
- Garantir coerência entre datas, idades, horários, duração das viagens, rotinas, ida e retorno.
- Distinguir premissas da simulação de informações verificadas. Durações e níveis de movimento definidos pelo projeto não são dados oficiais.
- Simular falhas apenas em equipamentos cuja existência esteja confirmada no cadastro. Quando faltar informação, não afirmar que um percurso é acessível.
- Usar geração reproduzível: mesmos parâmetros devem produzir os mesmos dados. Quando houver aleatoriedade, fixar e documentar a semente.
- Não sobrescrever o cadastro real com condições simuladas.
- Usar somente pessoas fictícias. Não buscar dados pessoais reais nem gerar credenciais ou CPFs válidos.
- Uma solicitação ou intenção de assistência não equivale a atendimento confirmado.

### Documentação dos dados simulados

O arquivo `dados-simulados.md` funciona como o registro de metadados e das decisões sobre os dados artificiais.

A cada criação ou alteração, documentar:

- Objetivo dos dados e funcionalidade ou cenário que irão apoiar.
- Arquivos e tabelas envolvidos.
- Granularidade: o que cada linha representa.
- Campos, tipos, formatos e valores permitidos.
- Chaves e relacionamentos entre tabelas.
- Fontes reais utilizadas como referência.
- Regras de geração, parâmetros e motivo das escolhas.
- Premissas de horários, durações e condições simuladas.
- Forma de reproduzir a geração.
- Validações executadas, limitações e pendências.
- Mudanças realizadas e impactos nos dados já existentes.

Explicar o processo de geração por tabela e campo, sem precisar narrar cada registro quando todos seguem a mesma regra. Documentar separadamente as exceções relevantes.

Se uma nova tarefa conflitar com decisões anteriores, registrar a mudança e avaliar os relacionamentos afetados. Não manter versões contraditórias da documentação e dos dados.

### Uso na demonstração

Os dados simulados serão definidos por etapa nos prompts das tarefas. O agente deve considerar o conjunto já existente para manter continuidade entre usuários, rotinas, viagens e eventos.

Identificar os registros sintéticos e apresentar as condições operacionais como simuladas na interface.

Esses dados servem para demonstrar e testar o comportamento do aplicativo no pitch. Não representam medições reais da operadora, previsões validadas ou confirmações reais de assistência.

## 6. STATUS.md como bússola do projeto

O `STATUS.md` registra onde o projeto está e orienta a continuidade do trabalho. O `AGENTS.md` define as regras; o `STATUS.md` mostra o andamento; o prompt atual define a tarefa autorizada.

- Ler o `STATUS.md` antes de iniciar uma tarefa e conferir os arquivos relevantes. Se houver divergência, registrar o estado verificado e corrigir a documentação.
- Se o arquivo não existir, criá-lo com base no que foi realmente encontrado no repositório.
- Atualizar ao concluir uma etapa ou quando houver mudança relevante, bloqueio ou trabalho incompleto.
- Diferenciar claramente: planejado, em andamento, implementado e validado. Arquivo existente não comprova funcionalidade.
- Registrar o objetivo atual, o que já funciona, o que falta, bloqueios, decisões recentes e próximo passo recomendado.
- Indicar os arquivos envolvidos e as validações realizadas, incluindo limitações e verificações pendentes.
- Referenciar `dados-simulados.md` para detalhes dos dados, sem duplicar seu conteúdo.
- Manter o documento curto e atualizado, sem transformá-lo em um histórico extenso de conversas.
- Próximos passos registrados não autorizam sua execução automática. Seguir o escopo do prompt atual.

Ao encerrar uma tarefa incompleta, deixar explícito onde o trabalho parou, o que foi alterado e o que é necessário para retomá-lo.

## 6. Funcionalidades planejadas

- Conta de demonstração com usuário fictício.
- Perfil com preferências e necessidades de acessibilidade, sem exigir diagnóstico.
- Perguntar diretamente qual apoio é necessário.
- Rotina com origem, destino, dias e horário habitual.
- Minha viagem com seleção de origem e destino, consulta ao percurso e informações de acessibilidade conhecidas.
- Condições simuladas e alertas relevantes ao usuário.
- Solicitação de assistência com acompanhamento dos estados pendente, confirmado e concluído.
- Responsável e ponto de encontro fictícios quando houver confirmação simulada.
- Controles da demonstração: selecionar cenário, avançar eventos, reiniciar e limpar estado anterior.

Priorizar, na implementação futura, transições de assistência, alertas relevantes, dados desconhecidos, prevenção de duplicidades e reinício dos cenários.


## 8. Documentação

- Documentação em português brasileiro.
- Atualizar README e documentos técnicos a cada ação.
- Não criar infraestrutura ou arquivos de código vazios como se fossem implementações.
- Quando houver proposta futura, documentar como proposta e não como funcionalidade existente.
- Explicar mudanças e limitações ao final das tarefas.
- As documentações deverão serguir um padrão de atividade academica com topicos e sub-topicos, com a presença de sumário se a documentação tiver como longa.
- Linguagem deve ser formal, mas não complexa e engessada, deverá ser uma escrita natural e envolvente, usando conectivos.

## 9. Regras finais

- A solicitação atual do autor define escopo e autonomia.
- Trabalhar em mudanças pequenas e revisáveis.
- Não introduzir frameworks, bancos ou cloud sem necessidade e decisão explícita.
- Separar cadastro real, eventos simulados e estado da sessão.
- Não prometer assistência nem acessibilidade sem confirmação.
- Distinguir informações reais de simuladas claramente.
- Preservar trabalho existente da dupla.
- Não declarar conclusões que extrapolem o estado real do repositório.


