# DEVELOP — change-003 — implementação parcial, validação bloqueada

## Autorização e execução

Contexto e seis caminhos aprovados pelo runtime com a referência literal `Aprovo a pós revisar o CONTEXT.md`. Roteamento DEVELOP autorizado como IMPLEMENTER/codex, v0.2.0 CORE IN. Lease desta sessão: `34bf7c64-77ed-42c4-a52d-1f3287b623a0`. Checagens retornaram VALID após repetição autorizada por Acesso negado ao python.exe no ambiente restrito. Nenhum outro token foi adotado; sem delegação, revisão automática, alteração manual de estado ou instalação de pacotes.

## Implementação realizada

- providers/_tests.py: controles literais 0x01/0x02 substituídos por escapes Python equivalentes; UTF-8 sem BOM e CRLF preservados. Snapshot anterior em before/providers-tests.py, SHA-256 igual ao baseline aprovado.
- Runner público executa nova cópia temporária de fontes a cada chamada; copia somente .py dos pacotes necessários e ui.py, com allowlist para memory. Não copia configuração, memória ou modelos. Diretórios de perfil/cache/temp do processo filho apontam para a árvore temporária. Retorno/saída/timeout do subprocesso são propagados; CREATE_NO_WINDOW no Windows.
- Vozes usam fixtures sintéticas e patches com cleanup; download e síntese são bloqueados. Configuração do painel fica em TemporaryDirectory com CONFIG_DIR/CONFIG_FILE redirecionados por patch. Não lê nem restaura config pessoal. Guard de teste bloqueia conexões fora de loopback e gravações fora do projeto descartável; não é sandbox de segurança nem proteção geral para subprocessos arbitrários.
- PASS/FAIL/SKIP separados, reset dos contadores e cleanup de tarefas/servidores entre cenários; servidor fecha socket e tem join limitado. Subprocesso de medição usa temporário com cleanup e timeout.
- Três novos arquivos de teste cobrem PCM/encoding com mutações negativas, isolamento/cleanup/contagens, e harness real com loader real e plugins sintéticos. README documenta execução e limitações. CHANGELOG não foi alterado: reservado ao CLOSE após revisão.

## Validação executada

Comandos executados no diretório do projeto com `python` do PATH, por permissão oficial após falha de inicialização no ambiente restrito. Nenhuma busca ou substituição de interpretador. Versão exata do Python não foi coletada; não inferida do launcher. Durações abaixo são as reportadas por unittest, exceto providers (tempo observado pelo executor).

| Comando | Retorno | Resultado | Duração |
|---|---|---|---|
| python -m unittest discover -s tests -p 'test_source_encoding.py' -v | 0 | 3 PASS | 0,048 s |
| python -m unittest discover -s tests -p 'test_provider_test_isolation.py' -v | 0 | 5 PASS, 1 SKIP | 1,160 s |
| python -m unittest discover -s tests -p 'test_smoke_harness.py' -v | 0 | 3 PASS, 1 SKIP | 0,882 s |
| python -m providers._tests | 1 | 52 PASS, 8 FAIL, 2 SKIP | 4,251 s no executor |
| python -m unittest discover -s tests -p 'test_dev_agent_vscode.py' -v | 0 | 29 PASS | 1,494 s |
| python -m unittest discover -s tests -p 'test_memory_persistence.py' -v | 0 | 13 PASS | 0,106 s |

Novos testes: 11 PASS, 2 SKIP; regressões existentes: 42 PASS. Contagens da suíte providers são asserções/cenários próprios, não casos unittest; não somar como se fossem a mesma unidade. Nenhum teste apresentou falha de produto demonstrada; o retorno 1 de providers permanece falha real da execução, não foi convertido em PASS.

Diagnósticos da execução providers:

| Cenário com FAIL | Diagnóstico observado |
|---|---|
| test_real_caller_shapes | ModuleNotFoundError: No module named 'google' |
| test_taskgroup_and_tool_loop | ModuleNotFoundError: No module named 'google' |
| test_full_stack_over_http | ModuleNotFoundError: No module named 'httpx' |
| test_vision_is_asked_not_guessed | ModuleNotFoundError: No module named 'httpx' |
| test_audio | ModuleNotFoundError: No module named 'numpy' |
| test_failures_name_the_part | ModuleNotFoundError: No module named 'httpx' |
| test_local_models_get_a_smaller_prompt | OpenAI-compatible needs httpx, which is not installed |
| PyQt6 available | No module named 'PyQt6' |

Piper: dois SKIP explícitos por dependência opcional ausente. Testes novos do painel e do perfil jarvis: um SKIP cada por PyQt6 ausente. A suíte ainda demonstrou tool deduplication, injeções durante resposta, filtros de fala/raciocínio, schemas, áudio sintético antes/depois da ferramenta, caminho não configurado e uso da pasta de vozes sintética. Não houve prova do turno com types.Blob, HTTP integrado, resampling nem painel/perfil Qt neste ambiente. Não há prova de UI interativa ou áudio real.

## Critérios e pendências

AC1 e preservação de bytes de AC2 têm prova focal. AC3/AC7 têm provas de temporários, patches de voz, timeout, contagens e guards; o ramo de exceção do painel está implementado mas não executado por falta de Qt. AC4–AC6/AC8 têm cobertura parcial: fluxo completo de providers e perfil Qt aguardam dependências. README registra esse alcance; código não instala dependências nem mascara ausências. D007/D011 não são promovidos a resolução integral. Intenção histórica sem BOM e cenários reais continuam UNKNOWN.

Bloqueio material em BOUNDARY-STOP-DEP-001.md. Trabalho independente realizado após o diagnóstico foi apenas documentação do resultado e preservação de evidência, já autorizado no CONTEXT; nenhum teste dependente, experimento de ambiente ou downstream foi aberto.

Não invocar complete DEVELOP com validação material pendente. Encerrar este lease pelo launcher suportado após parar o trabalho. Lifecycle permanece APPROVED_FOR_DEVELOP; REVIEW não iniciado. Retomada exige autorização humana explícita e delimitada conforme o registro de boundary, além de novo lease e checagens; não inferir reabertura da mera chegada de pacotes.
