# DEVELOP — change-004 — idioma da interface desktop

Implementação concluída no escopo de CONTEXT aprovado pela referência “Autorizo a execução após analisar o CONTEXT.md”. Adaptador codex, papel IMPLEMENTER. Lease desta sessão: d932546f-948d-48f9-a7b9-fd678ebd41b3. Não executar REVIEW ou decisão humana automaticamente.

## Comportamento implementado

Escolha English/en e Português (Brasil)/pt-BR em Configuração → Personalizar assistente. Inglês é padrão para ausência/valor inválido. Salvar persiste ui_language pelo config_manager e aplica imediatamente; cancelar não persiste. Persistência ocorre antes da alteração visual, e uma falha deixa o painel aberto com diagnóstico e idioma anterior. Troca isolada de idioma não emite atualização de identidade/voz nem reconecta o assistente.

Catálogo central gui/i18n.py com mensagens-fonte e traduções, placeholders e fallback em inglês. Text é uma marca explícita para texto próprio da interface; strings comuns de conteúdo/nomes/dados não são traduzidas. Bindings fracos atualizam apenas textos marcados, sem varrer/substituir textos arbitrários. Preservam seleção/dados de combos, inclusive entrada editável. Inserção/remoção de itens mantém suas associações de tradução. Qt recebe a atualização no thread principal; tentativa em worker é rejeitada.

Rótulos, instruções, tooltips, placeholders, diálogos próprios, controles, quiz/review, painel de providers/plugins, desenhos de estados e HUD, data e estruturas de progresso/rotinas foram localizados. Cache gráfico inclui o idioma. Conteúdo de código/review é redesenhado a partir do payload original preservando seleção e posição de rolagem; histórico de log não é reescrito. Campos de dados/provedor/modelo, conteúdo de conversas, resultados externos e prompts de ações da área de transferência permanecem intactos. A voz e idioma dos modelos não foram alterados.

Personalização tem formulário com scroll e ações fixas acessíveis a 420 px na fixture. Cards de providers usam labels com quebra de linha para o parágrafo inteiro caber nos dois idiomas; menus de configuração ganharam largura. Estilos seguem C e fontes existentes. readme.md documenta uso e limites. CHANGELOG.md permanece intacto para consolidação no CLOSE após revisão, conforme política/contexto.

## Ambiente e retomada

Python 3.15.2, PyQt6 6.12.1, Qt 6.12.0, Windows. Preparação autorizada de PyQt6, requirements.txt e Build Tools detalhada em RESUMPTION-004-DEP-004-001.md e históricos vinculados. Usuário concluiu instalação de Build Tools; PyYAML compilou e pip install -r requirements.txt terminou com exit code 0. pip check: No broken requirements found. Import ui verificado com threads desativadas. A retomada não converte UNKNOWN histórico em garantia universal.

O launcher Python do WindowsApps ainda falha com Acesso negado no contexto restrito; as repetições pelo mecanismo oficial executaram. Não houve alteração de PATH, UAC, ACL ou política do Codex. Comandos runtime sempre usaram runtime_root declarado em .ai/AI-SDD.yaml; não houve fallback para outro Python nem edição manual de estado/lease.

## Validação

- python -m unittest discover -s tests -v: exit code 0; 62 testes PASS em 7.941s na rodada final. Log completo unittest.log. Inclui 7 novos testes: catálogo/placeholders/cobertura, normalização/fallback, composição e preservação de dados, persistência/falha e teste Qt em subprocesso limitado. Mantém regressões VS Code, memória, isolamento, encoding e smoke harness.
- python -m providers._tests: exit code 0; 98 PASS, 0 FAIL, 2 SKIP. Log providers.log. Skips: Piper ausente, seleção de idiomas e síntese opcional não exercitadas; não contados como PASS. Não instalar extras opcionais para inflar evidência.
- Teste Qt: projeto temporário somente com fontes, configuração/cache/dados sintéticos, Qt offscreen e timeout 60s. Verificou inicialização no idioma salvo, en → pt-BR → en, cancelar, falha de gravação com painel aberto, texto digitado/conteúdo sentinela preservados, combo editável, IDs/seleções/sinais, ausência de reconexão da voz, painel novo e troca de idioma no painel existente de providers, estados internos estáveis, atualização estrutural de código/review, bloqueio de mudança por worker.
- Renders inspecionados de janela, Personalização a 480×420 e providers nos dois idiomas em renders/. A fixture redireciona perfil/caches e registra a fonte Segoe UI já instalada em Windows/Fonts para não ocultar as fontes do SO; isso não altera fontes do produto. Primeiras imagens mostraram glyphs ausentes, depois corrigidos na fixture; renders finais substituíram os de diagnóstico. Ícones de emoji/símbolos ainda dependem de fallback de fonte da plataforma e não foram tratados como prova de cobertura universal.
- python .ai/changes/change-004/validate_encoding.py: ENCODING_OK em 12 caminhos aprovados. Baseline SHA-256 vinculado à aprovação intacto; snapshots anteriores conferem; existentes UTF-8 sem BOM e CRLF/LF preservados, novos UTF-8 sem BOM/LF. Evidência DEVELOP-ENCODING.json. Intenção histórica continua UNKNOWN.
- git -c core.whitespace=cr-at-eol diff --check nos arquivos existentes de escopo: exit code 0. A configuração apenas por comando permite avaliar whitespace sem tratar CRLF preservado como erro; nenhuma configuração Git foi gravada.

## Escopo e limites

11 arquivos de produto/testes/documentação alterados/criados, todos em SCOPE.json; o 12º caminho (CHANGELOG.md) reservado ao CLOSE permaneceu intacto. Alterações preexistentes fora de escopo preservadas. Sem chaves/dados pessoais, rede/modelos nos testes, áudio físico, sessão real, versão nova, commit, tag ou publicação.

Esta evidência é integração sintética local em Windows/Python 3.15.2; não demonstra UI interativa em todas as resoluções/plataformas, áudio físico, acessibilidade completa, serviços externos ou crash. Descrições fornecidas por serviços/plugins/engines e diálogos nativos podem seguir o idioma de origem/SO, como delimitado no CONTEXT. Não alegar tradução de dados externos nem cobertura universal.

## Próxima etapa

Solicitar ai-sdd review quando desejado. Este relatório é evidência de implementação, não REVIEW.md ou decisão humana de revisão. Completar DEVELOP somente pelo launcher com execution_id desta sessão; não avançar automaticamente.