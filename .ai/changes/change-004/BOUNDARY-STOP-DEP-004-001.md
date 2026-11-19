# Boundary Stop — DEP-004-001

record_id: DEP-004-001
change_id: change-004
requirement_refs: CONTEXT AC3, AC6, AC8; Validação planejada; Riscos, incógnitas e limites
recorded_by: codex / IMPLEMENTER
recorded_at: 2026-11-19T02:47:03.9042873Z
primary_category: EXTERNAL_DEPENDENCY
additional_categories: NONE
classification_rationale: A dependência PyQt6 não está disponível no Python efetivamente executado; preparar ambiente/instalar pacotes foi explicitamente excluído do CONTEXT aprovado. Não há evidência de impossibilidade da plataforma, nem de ausência em outros ambientes.
knowledge_refs: .ai/knowledge/KNOWLEDGE-REGISTER.json; D011 e histórico DEP-001 de change-003 apenas como limites preservados, sem reabertura nem alteração de KR.
knowledge_classification: CONFIRMED para falha de import neste ambiente; UNKNOWN para outros ambientes e aspecto/comportamento da UI proposta.
evidence_refs_and_sha256:
- .ai/changes/change-004/DEVELOP-ENVIRONMENT-EVIDENCE.json: 52f0cfb268465f7f7228beef3e5b0d3c0e5fbf74dc1c50bd525c9783dd3c4508
- .ai/changes/change-004/CONTEXT.md: e4cee9f85da187acd6fa0ab85e6a2e495669d256ee8889e53d6767c2347985eb
- .ai/AI-SDD.yaml (snapshot do hash antes do encerramento do lease): f011b4d505df72099a8c5d1b26ed285ee3cc49c75997ecdf7a0b0f37926bf863
materiality: MATERIAL; os testes Qt e renders exigidos por AC8 não podem executar neste ambiente.
concrete_consequence: Não é possível produzir a evidência obrigatória de troca imediata, preservação de conteúdo e layout; não declarar DEVELOP completo.
missing_evidence: Comportamento Qt offscreen e renders en/pt-BR no perfil delimitado.
responsibility_limit: Instalação de dependências, escolha/ativação de outro ambiente e preparação de plataforma não autorizadas por este CONTEXT. Não buscar interpretadores alternativos, instalar pacotes ou reduzir critérios automaticamente.
external_owner_or_UNKNOWN: Responsável humano pelo ambiente do projeto (usuário desta conversa); identidade adicional UNKNOWN.
blocked_downstream: Implementação dependente, complete DEVELOP, REVIEW e CLOSE desta mudança; nenhuma promoção de readiness.
current_lifecycle_and_readiness_with_source: APPROVED_FOR_DEVELOP conforme route e .ai/AI-SDD.yaml; DEVELOP não concluído; evidência obrigatória indisponível. Não alterar enum ou estado manualmente.
disposition: STOPPED_AT_RESPONSIBILITY_BOUNDARY
recommended_human_action: Preparar um ambiente com as dependências do projeto ou autorizar explicitamente uma preparação delimitada, identificando ambiente/comando, alvos permitidos, evidência esperada, limite e condição de parada. Preservar o CONTEXT e critérios aprovados; se ampliar escopo material de produto, seguir scope-expansion/CONTEXT/aprovação.
objective_resumption_condition: Nova autorização humana rastreável vinculada a DEP-004-001, com objetivo de preparar/verificar PyQt6 no ambiente explicitamente identificado; import Qt bem-sucedido e execução dos testes aprovados possível, sem expandir outros ramos.
reopen_authorization_ref: NONE

## Trabalho realizado e preservação

Somente roteamento, leitura de normas/contexto/fontes, aquisição/checagem de lease e probe de disponibilidade do ambiente. Nenhum arquivo de produto alterado; nenhum teste de implementação executado; não foram instaladas dependências. Working tree preexistente preservado. O lease desta sessão deve ser encerrado pela operação canônica end-stage após cessar o trabalho; o estado de lifecycle não é editado. Este documento não revoga nem amplia a aprovação humana existente e não registra conclusão da etapa.