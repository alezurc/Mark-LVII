# DEVELOP — change-002 — D008

Implementação concluída no escopo aprovado pela referência literal “Após analisar o CONTEXT.md eu autorizo a execução.” Esta é evidência de desenvolvimento, não REVIEW nem decisão humana de revisão.

## Comportamento entregue

memory/memory_manager.py centraliza os três writes anteriores em _write_memory: serialização completa, NamedTemporaryFile exclusivo no diretório do destino, fechamento antes de os.replace e limpeza restrita ao temporário próprio. Erros anteriores ao replace preservam o destino. Falha na limpeza registra mensagem sem esconder a falha original. Não há retry nem espera introduzida. save_memory continua snapshot integral, com trim existente; sessões mantêm sua política anterior sem novo trim. update_memory, forget e save_session_summary agora mantêm RLock durante leitura/modificação/commit; pop_last_session já abrangia a operação e usa o mesmo writer. Aquisições aninhadas de load/save são reentrantes. APIs públicas, categorias, extras, Unicode, limites e ordem LIFO mantidos.

tests/test_memory_persistence.py usa módulo isolado, tempfile e MEMORY_PATH redirecionado antes de I/O. Falhas injetadas cobrem serialização, criação, escrita parcial, fechamento, replace e limpeza. Todos os mutadores têm testes de ausência de falso sucesso. Threads com eventos/lock observado e joins limitados demonstram serialização dos mutadores concorrentes; leitura direta repetida durante publicação verifica JSON completo. Fixtures são sintéticas.

CHANGELOG.md não editado: atualização reservada ao CLOSE após revisão conforme CONTEXT. Nenhum outro alvo de produto foi editado nesta etapa; alterações anteriores de actions/dev_agent.py e arquivos preexistentes foram preservadas.

## Validação

- python -B -m unittest discover -s tests -p test_memory_persistence.py -v: 13 testes PASS.
- Após ajustes finais, python -B -m unittest discover -s tests -p 'test_*.py' -v: 42 testes PASS em 1.632 s (13 persistência + 29 VS Code).
- Os dois módulos alterados são parseados/importados pelas suítes isoladas; sem import do aplicativo, GUI, serviços ou modelos.
- git diff --check simples acusa CR preexistente/preservado como whitespace. git -c core.whitespace=cr-at-eol diff --check -- memory/memory_manager.py: PASS, sem converter o encoding/finais de linha para satisfazer configuração local.
- Nenhum crash real, queda de energia ou teste integrado da aplicação foi executado. Nenhum conteúdo da memória real foi lido ou alterado.
- Launcher/testes inicialmente não resolveram python/py no PATH restrito. Repetições oficiais com permissão ampliada executaram o mesmo launcher/operação e os testes isolados; isto não constitui aprovação humana adicional.

## Encoding e hashes finais

Fonte original conferida com baseline aprovado antes de edição: 3ecf5a9d80484bec73eef67e54c7d7e2880c726e4bfac58d05b1a14b6e1988ce.
- memory/memory_manager.py: b7a58f550eb5b863c9b8c705fcf4263019f131eafd007965aea02449416d6f0a; UTF-8 válido sem BOM, 493 CRLF, zero LF isolado. Edições localizadas preservam demais funções.
- tests/test_memory_persistence.py: 61c1c443bd95f66bd93b8bf322eef73289c776cbd230cfd8961c1d8142b16808; novo UTF-8 sem BOM, 260 LF.
- CHANGELOG.md: b8ddd0143d5b73f128ad15d22418b95170491a1742d53c938a1126f9fd201b07, igual ao baseline.

Intenção histórica de encoding sem BOM continua UNKNOWN; não houve migração nem alteração da ENCODING-POLICY/baseline manual. REVIEW deve executar seus guards canônicos.

## Limites e continuidade

Publicação por replace e serialização dentro deste processo; não há coordenação entre processos, merge de snapshots externos, recuperação de dados já corrompidos, backup ou garantia de durabilidade física. Efeitos de energia/hardware/filesystem não demonstrados continuam UNKNOWN. Nenhuma dependência externa material bloqueou os critérios delimitados; Boundary Stop não acionada. Nenhum worker próprio segue executando após as suítes. REVIEW não iniciado automaticamente.
