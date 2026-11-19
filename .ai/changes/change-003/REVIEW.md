# REVIEW — change-003 — D007 e D011

## Resultado técnico

Não foram identificados achados acionáveis ou bloqueadores na implementação revisada, dentro do perfil sintético local aprovado. Os critérios AC1–AC8 têm evidência compatível com o alcance delimitado. Esta é uma conclusão técnica; a decisão humana continua pendente e não há autorização de CLOSE.

Limitação informada pelo runtime: NON_ISOLATED_REVIEW. Revisão executada por codex na mesma sessão que implementou a mudança; não constitui avaliação independente por outro agente/humano. Não houve delegação nem correção automática durante REVIEW.

## Autorização, método e escopo

Estado de entrada: DEVELOP_COMPLETED, active_change_id=change-003. CONTEXT aprovado com referência `Aprovo a pós revisar o CONTEXT.md`. A preparação de ambiente foi autorizada posteriormente pelo humano com a mensagem iniciada por `Autorizo explicitamente a retomada do DEVELOP da change-003, com o seguinte escopo:`, registrada em RESUMPTION-DEP-001.md; a parada DEP-001 original e a primeira tentativa foram preservadas. A invocação `$ai-sdd review` autoriza esta revisão técnica, sem fornecer decisão humana de approve/waive/changes-requested.

Roteamento: REVIEW/ORCHESTRATOR/codex, ALLOW, v0.2.0 CORE IN, sem expansão; lease fresco `e91c7b73-f77d-49f7-a0ce-1968e6cacf18`. Check-stage retornou VALID antes dos lotes. Os comandos canônicos inicialmente receberam Acesso negado de python.exe e foram repetidos uma vez por operação pelo mecanismo oficial, preservando launcher/argumentos/projeto.

Inspecionados: CONTEXT, APPROVED-SCOPE, ENCODING-BASELINE/POLICY, DEVELOP, autorização de retomada, diffs de providers/_tests.py e README contra snapshots pré-mudança, três testes novos, AGENTS.md, registros de validação e seus hashes. O snapshot inicial do provider coincide com o hash de contexto. Os seis alvos aprovados coincidem com FINAL-VALIDATION.json e permaneceram inalterados desde DEVELOP. CHANGELOG permanece reservado ao CLOSE. Mudanças anteriores em outros componentes não foram atribuídas a esta change.

Não foram editados produto, testes, requisitos, contexto, baseline ou decisões. Foram escritos somente este relatório, REVIEW-EVIDENCE.json e logs separados da revisão. Não houve acesso ao conteúdo de memória/configuração pessoal, chamadas de modelo/serviço externo, instalação adicional ou execução da aplicação principal.

## Critérios de aceitação

| Critério | Resultado | Evidência e alcance |
|---|---|---|
| AC1 — controles/PCM | Conforme | Diff troca somente o literal de áudio por escapes equivalentes nesse ponto; testes AST verificam bytes([1,2])*1000 e rejeitam controles/PCM alterado. As demais edições são de isolamento/relato autorizados. |
| AC2 — encoding | Conforme | Política de migração prospectiva aprovada para providers/_tests.py; seis alvos UTF-8 estrito sem BOM, CRLF preservado em provider/README e LF nos novos testes/CHANGELOG. Baseline íntegra e vinculada à aprovação. Intenção histórica continua UNKNOWN. |
| AC3 — isolamento | Conforme no perfil avaliado | Runner cria árvore temporária de fontes antes dos imports do filho, não copia dados/modelos, redireciona diretórios de perfil/cache/temp; painel usa config_manager com destinos temporários; patches de voz bloqueiam download/síntese. |
| AC4 — integração/recursos | Conforme no perfil avaliado | Suíte providers exercitou types.Blob, TaskGroup, tool loop, HTTP fragmentado em loopback, PCM/resampling, filtros e painel Qt offscreen. Timeout externo, cleanup de tasks e shutdown/server_close/join estão presentes. |
| AC5 — resultados honestos | Conforme | PASS/FAIL/SKIP separados, contadores resetados; testes negativos de falha/exceção/retorno/timeout e reentrada. Ausências opcionais não contam como PASS. |
| AC6 — harness | Conforme | Harness e loader reais com projetos/plugins sintéticos; import válido/falho, worker, chamadas de player, player=None no loader, rejeição de PLUGIN inválido, erro em run, relatório inválido/ausente/exit não zero e timeout. Perfil jarvis verifica QApplication no principal e stub de modelo. |
| AC7 — falhas/cleanup | Conforme no perfil avaliado | Falhas injetadas em temporário/runner/painel/vozes, restauração de patches e remoção de diretórios; guard contra escrita fora da árvore e conexão externa. Guard é auxiliar de teste, não sandbox de segurança universal. |
| AC8 — documentação/evidência | Conforme | README descreve comandos e limites; DEVELOP e logs registram versões/retornos/skips; três suítes novas e duas regressões reexecutadas. Sem anúncio de release ou edição antecipada de CHANGELOG. |

## Testes reexecutados nesta revisão

Ambiente: `.venv/Scripts/python.exe`, Python 3.15.2 AMD64, sem system-site-packages. Versões do ambiente registrado: google-genai 2.34.0, httpx 0.28.1, numpy 2.5.5, PyQt6 6.12.1, psutil 7.2.2; dependências transitivas em venv-packages.json. Hash desse inventário e dos logs de DEVELOP foi reconferido. Não se modificou requirements.txt (SHA-256 `1ca35b1d79ecfe78726476fb17c58df999b0021ab34135b0bd7779879430063e`).

| Comando | Retorno | Resultado | Duração |
|---|---|---|---|
| .venv/Scripts/python.exe -m unittest discover -s tests -p 'test_*.py' -v | 0 | 55 PASS, zero FAIL/SKIP | 5,946 s no unittest |
| .venv/Scripts/python.exe -m providers._tests | 0 | 98 PASS, zero FAIL, 2 SKIP | 9,744 s no executor |

Logs integrais: review-unittest.log e review-providers.log. REVIEW-EVIDENCE.json vincula seus hashes, baseline e os seis alvos. Os 55 casos incluem 13 novos e 42 regressões; as 98 verificações providers usam contagem própria e não são somadas como casos unittest.

## Encoding e integridade

SHA-256 de ENCODING-BASELINE.json: `b1e70e27b3ca4456ccbdf448f9e5bc3eae27ce6fba36454db59bf6754c9662fd`, igual a APPROVED-SCOPE.encoding_sha256. Migração UNKNOWN -> UTF-8/NONE de providers/_tests.py está explicitamente na política aprovada; não é inferência de codepage histórica. Novos arquivos estavam MISSING na baseline e têm o perfil textual proposto. CHANGELOG mantém o hash original. Nenhum alvo foi recodificado inesperadamente; a validação normativa final de encoding será executada pelo runtime ao concluir REVIEW.

## Limites e riscos residuais

- Piper não instalado: dois SKIPs explícitos, permitidos pelo contexto. Não demonstrada síntese real nem download de vozes; testes de isolamento usam arquivos sintéticos e patches.
- Python 3.15.2 está além da faixa historicamente testada 3.11–3.13 documentada pelo projeto, embora setup.py permita versões novas com aviso. Os resultados sustentam somente o perfil executado; não são certificação de versões/plataformas adicionais.
- Qt offscreen, áudio sintético e HTTP loopback não provam UI interativa, áudio físico, serviços reais ou recuperação após crash. D011 tem ampliação de evidência local, não garantia integrada universal; D007 não resolve intenção histórica sem BOM.
- O guard de auditoria se aplica ao filho Python de teste e não oferece isolamento de segurança para plugins arbitrários/subprocessos externos. As fixtures do harness são controladas; plugins reais não foram executados.

Esses limites estão explícitos no contexto/documentação e não constituem novo impedimento material para a mudança delimitada. Não foi acionado novo boundary externo nem investigado qualquer ramo além da autorização. Findings históricos/KR não foram reclassificados nesta revisão.

## Decisão humana pendente

Concluir tecnicamente pelo runtime resulta em REVIEW_PENDING. Não se escolhe decisão, referência ou waiver pelo humano. As três formas disponíveis são:

```text
$ai-sdd review approve "<referência explícita do revisor>"
$ai-sdd review changes-requested "<referência explícita do revisor>"
$ai-sdd review waive "<referência explícita do revisor>" "<referência explícita do waiver>"
```

CLOSE permanece bloqueado até decisão humana válida. Nenhuma etapa posterior é executada automaticamente.
