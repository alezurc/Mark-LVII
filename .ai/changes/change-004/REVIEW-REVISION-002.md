# REVIEW — change-004 — revisão 002

Revisão técnica concluída sem novos achados materiais no escopo examinado. R004-001 e R004-002 estão tratados nesta revisão, conforme código e regressões atuais. Isso não altera o resultado histórico da primeira REVIEW nem representa aprovação humana. Destino da conclusão técnica: REVIEW_PENDING; CLOSE depende de decisão humana explícita.

## Proveniência e limites

Adaptador codex; papel ORCHESTRATOR; Core v0.2.0; autorização ALLOW em capability, project_policy, stage_policy, role_policy, approved_scope e human_gates; sem expansão. Limitação retornada: NON_ISOLATED_REVIEW, pois a sessão também participou da implementação. Lease exclusivo adquirido nesta execução: 9ba8ef32-e62a-4741-bc89-43efc2386c4b. Referência de CONTEXT aprovada: “Aprovo o CONTEXT revisão 002 da change-004”.

Foram lidos CONTEXT revisão 002, escopo/aprovação, instruções canônicas REVIEW, contrato Day 2 e Boundary Stop Condition, relatório e diff de DEVELOP revisão 002. A revisão examinou as alterações reais dos quatro arquivos, os caminhos originais de persistência/seleção, testes e documentação. Não houve edição de produto, correção automática, instalação, serviço externo, alteração de settings pessoais, commit, tag ou publicação.

## Achados anteriores

- R004-001: tratado nesta revisão. As três rotinas plain/code/review mantêm apresentação normal por padrão; a retradução usa present=False e evita reveal, glance e timestamp novo. Mantém splitter, conteúdo dispensado e quiz ativo. Cursor/seleção são remapeados com offsets UTF-16 e a rolagem é restaurada. As regressões usam a rotina real de revelação sob spy, verificam tamanhos efetivos e confirmam que um resultado novo ainda abre o painel.
- R004-002: tratado nesta revisão. A pintura real marca FILE/FOLDER e o molde da contagem, preservando nome/extensão como valores opacos. Testes verificam en → pt-BR → en, 0/1/2/5000, singular/plural, marcador +, arquivo sem extensão e CLOSE.CLOSE; um mock falha se houver reenumeração da pasta carregada.

Nenhum novo achado acionável identificado. Os relatórios REVIEW.md e REVIEW-EVIDENCE.json anteriores permanecem intactos; sua decisão changes_requested continua sendo evidência histórica, sem promoção retroativa.

## Matriz de aceitação

| Critério | Resultado e evidência |
| --- | --- |
| AC1 | PASS no perfil testado: seletor com valores estáveis, inglês padrão, cancelar, aplicar e erro de gravação sem falso sucesso. Testes puros e cenário Qt original reexecutados. |
| AC2 | PASS: config_manager continua responsável pela persistência e preservação dos demais settings; ui.py carrega antes da janela; testes verificam ausência de callback de voz na troca isolada. |
| AC3 | PASS no perfil testado: bindings explícitos e listeners atualizam textos sem reconstruir a aplicação; input, seleção, conteúdo, quiz e callbacks preservados nos cenários cobertos. |
| AC4 | PASS: fallback, normalização, placeholders, composição e catálogo validados; quatro mensagens novas têm tradução; nenhum serviço de tradução. |
| AC5 | PASS no escopo revisado: atualização de superfícies existentes preservada; labels carregados corrigidos; valores sentinela e nomes técnicos continuam opacos. Não constitui prova exaustiva de toda combinação dinâmica. |
| AC6 | PASS no perfil offscreen Windows: mesmas APIs Qt no principal, nenhuma QApplication ou widget em worker novo; botão do quiz acomoda RESPONDER. Acessibilidade integral e todas as resoluções permanecem UNKNOWN. |
| AC7 | PASS: seis testes puros, configurações temporárias, defaults, outros settings e falha de escrita. |
| AC8 | PASS no perfil delimitado: cinco testes Qt em subprocessos com timeout, guards, dados sintéticos e retorno verificado. Renders examinados; sem sessão real ou áudio físico. |
| AC9 | PASS: 12 arquivos revalidados, baseline aprovado intacto, UTF-8 estrito sem BOM e CRLF/LF preservados; README continua coerente; CHANGELOG reservado a CLOSE. Intenção histórica de encoding continua UNKNOWN. |
| AC10 | PASS: conteúdo dispensado não reabre; quiz mantém espaço; splitter não muda; resultado novo abre nos três tipos. |
| AC11 | PASS: quiz na segunda pergunta, resposta anterior e entrada em andamento, flags e tamanhos, sem callbacks adicionais; painel visível preserva seleção com emoji/acentos e rolagem positiva nos dois sentidos. |
| AC12 | PASS: FILE/ARQUIVO, FOLDER/PASTA e contagem correta; nome, extensão e estado carregado preservados, sem reload. |
| AC13 | PASS: painter real alcançado com captura de textos e widget real renderizado; contagens e sentinelas requeridos cobertos. |

## Verificação desta REVIEW

- `python -m unittest discover -s tests -v`: exit 0, 66 testes PASS em 19.087s; REVIEW-REVISION-002-UNITTEST.log. Inclui 11 testes de idioma, cinco deles Qt.
- `python -m providers._tests`: exit 0, 98 PASS, 0 FAIL, 2 SKIP; REVIEW-REVISION-002-PROVIDERS.log. Piper ausente: seleção de idioma e síntese não exercitadas; skips não contados como PASS.
- Verificação independente dos 12 caminhos em REVIEW-REVISION-002-ENCODING-CHECK.json: SHA256 atuais iguais aos da implementação entregue; baseline aprovado d7087977fb69c8a593e6c07ad3ae2fc9e11c4f96f308dd4a7f64a115b542968d; quatro alterados e oito idênticos ao aprovado. UTF-8 estrito sem BOM, CRLF/LF preservados. Manifests históricos DEVELOP-EVIDENCE.json, REVIEW-EVIDENCE.json e DEVELOP-REVISION-002-EVIDENCE.json conferidos integralmente.
- `git -c core.whitespace=cr-at-eol diff --check -- gui/window.py gui/widgets.py`: exit 0.
- Inspeção focal dos renders finais existentes, com hashes conferidos: rev2-quiz-code-en.png e pt-BR mostram pergunta e resposta em andamento com quiz visível e botão inteiro; rev2-folder-en.png e pt-BR mostram FOLDER preservado e legenda traduzida; rev2-file-pt-BR.png mantém FILE como nome e ARQUIVO como legenda. Não foram usados os grabs diagnósticos isolados do quiz.

Ambiente reutilizado: Windows, Python 3.15.2, PyQt6 6.12.1, Qt 6.12.0. Testes isolam perfil/configuração e impedem rede/escrita externa. Execução normal do launcher recebeu Acesso negado; repetição idêntica pelo mecanismo oficial autorizado teve sucesso. A tentativa normal de unittest falhou antes de iniciar Python com erro de redirecionamento/StandardOutputEncoding; a repetição autorizada completou. Não se inferiu Python ausente nem se alterou PATH/ACL/política.

Persistem os limites declarados: NON_ISOLATED_REVIEW, evidência sintética/offscreen, UI interativa em outras plataformas/resoluções, fallback de fontes/ícones, acessibilidade integral, áudio físico e serviços reais UNKNOWN. Os registros históricos de boundary DEP-004-001 foram preservados; nenhuma nova dependência externa material foi identificada nesta revisão.

## Decisão humana pendente

Concluir apenas REVIEW técnica. Formas suportadas, com referências humanas explícitas:

- `$ai-sdd review approve <reviewer-reference>`
- `$ai-sdd review changes-requested <reviewer-reference>`
- `$ai-sdd review waive <reviewer-reference> <waiver-reference>`

Não selecionar decisão, inferir referência de aprovação anterior ou executar CLOSE automaticamente.
