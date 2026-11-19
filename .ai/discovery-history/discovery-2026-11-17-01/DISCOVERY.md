# Discovery — Mark-LVII

Execução: discovery-2026-11-17-01. Revisão Git: `f1a560b6073479990d92d3d34a90d7f41cdbfa00`. FIRST_BASELINE; baseline null porque não havia relatório anterior comparável. Nenhum histórico foi sobrescrito.

## Escopo e método

Inspeção estática aprofundada dos pontos de entrada, loaders, UI, configuração, memória, tarefas, rotinas, pesquisa, providers, dashboard e agente de código. Manifests: requirements.txt e setup.py; Python mínimo 3.11, PyQt6, sounddevice/numpy, google-genai/httpx, Playwright e FastAPI/Uvicorn. Origin: https://github.com/alezurc/Mark-LVII.git; upstream: https://github.com/FatihMakes/Mark-LVII.git.

O inventário em DISCOVERY-EVIDENCE.json captura hashes dos fontes e documentos selecionados, encoding/BOM, método, confiança e limitações. Foram analisados 102 arquivos, incluindo 95 arquivos Python por AST, sem importar o produto. Erros de sintaxe encontrados: 0. Isso não substitui testes comportamentais. Fontes locais/untracked são identificadas pelo hash; o SHA Git identifica o checkout, não os documentos de governança novos.

Segredos/configuração pessoal, conteúdo de memória, checkpoints, relatórios pessoais, mídia, dependências, caches e internals Git foram excluídos da leitura de conteúdo. Apenas metadados do índice demonstram artefatos runtime versionados. A busca de testes encontrou providers/_tests.py e o harness core/_smoke_harness.py; não estabelece ausência absoluta de outros testes.

## Arquitetura e contratos

main.py coordena voz e ferramentas; ui.py adapta chamadas thread-safe para gui/window.py. gui/theme.py e gui/style.py são os pontos de paleta/fontes. core/action_loader.py descobre TOOL e core/plugin_loader.py descobre PLUGIN; helpers iniciados por underscore são ignorados. Plugins são opt-out via config_manager. core/tasks contém scheduler, checkpoints, ferramentas limitadas e pesquisa; core/routines agenda ações recorrentes. agents/*.md descreve perfis, sem conceder ferramentas fora da allowlist. providers oferece pipeline STT/LLM/TTS opcional. dashboard/server.py fornece pareamento e controle remoto. core/confirm.py guarda ações irreversíveis atrás da UI; core/outcome.py distingue resultado verificado, não verificado e falha. core/code_checks.py e actions/dev_agent.py implementam verificações e proteção de projetos editados.

## Findings

| ID | Subject | Classification | Comparison | Evidence | Description / implication |
|---|---|---|---|---|---|
| D001 | architecture.qt-worker-boundary | 🟢 CONFIRMED | NEW | main.py:1727 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; main.py:3052 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; ui.py:103 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; ui.py:265 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; gui/window.py:398 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00 | Qt fica no thread principal; a sessão asyncio roda em thread dedicado; ações/plugins são despachados ao executor. JarvisUI emite sinais para a janela. / Mudanças de UI devem preservar os sinais e a única QApplication; ferramentas não podem construir widgets. |
| D002 | automation.background-policy | 🟢 CONFIRMED | NEW | core/tasks/tools.py:87 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; core/tasks/tools.py:96 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; core/tasks/engine.py:268 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00 | TaskEngine agenda workers e TaskTools filtra ferramentas, separa web de recall_memory e restringe caminhos à pasta da tarefa. / Trabalho longo pertence ao motor de tarefas; isto confirma controles estáticos, não isolamento completo demonstrado. |
| D003 | automation.routines-and-research | 🟢 CONFIRMED | NEW | core/routines/engine.py:114 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; core/tasks/research.py:111 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; core/tasks/research.py:342 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; main.py:726 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00 | Rotinas usam armazenamento compartilhado de JSON; pesquisa registra fontes e verifica trechos contra páginas salvas. / A verificação textual de citações não demonstra verdade factual nem qualidade global do relatório. |
| D004 | configuration.atomic-settings | 🟢 CONFIRMED | NEW | memory/config_manager.py:38 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; memory/config_manager.py:52 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; memory/config_manager.py:69 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00 | Configuração usa RLock, arquivo temporário e os.replace, com tratamento de arquivo corrompido. / Usar config_manager; serialização dentro do processo não prova coordenação entre processos ou durabilidade após perda de energia. |
| D005 | dashboard.transport-fallback | 🟢 CONFIRMED | NEW | dashboard/server.py:1248 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; dashboard/server.py:1276 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; dashboard/server.py:750 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00 | Dashboard usa pareamento/tokens e pode servir HTTP em 0.0.0.0 quando TLS não está disponível, com aviso explícito. / Exposição real depende da configuração/rede; não foi verificada. Requisito de TLS obrigatório exigiria contexto específico. |
| D006 | developer.vscode-success-claim | 🔴 CONFLICT | NEW | AGENTS.md @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; actions/dev_agent.py:299 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00 | _open_vscode descarta stdout/stderr com DEVNULL, espera 1,5 s e anuncia VSCode opened sem verificar janela/processo; conflita com a regra geral do AGENTS.md. / Uma tentativa pode ser anunciada como sucesso. Corrigir apenas em change com contexto e aprovação próprios. |
| D007 | encoding.intent-not-established | ⚪ UNKNOWN | NEW | .ai/DISCOVERY-EVIDENCE.json @ f1a560b6073479990d92d3d34a90d7f41cdbfa00 | O inventário registra hash, BOM e decodificação estrita por arquivo; a intenção de encoding sem BOM permanece desconhecida. / Antes de aprovação de CONTEXT, preparar SCOPE.json com arquivos exatos e política de encoding quando necessária; preservar bytes no DEVELOP. |
| D008 | memory.persistence-risk | 🟡 INFERRED | NEW | memory/memory_manager.py:118 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; core/tasks/store.py:31 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00 | save_memory grava o arquivo diretamente; o store de tarefas usa temporário e replace. Interrupção durante gravação pode afetar a memória de forma diferente. / Risco de truncamento inferido da estratégia de escrita; nenhum crash ou perda de dados foi reproduzido. |
| D009 | models.shared-ladder-coupling | 🟢 CONFIRMED | NEW | core/gemini.py:714 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; core/gemini.py:814 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; core/tasks/brain.py:142 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00 | core.gemini concentra deadlines/fallback; o motor de tarefas usa a ladder e helpers privados para chamadas com ferramentas. / Mudanças na ladder afetam voz, chamadas avulsas e tarefas; preservar compatibilidade dos caminhos com tool-calling. |
| D010 | repository.runtime-artifacts-tracked | 🟢 CONFIRMED | NEW | .gitignore @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; git ls-files memory/tasks reports @ f1a560b6073479990d92d3d34a90d7f41cdbfa00 | O índice Git contém checkpoints, páginas de pesquisa e um relatório gerado; .gitignore não exclui memory/tasks nem reports. / Revisar política de dados antes de futuras publicações. O conteúdo desses artefatos não foi lido nem classificado como segredo. |
| D011 | tests.end-to-end-evidence | ⚪ UNKNOWN | NEW | providers/_tests.py:1 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; core/_smoke_harness.py:1 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00 | Existem autotestes de providers e harness de smoke, mas esta execução não validou UI, áudio real, serviços externos, recuperação após crash ou plataformas alternativas. / Evidência mínima depende da futura change: testes focais e observação do fluxo afetado. Não declarar funcionamento integrado com base em parsing. |
| D012 | web.dns-rebinding-limitation | 🟢 CONFIRMED | NEW | core/tasks/web.py:21 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; core/tasks/web.py:52 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00; core/tasks/web.py:128 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00 | Fetch valida IPs públicos e redirects, mas documenta limitação quando o hostname resolve de modo diferente entre validação e conexão. / Não apresentar o filtro como sandbox completo; exploração e eficácia em execução não foram testadas. |

## Limites e próximos levantamentos

Não houve chamada de fornecedor, instalação, teste de áudio, abertura da aplicação, simulação de crash, alteração do produto ou teste de exploração. As alegações do README são contexto declarativo; não foram tratadas como medições atuais. Sem change/requisito concreto que dependa de evidência externa, nenhuma condição material de Boundary Stop foi acionada nesta inspeção. UNKNOWNs permanecem abertos, sem promover readiness ou autorização. Se um contexto futuro depender de evidência externa, aplicar o registro e a parada do contrato de boundary, sem expandir automaticamente a investigação.

Prioridades sugeridas para escolha humana: verificação do launcher VS Code; política de artefatos runtime no Git; persistência de memória; requisitos de transporte do dashboard. Nenhuma prioridade autoriza correção. CONTEXT exige change-id explícito, escopo exato e critérios de aceitação. SCOPE/ENCODING-POLICY devem estar preparados antes de aprovação; este inventário não substitui o baseline capturado pelo runtime. Sem criar Knowledge Register paralelo: eventual impacto duradouro de encoding deve usar o KR Day1 no lifecycle apropriado.

## finding_registry

```json
{
  "run_id": "discovery-2026-11-17-01",
  "project_scope": "Mark-LVII / whole-project static discovery",
  "baseline": null,
  "baseline_reason": "Primeiro relatório canônico: .ai/DISCOVERY.md ausente antes desta execução.",
  "comparison_mode": "FIRST_BASELINE",
  "findings": [
    {
      "subject": "architecture.qt-worker-boundary",
      "classification": "CONFIRMED",
      "evidence": [
        "main.py:1727 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "main.py:3052 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "ui.py:103 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "ui.py:265 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "gui/window.py:398 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00"
      ],
      "description": "Qt fica no thread principal; a sessão asyncio roda em thread dedicado; ações/plugins são despachados ao executor. JarvisUI emite sinais para a janela.",
      "implication": "Mudanças de UI devem preservar os sinais e a única QApplication; ferramentas não podem construir widgets.",
      "material": "Qt fica no thread principal; a sessão asyncio roda em thread dedicado; ações/plugins são despachados ao executor. JarvisUI emite sinais para a janela. Mudanças de UI devem preservar os sinais e a única QApplication; ferramentas não podem construir widgets.",
      "id": "D001",
      "comparison_status": "NEW",
      "last_observed": "discovery-2026-11-17-01"
    },
    {
      "subject": "automation.background-policy",
      "classification": "CONFIRMED",
      "evidence": [
        "core/tasks/tools.py:87 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "core/tasks/tools.py:96 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "core/tasks/engine.py:268 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00"
      ],
      "description": "TaskEngine agenda workers e TaskTools filtra ferramentas, separa web de recall_memory e restringe caminhos à pasta da tarefa.",
      "implication": "Trabalho longo pertence ao motor de tarefas; isto confirma controles estáticos, não isolamento completo demonstrado.",
      "material": "TaskEngine agenda workers e TaskTools filtra ferramentas, separa web de recall_memory e restringe caminhos à pasta da tarefa. Trabalho longo pertence ao motor de tarefas; isto confirma controles estáticos, não isolamento completo demonstrado.",
      "id": "D002",
      "comparison_status": "NEW",
      "last_observed": "discovery-2026-11-17-01"
    },
    {
      "subject": "automation.routines-and-research",
      "classification": "CONFIRMED",
      "evidence": [
        "core/routines/engine.py:114 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "core/tasks/research.py:111 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "core/tasks/research.py:342 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "main.py:726 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00"
      ],
      "description": "Rotinas usam armazenamento compartilhado de JSON; pesquisa registra fontes e verifica trechos contra páginas salvas.",
      "implication": "A verificação textual de citações não demonstra verdade factual nem qualidade global do relatório.",
      "material": "Rotinas usam armazenamento compartilhado de JSON; pesquisa registra fontes e verifica trechos contra páginas salvas. A verificação textual de citações não demonstra verdade factual nem qualidade global do relatório.",
      "id": "D003",
      "comparison_status": "NEW",
      "last_observed": "discovery-2026-11-17-01"
    },
    {
      "subject": "configuration.atomic-settings",
      "classification": "CONFIRMED",
      "evidence": [
        "memory/config_manager.py:38 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "memory/config_manager.py:52 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "memory/config_manager.py:69 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00"
      ],
      "description": "Configuração usa RLock, arquivo temporário e os.replace, com tratamento de arquivo corrompido.",
      "implication": "Usar config_manager; serialização dentro do processo não prova coordenação entre processos ou durabilidade após perda de energia.",
      "material": "Configuração usa RLock, arquivo temporário e os.replace, com tratamento de arquivo corrompido. Usar config_manager; serialização dentro do processo não prova coordenação entre processos ou durabilidade após perda de energia.",
      "id": "D004",
      "comparison_status": "NEW",
      "last_observed": "discovery-2026-11-17-01"
    },
    {
      "subject": "dashboard.transport-fallback",
      "classification": "CONFIRMED",
      "evidence": [
        "dashboard/server.py:1248 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "dashboard/server.py:1276 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "dashboard/server.py:750 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00"
      ],
      "description": "Dashboard usa pareamento/tokens e pode servir HTTP em 0.0.0.0 quando TLS não está disponível, com aviso explícito.",
      "implication": "Exposição real depende da configuração/rede; não foi verificada. Requisito de TLS obrigatório exigiria contexto específico.",
      "material": "Dashboard usa pareamento/tokens e pode servir HTTP em 0.0.0.0 quando TLS não está disponível, com aviso explícito. Exposição real depende da configuração/rede; não foi verificada. Requisito de TLS obrigatório exigiria contexto específico.",
      "id": "D005",
      "comparison_status": "NEW",
      "last_observed": "discovery-2026-11-17-01"
    },
    {
      "subject": "developer.vscode-success-claim",
      "classification": "CONFLICT",
      "evidence": [
        "AGENTS.md @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "actions/dev_agent.py:299 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00"
      ],
      "description": "_open_vscode descarta stdout/stderr com DEVNULL, espera 1,5 s e anuncia VSCode opened sem verificar janela/processo; conflita com a regra geral do AGENTS.md.",
      "implication": "Uma tentativa pode ser anunciada como sucesso. Corrigir apenas em change com contexto e aprovação próprios.",
      "material": "_open_vscode descarta stdout/stderr com DEVNULL, espera 1,5 s e anuncia VSCode opened sem verificar janela/processo; conflita com a regra geral do AGENTS.md. Uma tentativa pode ser anunciada como sucesso. Corrigir apenas em change com contexto e aprovação próprios.",
      "id": "D006",
      "comparison_status": "NEW",
      "last_observed": "discovery-2026-11-17-01"
    },
    {
      "subject": "encoding.intent-not-established",
      "classification": "UNKNOWN",
      "evidence": [
        ".ai/DISCOVERY-EVIDENCE.json @ f1a560b6073479990d92d3d34a90d7f41cdbfa00"
      ],
      "description": "O inventário registra hash, BOM e decodificação estrita por arquivo; a intenção de encoding sem BOM permanece desconhecida.",
      "implication": "Antes de aprovação de CONTEXT, preparar SCOPE.json com arquivos exatos e política de encoding quando necessária; preservar bytes no DEVELOP.",
      "material": "O inventário registra hash, BOM e decodificação estrita por arquivo; a intenção de encoding sem BOM permanece desconhecida. Antes de aprovação de CONTEXT, preparar SCOPE.json com arquivos exatos e política de encoding quando necessária; preservar bytes no DEVELOP.",
      "id": "D007",
      "comparison_status": "NEW",
      "last_observed": "discovery-2026-11-17-01"
    },
    {
      "subject": "memory.persistence-risk",
      "classification": "INFERRED",
      "evidence": [
        "memory/memory_manager.py:118 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "core/tasks/store.py:31 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00"
      ],
      "description": "save_memory grava o arquivo diretamente; o store de tarefas usa temporário e replace. Interrupção durante gravação pode afetar a memória de forma diferente.",
      "implication": "Risco de truncamento inferido da estratégia de escrita; nenhum crash ou perda de dados foi reproduzido.",
      "material": "save_memory grava o arquivo diretamente; o store de tarefas usa temporário e replace. Interrupção durante gravação pode afetar a memória de forma diferente. Risco de truncamento inferido da estratégia de escrita; nenhum crash ou perda de dados foi reproduzido.",
      "id": "D008",
      "comparison_status": "NEW",
      "last_observed": "discovery-2026-11-17-01"
    },
    {
      "subject": "models.shared-ladder-coupling",
      "classification": "CONFIRMED",
      "evidence": [
        "core/gemini.py:714 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "core/gemini.py:814 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "core/tasks/brain.py:142 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00"
      ],
      "description": "core.gemini concentra deadlines/fallback; o motor de tarefas usa a ladder e helpers privados para chamadas com ferramentas.",
      "implication": "Mudanças na ladder afetam voz, chamadas avulsas e tarefas; preservar compatibilidade dos caminhos com tool-calling.",
      "material": "core.gemini concentra deadlines/fallback; o motor de tarefas usa a ladder e helpers privados para chamadas com ferramentas. Mudanças na ladder afetam voz, chamadas avulsas e tarefas; preservar compatibilidade dos caminhos com tool-calling.",
      "id": "D009",
      "comparison_status": "NEW",
      "last_observed": "discovery-2026-11-17-01"
    },
    {
      "subject": "repository.runtime-artifacts-tracked",
      "classification": "CONFIRMED",
      "evidence": [
        ".gitignore @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "git ls-files memory/tasks reports @ f1a560b6073479990d92d3d34a90d7f41cdbfa00"
      ],
      "description": "O índice Git contém checkpoints, páginas de pesquisa e um relatório gerado; .gitignore não exclui memory/tasks nem reports.",
      "implication": "Revisar política de dados antes de futuras publicações. O conteúdo desses artefatos não foi lido nem classificado como segredo.",
      "material": "O índice Git contém checkpoints, páginas de pesquisa e um relatório gerado; .gitignore não exclui memory/tasks nem reports. Revisar política de dados antes de futuras publicações. O conteúdo desses artefatos não foi lido nem classificado como segredo.",
      "id": "D010",
      "comparison_status": "NEW",
      "last_observed": "discovery-2026-11-17-01"
    },
    {
      "subject": "tests.end-to-end-evidence",
      "classification": "UNKNOWN",
      "evidence": [
        "providers/_tests.py:1 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "core/_smoke_harness.py:1 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00"
      ],
      "description": "Existem autotestes de providers e harness de smoke, mas esta execução não validou UI, áudio real, serviços externos, recuperação após crash ou plataformas alternativas.",
      "implication": "Evidência mínima depende da futura change: testes focais e observação do fluxo afetado. Não declarar funcionamento integrado com base em parsing.",
      "material": "Existem autotestes de providers e harness de smoke, mas esta execução não validou UI, áudio real, serviços externos, recuperação após crash ou plataformas alternativas. Evidência mínima depende da futura change: testes focais e observação do fluxo afetado. Não declarar funcionamento integrado com base em parsing.",
      "id": "D011",
      "comparison_status": "NEW",
      "last_observed": "discovery-2026-11-17-01"
    },
    {
      "subject": "web.dns-rebinding-limitation",
      "classification": "CONFIRMED",
      "evidence": [
        "core/tasks/web.py:21 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "core/tasks/web.py:52 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00",
        "core/tasks/web.py:128 @ f1a560b6073479990d92d3d34a90d7f41cdbfa00"
      ],
      "description": "Fetch valida IPs públicos e redirects, mas documenta limitação quando o hostname resolve de modo diferente entre validação e conexão.",
      "implication": "Não apresentar o filtro como sandbox completo; exploração e eficácia em execução não foram testadas.",
      "material": "Fetch valida IPs públicos e redirects, mas documenta limitação quando o hostname resolve de modo diferente entre validação e conexão. Não apresentar o filtro como sandbox completo; exploração e eficácia em execução não foram testadas.",
      "id": "D012",
      "comparison_status": "NEW",
      "last_observed": "discovery-2026-11-17-01"
    }
  ]
}
```
