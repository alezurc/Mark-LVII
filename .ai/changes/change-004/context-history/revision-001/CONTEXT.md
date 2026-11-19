# CONTEXT — change-004 — idioma da interface desktop

## Intenção e gate

Pedido humano: “quero implementar a possibilidade de escolher o idioma da interface, entre o inglês, idioma atual e o pt-br”. Interpretação: dois idiomas, English (en) e Português (Brasil) (pt-BR); inglês é o padrão atual. Preparar escolha persistente, reversível e aplicada imediatamente na interface desktop existente.

human_gate PENDING; reference NONE. Esta proposta não autoriza DEVELOP. Não reutilizar aprovações anteriores. Não avançar automaticamente.

## Evidência e arquitetura

DISCOVERY discovery-2026-11-18-02 confirma GUI Qt no thread principal, workers para ferramentas, configuração por memory/config_manager.py e intenção histórica de encoding UNKNOWN (D007). D011 conserva limites da evidência integrada; esta mudança não prova áudio físico ou serviços reais. PROJECT-POLICY.md exige documentação operacional e changelog por change-id, sem nova versão automática.

Inspeção estática: JarvisUI em ui.py cria/reutiliza a única QApplication antes de MainWindow. CustomizeOverlay em gui/overlays.py contém nome, voz e cor; MainWindow._open_customize conecta saved a _apply_name_update, que persiste por update_config. Existe configuração atômica com RLock; não foi lido config/api_keys.json. Textos fixos estão distribuídos em window, overlays, providers_panel, widgets e estados pintados em hud. Não foi encontrado mecanismo de localização nessas superfícies. Estados internos como LISTENING/THINKING são identificadores funcionais e não devem ser traduzidos internamente.

CONTEXT-EVIDENCE.json registra hashes, validação UTF-8 estrita, BOM e finais de linha dos alvos existentes e MISSING dos novos. Bytes UTF-8 válidos não provam intenção histórica. Nenhum teste/aplicativo/serviço foi executado nesta etapa; houve apenas leitura de fontes e documentos.

## Escopo exato

SCOPE.json enumera 12 arquivos:

- gui/i18n.py (novo): catálogo central en/pt-BR, resolução de idioma, fallback e formatação; sem chamada de modelo, rede ou dependência nova.
- memory/config_manager.py: leitura/validação e gravação da preferência ui_language pelos mecanismos existentes, preservando demais settings.
- ui.py: carregar idioma antes da construção da janela; manter API pública e reexports compatíveis.
- gui/overlays.py: seletor de idioma em Personalização e localização dos textos próprios dos overlays, inclusive setup, áudio, memória, remoto e plugins.
- gui/window.py: aplicar preferência no Qt principal e atualizar textos fixos da janela, drawers, conteúdo estrutural, estados e avisos próprios.
- gui/providers_panel.py: traduzir estrutura, instruções e controles do painel; preservar IDs e nomes de provedores/modelos.
- gui/widgets.py e gui/hud.py: traduzir rótulos e estados visuais próprios, inclusive textos pintados, sem alterar tokens funcionais.
- tests/test_ui_language.py e tests/test_ui_language_qt.py (novos): catálogo, persistência isolada e comportamento Qt offscreen.
- readme.md: instrução de escolha, persistência, padrão e limites.
- CHANGELOG.md: consolidar resultado revisado no CLOSE, conforme política.

Não editar main.py, actions, plugins, providers de produção, dashboard web, prompts, engines, tema, fontes ou dependências. Não alterar idioma de voz/STT/TTS/modelos/conversas. Não traduzir nomes próprios, marcas, comandos, IDs, caminhos, URLs, chaves, dados pessoais, conteúdo gerado ou recebido, mensagens brutas de exceção ou logs originados fora da GUI. Textos próprios da GUI que envolvem dados variáveis devem traduzir somente o molde. Histórico já exibido não será reescrito. Formulários genéricos de plugins traduzem estrutura própria, preservando descrições e nomes fornecidos pelo plugin. Diálogos nativos do sistema seguem o idioma do sistema e não fazem parte do catálogo desktop.

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

## Validação planejada

Não executar implementação/testes nesta etapa. No DEVELOP autorizado: testes focais novos, regressões unittest existentes pertinentes e suíte providers isolada quando disponível; não iniciar main.py nem usar chaves/áudio real. Qt offscreen com fixtures e configuração temporárias, sem rede/modelos, sem instalação de dependências ou download. Registrar comandos, retornos, contagens e cobertura ausente; diff/AST não substituem prova comportamental. Rever cobertura do catálogo contra fontes GUI e registrar exceções justificadas de nomes/dados. Comparar encoding antes/depois e no REVIEW.

## Riscos, incógnitas e limites

INFERRED: textos montados dinamicamente, estados pintados e dimensões fixas dos overlays podem deixar traduções incompletas ou cortes. Mitigar por catálogo, testes de estados e renders. UNKNOWN: aspecto interativo em todas as resoluções/plataformas; teste offscreen não demonstra acessibilidade ou layout universal. Intenção histórica de encoding permanece UNKNOWN; não converter arquivos globalmente.

Nenhum blocker externo material identificado para preparar este contexto. Não reabrir DEP-001 de change-003. Se dependência ausente bloquear evidência requerida, registrar consequência e aplicar Boundary Stop sem instalar/contornar automaticamente. Se surgir necessidade de editar arquivo fora de SCOPE, parar antes da alteração e pedir expansão auditável pelo fluxo canônico.

Working tree e dados preexistentes não pertencem automaticamente a change-004; preservar alterações alheias e comparar com hashes atuais antes do trabalho. Não ler dados privados, editar runtime manualmente, atribuir versão, criar commit/tag ou publicar.

## Gate humano

Proposta pronta para revisão da intenção, 12 caminhos, AC1–AC9 e limites. Completar CONTEXT apenas registra preparação; aprovação humana explícita com referência é necessária antes de DEVELOP. Sem avanço automático.