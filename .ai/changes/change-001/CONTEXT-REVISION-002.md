# Proveniência — revisão 002

Motivo: REVIEW.md R001/P2; decisão explícita de changes-requested com referência “Autorizado a correção do achado P2”; solicitação subsequente de context change-001.

Fonte anterior preservada byte a byte em `context-history/revision-001/CONTEXT.md`, SHA-256 `e1d413e4c1f55dcba1dee4853868455aac89d6cf8137cfa5fb26e57191b7b417`. Snapshots de ENCODING-BASELINE.json e APPROVED-SCOPE.json anteriores acompanham o contexto histórico; não são novas autorizações. DEVELOP.md, REVIEW.md e decisões passadas não foram reescritos.

Revisão 002 mantém os mesmos dois arquivos exatos em SCOPE.json e a política sem migrações. Acrescenta orçamento de 64 KiB por stream, leitura incremental, excesso conservador, cleanup finito e provas de limite/concorrência nos testes. Nenhum código de produto/teste foi alterado. Fonte UTF-8 sem BOM/CRLF e teste UTF-8 sem BOM/LF devem ser preservados. UNKNOWN sobre intenção histórica de encoding permanece; não há conversão proposta.

Fontes normativas aplicadas da instalação declarada: operational-v0.1/stages/CONTEXT.md, docs/ROADMAP-HARDENING-DAY2.md e operational-v0.2/BOUNDARY-STOP-CONDITION.md. A correção local de captura não depende de evidência externa material; nenhuma condição de parada no limite de responsabilidade foi acionada. Não autoriza engenharia adicional nem expansão de escopo.

Nova aprovação humana necessária após conclusão de CONTEXT. A referência de changes-requested não foi tratada como aprovação desta revisão.
