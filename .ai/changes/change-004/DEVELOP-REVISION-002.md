# DEVELOP — change-004 — revisão 002

Implementação das correções R004-001 e R004-002 concluída para revisão técnica posterior. Referência humana de aprovação desta revisão: “Aprovo o CONTEXT revisão 002 da change-004”. Papel IMPLEMENTER; adaptador codex; versão Core v0.2.0; autorização ALLOW em todos os termos, sem expansão/fallback. Lease novo desta sessão: ffaf7892-e09c-45d3-a49a-1643fcb9dcdd.

Este relatório não substitui nem reclassifica a REVIEW anterior. Nenhuma nova decisão humana de revisão foi inferida e nenhuma etapa REVIEW/CLOSE foi executada automaticamente. Os logs e resultados anteriores continuam preservados; sua integridade foi verificada por hash.

## Correções e nexo com o contexto

R004-001 / AC3, AC10, AC11: _show_content, _show_code_job e _show_review agora distinguem renderização textual de apresentação pelo parâmetro interno keyword-only present (padrão True, preservando chamadas por sinais/APIs existentes). O listener de idioma usa present=False: não revela painel, não muda tamanhos de QSplitter, não repete glance do HUD, não redefine timestamp como se fosse conteúdo novo e não reseta a leitura. O fluxo normal de novos resultados continua revelando o painel.

A seleção é remapeada sobre os trechos de texto preservados quando rótulos traduzidos mudam de comprimento, usando SequenceMatcher da biblioteca padrão e conversão explícita entre índices de texto Python e unidades UTF-16 do QTextCursor. Preserva seleção inclusive com emoji/acentos; posição de rolagem é restaurada. Não altera dados, opções ou respostas do quiz. Testes cobrem conteúdo dispensado, quiz na segunda pergunta com resposta anterior e campo digitado, além de painel visível para plain/code/review, em en → pt-BR → en. Sinais/callbacks de graduação, conversa e voz não recebem chamadas extras.

R004-002 / AC4, AC5, AC12, AC13: _DropCanvas._paint_file marca FILE/FOLDER e o molde da contagem para tradução. Exibe FILE/FOLDER em inglês e ARQUIVO/PASTA em pt-BR; 1 file/arquivo, demais contagens files/arquivos e marcador + a partir de 5000. Extensões, caminhos e nomes são valores opacos, inclusive FILE, FOLDER e CLOSE. O estado carregado se atualiza pela pintura existente sem recarregar/enumerar a pasta. Testes alcançam o método real de pintura com painter de captura e também o widget real em render.

AC6/AC8: o botão de resposta do quiz passou de largura fixa de 90 px para largura mínima de 110 px, deixando o layout acomodar RESPONDER sem corte. Nenhuma fonte, tema, QApplication ou widget em worker foi adicionado. A captura offscreen espera um breve processamento de eventos de pintura/layout; a verificação funcional de estado e splitter permanece obrigatória e independente das imagens.

## Escopo efetivamente alterado

Quatro arquivos, todos na lista aprovada de 12 caminhos:
- gui/window.py: separar apresentação de retradução, preservar seleção/rolagem e acomodar botão do quiz.
- gui/widgets.py: formar rótulos carregados com mensagens explícitas.
- gui/i18n.py: quatro entradas de catálogo para arquivo/pasta e contagem singular/plural.
- tests/test_ui_language_qt.py: quatro regressões isoladas, preservando o teste anterior; fixtures de Windows explícitas e nomes sentinela.

Os outros oito caminhos aprovados ficaram byte a byte iguais ao baseline da revisão 002. tests/test_ui_language.py continua verificando catálogo/placeholders, fallback e persistência. readme.md não mudou porque as instruções de operação e os limites documentados permanecem corretos; as correções restauram o comportamento prometido. CHANGELOG.md continua reservado ao CLOSE após revisão, conforme PROJECT-POLICY/contexto. Nenhum arquivo de produto fora de SCOPE foi alterado.

## Evidência antes/depois

Antes dos reparos foram acrescentadas regressões e executados os fontes aprovados sem as correções. DEVELOP-REVISION-002-RED.log e DEVELOP-REVISION-002-RED-PRESENTATION.log preservam 4 falhas entre 5 testes Qt. No segundo log, spies mantêm a rotina de apresentação real e mostram explicitamente “dismissed panel reopened”, “quiz lost its space”, “1 files” e callbacks de glance inesperados. O teste original continua passando.

As primeiras rodadas após a correção revelaram erros nas novas fixtures, preservados nos logs FOCAL-INITIAL e FOCAL-GUARD: nome incorreto do helper de contagem, busca Qt de seleção com emoji e sondagem de platform.system no Python 3.15 que tentou acesso fora do projeto descartável. Foram corrigidos o nome para _count_files, a seleção para offsets UTF-16 reais e o perfil Windows explícito durante import, sem desabilitar os guards. Nenhuma mudança de OS/ambiente ou instalação foi feita.

Resultado final:
- python -m unittest discover -s tests -v: exit code 0; 66 testes PASS em 20.874s. Log DEVELOP-REVISION-002-UNITTEST-FINAL.log. São os 62 anteriores mais quatro regressões. Os 11 testes de idioma incluem as seis verificações de catálogo/configuração e os cinco cenários Qt.
- python -m providers._tests: exit code 0; 98 PASS, 0 FAIL, 2 SKIP. Log DEVELOP-REVISION-002-PROVIDERS.log. Skips opcionais: Piper ausente, seleção de idioma e síntese não exercitadas; não contados como PASS.
- Testes Qt em subprocessos com timeout de 60s, projeto temporário contendo somente fontes e dados sintéticos, perfil/caches redirecionados, fontes locais já instaladas e guard existente contra rede/escritas externas. Nenhuma sessão real, chave, áudio físico ou modelo/serviço externo.
- Pintura/formatação real de pasta e arquivo sem extensão/com extensão: idiomas en, pt-BR, en; contagens 0, 1, 2, 5000; marcador +; nomes sentinela preservados. Repaint de widget já carregado tem helper de enumeração protegido por mock que falha se for chamado.
- Painel visível: seleção contém emoji/acentos, rolagem positiva (25), rótulos code/review atualizados, tamanhos e visibilidade preservados. Quiz: segunda pergunta, resultado anterior e texto em andamento mantidos, conteúdo anterior continua sem espaço, callbacks adicionais ausentes, nos três tipos de payload.
- Renders novos em renders-revision-002/: rev2-folder-*, rev2-file-* e rev2-quiz-plain/code/review-* nos dois idiomas. Inspeção focal dos renders completos confirmou texto traduzido, dados preservados, quiz visível e botão RESPONDER inteiro. Capturas isoladas do subpainel feitas durante diagnóstico podem conter artefatos de repintura do offscreen; não foram usadas como evidência visual final. Os renders completos finais são os arquivos rev2-quiz-<tipo>-<idioma>.png.
- python .ai/changes/change-004/validate_revision_002.py: exit code 0; 12 caminhos aprovados verificados, quatro alterados. Baseline aprovado intacto e snapshots anteriores conferem; UTF-8 estrito sem BOM; CRLF dos fontes que o usavam e LF de i18n/testes preservados; nenhuma conversão/migração. DEVELOP-REVISION-002-ENCODING.json registra hashes anteriores/atuais. Intenção histórica continua UNKNOWN.
- git -c core.whitespace=cr-at-eol diff --check -- gui/window.py gui/widgets.py: exit code 0, sem alterar configuração Git. Diff exato contra o snapshot aprovado em DEVELOP-REVISION-002.patch.

## Ambiente, segurança e limites

Windows, Python 3.15.2, PyQt6 6.12.1, Qt 6.12.0. Reutilizado o ambiente preparado e autorizado anteriormente; não houve nova instalação, download, alteração de requirements, PATH, ACL, UAC ou política do Codex. O launcher normal retornou Acesso negado; cada repetição de operação runtime usou o mecanismo oficial com os mesmos argumentos/cwd/runtime_root, sem substituir interpretador nem editar estado/lock manualmente.

A evidência é local/sintética/offscreen. Permanecem UNKNOWN UI interativa em todas as resoluções/plataformas, fallback de ícones/fontes, acessibilidade integral, áudio físico e serviços reais. Não houve nova Boundary Stop material; os registros DEP-004-001 e retomadas anteriores permanecem históricos. Sem alterações de KR, versão, commit, tag ou publicação.

## Conclusão desta etapa

R004-001 e R004-002 estão tratados pela implementação e regressões acima, sujeitos à nova REVIEW. Não apagar a condição histórica de achados da primeira revisão nem registrar aprovação humana automática. Completar somente DEVELOP pelo Core com o lease desta sessão; próxima etapa depende de pedido ai-sdd review.