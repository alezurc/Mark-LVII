# DEP-001 — validação integrada depende do ambiente Python

- record_id: DEP-001
- change_id: change-003
- requirement_refs: D011; AC4, AC6, AC7 e AC8 do CONTEXT.md
- recorded_by: codex, sessão do lease 34bf7c64-77ed-42c4-a52d-1f3287b623a0
- recorded_at: sessão de DEVELOP em 2026-11-18, America/Sao_Paulo; horário exato não coletado
- primary_category: EXTERNAL_DEPENDENCY
- additional_categories: OUTSIDE_AI_SDD_RESPONSIBILITY
- classification_rationale: integração com types.Blob/HTTP/audio/Qt precisa dos pacotes declarados em requirements.txt no perfil Python de execução. Entrega/preparação desse ambiente não integra o escopo aprovado; CONTEXT proíbe instalar dependências e buscar outro interpretador. Governança AI-SDD não provisiona o ambiente por implicação.
- knowledge_refs: KR-change-001-002 e KR-change-002-002 (limites históricos/UNKNOWN); nenhum registro anterior supre a evidência ausente.
- knowledge_classification: CONFIRMED para ModuleNotFoundError no Python invocado; UNKNOWN para resultado dos cenários não executados e disponibilidade em outros ambientes.
- evidence_refs_and_sha256: DEVELOP.md descreve comandos, retornos e diagnósticos; IMPLEMENTATION-EVIDENCE.json registra hashes dos artefatos e do snapshot. Saída do executor da suíte providers retornou 1, 52 passed, 8 failed, 2 skipped. Não foi coletado inventário de instalações alternativas.
- materiality: material para demonstrar os critérios integrados de D011; não bloqueia a prova focal de equivalência PCM de D007 nem o registro documental independente.
- concrete_consequence: turno types.Blob/TaskGroup, HTTP integrado, resampling e painel/perfil Qt não demonstrados; não concluir DEVELOP/REVIEW nem afirmar suíte completa validada.
- missing_evidence: execução desses cenários em perfil com google-genai, httpx, numpy e PyQt6 disponíveis. Piper é opcional e seus SKIPs não provam síntese física.
- responsibility_limit: preparar/alterar ambiente ou selecionar outro perfil Python requer nova decisão humana delimitada; não buscar instalações, instalar, baixar, substituir bibliotecas ou experimentar alternativas automaticamente.
- external_owner_or_UNKNOWN: responsável humano pelo ambiente do projeto; identidade nominal UNKNOWN.
- blocked_downstream: complete DEVELOP, REVIEW e CLOSE dependentes de validação suficiente.
- current_lifecycle_and_readiness_with_source: APPROVED_FOR_DEVELOP conforme .ai/AI-SDD.yaml lido nesta sessão; validação parcial/bloqueada em DEVELOP.md. Nenhum novo enum de lifecycle/readiness foi gravado.
- disposition: STOPPED_AT_RESPONSIBILITY_BOUNDARY
- recommended_human_action: autorizar explicitamente a preparação de um ambiente com as dependências declaradas ou indicar um perfil já preparado, identificando este registro, responsável/referência, escopo, evidência esperada e limite da retomada.
- objective_resumption_condition: nova autorização humana rastreável e delimitada para retomar DEP-001 e executar os testes pendentes em ambiente fornecido/preparado dentro desse escopo. Resultado deve ser reavaliado; autorização ou presença de pacotes não equivale a PASS.
- reopen_authorization_ref: NONE

Parada preserva o código parcial, os UNKNOWNs e o histórico. Nenhuma investigação de engenharia externa, instalação, pesquisa de fornecedor ou teste downstream é autorizada por este registro. Encerrar somente o lease desta sessão após parar o trabalho, sem alterar estado/lock manualmente.
