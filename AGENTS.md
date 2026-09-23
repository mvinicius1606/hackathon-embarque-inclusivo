# AGENTS.md

## 1. Escopo e autonomia

- A solicitação atual do autor define o escopo, a autonomia e os entregáveis.
- Trabalhar em mudanças pequenas e revisáveis.
- Ler o estado real do repositório antes de editar qualquer documentação ou implementação.
- Preservar trabalho existente da dupla e evitar refatorações sem necessidade.
- Não transformar sugestões ou ideias em requisitos obrigatórios sem autorização explícita.
- Não iniciar etapas adicionais sem autorização.

## 2. Estado real do repositório

Este repositório está em fase de documentação e planejamento para um MVP de apresentação em hackathon. Não há protótipo funcional implementado nesta etapa.

- O arquivo [ingestao-bronze/src/api.py](ingestao-bronze/src/api.py) aparece apenas como placeholder de uma proposta anterior e não deve ser tratado como funcionalidade atual.
- O projeto não deve apresentar integração real com a operadora, nem prometer atendimento em produção.
- O foco atual é a jornada demonstrada e a documentação do escopo proposto.

## 3. Novo objetivo do projeto

Nome: hackathon-embarque-inclusivo.

Recorte: Linha 7–Rubi, em São Paulo.

Proposta: um protótipo de aplicativo para mobilidade inclusiva que reúne informações de acessibilidade, considera necessidades e rotinas do passageiro e facilita a solicitação de assistência durante a viagem.

O foco do hackathon é demonstrar a jornada de um usuário fictício em diferentes situações e mostrar como o aplicativo reage. O projeto também serve como portfólio, mas a arquitetura de dados não deve ampliar desnecessariamente o escopo.

## 4. Decisões de arquitetura atuais

- Python e Streamlit como base para o protótipo web, pensado para uso no celular.
- Prototipo não apresentado como aplicativo mobile nativo.
- Arquivos JSON para cadastro de estações, usuário fictício, rotinas e cenários.
- Estado das interações mantido inicialmente na sessão do Streamlit.
- Sem persistência permanente nesta primeira versão; encerrar a sessão pode reiniciar as interações.
- Entrada com conta de demonstração e login explicitamente simulado, sem autenticação real ou coleta de senhas.
- Sem arquitetura medallion.
- Sem Amazon S3, FastAPI, banco de dados, pipelines recorrentes, cloud ou serviços extras como requisitos do MVP.
- Sem análise de sentimento, processamento de relatos, dashboard empresarial, WhatsApp ou retroalimentação no escopo atual.
- Novas funcionalidades só entram por decisão futura explícita.

Manter separação simples entre dados, regras da aplicação e telas. Evitar abstrações ou serviços sem necessidade concreta.

## 5. Dados reais e dados simulados

Cadastro real:
- Identificador e nome da estação.
- Ordem da estação na linha.
- Endereço e integrações, quando confirmados.
- Recursos de acessibilidade publicados pela fonte.
- URL da fonte e data da consulta.

Regra de confiabilidade:
- Recurso ausente na fonte significa “não informado”, não “inexistente”.
- Presença de elevador não comprova funcionamento atual.
- Integrações futuras devem ser diferenciadas das disponíveis.
- Acessibilidade deve ser verificada para o acesso e o percurso relevantes, não resumida automaticamente a um único indicador.
- Identificadores devem conectar cadastro, percurso e eventos.

Dados simulados:
- Usuário fictício, suas preferências e rotinas.
- Movimento nas estações.
- Condições operacionais.
- Ocorrências.
- Solicitações e confirmações de assistência.
- Funcionários e pontos de encontro usados na demonstração.

Dados sintéticos não devem ser apresentados como medição real da operadora.

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

## 7. Acessibilidade, privacidade e validação

- Usar linguagem simples, rótulos claros e avisos que não dependam apenas de cores.
- Não prometer assistência nem acessibilidade sem confirmação.
- Verificar uso no celular, teclado e leitor de tela conforme aplicável, registrando o que ainda não foi validado.
- Usar apenas perfis fictícios na demonstração.
- Não versionar credenciais nem dados pessoais reais.
- Testar proporcionalmente à mudança.
- Distinguir planejado, implementado e validado.
- Não declarar testes que não foram executados.

## 8. Documentação

- Documentação em português brasileiro.
- Atualizar README e documentos técnicos conforme o estado real do repositório.
- Não criar infraestrutura ou arquivos de código vazios como se fossem implementações.
- Quando houver proposta futura, documentar como proposta e não como funcionalidade existente.
- Explicar mudanças e limitações ao final das tarefas.

## 9. Regras finais

- A solicitação atual do autor define escopo e autonomia.
- Trabalhar em mudanças pequenas e revisáveis.
- Não introduzir frameworks, bancos ou cloud sem necessidade e decisão explícita.
- Separar cadastro real, eventos simulados e estado da sessão.
- Não prometer assistência nem acessibilidade sem confirmação.
- Distinguir informações reais de simuladas claramente.
- Preservar trabalho existente da dupla.
- Não declarar conclusões que extrapolem o estado real do repositório.


