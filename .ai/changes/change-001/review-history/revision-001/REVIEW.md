# REVIEW — change-001

Revisão técnica não isolada (`NON_ISOLATED_REVIEW`) pelo adaptador codex, conforme política do projeto. Não constitui decisão humana de aprovação. Escopo: D006 e os dois arquivos em APPROVED-SCOPE.json. Nenhuma implementação foi alterada nesta revisão.

## Resultado técnico

Um achado P2 aberto. Recomenda-se corrigir o limite de captura antes de aprovar; a decisão pública continua pertencendo ao humano. Os 19 testes existentes passaram novamente, mas não cobrem volume de stdout/stderr. A implementação evita sucesso baseado apenas no launcher nos casos cobertos.

### R001 — P2 — captura de saída sem limite de bytes

CONFIRMED, OPEN. Evidência: `actions/dev_agent.py:393-397`, com padrão equivalente em `:361-364`. O launcher usa `subprocess.run(capture_output=True)`; stdout e stderr inteiros são acumulados em memória antes de `_vscode_output` registrar somente suas contagens. Não há limite de bytes, truncamento durante leitura ou estratégia de captura limitada. O timeout limita o tempo solicitado, não o volume que um CLI com erro ou wrapper no PATH pode produzir nesse intervalo. Isso deixa parcialmente atendido o critério 4 do CONTEXT (“com limites de tamanho”) e pode consumir memória desnecessária da aplicação.

Correção proposta para etapa autorizada posterior: impor orçamento explícito por stream durante captura, preservando diagnóstico seguro e indicando truncamento; adicionar teste que exceda o orçamento e confirme memória/saída limitada, sem lançar editor real. Não corrigido automaticamente. Não houve teste de stress ou exaustão de memória; o achado deriva da API e do fluxo estático de captura, não de incidente observado.

## Matriz de aceitação

| Critério | Resultado | Evidência e limite |
|---|---|---|
| 1 — janela associada à pasta | PASS nos casos isolados | Probe exige processo Code/code.exe e campo de título com caminho completo normalizado; não depende de PID novo. Testes executam o payload com fonte falsa. |
| 2 — incerteza sem sucesso | PASS nos casos isolados | Janela ausente, projeto diferente, basename/homônimos, processo sem janela e observação negada não confirmam. |
| 3 — falhas e fallback | PASS nos casos isolados | Ausência, erro de início, exit code, timeout, fallback com três candidatos e diretório inválido. |
| 4 — captura, diagnóstico e tamanho | PARCIAL — R001 | Captura/contagens sem conteúdo sensível nos logs; sem DEVNULL neste fluxo; falta limite de bytes de captura. |
| 5 — argumentos como dados | PASS estático/isolado | shell=False e URI em argumento separado; wrapper .cmd convertido em argv nativo de Code.exe/cli.js. |
| 6 — deadline e threading | PASS nos casos isolados | Relógio simulado inclui launcher e observação; timeout no subprocesso observador; sem widgets novos. Não equivale a medição real de latência ou garantia sobre I/O bloqueante do sistema. |
| 7 — chamadores | PASS nos casos isolados | Os dois chamadores registram bool verificado/não confirmado sem invalidar trabalho salvo; testes executam seus statements reais via AST. |
| 8 — testes focais | PASS com lacuna R001 | 19 testes passaram; não há caso de volume de saída. |

## Verificações e proveniência

- `python -B tests/test_dev_agent_vscode.py`: 19 PASS nesta revisão, por execução oficial permitida após python não resolvido no PATH restrito. Parsing de ambos os arquivos e mocks isolados; sem import geral do produto, modelos, chaves, GUI ou editor real.
- `git -c core.whitespace=cr-at-eol diff --check`: PASS. Configuração somente por comando para respeitar CRLF existente; configuração Git persistente não foi alterada.
- Hashes atuais iguais aos registrados em DEVELOP: actions/dev_agent.py `3d48b90554a97c7903774a404da94c831d8f607b507d3e08b5e5aab367f88c85`; tests/test_dev_agent_vscode.py `3c9e22694e1d20f7dfb9379c6ae2b7bc44b5f059ec72c0e9375716963d8c921a`.
- ENCODING-BASELINE.json: SHA-256 `8f65b8a62fe9a3df1c0f23d1a6530b33d6efec898050c2d785b41ad03aa21443`, igual ao vínculo em APPROVED-SCOPE.json. Todos os alvos foram revalidados em UTF-8 estrito, sem BOM; CRLF preservado no fonte existente; teste novo UTF-8 sem BOM. Nenhuma migração autorizada ou observada. A conclusão canônica deve realizar também o guard de encoding e produzir sua evidência oficial.
- Escopo produto/teste: actions/dev_agent.py alterado e tests/test_dev_agent_vscode.py novo. Governança preexistente untracked não foi tratada como implementação adicional.

## Limitações e gate humano

Teste manual do editor e integração completa da aplicação não executados. Títulos padrão sem caminho completo continuam como não verificados; observação indisponível em plataformas ou executável empacotado também não confirma. Essas limitações estão expressas no contexto e em DEVELOP, sem alegação de funcionamento integrado/multiplataforma. Intenção histórica de encoding sem BOM permanece UNKNOWN; a validação estabelece apenas bytes válidos e preservação. Nenhuma dependência externa material foi criada para concluir esta revisão documental; não houve investigação de fornecedor ou expansão além da responsabilidade autorizada.

Lease desta revisão: `8e21d2f2-17b7-4b46-84f4-73cd3da9035a`, adquirido nesta sessão e validado antes das verificações. Nenhum worker permanece ativo. Não foi adotado token de DEVELOP. Conclusão técnica deve produzir REVIEW_PENDING; referência humana de decisão e waiver permanecem ausentes. CLOSE continua bloqueado até decisão permitida pelo runtime.

Formas públicas disponíveis após REVIEW_PENDING:

- `$ai-sdd review approve '<referência-do-revisor>'`
- `$ai-sdd review changes-requested '<referência-do-revisor>'`
- `$ai-sdd review waive '<referência-do-revisor>' '<referência-do-waiver>'`

Referências devem ser explícitas e literais; aprovação de DEVELOP não fornece decisão de REVIEW. Nenhuma dessas alternativas foi selecionada automaticamente.
