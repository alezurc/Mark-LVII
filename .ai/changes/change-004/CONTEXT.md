# CONTEXT — change-004 — revisão 002 — correções do REVIEW

## Intenção, origem e gate humano

Preservar a funcionalidade de escolha persistente e imediata entre English/en (padrão) e Português (Brasil)/pt-BR na interface desktop e corrigir os achados R004-001 e R004-002 da primeira REVIEW.

Origem rastreável: decisão humana registrada pelo Core como REVIEW_CHANGES_REQUESTED, referência literal “Autorizo realizar todas as correções necessárias indicadas no REVIEW.md”, seguida de `$ai-sdd context change-004` e “pode continuar” nesta conversa. Essas mensagens autorizam preparar este CONTEXT revisado; a referência de changes-requested não substitui nova aprovação do CONTEXT. Estado observado: develop_authorized=false.

Revisão 002 proposta; human_gate PENDING; approval_reference desta revisão NONE. Não implementar correções, executar testes de implementação ou avançar automaticamente nesta etapa. O CONTEXT anterior, seus artefatos de aprovação/baseline e relatórios foram copiados byte a byte para context-history/revision-001/, com hashes em MANIFEST.json. Os relatórios/evidências originais de DEVELOP/REVIEW e os registros DEP-004-001 permanecem preservados; resultados anteriores não são reclassificados.

## Evidência atual e diagnóstico delimitado

A implementação de idioma já existe. gui/i18n.py possui catálogo, Text explícito, bindings fracos e fallback; ui.py carrega a preferência antes da construção da janela, e config_manager persiste pelo gerenciador existente. A versão anterior da proposta descrevia esses componentes como futuros; nesta revisão eles são a base existente a preservar.

R004-001, CONFIRMED por REVIEW.md/REVIEW-PROBES.log: _refresh_language_content em gui/window.py chama rotinas de apresentação que revelam o painel e alteram QSplitter. Conteúdo dispensado reabre ao trocar idioma (isHidden True → False); em quiz ativo, tamanhos HUD/conteúdo/quiz [526, 0, 250] passaram a [556, 220, 0]. A visibilidade Qt isolada não demonstra se um item do splitter possui espaço real. Preservar os tamanhos e o estado de apresentação é parte de AC3.

R004-002, CONFIRMED: _DropCanvas._paint_file em gui/widgets.py forma FILE/FOLDER e contagem files como strings comuns. Em pt-BR, a reprodução registrou ['📁', 'CLOSE', 'FOLDER  ·  3 files']; CLOSE era nome sintético que deve continuar intacto. render() deliberadamente não traduz strings comuns. Corrigir o molde próprio, sem buscar/substituir palavras em conteúdo arbitrário.

A primeira revisão reexecutou 62 unittest PASS e providers 98 PASS/0 FAIL/2 SKIP opcionais de Piper, mas seus probes confirmaram os dois defeitos fora da cobertura existente. São evidências históricas, não testes novos nesta etapa. Não apagar o REVIEW anterior nem executar seu probe como se exit 0 comprovasse correção: o script histórico afirma a presença dos bugs.

CONTEXT-EVIDENCE-REVISION-002.json contém hashes atuais dos 12 alvos, UTF-8 estrito, BOM e finais de linha. Arquivos originalmente novos na proposta 001 agora existem; todos os alvos atuais são TEXT no perfil conservador. Bytes válidos não provam intenção histórica de encoding, que permanece UNKNOWN.

## Escopo exato e limites

SCOPE.json mantém os mesmos 12 caminhos exatos, sem novos caminhos/globs/diretórios. Nenhum aumento de escopo foi solicitado:

- gui/window.py: corrigir retradução para preservar apresentação, visibilidade, tamanhos do splitter, seleção/rolagem e quiz ativo; manter APIs/sinais e fluxo de abertura normal.
- gui/widgets.py e gui/i18n.py: catalogar e desenhar rótulos/molde de arquivo/pasta carregados, incluindo singular/plural e limiar de contagem, mantendo dados opacos e fallback.
- tests/test_ui_language.py e tests/test_ui_language_qt.py: incorporar regressões dos dois achados nos arquivos de teste já existentes; não criar um terceiro arquivo fora da lista.
- gui/overlays.py, gui/providers_panel.py, gui/hud.py, ui.py e memory/config_manager.py: permanecem superfícies da funcionalidade original, sujeitas à regressão e à preservação dos requisitos. Não usá-las para refatoração sem nexo com a correção delimitada.
- readme.md: ajustar somente se comportamento/instruções realmente mudarem; se mantidas, justificar no relatório. CHANGELOG.md permanece reservado à consolidação de resultados revisados no CLOSE.

Não editar main.py, actions, plugins, providers de produção, dashboard, engines, tema, fontes, requirements.txt ou configuração pessoal. Não mudar idioma da conversa/voz/STT/TTS/modelos, nomes, IDs, caminhos, extensões ou dados recebidos. Sem pesquisa/contato externo, instalações/downloads, nova preparação de ambiente, versão, commit, tag ou publicação. Manter política de C/fontes e única QApplication no principal; widgets nunca em worker.

Os critérios AC1–AC9 originais abaixo continuam obrigatórios e não são reduzidos por esta revisão. A regra original de UTF-8 sem BOM/LF para fontes que eram novos na revisão 001 passa a ser preservação dos bytes/finais de linha atuais desses mesmos arquivos (já existentes), sem migração.

## Critérios de aceitação

AC1 — Escolha explícita em Personalização com nomes reconhecíveis English e Português (Brasil), valores estáveis en e pt-BR. Sem preferência ou com valor inválido, usar inglês. Não inferir idioma pelo SO. Cancelar não salva nem altera o idioma; salvar aplica e persiste. Falha de gravação deve aparecer ao usuário, sem anunciar persistência bem-sucedida ou apagar outros settings.

AC2 — Persistência exclusivamente por config_manager, com locking e atualização mesclada existentes. Reiniciar carrega a preferência antes de construir widgets. Idioma da UI é independente de voz e serviços; trocar somente idioma não reconecta sessão nem muda provedor, voz, nomes, cor ou dados.

AC3 — Aplicação imediata en → pt-BR → en na janela aberta, sem reinício da aplicação. Atualizar rótulos, botões, placeholders, tooltips, cabeçalhos, instruções, estados pintados e mensagens estruturais das superfícies em escopo; widgets/painéis criados depois usam o idioma vigente. Preservar texto digitado, seleções, sessão, conteúdo, tarefas, callbacks e conexões; não reconstruir a aplicação ou duplicar timers/sinais para traduzir. Não traduzir conteúdo por varredura/substituição arbitrária de todos os textos dos widgets.

AC4 — Catálogo central com chaves estáveis ou mensagens-fonte explicitamente catalogadas e cobertura simétrica para os dois idiomas. Preservar placeholders nomeados, plural/contagens quando aplicável, símbolos e escapes. Chave/tradução ausente ou locale inválido não pode derrubar UI: fallback determinístico em inglês. Falhas de catálogo devem ser detectáveis na validação; fallback não justifica catálogo pt-BR incompleto. Nunca chamar core.gemini para traduzir a interface.

AC5 — Localizar todas as mensagens próprias de UI presentes nos seis módulos GUI delimitados, inclusive estados alternativos, painéis abertos após a troca, confirmação, quiz/review e controles de providers/plugins. Conteúdo do usuário e valores dinâmicos ficam intactos, mesmo se iguais a uma chave ou frase inglesa do catálogo. Manter tokens internos, atalhos e comportamento dos comandos; nomes técnicos adequados permanecem nomes próprios.

AC6 — Qt somente no thread principal; nenhuma QApplication adicional e nenhum widget em worker. Se houver nova entrada cross-thread, usar signal em MainWindow e método fino emissor em JarvisUI. Cor/fontes seguem C e helpers existentes. Acomodar expansão do português com layouts/scroll/tamanhos responsivos; seletor e ações salvar/cancelar devem permanecer acessíveis na menor altura suportada pelo painel atual.

AC7 — Testes puros de normalização, fallback, paridade de chaves e placeholders, acentos e persistência com CONFIG_DIR/CONFIG_FILE temporários. Provar preservação de outros settings e falha de gravação sem sucesso falso. Não ler/restaurar configuração real como técnica de isolamento.

AC8 — Testes Qt offscreen no principal de subprocesso limitado: mudança nos dois sentidos em janela/painéis representativos, estado pintado, painel criado após troca, cancelamento e inicialização no idioma salvo. Incluir conteúdo sentinela e entrada digitada para provar que não são traduzidos/perdidos; provar que troca de idioma isolada não dispara reconexão de voz. Capturar retorno/logs sem DEVNULL; timeout/falha/skip não conta como PASS. Registrar ambiente e limites. Evidenciar layout por render offscreen em ambos os idiomas e inspeção visual focal, sem alegar equivalência a observação interativa real.

AC9 — Preservar bytes de encoding/BOM/finais de linha dos arquivos existentes; novos fontes/testes UTF-8 sem BOM, LF. ENCODING-POLICY.json não propõe migração nem decisão UNKNOWN. Runtime captura baseline em complete CONTEXT e recaptura na aprovação. Caso detecte UNKNOWN material, parar e revisar a proposta antes do gate humano. readme e changelog devem descrever comportamento verificado, sem prometer tradução de conteúdo/serviços.


## Critérios adicionais de correção e regressão

AC10 — R004-001: retraduzir nunca deve reabrir conteúdo dispensado, revelar conteúdo colapsado pelo quiz, ocultar o quiz, mudar a aba ativa ou alterar os tamanhos do splitter. Separar atualização textual de abertura/revelação, ou adotar outra solução equivalente que preserve esse contrato sem reconstruir a aplicação. O caminho normal de receber um conteúdo novo ainda deve abri-lo conforme o comportamento existente.

AC11 — R004-001: testes Qt offscreen devem cobrir troca en → pt-BR → en após dispensar conteúdo e com quiz ativo após conteúdo anterior, inclusive payloads plain/code/review onde suas rotinas possam revelar o painel. Afirmar tamanhos efetivos de QSplitter, visibilidade, índice/pergunta/resposta em andamento, conteúdo sentinela e ausência de callbacks/reconexões adicionais. Cobrir também painel visível que precisa atualizar rótulos mantendo rolagem/seleção. Não depender somente de isHidden, nem tornar a regressão verde apagando os testes existentes.

AC12 — R004-002: localizar FILE como rótulo fallback de arquivo sem extensão, FOLDER e o molde da contagem de arquivos. Em inglês, usar file/files conforme 1 e demais contagens; em pt-BR, arquivo/arquivos. Preservar o marcador + quando a contagem atingir o limite já usado (5000). O nome da pasta, caminho, extensão e conteúdo ficam idênticos, mesmo quando forem CLOSE, FILE ou FOLDER. A alternância atualiza o estado carregado por repintura, sem recarregar a pasta, enumerar dados pessoais ou alterar a seleção.

AC13 — R004-002: testes precisam alcançar o ramo real de pintura/formatação do item carregado, além de verificar presença de entradas no catálogo. Cobrir arquivo sem extensão, arquivo com extensão preservada e diretório sintético; contagens 0, 1, 2 e limite 5000 com +, em en e pt-BR e nos dois sentidos de troca. Usar nomes sentinela iguais a mensagens do catálogo para provar que não foram traduzidos. Mock de painter pode verificar texto exato; render focal verifica layout sem truncamento indevido do molde.

## Validação planejada para DEVELOP/REVIEW posteriores

Primeiro registrar regressões que demonstrem os defeitos nos fontes atuais; depois implementar somente as correções delimitadas e comprovar os cenários corrigidos. Usar projetos/fixtures temporários, Qt offscreen no principal de subprocesso com timeout, dados sintéticos e guards existentes. Não iniciar main.py, sessão real, serviços, áudio físico ou modelos. Reaproveitar a preparação de ambiente já autorizada/documentada em RESUMPTION-004-DEP-004-001.md; não reinstalar nada nesta revisão.

Executar testes focais de idioma, unittest existente e suíte providers isolada; registrar comandos, ambiente, duração, contagens, retorno e limites sem DEVNULL. SKIP não é PASS. Renders en/pt-BR devem incluir estado de pasta/arquivo carregado e cenários relevantes de conteúdo/quiz; não usar somente os renders antigos de seletores como evidência dos novos critérios. A suite verde anterior não prova os dois reparos.

Registrar evidência nova com nomes/revisão próprios (por exemplo DEVELOP-REVISION-002.md e REVIEW-REVISION-002.md), preservando os relatórios/logs anteriores. Atualização de arquivos canônicos de relatório, se necessária pelo runtime, exige preservar primeiro a versão anterior e sua proveniência; jamais apagar achados ou promover resultado histórico. Nenhuma edição manual de .ai/AI-SDD.yaml, APPROVED-SCOPE, lock ou baseline: complete CONTEXT recaptura baseline pelo Core e a nova aprovação recaptura/vincula o escopo.

## Encoding, riscos, incógnitas e gate

ENCODING-POLICY.json continua com migrations=[] e unknown_decisions=[]. Preservar UTF-8 sem BOM e CRLF dos fontes existentes que o usam; preservar LF dos testes/gui/i18n.py/CHANGELOG conforme evidência atual. Não fazer recodificação integral incidental nem converter UNKNOWN histórico em intenção confirmada. Se aparecer UNKNOWN material ou divergência de bytes não explicada, parar e revisar a proposta antes de nova aprovação.

Riscos INFERRED: reapresentação acidental por helpers compartilhados, restauração de splitter baseada só em flags, perda de seleção ao redesenhar conteúdo e tratamento incorreto de singular/plural/limiar. Mitigar por AC10–AC13 e regressão dos fluxos normais. Mantêm-se UNKNOWN UI interativa, acessibilidade integral e comportamento em todas as plataformas/resoluções. Não investigar engenharia externa para preencher esses limites.

Não há nova Boundary Stop material nesta preparação estática; DEP-004-001 e sua resolução delimitada permanecem históricos, sem reabertura automática. Falha futura fora da capacidade/escopo autorizado exige registrar limite e parar o ramo conforme BOUNDARY-STOP-CONDITION, sem instalar/contornar automaticamente.

Nova aprovação humana explícita deste CONTEXT revisão 002 é obrigatória para reautorizar DEVELOP. A decisão changes-requested, aprovações anteriores e “pode continuar” não são usadas como referência de aprovação desta proposta. Concluir apenas CONTEXT; não avançar automaticamente.