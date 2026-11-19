# Discovery — Mark-LVII — comparação após change-001

Execução: discovery-2026-11-18-01. Escopo: Mark-LVII / whole-project static discovery. Revisão Git: `f1a560b6073479990d92d3d34a90d7f41cdbfa00`; alterações locais são identificadas por SHA-256 no inventário, não atribuídas indevidamente ao commit. Modo COMPARED. Fonte anterior preservada em `.ai/discovery-history/discovery-2026-11-17-01/DISCOVERY.md`, SHA-256 `815d27674713b31e266172cca930831c987cba7d91c0541c6397b62f9c862ed2`.

## Método e arquitetura revalidada

Inspeção estática de 105 arquivos, com parsing AST de 96 arquivos Python: 0 erros. Dos 102 arquivos da baseline, somente actions/dev_agent.py mudou; os outros contratos estáticos foram reconfirmados por igualdade dos bytes e pelas evidências originais. Fontes alteradas, novos testes, políticas, auditoria de CLOSE e KR foram inspecionados nesta execução. Evidência completa em `.ai/discovery-runs/discovery-2026-11-18-01/EVIDENCE.json`.

Python mínimo 3.11; PyQt6, sounddevice/numpy, google-genai/httpx, Playwright e FastAPI/Uvicorn continuam declarados nos manifests sem mudança. main.py mantém sessão asyncio em thread e dispatch ao executor; ui.py mantém QApplication/sinais para gui/window.py. Loaders descobrem TOOL/PLUGIN, ignorando helpers com underscore. TaskEngine/rotinas, isolamento de ferramentas de background, pesquisa com verificação textual de citações, memória, settings e providers mantêm os contratos da inspeção anterior. Não se infere eficácia integrada a partir da existência desses controles.

Caches, segredos/configuração pessoal, conteúdo de memória, checkpoints, mídia e relatórios pessoais foram excluídos da leitura. Somente metadados do índice confirmam 24 artefatos runtime versionados. Não houve instalação, imports do produto, chamadas de modelos/serviços, exploração de rede ou execução da aplicação. Os 29 testes são evidência documental da revisão fechada; não foram executados novamente neste DISCOVERY. AST não é teste comportamental.

## Findings e reconciliação

IDs/subjects anteriores preservados. D006 muda de CONFLICT para CONFIRMED com treatment_status=RESOLVED; o original fica em previous. D011 conserva UNKNOWN, com evidência focal ampliada; não equivale a validação integrada. Os novos subjects de governança recebem IDs acima do máximo anterior, por ordenação lexical do auxiliar oficial. Nenhum finding foi apagado ou renumerado por posição.

| ID | Subject | Classification | Comparison | Evidence | Description / implication |
|---|---|---|---|---|---|
| D001 | architecture.qt-worker-boundary | 🟢 CONFIRMED | SAME_FINDING | main.py:1727 @ working-tree sha256:86d91b4af3f04a36431ad99f1231684f78abacd653e5b850f3f9187aa9267d70; main.py:3052 @ working-tree sha256:86d91b4af3f04a36431ad99f1231684f78abacd653e5b850f3f9187aa9267d70; ui.py:103 @ working-tree sha256:c76cee3d2fd0870ed78f8fbb375c7718e78a6e1634726b567b411577b2fc47c4; ui.py:265 @ working-tree sha256:c76cee3d2fd0870ed78f8fbb375c7718e78a6e1634726b567b411577b2fc47c4; gui/window.py:398 @ working-tree sha256:a92f6ae7697b306c12d3630f01ae5661baad8fc7269ef5e4ee324d999561a254 | Qt fica no thread principal; a sessão asyncio roda em thread dedicado; ações/plugins são despachados ao executor. JarvisUI emite sinais para a janela. / Mudanças de UI devem preservar os sinais e a única QApplication; ferramentas não podem construir widgets. |
| D002 | automation.background-policy | 🟢 CONFIRMED | SAME_FINDING | core/tasks/tools.py:87 @ working-tree sha256:ec3e51809d5abbaf4f9f49ed2b1ddaf92688b56f84847dfe32d479c05437453c; core/tasks/tools.py:96 @ working-tree sha256:ec3e51809d5abbaf4f9f49ed2b1ddaf92688b56f84847dfe32d479c05437453c; core/tasks/engine.py:268 @ working-tree sha256:c3b3dd32ff3acf12a7bc83e6458458e6356298c98e53245cece64c17b08d0675 | TaskEngine agenda workers e TaskTools filtra ferramentas, separa web de recall_memory e restringe caminhos à pasta da tarefa. / Trabalho longo pertence ao motor de tarefas; isto confirma controles estáticos, não isolamento completo demonstrado. |
| D003 | automation.routines-and-research | 🟢 CONFIRMED | SAME_FINDING | core/routines/engine.py:114 @ working-tree sha256:41ba8ff259f3f1b023432b05a8247f3ab6992a8eecd71657fc37fafbff3d258e; core/tasks/research.py:111 @ working-tree sha256:04b4280f3a2a3a2131a3ed26afa1691a4b67ccfa656e5b5b107ef588af2b1e5f; core/tasks/research.py:342 @ working-tree sha256:04b4280f3a2a3a2131a3ed26afa1691a4b67ccfa656e5b5b107ef588af2b1e5f; main.py:726 @ working-tree sha256:86d91b4af3f04a36431ad99f1231684f78abacd653e5b850f3f9187aa9267d70 | Rotinas usam armazenamento compartilhado de JSON; pesquisa registra fontes e verifica trechos contra páginas salvas. / A verificação textual de citações não demonstra verdade factual nem qualidade global do relatório. |
| D004 | configuration.atomic-settings | 🟢 CONFIRMED | SAME_FINDING | memory/config_manager.py:38 @ working-tree sha256:e0301bb17b2d733def5d1a15b77a2abd4a2e32986981a4b2e8b196b0fce1d528; memory/config_manager.py:52 @ working-tree sha256:e0301bb17b2d733def5d1a15b77a2abd4a2e32986981a4b2e8b196b0fce1d528; memory/config_manager.py:69 @ working-tree sha256:e0301bb17b2d733def5d1a15b77a2abd4a2e32986981a4b2e8b196b0fce1d528 | Configuração usa RLock, arquivo temporário e os.replace, com tratamento de arquivo corrompido. / Usar config_manager; serialização dentro do processo não prova coordenação entre processos ou durabilidade após perda de energia. |
| D005 | dashboard.transport-fallback | 🟢 CONFIRMED | SAME_FINDING | dashboard/server.py:1248 @ working-tree sha256:5355d250a0364c7dab38dc254aa21cb81ccd8ff18200dca61d05069416ca3fdb; dashboard/server.py:1276 @ working-tree sha256:5355d250a0364c7dab38dc254aa21cb81ccd8ff18200dca61d05069416ca3fdb; dashboard/server.py:750 @ working-tree sha256:5355d250a0364c7dab38dc254aa21cb81ccd8ff18200dca61d05069416ca3fdb | Dashboard usa pareamento/tokens e pode servir HTTP em 0.0.0.0 quando TLS não está disponível, com aviso explícito. / Exposição real depende da configuração/rede; não foi verificada. Requisito de TLS obrigatório exigiria contexto específico. |
| D006 | developer.vscode-success-claim | 🟢 CONFIRMED | CHANGED | actions/dev_agent.py:333; actions/dev_agent.py:364; actions/dev_agent.py:456; tests/test_dev_agent_vscode.py; .ai/changes/change-001/REVIEW-REVISION-002.md; .ai/changes/change-001/AI-SDD-CLOSE.json | Mudança material desde a baseline: change-001 substituiu o sucesso presumido por observação de janela com caminho completo, captura limitada a 64 KiB por stream e resultado conservador. A revisão registrou 29 testes PASS; a mudança está CLOSED. / D006 tratado (RESOLVED), preservando o conflito histórico em previous. Títulos sem caminho completo continuam não verificados; não há teste manual do editor nem prova integrada. |
| D007 | encoding.intent-not-established | ⚪ UNKNOWN | SAME_FINDING | .ai/discovery-runs/discovery-2026-11-18-01/EVIDENCE.json | O inventário registra hash, BOM e decodificação estrita por arquivo; a intenção de encoding sem BOM permanece desconhecida. / Antes de aprovação de CONTEXT, preparar SCOPE.json com arquivos exatos e política de encoding quando necessária; preservar bytes no DEVELOP. |
| D008 | memory.persistence-risk | 🟡 INFERRED | SAME_FINDING | memory/memory_manager.py:118 @ working-tree sha256:3ecf5a9d80484bec73eef67e54c7d7e2880c726e4bfac58d05b1a14b6e1988ce; core/tasks/store.py:31 @ working-tree sha256:eba554771e86fb4e2f441073aaa91f542071f3944c0ed883af9ef789c33f8072 | save_memory grava o arquivo diretamente; o store de tarefas usa temporário e replace. Interrupção durante gravação pode afetar a memória de forma diferente. / Risco de truncamento inferido da estratégia de escrita; nenhum crash ou perda de dados foi reproduzido. |
| D009 | models.shared-ladder-coupling | 🟢 CONFIRMED | SAME_FINDING | core/gemini.py:714 @ working-tree sha256:8f8c2e5c6d31d1753c48ab5472ba897fab10c75d5512752b6d41f34fcbbd90bb; core/gemini.py:814 @ working-tree sha256:8f8c2e5c6d31d1753c48ab5472ba897fab10c75d5512752b6d41f34fcbbd90bb; core/tasks/brain.py:142 @ working-tree sha256:bc0131df3bd42c6035a080d51b4e454894a96c574185166cbb8a61777066cd3f | core.gemini concentra deadlines/fallback; o motor de tarefas usa a ladder e helpers privados para chamadas com ferramentas. / Mudanças na ladder afetam voz, chamadas avulsas e tarefas; preservar compatibilidade dos caminhos com tool-calling. |
| D010 | repository.runtime-artifacts-tracked | 🟢 CONFIRMED | SAME_FINDING | .gitignore @ working-tree sha256:4358a2cb0ca9d46ee6997e4e1847ec144c6fdda9ff6c921ed669c9a6001bdf9f; .ai/discovery-runs/discovery-2026-11-18-01/EVIDENCE.json / tracked_runtime_artifact_count=24 | O índice Git contém checkpoints, páginas de pesquisa e um relatório gerado; .gitignore não exclui memory/tasks nem reports. / Revisar política de dados antes de futuras publicações. O conteúdo desses artefatos não foi lido nem classificado como segredo. |
| D011 | tests.end-to-end-evidence | ⚪ UNKNOWN | CHANGED | providers/_tests.py:1; core/_smoke_harness.py:1; tests/test_dev_agent_vscode.py; .ai/changes/change-001/REVIEW-REVISION-002.md | Mudança de evidência: além dos autotestes de providers e do harness, há 29 testes focais documentados e aprovados para VS Code, incluindo fixtures locais. UI, áudio real, serviços externos, recuperação após crash e outras plataformas continuam sem validação integrada nesta inspeção. / Evidência mínima depende da futura change: testes focais e observação do fluxo afetado. Não declarar funcionamento integrado com base em parsing. |
| D012 | web.dns-rebinding-limitation | 🟢 CONFIRMED | SAME_FINDING | core/tasks/web.py:21 @ working-tree sha256:b265d179df2aa4468e30308059bfa8c868cb4bc70023ca347e1e1ca4d979b924; core/tasks/web.py:52 @ working-tree sha256:b265d179df2aa4468e30308059bfa8c868cb4bc70023ca347e1e1ca4d979b924; core/tasks/web.py:128 @ working-tree sha256:b265d179df2aa4468e30308059bfa8c868cb4bc70023ca347e1e1ca4d979b924 | Fetch valida IPs públicos e redirects, mas documenta limitação quando o hostname resolve de modo diferente entre validação e conexão. / Não apresentar o filtro como sandbox completo; exploração e eficácia em execução não foram testadas. |
| D013 | governance.closed-change-knowledge | 🟢 CONFIRMED | NEW | .ai/changes/change-001/AI-SDD-CLOSE.json; .ai/knowledge/KNOWLEDGE-REGISTER.json; .ai/AI-SDD.yaml | change-001 foi encerrada pelo runtime, com auditoria, bootstrap documental autorizado e dois registros no Knowledge Register canônico (CONFIRMED e UNKNOWN). / Reutilizar a evidência duradoura, sem promover UNKNOWN ou reclassificar retrospectivamente o finding aberto original; não há autorização ativa de desenvolvimento. |
| D014 | governance.documentation-policy | 🟢 CONFIRMED | NEW | PROJECT-POLICY.md; CHANGELOG.md; .ai/changes/change-001/CLOSE-POLICY-BOOTSTRAP-EVIDENCE.json | Política publicada em PROJECT-POLICY.md: changelog por change-id, documentação atualizada quando instruções forem afetadas, identificação Mark LVII preservada e versão futura por decisão humana. / Novas mudanças devem avaliar documentação e registrar histórico; a política não cria automaticamente versão, commit, tag ou release. |

## Encoding, limites e próximos contextos

O inventário registra bytes, hash, BOM, método e confiança por arquivo. UTF-8 sem BOM prova validade dos bytes, não intenção histórica; D007 permanece UNKNOWN. CONTEXT futuro deve listar caminhos exatos em SCOPE.json e preparar ENCODING-POLICY quando necessária antes de aprovação. Preservar encoding/BOM no DEVELOP e reutilizar o KR canônico para conhecimento duradouro, sem criar registro paralelo.

O conflito de D006 foi tratado; candidatos remanescentes para escolha humana incluem D008 (persistência de memória, risco INFERRED), D010 (artefatos runtime no Git), D005 (requisitos de transporte do dashboard) e D011 (evidência integrada UNKNOWN). Isso não autoriza correção, teste externo ou implementação. D012 continua limitação documentada de DNS rebinding; não se afirma sandbox completo. Nenhum requisito material desta inspeção dependeu de evidência externa, portanto nenhuma Boundary Stop foi acionada. UNKNOWNs e riscos foram preservados; não foi aberto novo ciclo CONTEXT.

## finding_registry

```json
{
  "run_id": "discovery-2026-11-18-01",
  "project_scope": "Mark-LVII / whole-project static discovery",
  "baseline": {
    "source": ".ai/discovery-history/discovery-2026-11-17-01/DISCOVERY.md",
    "sha256": "815d27674713b31e266172cca930831c987cba7d91c0541c6397b62f9c862ed2",
    "run_id": "discovery-2026-11-17-01",
    "revision": "f1a560b6073479990d92d3d34a90d7f41cdbfa00",
    "project_scope": "Mark-LVII / whole-project static discovery"
  },
  "comparison_mode": "COMPARED",
  "findings": [
    {
      "subject": "architecture.qt-worker-boundary",
      "classification": "CONFIRMED",
      "evidence": [
        "main.py:1727 @ working-tree sha256:86d91b4af3f04a36431ad99f1231684f78abacd653e5b850f3f9187aa9267d70",
        "main.py:3052 @ working-tree sha256:86d91b4af3f04a36431ad99f1231684f78abacd653e5b850f3f9187aa9267d70",
        "ui.py:103 @ working-tree sha256:c76cee3d2fd0870ed78f8fbb375c7718e78a6e1634726b567b411577b2fc47c4",
        "ui.py:265 @ working-tree sha256:c76cee3d2fd0870ed78f8fbb375c7718e78a6e1634726b567b411577b2fc47c4",
        "gui/window.py:398 @ working-tree sha256:a92f6ae7697b306c12d3630f01ae5661baad8fc7269ef5e4ee324d999561a254"
      ],
      "description": "Qt fica no thread principal; a sessão asyncio roda em thread dedicado; ações/plugins são despachados ao executor. JarvisUI emite sinais para a janela.",
      "implication": "Mudanças de UI devem preservar os sinais e a única QApplication; ferramentas não podem construir widgets.",
      "material": "Qt fica no thread principal; a sessão asyncio roda em thread dedicado; ações/plugins são despachados ao executor. JarvisUI emite sinais para a janela. Mudanças de UI devem preservar os sinais e a única QApplication; ferramentas não podem construir widgets.",
      "id": "D001",
      "comparison_status": "SAME_FINDING",
      "last_observed": "discovery-2026-11-18-01"
    },
    {
      "subject": "automation.background-policy",
      "classification": "CONFIRMED",
      "evidence": [
        "core/tasks/tools.py:87 @ working-tree sha256:ec3e51809d5abbaf4f9f49ed2b1ddaf92688b56f84847dfe32d479c05437453c",
        "core/tasks/tools.py:96 @ working-tree sha256:ec3e51809d5abbaf4f9f49ed2b1ddaf92688b56f84847dfe32d479c05437453c",
        "core/tasks/engine.py:268 @ working-tree sha256:c3b3dd32ff3acf12a7bc83e6458458e6356298c98e53245cece64c17b08d0675"
      ],
      "description": "TaskEngine agenda workers e TaskTools filtra ferramentas, separa web de recall_memory e restringe caminhos à pasta da tarefa.",
      "implication": "Trabalho longo pertence ao motor de tarefas; isto confirma controles estáticos, não isolamento completo demonstrado.",
      "material": "TaskEngine agenda workers e TaskTools filtra ferramentas, separa web de recall_memory e restringe caminhos à pasta da tarefa. Trabalho longo pertence ao motor de tarefas; isto confirma controles estáticos, não isolamento completo demonstrado.",
      "id": "D002",
      "comparison_status": "SAME_FINDING",
      "last_observed": "discovery-2026-11-18-01"
    },
    {
      "subject": "automation.routines-and-research",
      "classification": "CONFIRMED",
      "evidence": [
        "core/routines/engine.py:114 @ working-tree sha256:41ba8ff259f3f1b023432b05a8247f3ab6992a8eecd71657fc37fafbff3d258e",
        "core/tasks/research.py:111 @ working-tree sha256:04b4280f3a2a3a2131a3ed26afa1691a4b67ccfa656e5b5b107ef588af2b1e5f",
        "core/tasks/research.py:342 @ working-tree sha256:04b4280f3a2a3a2131a3ed26afa1691a4b67ccfa656e5b5b107ef588af2b1e5f",
        "main.py:726 @ working-tree sha256:86d91b4af3f04a36431ad99f1231684f78abacd653e5b850f3f9187aa9267d70"
      ],
      "description": "Rotinas usam armazenamento compartilhado de JSON; pesquisa registra fontes e verifica trechos contra páginas salvas.",
      "implication": "A verificação textual de citações não demonstra verdade factual nem qualidade global do relatório.",
      "material": "Rotinas usam armazenamento compartilhado de JSON; pesquisa registra fontes e verifica trechos contra páginas salvas. A verificação textual de citações não demonstra verdade factual nem qualidade global do relatório.",
      "id": "D003",
      "comparison_status": "SAME_FINDING",
      "last_observed": "discovery-2026-11-18-01"
    },
    {
      "subject": "configuration.atomic-settings",
      "classification": "CONFIRMED",
      "evidence": [
        "memory/config_manager.py:38 @ working-tree sha256:e0301bb17b2d733def5d1a15b77a2abd4a2e32986981a4b2e8b196b0fce1d528",
        "memory/config_manager.py:52 @ working-tree sha256:e0301bb17b2d733def5d1a15b77a2abd4a2e32986981a4b2e8b196b0fce1d528",
        "memory/config_manager.py:69 @ working-tree sha256:e0301bb17b2d733def5d1a15b77a2abd4a2e32986981a4b2e8b196b0fce1d528"
      ],
      "description": "Configuração usa RLock, arquivo temporário e os.replace, com tratamento de arquivo corrompido.",
      "implication": "Usar config_manager; serialização dentro do processo não prova coordenação entre processos ou durabilidade após perda de energia.",
      "material": "Configuração usa RLock, arquivo temporário e os.replace, com tratamento de arquivo corrompido. Usar config_manager; serialização dentro do processo não prova coordenação entre processos ou durabilidade após perda de energia.",
      "id": "D004",
      "comparison_status": "SAME_FINDING",
      "last_observed": "discovery-2026-11-18-01"
    },
    {
      "subject": "dashboard.transport-fallback",
      "classification": "CONFIRMED",
      "evidence": [
        "dashboard/server.py:1248 @ working-tree sha256:5355d250a0364c7dab38dc254aa21cb81ccd8ff18200dca61d05069416ca3fdb",
        "dashboard/server.py:1276 @ working-tree sha256:5355d250a0364c7dab38dc254aa21cb81ccd8ff18200dca61d05069416ca3fdb",
        "dashboard/server.py:750 @ working-tree sha256:5355d250a0364c7dab38dc254aa21cb81ccd8ff18200dca61d05069416ca3fdb"
      ],
      "description": "Dashboard usa pareamento/tokens e pode servir HTTP em 0.0.0.0 quando TLS não está disponível, com aviso explícito.",
      "implication": "Exposição real depende da configuração/rede; não foi verificada. Requisito de TLS obrigatório exigiria contexto específico.",
      "material": "Dashboard usa pareamento/tokens e pode servir HTTP em 0.0.0.0 quando TLS não está disponível, com aviso explícito. Exposição real depende da configuração/rede; não foi verificada. Requisito de TLS obrigatório exigiria contexto específico.",
      "id": "D005",
      "comparison_status": "SAME_FINDING",
      "last_observed": "discovery-2026-11-18-01"
    },
    {
      "subject": "developer.vscode-success-claim",
      "classification": "CONFIRMED",
      "evidence": [
        "actions/dev_agent.py:333",
        "actions/dev_agent.py:364",
        "actions/dev_agent.py:456",
        "tests/test_dev_agent_vscode.py",
        ".ai/changes/change-001/REVIEW-REVISION-002.md",
        ".ai/changes/change-001/AI-SDD-CLOSE.json"
      ],
      "description": "Mudança material desde a baseline: change-001 substituiu o sucesso presumido por observação de janela com caminho completo, captura limitada a 64 KiB por stream e resultado conservador. A revisão registrou 29 testes PASS; a mudança está CLOSED.",
      "implication": "D006 tratado (RESOLVED), preservando o conflito histórico em previous. Títulos sem caminho completo continuam não verificados; não há teste manual do editor nem prova integrada.",
      "material": "Mudança material desde a baseline: change-001 substituiu o sucesso presumido por observação de janela com caminho completo, captura limitada a 64 KiB por stream e resultado conservador. A revisão registrou 29 testes PASS; a mudança está CLOSED. D006 tratado (RESOLVED), preservando o conflito histórico em previous. Títulos sem caminho completo continuam não verificados; não há teste manual do editor nem prova integrada.",
      "treatment_status": "RESOLVED",
      "id": "D006",
      "comparison_status": "CHANGED",
      "previous": {
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
      "last_observed": "discovery-2026-11-18-01"
    },
    {
      "subject": "encoding.intent-not-established",
      "classification": "UNKNOWN",
      "evidence": [
        ".ai/discovery-runs/discovery-2026-11-18-01/EVIDENCE.json"
      ],
      "description": "O inventário registra hash, BOM e decodificação estrita por arquivo; a intenção de encoding sem BOM permanece desconhecida.",
      "implication": "Antes de aprovação de CONTEXT, preparar SCOPE.json com arquivos exatos e política de encoding quando necessária; preservar bytes no DEVELOP.",
      "material": "O inventário registra hash, BOM e decodificação estrita por arquivo; a intenção de encoding sem BOM permanece desconhecida. Antes de aprovação de CONTEXT, preparar SCOPE.json com arquivos exatos e política de encoding quando necessária; preservar bytes no DEVELOP.",
      "id": "D007",
      "comparison_status": "SAME_FINDING",
      "last_observed": "discovery-2026-11-18-01"
    },
    {
      "subject": "memory.persistence-risk",
      "classification": "INFERRED",
      "evidence": [
        "memory/memory_manager.py:118 @ working-tree sha256:3ecf5a9d80484bec73eef67e54c7d7e2880c726e4bfac58d05b1a14b6e1988ce",
        "core/tasks/store.py:31 @ working-tree sha256:eba554771e86fb4e2f441073aaa91f542071f3944c0ed883af9ef789c33f8072"
      ],
      "description": "save_memory grava o arquivo diretamente; o store de tarefas usa temporário e replace. Interrupção durante gravação pode afetar a memória de forma diferente.",
      "implication": "Risco de truncamento inferido da estratégia de escrita; nenhum crash ou perda de dados foi reproduzido.",
      "material": "save_memory grava o arquivo diretamente; o store de tarefas usa temporário e replace. Interrupção durante gravação pode afetar a memória de forma diferente. Risco de truncamento inferido da estratégia de escrita; nenhum crash ou perda de dados foi reproduzido.",
      "id": "D008",
      "comparison_status": "SAME_FINDING",
      "last_observed": "discovery-2026-11-18-01"
    },
    {
      "subject": "models.shared-ladder-coupling",
      "classification": "CONFIRMED",
      "evidence": [
        "core/gemini.py:714 @ working-tree sha256:8f8c2e5c6d31d1753c48ab5472ba897fab10c75d5512752b6d41f34fcbbd90bb",
        "core/gemini.py:814 @ working-tree sha256:8f8c2e5c6d31d1753c48ab5472ba897fab10c75d5512752b6d41f34fcbbd90bb",
        "core/tasks/brain.py:142 @ working-tree sha256:bc0131df3bd42c6035a080d51b4e454894a96c574185166cbb8a61777066cd3f"
      ],
      "description": "core.gemini concentra deadlines/fallback; o motor de tarefas usa a ladder e helpers privados para chamadas com ferramentas.",
      "implication": "Mudanças na ladder afetam voz, chamadas avulsas e tarefas; preservar compatibilidade dos caminhos com tool-calling.",
      "material": "core.gemini concentra deadlines/fallback; o motor de tarefas usa a ladder e helpers privados para chamadas com ferramentas. Mudanças na ladder afetam voz, chamadas avulsas e tarefas; preservar compatibilidade dos caminhos com tool-calling.",
      "id": "D009",
      "comparison_status": "SAME_FINDING",
      "last_observed": "discovery-2026-11-18-01"
    },
    {
      "subject": "repository.runtime-artifacts-tracked",
      "classification": "CONFIRMED",
      "evidence": [
        ".gitignore @ working-tree sha256:4358a2cb0ca9d46ee6997e4e1847ec144c6fdda9ff6c921ed669c9a6001bdf9f",
        ".ai/discovery-runs/discovery-2026-11-18-01/EVIDENCE.json / tracked_runtime_artifact_count=24"
      ],
      "description": "O índice Git contém checkpoints, páginas de pesquisa e um relatório gerado; .gitignore não exclui memory/tasks nem reports.",
      "implication": "Revisar política de dados antes de futuras publicações. O conteúdo desses artefatos não foi lido nem classificado como segredo.",
      "material": "O índice Git contém checkpoints, páginas de pesquisa e um relatório gerado; .gitignore não exclui memory/tasks nem reports. Revisar política de dados antes de futuras publicações. O conteúdo desses artefatos não foi lido nem classificado como segredo.",
      "id": "D010",
      "comparison_status": "SAME_FINDING",
      "last_observed": "discovery-2026-11-18-01"
    },
    {
      "subject": "tests.end-to-end-evidence",
      "classification": "UNKNOWN",
      "evidence": [
        "providers/_tests.py:1",
        "core/_smoke_harness.py:1",
        "tests/test_dev_agent_vscode.py",
        ".ai/changes/change-001/REVIEW-REVISION-002.md"
      ],
      "description": "Mudança de evidência: além dos autotestes de providers e do harness, há 29 testes focais documentados e aprovados para VS Code, incluindo fixtures locais. UI, áudio real, serviços externos, recuperação após crash e outras plataformas continuam sem validação integrada nesta inspeção.",
      "implication": "Evidência mínima depende da futura change: testes focais e observação do fluxo afetado. Não declarar funcionamento integrado com base em parsing.",
      "material": "Mudança de evidência: além dos autotestes de providers e do harness, há 29 testes focais documentados e aprovados para VS Code, incluindo fixtures locais. UI, áudio real, serviços externos, recuperação após crash e outras plataformas continuam sem validação integrada nesta inspeção. Evidência mínima depende da futura change: testes focais e observação do fluxo afetado. Não declarar funcionamento integrado com base em parsing.",
      "id": "D011",
      "comparison_status": "CHANGED",
      "previous": {
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
      "last_observed": "discovery-2026-11-18-01"
    },
    {
      "subject": "web.dns-rebinding-limitation",
      "classification": "CONFIRMED",
      "evidence": [
        "core/tasks/web.py:21 @ working-tree sha256:b265d179df2aa4468e30308059bfa8c868cb4bc70023ca347e1e1ca4d979b924",
        "core/tasks/web.py:52 @ working-tree sha256:b265d179df2aa4468e30308059bfa8c868cb4bc70023ca347e1e1ca4d979b924",
        "core/tasks/web.py:128 @ working-tree sha256:b265d179df2aa4468e30308059bfa8c868cb4bc70023ca347e1e1ca4d979b924"
      ],
      "description": "Fetch valida IPs públicos e redirects, mas documenta limitação quando o hostname resolve de modo diferente entre validação e conexão.",
      "implication": "Não apresentar o filtro como sandbox completo; exploração e eficácia em execução não foram testadas.",
      "material": "Fetch valida IPs públicos e redirects, mas documenta limitação quando o hostname resolve de modo diferente entre validação e conexão. Não apresentar o filtro como sandbox completo; exploração e eficácia em execução não foram testadas.",
      "id": "D012",
      "comparison_status": "SAME_FINDING",
      "last_observed": "discovery-2026-11-18-01"
    },
    {
      "subject": "governance.closed-change-knowledge",
      "classification": "CONFIRMED",
      "evidence": [
        ".ai/changes/change-001/AI-SDD-CLOSE.json",
        ".ai/knowledge/KNOWLEDGE-REGISTER.json",
        ".ai/AI-SDD.yaml"
      ],
      "description": "change-001 foi encerrada pelo runtime, com auditoria, bootstrap documental autorizado e dois registros no Knowledge Register canônico (CONFIRMED e UNKNOWN).",
      "implication": "Reutilizar a evidência duradoura, sem promover UNKNOWN ou reclassificar retrospectivamente o finding aberto original; não há autorização ativa de desenvolvimento.",
      "material": "change-001 foi encerrada pelo runtime, com auditoria, bootstrap documental autorizado e dois registros no Knowledge Register canônico (CONFIRMED e UNKNOWN). Reutilizar a evidência duradoura, sem promover UNKNOWN ou reclassificar retrospectivamente o finding aberto original; não há autorização ativa de desenvolvimento.",
      "id": "D013",
      "comparison_status": "NEW",
      "last_observed": "discovery-2026-11-18-01"
    },
    {
      "subject": "governance.documentation-policy",
      "classification": "CONFIRMED",
      "evidence": [
        "PROJECT-POLICY.md",
        "CHANGELOG.md",
        ".ai/changes/change-001/CLOSE-POLICY-BOOTSTRAP-EVIDENCE.json"
      ],
      "description": "Política publicada em PROJECT-POLICY.md: changelog por change-id, documentação atualizada quando instruções forem afetadas, identificação Mark LVII preservada e versão futura por decisão humana.",
      "implication": "Novas mudanças devem avaliar documentação e registrar histórico; a política não cria automaticamente versão, commit, tag ou release.",
      "material": "Política publicada em PROJECT-POLICY.md: changelog por change-id, documentação atualizada quando instruções forem afetadas, identificação Mark LVII preservada e versão futura por decisão humana. Novas mudanças devem avaliar documentação e registrar histórico; a política não cria automaticamente versão, commit, tag ou release.",
      "id": "D014",
      "comparison_status": "NEW",
      "last_observed": "discovery-2026-11-18-01"
    }
  ]
}
```
