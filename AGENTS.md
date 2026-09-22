# AGENTS.md

## 1. Finalidade e execução das tarefas

Estas regras se aplicam a todo o repositório **hackathon-embarque-inclusivo**. Arquivos `AGENTS.md` locais, quando existirem, complementam as orientações para seus diretórios.

- A solicitação atual do autor define objetivo, escopo, autonomia e entregáveis. Não exigir um formulário de prompt para tarefas simples.
- Trabalhar em unidades pequenas e revisáveis: entender, executar, validar e documentar o necessário.
- Ler as instruções aplicáveis, os arquivos envolvidos e, quando existirem, o `STATUS.md` e as decisões relevantes antes de alterar a implementação.
- Pesquisa não autoriza implementação. Concluir uma tarefa não autoriza iniciar a próxima, salvo autonomia já concedida.
- Resolver detalhes internos dentro do escopo autorizado. Mudanças de arquitetura, tecnologias principais, fontes, contratos ou regras de negócio exigem autorização, caso ainda não esteja presente na solicitação.
- Preservar alterações da dupla e componentes funcionais. Não fazer refatorações, reorganizações ou mudanças destrutivas sem necessidade e autorização adequadas.

## 2. Objetivo e limites do projeto

O projeto é um MVP para hackathon e portfólio, com recorte na **Linha 7–Rubi**. O foco é facilitar o acesso à informação e o planejamento de viagens, principalmente para pessoas com deficiência, além de registrar relatos dos passageiros.

A jornada prioritária é consultar o percurso, informar o apoio necessário, solicitar assistência e acompanhar confirmação, responsável e ponto de encontro. Consultas e relatos também atendem ao público geral.

- Priorizar uma jornada demonstrável e compreensível ao passageiro.
- A operação de atendimento será simulada enquanto não houver integração real com a operadora. Não presumir vínculo com a TIC Trens.
- Não apresentar uma solicitação como atendimento confirmado, nem prometer percurso garantido.
- Dashboard empresarial amplo, app nativo, WhatsApp, expansão para outras linhas e decisões automáticas baseadas em relatos são evoluções, não requisitos da primeira entrega.
- Não transformar possibilidades discutidas em funcionalidades obrigatórias sem decisão do autor.

## 3. Arquitetura acordada

- **Streamlit:** interface inicial do MVP. Outra interface web depende de decisão posterior.
- **FastAPI:** API REST para consultas, solicitações e regras da aplicação.
- **Python:** coleta e transformação; BeautifulSoup quando a fonte oferecer HTML e APIs REST quando disponíveis.
- **Amazon S3:** armazenamento do data lake do MVP. Não tratá-lo como banco relacional ou pressupor transações e atualizações concorrentes de registros.
- Não introduzir dbt, orquestradores, novos bancos ou serviços sem necessidade concreta e autorização compatível com a tarefa.

Manter dois domínios lógicos: **estações e operação** e **interações e atendimentos**. Ambos seguem Bronze, Silver e Gold; isso não exige buckets ou infraestrutura física separados.

| Camada | Responsabilidade |
| --- | --- |
| Bronze | Preservar dados brutos necessários, texto original dos relatos e eventos, com origem e horários |
| Silver | Limpar e padronizar em Python, tratar duplicidades e extrair informações dos textos |
| Gold | Preparar dados consolidados para consulta, acompanhamento e síntese de feedbacks |

Separar acesso externo, storage, transformação, regras e interface. A Gold fornece dados preparados; a API executa as regras e os entrega à aplicação. Criar módulos e diretórios conforme a implementação exigir, sem scaffolding vazio.

## 4. Fontes e confiabilidade dos dados

- Separar cadastro físico de condição operacional: possuir elevador não significa que ele esteja funcionando.
- O site oficial é fonte das informações que efetivamente publica. Monitoramento em tempo real depende de uma fonte ainda a validar; não inventar endpoints, cobertura ou frequência de atualização.
- Consultas periódicas são polling. Não chamar dados antigos de tempo real porque o coletor executa frequentemente.
- Registrar origem, horário de coleta e horário do evento ou atualização quando fornecido. Sinalizar dados ausentes, antigos ou indisponíveis.
- Manter identificadores consistentes de estação e evento. Avaliar impactos antes de alterar nomes, tipos, chaves, granularidade e contratos entre camadas.
- Identificar separadamente dados oficiais, relatos não verificados e eventos simulados. Simulações não podem contaminar o conjunto real.

## 5. Relatos e retroalimentação

Guardar na Bronze o texto necessário ao processamento, reduzindo dados pessoais ao mínimo. Na Silver, extrair estação, assunto, intenção e problema; análise de sentimento é complementar e sua biblioteca ou modelo ainda será escolhido.

- Tratar classificações automáticas como inferências, com possibilidade de erro e revisão.
- Não inferir deficiência, diagnóstico ou veracidade de um relato a partir do sentimento.
- Não usar mensagens produzidas pelo próprio sistema como nova evidência de uma ocorrência.
- No MVP, retroalimentação significa registrar e analisar interações. Relatos não substituem automaticamente informações oficiais nem alteram orientações de viagem.

## 6. Acessibilidade e privacidade

- Perguntar qual apoio é necessário na viagem, sem exigir diagnóstico para personalizar a experiência.
- Usar linguagem simples, campos com rótulos claros e estados compreensíveis. Não comunicar situações apenas por cores ou ícones.
- Validar os fluxos principais no celular, por teclado e com leitor de tela quando aplicável; registrar verificações ainda pendentes.
- Não versionar credenciais, `.env`, tokens, dados pessoais reais, laudos, dumps ou datasets volumosos. Usar configurações externas e `.env.example` sem segredos.
- Usar dados sintéticos nos testes. Restringir o acesso a textos e necessidades de assistência; S3 não deve ser público para expor esses dados à interface.
- Não confundir identificador pseudonimizado com anonimização irreversível.

## 7. Simulação e validação

O simulador deve exercitar os mesmos contratos e fluxos de processamento usados pelas entradas reais, em ambiente separado ou explicitamente identificado.

Priorizar os cenários relevantes à tarefa: assistência confirmada, solicitação pendente, equipamento indisponível, fonte desatualizada ou inacessível e entradas duplicadas. Verificar persistência e impedir que uma repetição gere agendamentos duplicados.

Separar testes locais de integrações com APIs e AWS. Não criar recursos pagos ou executar operações destrutivas sem autorização. Tratar falhas com contexto, sem ocultá-las silenciosamente ou enfraquecer testes para obter sucesso.

Executar validações proporcionais à mudança. Não exigir testes de código para alterações apenas documentais. Nunca declarar validações que não foram executadas; informar bloqueios e impactos.

## 8. Documentação e aprendizado

- Usar português brasileiro claro, mantendo termos técnicos usuais em inglês.
- Distinguir planejado, em desenvolvimento e implementado e validado. Arquivo existente ou placeholder não comprova funcionalidade.
- Atualizar documentação realmente afetada. O README resume o projeto; não deve concentrar toda a documentação técnica.
- Quando necessários, `STATUS.md` registra o estado atual, `docs/decisoes.md` registra decisões adotadas e motivos, e `CHANGELOG.md` registra marcos relevantes. Não criar esses arquivos apenas por formalidade.
- Decisões importantes devem indicar contexto, escolha, origem da decisão, validação e limitações. Hipóteses permanecem identificadas como hipóteses.
- Fundamentar alegações externas em fontes, preservando país, período, amostra e limites. Não atribuir à Linha 7–Rubi resultados de outros sistemas.
- Ao concluir, explicar o que mudou, arquivos envolvidos, fluxo de entradas e saídas quando houver código, validações e pendências. A entrega deve permitir que a dupla compreenda e apresente o trabalho.

Uma tarefa termina quando o escopo autorizado foi atendido, as validações relevantes foram realizadas ou suas limitações informadas e a documentação afetada corresponde ao estado real. Sugerir próximos passos não autoriza executá-los.
