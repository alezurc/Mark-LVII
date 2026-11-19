# CONTEXT — change-002 — D008 persistência de memória

## Intenção e evidências

Pedido humano literal nesta conversa: “D008 (persistência de memória)”, após context change-002. Objetivo proposto: evitar que uma gravação incompleta destrua o JSON anterior da memória. Seleção de objetivo não é aprovação de desenvolvimento.

DISCOVERY discovery-2026-11-18-01, finding D008: risco de truncamento INFERRED; nenhum crash ou perda foi reproduzido. Inspeção estática atual CONFIRMED: memory/memory_manager.py grava diretamente em save_memory, save_session_summary e pop_last_session. Lock protege operações individuais, mas update_memory, forget e save_session_summary leem e gravam em seções separadas; há risco INFERRED de atualização perdida entre threads. core/tasks/store.py:write_json serve de referência local de temporário/replace, sem conceder garantia integrada ou autorização para alterá-lo.

SHA256 das fontes consultadas:
- memory/memory_manager.py: 3ecf5a9d80484bec73eef67e54c7d7e2880c726e4bfac58d05b1a14b6e1988ce
- core/tasks/store.py: eba554771e86fb4e2f441073aaa91f542071f3944c0ed883af9ef789c33f8072
- .ai/DISCOVERY.md: 9361d0d3e0ca734710661efb7272eeb3315ff181544c6e3626b55770a2aafa3e5
- PROJECT-POLICY.md: 5cd687ff9a76754abf8224df6ebeaccfd2b03faa90f6764a093dcb7fa01b057e

## Escopo exato e resultado esperado

SCOPE.json lista os únicos alvos de edição de produto/teste/documentação:
- memory/memory_manager.py: persistência local, helpers privados e sincronização dos caminhos de mutação existentes; preservar APIs públicas e formato JSON.
- tests/test_memory_persistence.py: novo teste focal stdlib, fixtures temporárias e dados sintéticos.
- CHANGELOG.md: registro de change-002 no CLOSE somente após revisão, conforme PROJECT-POLICY.md, incluindo validação e limites.

Documentos de governança ficam nesta pasta da change. core/tasks/store.py e os chamadores são apenas referências de leitura. Não editar long_term.json real, configurações, dados pessoais, UI, providers, task engine ou outros findings. Sem novas dependências. Sem versão, commit, tag, release ou publicação. README permanece adequado por se tratar de correção interna sem mudança de instalação/operação; reavaliar se o resultado alterar instruções.

## Critérios de aceitação

1. Todos os caminhos que persistem long_term.json usam um único mecanismo privado: serializar o documento completo antes de substituir o destino, gravar temporário exclusivo no mesmo diretório e usar os.replace somente após escrita e fechamento bem-sucedidos. Não truncar o destino antes do commit. Preservar JSON indentado, ensure_ascii=False e UTF-8 sem BOM do contrato existente.
2. Falha de serialização, criação/escrita/fechamento do temporário ou replace conserva bytes anteriores do destino; se o destino não existia, não criar JSON parcial. Limpar apenas temporário desta operação quando possível, sem mascarar a falha original. Retries, se usados para compartilhamento Windows, são limitados e testáveis; não esperar indefinidamente.
3. save_memory, update_memory/remember, forget, save_session_summary e pop_last_session compartilham esse mecanismo. Não retornar resultado de gravação bem-sucedida antes do replace. Preservar contratos de erro: save_memory e mutadores que já propagam falhas continuam a propagá-las; pop_last_session pode manter diagnóstico e None, mas não devolver entrada consumida quando o commit falhar. Não incluir valores pessoais em novos diagnósticos.
4. Operações read-modify-write internas de update_memory, forget, save_session_summary e pop_last_session são serializadas integralmente dentro deste processo, incluindo leitura e commit, com sincronização sem deadlock por aquisição aninhada. Leitores não observam JSON parcial. save_memory continua gravação de snapshot completo: não promete mesclar snapshots externos obsoletos. Não prometer coordenação entre processos.
5. Preservar categorias, campos extras, entradas legadas, Unicode, truncamento de valores, trim e seu aviso, limite de sessões, ordem LIFO e comportamento para ausência/JSON inválido. A recuperação de arquivo já corrompido, backup e restauração automática ficam fora do escopo; não afirmar que a correção recupera perdas anteriores.
6. Testes isolados redirecionam MEMORY_PATH para diretório temporário antes de qualquer I/O. Cobrir round-trip Unicode/campos legados, arquivo ausente, erro de serialização, escrita parcial com falha, fechamento com falha, replace negado e limpeza; verificar igualdade exata dos bytes anteriores nos casos de erro. Cobrir os três pontos originais de escrita e todos os mutadores, consumo sem falso sucesso e leitura repetida durante substituições.
7. Testes de threads com sincronização determinística e joins limitados demonstram ausência de atualização perdida nos mutadores internos e ausência de deadlock; sleeps isolados não são prova de concorrência. Nenhum teste acessa memória real, GUI, modelos, serviços ou credenciais. Não provocar crash real da aplicação.
8. REVIEW revalida diff, APIs, critérios, encoding/BOM e evidência focal. Testes locais e falhas injetadas sustentam apenas o comportamento demonstrado; não equivalem a garantia universal de filesystem, crash ou hardware.

## Validação planejada

DEVELOP: unittest focal tests/test_memory_persistence.py com tempfile e mocks, parsing das fontes alteradas, diff e verificações de preservação de bytes. Reexecutar a suíte existente tests/test_dev_agent_vscode.py como regressão local se seu ambiente isolado estiver disponível. Registrar comandos, resultados e limitações reais. CONTEXT não executa testes de implementação ainda inexistente. CLOSE atualiza CHANGELOG.md com resultado revisado, sem anunciar proposta como concluída.

## Encoding e restrições

memory/memory_manager.py é UTF-8 estritamente válido, sem BOM, 478 CRLF e zero LF isolados na inspeção. Intenção histórica sem BOM permanece UNKNOWN; preservar encoding/BOM/finais de linha e bytes fora das edições localizadas. CHANGELOG.md terá baseline capturada pelo runtime; preservar seu perfil. Novo teste será UTF-8 sem BOM com LF. ENCODING-POLICY.json não propõe migração ou decisão UNKNOWN: nenhum alvo material de bytes opacos foi identificado. O runtime captura ENCODING-BASELINE.json ao completar CONTEXT e recaptura no gate humano. Não editar baseline/approved scope manualmente.

AGENTS.md é obrigatório: Qt somente no thread principal; este trabalho não toca widgets. Usar stdlib/dependências existentes. Não importar ou executar o aplicativo para validar contexto. Não ler conteúdo da memória pessoal. Knowledge Register canônico consultado na preparação anterior: KR-change-001-001/002 tratam VS Code e encoding da change anterior, sem provar persistência nem autorizar esta mudança; preservar suas classificações e avaliar conhecimento duradouro no CLOSE.

## Riscos, incógnitas e limites

INFERRED: truncamento por escrita direta e atualização perdida entre threads; não há reprodução histórica de perda real. CONFIRMED: três writes diretos e locks por operação. UNKNOWN: efeitos de queda de energia, comportamento de hardware/filesystem, processos concorrentes e disponibilidade de substituição em todos os ambientes. A proposta cobre publicação por replace em filesystem local que o suporte, não transação distribuída nem durabilidade física. Um erro de replace deve ser comunicado preservando o arquivo anterior; não implementar backend alternativo, locks entre processos, backup, migração ou engenharia de OS.

Nenhuma dependência externa material bloqueia o objetivo delimitado e testável neste contexto; não há Boundary Stop acionada. Se um requisito futuro exigir garantia externa de durabilidade/plataforma, aplicar BOUNDARY-STOP-CONDITION, preservar UNKNOWN e parar o ramo sem investigação externa automática. A limitação documentada não constitui evidência de durabilidade.

## Gate humano

Contexto proposto, aprovação PENDING e referência NONE. Completar CONTEXT não autoriza DEVELOP. Revisão humana deve avaliar os critérios, os três caminhos exatos de SCOPE e os limites antes de uma referência explícita de approve. Não reutilizar referências de change-001. Não avançar automaticamente.
