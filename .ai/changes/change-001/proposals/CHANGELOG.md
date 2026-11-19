# Histórico de mudanças — Mark LVII

As entradas registram mudanças revisadas, sem representar release ou publicação automática.

## change-001 — confirmação da abertura do VS Code

- A abertura só é anunciada como confirmada após observar uma janela do VS Code associada ao caminho completo do projeto. Sem evidência suficiente, o agente informa que a abertura não foi confirmada e preserva o trabalho de código salvo.
- stdout e stderr dos subprocessos desse fluxo têm limite de 64 KiB por stream, com leitura incremental. Excesso interrompe a tentativa, sem anunciar sucesso ou tentar outro candidato; os subprocessos próprios são encerrados e seus pipes fechados.
- Validação: 29 testes passaram, incluindo limite exato, primeiro byte excedente, dois streams ativos, timeout e encerramento. UTF-8 sem BOM e finais de linha foram preservados.
- Limitações: revisão não isolada e sem teste manual do editor ou integração completa da aplicação. Títulos sem caminho completo e perfis sem observação continuam não verificados.
- Identificação mantida: **Mark LVII**. Nenhuma nova versão, tag ou release atribuída.

Evidência técnica: `.ai/changes/change-001/REVIEW-REVISION-002.md` e `.ai/changes/change-001/DEVELOP-REVISION-002.md`.
