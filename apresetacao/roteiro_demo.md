# Roteiro de demonstração

## 1. Problema apresentado

A demonstração mostra uma pessoa que precisa viajar em um trecho da Linha 7–Rubi e enfrenta incerteza sobre acesso, apoio e condições do percurso. O aplicativo busca responder: a estação oferece suporte adequado para a minha viagem? Existe alguma condição que pode afetar o deslocamento? Como solicitar ajuda de forma clara e segura?

O foco não é apresentar um sistema operacional real, e sim ilustrar um protótipo de decisão em contexto de mobilidade inclusiva.

## 2. Perfil e necessidade do usuário

Usar um usuário fictício, por exemplo Alex, que utiliza cadeira de rodas e tem uma rotina de deslocamento.

Perfil ilustrativo:
- Nome fictício: Alex.
- Necessidade: mobilidade com cadeira de rodas.
- Rotina: deslocamento frequente entre duas estações da linha.
- Objetivo: chegar ao destino com segurança e previsibilidade.

A informação sobre deficiência deve ser opcional e não depender de diagnóstico. A pergunta relevante é: qual apoio a pessoa precisa durante a viagem?

## 3. Jornada principal

1. A pessoa entra no app com uma conta de demonstração.
2. O app mostra que a autenticação é simulada e não é real.
3. O usuário informa seu perfil e necessidades de acessibilidade.
4. O sistema apresenta a rotina habitual e permite alterar origem, destino e horários.
5. A pessoa consulta seu percurso e recebe informações conhecidas sobre acessibilidade.
6. O app mostra condições simuladas relevantes para a viagem.
7. Se houver impacto, explica por que a situação afeta o acesso necessário.
8. O usuário solicita assistência.
9. O sistema acompanha o estado da solicitação, como pendente, confirmado ou concluído.
10. Quando houver confirmação simulada, o app informa responsável e ponto de encontro fictício.

## 4. Os quatro cenários

### Cenário 1: baixo movimento
- Horário de referência: 22h.
- Sem ocorrências.
- A jornada é estável e a pessoa vê um percurso simples e previsível.

### Cenário 2: movimento moderado
- Horário de referência: 14h.
- Sem ocorrências.
- O app mostra uma rotina normal, sem impactos relevantes.

### Cenário 3: horário de pico
- Horário de referência: 7h30.
- Movimento intenso, sem ocorrências.
- A demonstração reforça que o pico de movimento sozinho não basta para gerar uma ocorrência; ele aumenta a pressão da viagem.

### Cenário 4: horário de pico com ocorrência
- Horário de referência: 7h30.
- Movimento intenso e ocorrência programada.
- Exemplo: indisponibilidade simulada de elevador que afeta um acesso necessário à viagem do usuário.
- O app explica o impacto e permite solicitar orientação.
- Somente oferece alternativa de percurso se houver uma alternativa verificada.

## 5. Ações do apresentador

O apresentador deve:
- iniciar a conta de demonstração;
- escolher o cenário;
- avançar eventos de forma determinística;
- mostrar como o app responde aos diferentes contextos;
- explicar que os dados são simulados e não representam operação real;
- reforçar que a assistência confirmada é fictícia e pode ser reiniciada.

## 6. Reações esperadas do aplicativo

- Rótulos claros e linguagem simples.
- Avisos que não dependam apenas de cor.
- Explicação do impacto do problema para aquele usuário e aquele percurso.
- Indicação de que a informação é desconhecida quando não houver confirmação.
- Solicitação de assistência com estado visível e sem confundir pedido com atendimento confirmado.
- Reinício dos cenários sem manter eventos anteriores na sessão.

## 7. Distinção entre informações reais e simulações

A demonstração deve deixar explícito que:
- o cadastro de estações e recursos é real apenas quando a fonte oficial tiver publicado informação;
- recursos ausentes na fonte são “não informados”, não “inexistentes”;
- a presença de elevador não garante que ele esteja funcionando;
- dados de usuário, preferências, rotina, cenário, ocorrência e assistência são simulados;
- a operadora não foi integrada e não há atendimento real.

## 8. Critérios para considerar a demonstração pronta

A demonstração pode ser considerada pronta quando:
- a jornada principal está clara e compreensível;
- os quatro cenários estão alinhados com o roteiro;
- a experiência diferencia dados reais de simulados;
- o app explica por que a ocorrência afeta aquela viagem;
- a assistência é apresentada como simulada;
- a ação de reiniciar remove o estado anterior da demonstração;
- a interface funciona bem em celular e com teclado;
- os limites do protótipo ficam explicitados durante a apresentação.

## 9. Observação sobre o escopo

Este roteiro é planejado e não comprova funcionalidade implementada. Ele serve para orientar a apresentação do MVP e a documentação do projeto, mantendo o escopo consistente com o estado real do repositório.
