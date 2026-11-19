# CONTEXT — change-003 — D007 e D011

## Intenção e origem

Pedido humano nesta conversa: `tratar a D007 e D011`, após `$ai-sdd context change-003`. Preparar uma mudança verificável para tratar os controles opacos identificados em providers/_tests.py (D007) e produzir evidência comportamental local, repetível e isolada para providers e smoke harness (D011). Não declarar validação universal da aplicação nem reconstruir a intenção histórica de encoding.

Proposta de CONTEXT; human_gate PENDING, referência NONE. Não há autorização de DEVELOP. Não reutilizar referências das changes anteriores. Este documento não implementa a mudança.

## Evidência consultada

O DISCOVERY comparado discovery-2026-11-18-01 preserva D007 como UNKNOWN e D011 como UNKNOWN. Seu texto é anterior ao encerramento de change-002; não tratá-lo como inventário atual de resultados de testes. KR-change-001-002 e KR-change-002-002 preservam UNKNOWN da intenção histórica de encoding; KR-change-001-001 e KR-change-002-001 registram evidência focal de changes fechadas, sem demonstrar integração geral.

Inspeção estática atual, sem executar testes, importar o app, ler dados pessoais ou acessar serviços:

| Fonte | SHA-256 dos bytes consultados | Observação |
|---|---|---|
| providers/_tests.py | b4a8a1ea4bc373efb97d036cb61b6c49dae2786758bd9afd4812592edb49fcda | UTF-8 estrito válido, sem BOM, 1110 CRLF; dois controles literais U+0001/U+0002 em TTS.speak de test_it_speaks_before_the_tool_runs |
| core/_smoke_harness.py | 25081959d547c3a9dc55227f389e497f87528a038d59e6d99c71948b6c92ac51 | UTF-8 válido sem BOM, 207 CRLF; subprocesso recebe ROOT/SPEC e emite @@REPORT@@ |
| memory/config_manager.py | e0301bb17b2d733def5d1a15b77a2abd4a2e32986981a4b2e8b196b0fce1d528 | CONFIG_DIR/CONFIG_FILE globais; setters passam pelo gerenciador |
| providers/tts_piper.py | e7ca234abafb73807651b60f5026aac631906b3a1b7d9e93b568394017407ccd | _VOICE_DIR inicializa no import e pode criar pasta/probe; testes atuais consultam vozes instaladas |
| README.md | 2529f75d0fdf6c3805b00828be8a7da65321aee870f10c23752446df51e5dcf4 | UTF-8 válido sem BOM, 1025 CRLF; documenta python -m providers._tests |
| CHANGELOG.md | fdd512f84650edce0d074b9b4debef932d63ef699d23bd4c0b93391ee6fed768 | UTF-8 válido sem BOM, 23 LF |
| .ai/DISCOVERY.md | 9361d0d3e0ca734710661efb7272eeb3315ff181544c6e3626b55770a2aafa3e5 | Fonte dos IDs D007/D011 |

CONFIRMED por inspeção: test_panel_settings_survive lê e modifica config/api_keys.json real e tenta restaurar providers; isso não isola outros efeitos nem falhas/interrupções. test_voice_folder_is_writable escreve na pasta selecionada pelo módulo; o import de tts_piper já pode escrever. test_costs_nothing_when_unused cria temporário em subprocesso sem cleanup explícito ou timeout. Skips opcionais são hoje contabilizados como PASS. O harness usa stubs de core.gemini, mas isso não constitui isolamento de rede geral para plugins arbitrários.

O working tree já contém mudanças de produto e dados anteriores a este CONTEXT. Não revertê-las, atribuí-las a change-003 ou lê-las para expandir o escopo. Revalidar hashes antes de DEVELOP e revisar somente o diff desta mudança.

## Escopo e exclusões

SCOPE.json é a lista exata de seis alvos editáveis:

- providers/_tests.py: escapes dos controles, isolamento da suíte, cleanup/timeouts e relato fiel de PASS/FAIL/SKIP. Preservar testes e contratos existentes.
- tests/test_source_encoding.py: regressão da equivalência semântica do áudio sintético e ausência de controles literais inesperados no alvo delimitado.
- tests/test_provider_test_isolation.py: provas de isolamento, falhas e restauração dos recursos da suíte.
- tests/test_smoke_harness.py: integração do harness existente com fixtures sintéticas descartáveis, em subprocessos limitados.
- README.md: instruções de execução, requisitos, perfil offline/local e alcance da evidência.
- CHANGELOG.md: entrada por change-id somente no CLOSE após REVIEW, conforme PROJECT-POLICY.md.

core/_smoke_harness.py, core/code_checks.py, providers de produção, config_manager, UI e testes existentes são referências de leitura/regressão. Não editar esses módulos nesta mudança. Não editar findings históricos, baseline ou Knowledge Register manualmente para alegar resolução. Avaliar registros duradouros pelo mecanismo de CLOSE. Sem instalação de dependências, downloads de modelos, chamadas de API, áudio físico, navegador, memória/configuração pessoal, servidor externo, versão, commit, tag ou publicação.

## Critérios de aceitação

AC1 — D007: substituir os bytes literais 0x01/0x02 em providers/_tests.py por escapes textuais Python equivalentes. Provar que o literal continua produzindo exatamente bytes([1, 2]) * 1000 e que nenhuma alteração incidental afeta Unicode, BOM ou CRLF. Não remover controles indiscriminadamente nem mudar o áudio para silêncio. Teste focal deve falhar para regressão dos controles e para alteração dos bytes sintetizados.

AC2 — D007: aplicar somente a migração prospectiva explícita de ENCODING-POLICY.json após aprovação humana. Destino UTF-8 sem BOM, CRLF preservado; nenhuma conversão global do repositório. Bytes válidos sem BOM não provam intenção histórica; esse UNKNOWN permanece. Novos testes serão UTF-8 sem BOM, LF. README preserva CRLF e CHANGELOG preserva LF. Revalidar encoding/BOM de todos os alvos baselineados no REVIEW.

AC3 — D011: python -m providers._tests deve operar com configuração, caches e vozes sintéticos em TemporaryDirectory, isolados antes de import/call com efeitos. Não ler, copiar ou restaurar dados pessoais reais como estratégia de isolamento. Operações de settings usam config_manager com destinos redirecionados; não escrever config/api_keys.json real. Impedir efeitos de _voice_dir no import no projeto/perfil real e impedir downloads/síntese física. Piper opcional deve ser simulado ou explicitamente SKIP, sem usar vozes reais. Fixtures e alterações globais são desfeitas também em exceção.

AC4 — D011: preservar a execução dos testes de formas de chamada types.Blob, TaskGroup/tool loop, streaming HTTP fragmentado, transcrição/PCM sintético, filtros e painel Qt. Servidor de teste liga somente em loopback e porta efêmera; shutdown e server_close em finally. Nenhum serviço fora do host. Subprocessos têm timeout, saída/returncode capturados e diagnóstico; joins/tasks têm término limitado e cleanup. Qt offscreen no thread principal de processo de teste, com uma QApplication; nenhum widget em worker. Não importar main.py para iniciar a sessão real.

AC5 — D011: relato diferencia PASS, FAIL e SKIP, com motivos e contagens; skip não incrementa PASS. Ausência de requisito obrigatório é erro explícito ou SKIP claramente reportado como cobertura ausente; não anunciar suíte integral validada. Asserção falha ou exceção gera status de saída não zero. Reentrância no mesmo processo não acumula contadores ou recursos da execução anterior. Não silenciar erros para tornar a suíte verde.

AC6 — D011: testes do smoke harness usam apenas projetos/fixtures sintéticos temporários e o harness real como subprocesso, sem executar plugins reais. Demonstrar import bem-sucedido e falho, plugin válido executado em worker (thread diferente do principal), player=None conforme contrato quando aplicável ao loader, chamadas registradas no player, rejeição de PLUGIN inválido e erro de run(). No perfil jarvis, demonstrar um QApplication no principal e modelo stub retornando None, quando PyQt6 e dependências necessárias estiverem disponíveis. Timeout do subprocesso é falha diagnosticada; @@REPORT@@ ausente/malformado não conta como sucesso. Não testar plugin que cria widget no worker nem provocar deadlock/crash real para satisfazer o critério. O harness não é sandbox de segurança.

AC7 — Isolamento verificável: testes negativos injetam falha durante o teste do painel/vozes e conferem cleanup/restauração dos patches e uso exclusivo dos destinos temporários. Verificar tentativas de acesso aos caminhos reais com guards/mocks, sem ler seu conteúdo. Cobrir exit code de FAIL e contagem de SKIP. Nenhum teste requer chaves, download, serviço externo ou saída audível. Alterações não podem apagar testes comportamentais existentes para evitar falhas.

AC8 — Evidência e documentação: DEVELOP/REVIEW registram comando, ambiente/dependências relevantes, retorno, duração, contagens, skips, logs e alcance por cenário. Executar novos testes e as duas suítes focais existentes (VS Code/memória) em isolamento, além da suíte providers somente após AC3. Validar o perfil Qt offscreen quando disponível. README distingue integração sintética local de observação manual/serviços reais. CHANGELOG só descreve resultado revisado.

## Estratégia de validação

Planejar unittest discovery restrito aos três novos arquivos, regressões tests/test_dev_agent_vscode.py e tests/test_memory_persistence.py, e python -m providers._tests após isolamento. Usar sys.executable do ambiente de teste, sem buscar/substituir interpretadores fora das regras do ambiente. Capturar logs sem DEVNULL; não executar aplicativo principal. Fixtures de harness são geradas dentro de temporários e nunca adicionadas a plugins/. AST/compilação e diff são verificações complementares, não prova comportamental. Não executar testes de implementação na etapa CONTEXT.

Provar equivalência específica dos escapes independentemente das demais melhorias da suíte, pois o arquivo também terá mudanças autorizadas de isolamento. Preservar snapshot/hash anterior para comparação localizada; não modificar ENCODING-BASELINE/APPROVED-SCOPE manualmente. Runtime captura baseline ao completar CONTEXT e recaptura no gate humano.

## Riscos, incógnitas e tratamento dos findings

D007 é tratado pelo controle prospectivo e regressão focal dos bytes identificados; não se afirma que a intenção histórica do repositório foi descoberta. D011 é tratado pela ampliação de evidência integrada local e pela remoção de efeitos pessoais dos testes. UI offscreen e mocks não demonstram tela interativa, som audível, STT real, credenciais/serviços, recuperação de crash ou outras plataformas. Esses cenários permanecem UNKNOWN e devem aparecer como não demonstrados, sem PASS geral ou reclassificação retrospectiva do DISCOVERY.

Riscos INFERRED: isolamento incompleto em import-time, dependências opcionais e vazamento de tarefas podem comprometer repetibilidade. Mitigar com guards, fixtures sintéticas, cleanup e timeouts. Se testes revelarem defeito em módulo de produção fora de SCOPE, registrar falha e parar a correção; pedir scope-expansion com referência auditável, sem ampliar arquivos automaticamente.

Nenhum requisito delimitado depende de garantia externa: não há Boundary Stop acionada nesta preparação. Não investigar fornecedores/OS/hardware para resolver UNKNOWN residual. Se um requisito material futuro depender deles, aplicar BOUNDARY-STOP-CONDITION, registrar evidência/categoria/dono e STOPPED_AT_RESPONSIBILITY_BOUNDARY; não iniciar downstream dependente. Falta de pacote/teste deve ser reportada com alcance concreto, nunca mascarada como sucesso.

## Gate humano

Revisar os seis caminhos exatos, critérios AC1–AC8, migração proposta de encoding e limites da evidência antes de aprovar. A solicitação de tratar findings fornece intenção para CONTEXT; não constitui aprovação desta proposta. Completar CONTEXT não autoriza DEVELOP e não resolve D007/D011 por si só. Não avançar automaticamente.
