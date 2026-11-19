# REVIEW — change-004 — idioma da interface desktop

Resultado técnico: dois achados P2 confirmados; AC3 e AC5 não atendidos integralmente. Recomenda-se corrigir antes da aprovação. Nenhuma correção ou decisão humana foi executada. A conclusão técnica deve registrar REVIEW_PENDING pelo Core; CLOSE permanece bloqueado até decisão humana explícita.

## Identidade e limites

ai-sdd:review; codex; papel ORCHESTRATOR; v0.2.0; autorização ALLOW em todos os termos; active_change_id change-004; sem scope-expansion. Runtime retornou NON_ISOLATED_REVIEW: revisão realizada no mesmo histórico do implementador, sem alegar independência de agente. Lease novo desta revisão: b3d6df31-f6b3-4ac6-b668-e455fac5ba29; não adotado token anterior.

Revisado CONTEXT AC1–AC9, APPROVED-SCOPE, ENCODING-BASELINE/POLICY, implementação nos arquivos delimitados, testes, documentação, evidências e retomada de ambiente. Preservados registros históricos de parada/retomada e UNKNOWN de intenção de encoding. Sem nova dependência externa material ou nova Boundary Stop; esta revisão não investiga fornecedor/OS/hardware.

## Achados

### R004-001 — [P2] Preservar painel dispensado e quiz ativo ao trocar o idioma

Fonte: gui/window.py:1875–1880, em _refresh_language_content. Critério afetado: AC3 (preservar estado/conteúdo/sessão sem efeitos adicionais).

O listener de idioma chama os métodos de apresentação _show_content/_show_review/_show_code_job mesmo quando o conteúdo antigo foi ocultado. Esses métodos terminam em _reveal_below_hud, que mostra o painel e altera os tamanhos do QSplitter. Dispensar o conteúdo não limpa _localized_content. Consequência: trocar idioma reabre conteúdo dispensado; se um quiz ocupa o espaço abaixo do HUD e existe payload antigo, a troca remove o espaço visível do quiz.

Reprodução isolada confirmada em REVIEW-PROBES.log:
- Mostrar conteúdo sintético, ocultar seu painel e trocar idioma: DISMISSED_PANEL True False (isHidden antes/depois).
- Em seguida abrir quiz e trocar idioma: tamanhos [526, 0, 250] → [556, 220, 0]. Ordem HUD/conteúdo/quiz; quiz passa de 250 px para 0, conteúdo antigo reaparece com 220 px. isHidden sozinho não detecta a ocultação por altura zero do splitter.

Correção proposta para futuro DEVELOP: separar retradução de abertura/revelação, preservar visibilidade e tamanhos do splitter, ou invalidar payload dispensado conforme comportamento desejado. Adicionar regressões de conteúdo dispensado e quiz ativo com payload anterior. Não foi aplicada correção nesta etapa.

### R004-002 — [P2] Traduzir os rótulos da pasta carregada

Fonte: gui/widgets.py:462–465 e 479–480, em _DropCanvas._paint_file. Critérios afetados: AC4/AC5 (cobertura das mensagens próprias de UI nos módulos delimitados).

Os textos FILE/FOLDER e a contagem “files” são construídos como strings comuns, sem entrada marcada de catálogo. render() preserva strings comuns por projeto, portanto esse ramo nunca traduz. Não são nomes de usuário nem metadados externos: são rótulos fixos da GUI incluídos no escopo.

Reprodução isolada: locale pt-BR, diretório temporário chamado CLOSE e três arquivos informados. Painter registrou ['📁', 'CLOSE', 'FOLDER  ·  3 files']. O nome CLOSE corretamente permaneceu intacto, mas o molde próprio permaneceu inglês.

Correção proposta para futuro DEVELOP: catalogar os rótulos/molde da contagem e formatar só os campos variáveis, mantendo nome/caminho e extensões como dados opacos. Incluir teste do estado de arquivo/pasta carregado em ambos os idiomas. Não foi aplicada correção nesta etapa.

## Matriz de aceitação

| Critério | Resultado nesta revisão |
|---|---|
| AC1 | Evidência focal positiva: seleção, cancelar, persistência e falha de gravação com diagnóstico. |
| AC2 | Evidência focal positiva: config_manager com locking/merge, carregamento antes da janela e ausência de reconexão de voz no teste isolado. |
| AC3 | NÃO ATENDIDO integralmente — R004-001. Cenários usuais de troca/texto/seleção passam; estado de painel/quiz falha no novo probe. |
| AC4 | Paridade de placeholders das entradas marcadas passa; cobertura incompleta de mensagens próprias demonstrada por R004-002. |
| AC5 | NÃO ATENDIDO integralmente — R004-002. O teste de cobertura atual percorre somente chamadas tr existentes e não detecta rótulos que nunca foram marcados. |
| AC6 | Qt/worker conforme nos testes e inspeção. Personalização com scroll e ações visíveis; cards providers com quebra de linha. Sem garantia universal de layout. |
| AC7 | Testes isolados de normalização, fallback, composição, configuração e erro de gravação passam. |
| AC8 | Qt offscreen e renders fornecem evidência focal; novo probe identifica lacuna não coberta pela suíte atual. Não confundir suíte verde com satisfação integral. |
| AC9 | PASS do controle de encoding/hashes nos 12 caminhos; baseline e evidência de DEVELOP intactos. README documenta função e limites, mas o estado final ainda exige as correções acima. CHANGELOG reservado ao CLOSE permanece intacto. |

## Verificações executadas nesta REVIEW

- python -m unittest discover -s tests -v: exit code 0; 62 testes PASS em 9.844s. Log REVIEW-UNITTEST.log.
- python -m providers._tests: exit code 0; 98 PASS, 0 FAIL, 2 SKIP opcionais de Piper (ausente; seleção de idioma e síntese não exercitadas). Log REVIEW-PROVIDERS.log. SKIP não foi contado como PASS.
- python .ai/changes/change-004/review_probes.py: exit code 0; reproduziu positivamente os dois defeitos e executou as demais asserções do fluxo Qt. Exit 0 significa confirmação das condições do probe, não aprovação da implementação. Log REVIEW-PROBES.log.
- O primeiro ensaio do probe falhou ao usar isHidden como expectativa para QSplitter; a saída já mostrava altura zero. Corrigido somente o script de evidência para comparar tamanhos efetivos; ensaio preservado em REVIEW-PROBES-INITIAL.log. Nenhum fonte/teste de produto foi editado.
- python .ai/changes/change-004/review_encoding.py: exit code 0. Conferiu SHA-256 dos 12 caminhos contra DEVELOP, baseline aprovado e hashes de todas as evidências de DEVELOP; UTF-8 estrito, BOM e finais de linha íntegros. REVIEW-ENCODING-CHECK.json contém hashes próprios. A intenção histórica permanece UNKNOWN.
- git -c core.whitespace=cr-at-eol diff --check nos existentes de escopo: exit code 0. CRLF foi preservado, sem mudar configuração Git.
- Inspeção dos renders de Personalização e providers em pt-BR: seletor legível, ações alcançáveis a 480×420 e parágrafos sem o corte anterior dos cards. Imagens en/pt-BR e hashes da implementação preservados. Não se afirma observação interativa real nem fonte/ícone universal.

Ambiente: Windows, Python 3.15.2, PyQt6 6.12.1, Qt 6.12.0. Execução de Python normal ainda retorna Acesso negado; repetições canônicas pelo mecanismo oficial foram usadas, sem alterar PATH/UAC/ACL/política. Fixtures copiaram apenas fontes para projeto descartável, com dados sintéticos, Qt offscreen, guards e timeout; sem sessão real, chaves, áudio físico, modelos ou serviços externos. Permanecem UNKNOWN outras plataformas/resoluções, acessibilidade completa e serviços/áudio reais.

## Escopo e decisão humana

Nenhum arquivo de produto/teste/documentação operacional foi corrigido na revisão; somente dossiê de REVIEW escrito. Não foram apagados achados, renomeados resultados históricos ou alterado KR/runtime manualmente. A evidência atual não sustenta afirmar AC1–AC9 integralmente atendidos.

Formas públicas disponíveis após conclusão técnica, sempre com referências explícitas fornecidas pelo humano:
- $ai-sdd review approve "referência do revisor"
- $ai-sdd review changes-requested "referência do revisor"
- $ai-sdd review waive "referência do revisor" "referência do waiver"

O relatório recomenda tratar R004-001/R004-002; isso não registra changes-requested nem fornece referência humana. Aprovação de DEVELOP ou permissão de ambiente não é decisão de REVIEW. Não executar correções/CLOSE automaticamente.