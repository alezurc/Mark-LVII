# Proposta concreta de política e changelog

Solicitação humana: após informar que não há política de documentação no projeto, o usuário aceitou a abordagem de histórico por change-id, arquivo de política e preservação de Mark LVII sem nova versão, com referência literal “pode seguir com essa abordagem”.

Conteúdos preparados:

- `proposals/PROJECT-POLICY.md` → destino proposto `PROJECT-POLICY.md` na raiz.
- `proposals/CHANGELOG.md` → destino proposto `CHANGELOG.md` na raiz, com entrada change-001.

Na publicação definitiva, remover somente os avisos de proposta/publicação pendente. Não há atribuição de versão, commit, tag ou release nesta proposta.

Os dois destinos ainda não constam de APPROVED-SCOPE.json, que contém somente actions/dev_agent.py e tests/test_dev_agent_vscode.py. A aceitação da abordagem é autorização humana para prepará-la; não altera o snapshot de escopo do runtime. Não foram editados SCOPE.json, APPROVED-SCOPE.json, contexto aprovado ou estado runtime para simular essa inclusão.

Limitação operacional comprovada por leitura da instalação declarada: `runtime/ai_sdd.py`, função scope_expansion, aceita somente APPROVED_FOR_DEVELOP e DEVELOP_COMPLETED e bloqueia outros estados. O estado corrente é REVIEW_APPROVED. O contrato docs/VNEXT-001-004-CLOSE-LIFECYCLE.md determina que alvo fora do escopo bloqueia antes da edição e que esta entrega não cria rewind automático de REVIEW_APPROVED. Portanto, não publicar os destinos propostos nem registrar CLOSED até existir caminho suportado para autorizar seu escopo.

Próxima ação: o responsável pelo AI-SDD deve fornecer o procedimento suportado para revisar o escopo deste CLOSE ou corrigir essa limitação na instalação por processo próprio. Não editar estado/lock manualmente, reabrir revisão por inferência, criar uma aprovação material com hash não apresentado, nem tratar os arquivos de proposta como políticas já publicadas para passar o guard.

A proposta não modifica os resultados históricos da revisão. Nenhum worker permanece ativo após sua preparação; encerrar o lease CLOSE próprio sem mudança de lifecycle.
