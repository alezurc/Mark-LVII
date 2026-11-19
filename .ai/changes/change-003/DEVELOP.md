# DEVELOP — change-003 — implementação validada após retomada humana

## Resultado final da retomada

Validação concluída no ambiente virtual local `.venv`, Python 3.15.2 AMD64, com `include-system-site-packages = false`. A autorização humana registrada em RESUMPTION-DEP-001.md reabriu exclusivamente DEP-001 para preparar esse ambiente e concluir a validação do DEVELOP. Referência literal: `Autorizo explicitamente a retomada do DEVELOP da change-003, com o seguinte escopo:`; mensagem completa nesta conversa, em 2026-11-18, America/Sao_Paulo. Novo lease: `2e8e68e9-1bf1-4a92-b00e-f4cec2314cc1`.

O responsável autorizou conferir declarações, preparar ambiente virtual, instalar somente dependências necessárias nele, repetir FAIL/SKIP e verificações finais, e atualizar este relatório. Proibiu alteração de dependências, instalação global, upgrades indiscriminados e expansão de produto. A execução respeitou esses limites e não iniciou VERIFY, REVIEW ou CLOSE.

As quatro dependências já estavam declaradas em requirements.txt. Instaladas no .venv: google-genai 2.34.0 (>=2.8.0,<3), httpx 0.28.1 (>=0.27,<1), numpy 2.5.5 (>=1.24,<3), PyQt6 6.12.1 (>=6.6,<7), além de psutil 7.2.2 (>=5.9,<8), necessário para os imports do painel, e dependências transitivas. A lista completa está em venv-packages.json. Não se instalou o aplicativo completo nem extras de voz.

Comandos de preparação: `python -m venv .venv`; instalação com `.venv/Scripts/python.exe -m pip install --only-binary=:all:` e as cinco linhas selecionadas diretamente do requirements.txt, sem --upgrade. O pip inicialmente recusou usar o arquivo completo como constraints por conter extras (`uvicorn[standard]`); criou-se validation-constraints.txt na pasta desta change, derivado das linhas originais e removendo somente a sintaxe de extras. Uma reconciliação com essas constraints ajustou exclusivamente cryptography de 50.0.2 para 49.0.0 para respeitar o limite <50 do projeto. Nenhuma alteração de requirements.txt ou pip global; não se atualizou o pip do venv.

| Comando no ambiente virtual | Retorno | Resultado | Duração |
|---|---|---|---|
| .venv/Scripts/python.exe -m providers._tests | 0 | 98 PASS, 0 FAIL, 2 SKIP | 9,794 s no executor |
| .venv/Scripts/python.exe -m unittest discover -s tests -p 'test_*.py' -v | 0 | 55 PASS, 0 FAIL, 0 SKIP | 5,056 s no unittest |
| .venv/Scripts/python.exe -m pip check | 0 | No broken requirements found | — |
| .venv/Scripts/python.exe .ai/changes/change-003/final_validation.py | 0 | versões, isolamento do venv, AST, hashes e encoding conformes | — |
| git diff --exit-code -- requirements.txt | 0 | arquivo de dependências inalterado | — |
| git diff --check nos seis alvos aprovados | 0 | sem diagnóstico | — |

Logs integrais: providers-resumed.log e unittest-resumed.log. FINAL-VALIDATION.json vincula seus hashes, versões, executável, hash do requirements.txt e os seis arquivos aprovados. A validação final confirmou que os seis alvos de produto/testes/documentação mantêm os mesmos bytes da tentativa anterior, preservando UTF-8 sem BOM, CRLF em providers/_tests.py/README.md e LF nos testes novos/CHANGELOG. A retomada não exigiu correção adicional de produto. Para os arquivos novos ainda não versionados, a verificação de bytes/AST/encoding complementa git diff --check.

As oito falhas anteriores de dependências foram reexecutadas com sucesso. Os dois testes novos antes em SKIP por PyQt6 também passaram: exceção do painel com restauração da configuração temporária e perfil jarvis com QApplication no principal/modelo stub. Os 55 unittest compreendem 13 casos novos e 42 regressões existentes. Os dois SKIPs restantes da suíte providers foram reexecutados e continuam opcionais por Piper ausente; são reportados separadamente, não convertidos em PASS. O CONTEXT permite Piper simulado ou SKIP explícito, portanto não é requisito instalar piper-tts nem baixar modelos para concluir este perfil local. A prova de patches e vozes sintéticas passou; síntese física continua não demonstrada.

AC1–AC8: evidência suficiente para o perfil sintético local delimitado. Equivalência de PCM, ausência de controles, encoding, isolamento/cleanup, turno types.Blob/TaskGroup, streaming HTTP fragmentado, resampling, painel Qt offscreen, worker/loader e tratamento de falhas foram exercitados. DEP-001 fica superado no alcance desta retomada pela evidência acima, sem reclassificar a tentativa inicial ou apagar a parada original. D007 é tratado prospectivamente; intenção histórica de encoding continua UNKNOWN. D011 tem evidência integrada local ampliada; áudio físico, UI interativa, serviços reais, crash e outras plataformas continuam UNKNOWN.

Limitação de ambiente: setup.py documenta Python >=3.11 e faixa historicamente testada até 3.13, permitindo versões novas com aviso. O perfil disponível 3.15.2 foi usado com wheels compatíveis e passou os testes registrados; isso não amplia a garantia a outras versões. Nenhum novo impedimento fora da autorização foi encontrado. A conclusão de DEVELOP será registrada exclusivamente pelo launcher com o novo execution_id. Não avançar automaticamente para nenhuma etapa posterior.

## Histórico preservado da primeira tentativa

O relatório original foi preservado integralmente em DEVELOP-INITIAL.md, SHA-256 `4d44e0a0832669a36b2317a79072ad0b4bd886ad279f5eaf0684893df09852f4`. O texto abaixo descreve apenas a tentativa anterior, já substituída pelo resultado final acima; bloqueios e referências a lease nela são históricos.

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
