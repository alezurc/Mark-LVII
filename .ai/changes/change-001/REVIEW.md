# REVIEW — revisão 002 — change-001

Resultado técnico: **R001/P2 corrigido e verificado no escopo avaliado; nenhum novo achado material identificado**. Decisão humana de aprovação permanece pendente. Revisão não isolada (`NON_ISOLATED_REVIEW`) pelo adaptador codex, conforme a política declarada; não se apresenta como validação independente.

## Continuidade

Reavaliação da implementação após CONTEXT revisão 002 e nova aprovação registrada pelo runtime. Fonte da correção: DEVELOP-REVISION-002.md. O relatório anterior foi preservado byte a byte em `review-history/revision-001/REVIEW.md`, SHA-256 `6452e5ab980cd2f49b6795a83a755bf8be07661abeffc61ceef5a7180fe24d85`. Seu resultado histórico R001 OPEN e a decisão REVIEW_CHANGES_REQUESTED não foram reclassificados retroativamente. O estado RESOLVED abaixo descreve apenas a evidência atual.

## R001 — captura sem limite — RESOLVED nesta revisão

CONFIRMED pela inspeção dos helpers `_vscode_capture` / `_vscode_read_ready`, dos dois pontos de uso e pelos testes executados novamente. stdout/stderr agora têm buffers fixos separados de 65.536 bytes. Resultados e exceções retêm views dos buffers; não há captura integral seguida de truncamento. Os reads têm teto de 8.192 bytes e passam a solicitar um byte ao atingir o limite para distinguir EOF de excesso. A captura não depende de queue/spool ou thread leitora.

Overflow em qualquer stream interrompe a operação e não leva a outro candidato nem a confirmação de janela. O log informa stream, teto e truncamento sem conteúdo bruto. O helper encerra apenas seu subprocesso próprio quando necessário, aguarda com timeout e fecha ambos os pipes em finally. Há reserva de cleanup dentro do timeout; não foi acrescentada espera ilimitada. A leitura dos dois pipes é alternada e não bloqueante no perfil testado.

O finding anterior de retenção proporcional ao volume emitido não se reproduz pela nova estratégia: o armazenamento possui capacidade fixa por subprocesso, com um bloco transitório de leitura limitado. As fixtures verificaram buffers reais e tamanhos dos pedidos de leitura, não apenas tamanho do log final.

## Matriz dos critérios aprovados

| Critério | Avaliação | Evidência |
|---|---|---|
| 1–2 — confirmação/ambiguidade | PASS nos casos isolados | Payload de observação com janelas falsas: caminho completo, janela existente, outro projeto, homônimos, processo sem janela e observação negada. |
| 3 — falhas/fallback | PASS nos casos isolados | Ausência, erro ao iniciar, status não zero, timeout e até três candidatos. |
| 4 — captura e logs | PASS para a correção avaliada | Captura limitada; diagnóstico de recebimento por contagem, status/timeout/excesso; sem DEVNULL ou conteúdo bruto neste fluxo. |
| 5 — argv sem shell | PASS estático/isolado | URI em argumento separado; wrapper Windows convertido em Code.exe/cli.js. |
| 6 — prazo/threading | PASS nos casos testados | Deadline compartilhado simulado; timeout real de fixture e reserva para cleanup; sem Qt ou leitores em threads. Não é garantia de tempo real sobre I/O do sistema operacional. |
| 7 — chamadores | PASS nos casos isolados | Ambos distinguem bool confirmado/não confirmado; trabalho salvo não é invalidado pela abertura. |
| 8 — regressões | PASS | Preservados os 19 cenários anteriores. |
| 9 — limites de retenção/leitura | PASS | Buffers reais de 65.536 bytes e reads de até 8.192; sem communicate/capture_output no helper. |
| 10 — excesso e cleanup | PASS nos casos testados | Excesso em launcher/observador não confirma nem faz fallback; subprocessos de fixture colhidos e pipes fechados. |
| 11 — fronteira/concorrência | PASS nos casos testados | EOF exatamente no teto aceito; primeiro byte adicional rejeitado em ambos os streams; dois streams ativos, um fechado cedo e silêncio. |
| 12 — provas de limite | PASS | 29 testes com subcasos de abaixo/no/acima do teto, excesso contínuo, timeout, cleanup e proteção de logs. |

## Verificações desta revisão

- `python -B tests/test_dev_agent_vscode.py`: **29 PASS**, suíte concluída em 1,385 s nesta execução. Permissão oficial aplicada após python não resolvido no PATH restrito; sem alterar PATH ou substituir intérprete. Fixtures locais apenas emitem dados sintéticos/aguardam sob timeout. Os testes afirmam término dos subprocessos próprios, pipes fechados e ausência de threads leitoras residuais.
- Parsing de ambos os arquivos ocorre na carga da suíte. Sem import geral do produto, editor real, GUI, modelos, credenciais ou serviços externos.
- `git -c core.whitespace=cr-at-eol diff --check`: PASS; nenhuma configuração Git persistente alterada.
- UTF-8 estrito sem BOM em todos os alvos. CRLF de actions/dev_agent.py e LF do teste preservados; nenhuma migração proposta ou observada. Intenção histórica de encoding sem BOM permanece UNKNOWN.
- ENCODING-BASELINE.json SHA-256 `cc365165afe8fdec0612111cb5d75c9f41277da5a962ce5de43cb8db382fd619`, igual ao vínculo em APPROVED-SCOPE.json. O guard canônico de conclusão revalida e registra ENCODING-REVIEW.json; não editar esses artefatos manualmente.

Hashes dos alvos revisados, iguais aos de DEVELOP revisão 002:

- actions/dev_agent.py: `a037c36d50dac943fe18168fe9a3e278f7c94e4d159ae8c0554ee31ace344d8c`
- tests/test_dev_agent_vscode.py: `e87a0e53312e8c12073d87642e268b936445b3ff74cd38aa5194dd425a0885ce`

## Limitações e gate

Sem teste manual do editor e sem validação integrada da aplicação. Títulos de janela que não exponham caminho completo permanecem não verificados; plataformas sem observação e executável empacotado também não confirmam. Fixtures reais sustentam somente o ambiente em que foram executadas; não se alega cobertura real de todos os sistemas. Essas limitações preservam o comportamento conservador aprovado e não reabrem investigação externa. Nenhuma nova dependência material de fornecedor/plataforma foi necessária para a revisão; nenhuma expansão de escopo ou correção automática ocorreu.

Lease REVIEW desta sessão: `ac5dc99e-758d-47fd-8989-80323ca1d9f5`, adquirido por begin-stage e validado por check-stage. Todos os testes/fixtures terminaram. Nenhum arquivo de implementação foi alterado durante REVIEW.

Conclusão técnica deve registrar REVIEW_PENDING, sem referência humana de decisão inferida. CLOSE continua bloqueado até decisão permitida pelo runtime. Opções, exigindo referências explícitas:

- `$ai-sdd review approve '<referência-do-revisor>'`
- `$ai-sdd review changes-requested '<referência-do-revisor>'`
- `$ai-sdd review waive '<referência-do-revisor>' '<referência-do-waiver>'`

Nenhuma dessas decisões foi executada automaticamente.
