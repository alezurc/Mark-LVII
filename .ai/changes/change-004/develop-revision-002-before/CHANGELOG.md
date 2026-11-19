# Histórico de mudanças — Mark LVII

As entradas registram mudanças revisadas, sem representar release ou publicação automática.

## change-003 — encoding e evidência de integração local

- Os controles literais do áudio sintético em providers/_tests.py foram substituídos por escapes Python equivalentes, preservando os bytes de PCM, UTF-8 sem BOM e CRLF.
- A suíte providers executa fontes em projeto temporário, com configuração e vozes sintéticas isoladas, cleanup, timeouts e resultados PASS/FAIL/SKIP separados. Novos testes verificam encoding, isolamento e o harness real com plugins sintéticos; README documenta execução e limites.
- Validação na revisão: 55 testes unittest passaram; providers registrou 98 PASS, zero FAIL e dois SKIPs opcionais por Piper ausente. Ambiente virtual local com dependências declaradas, Python 3.15.2 AMD64; requirements.txt preservado.
- Limitações: revisão não isolada; Python além da faixa historicamente testada até 3.13. Áudio físico, UI interativa, serviços reais, crash e outras plataformas não foram validados; intenção histórica de encoding sem BOM permanece UNKNOWN. O harness e os guards de teste não são sandbox de segurança.
- Identificação mantida: **Mark LVII**, conforme PROJECT-POLICY.md. Sem nova versão, tag ou release.

Evidência técnica: .ai/changes/change-003/REVIEW.md e .ai/changes/change-003/DEVELOP.md.

## change-002 — persistência de memória

- As gravações de memória e sessões preparam um JSON completo em arquivo temporário exclusivo e substituem o destino após fechar a escrita. Falhas anteriores à substituição preservam o arquivo anterior, sem anunciar sucesso.
- Operações internas de leitura, alteração e gravação são serializadas entre threads do mesmo processo, preservando os contratos públicos e o formato da memória.
- Validação: 42 testes passaram na revisão (13 de persistência e 29 de regressão do VS Code), incluindo falhas de escrita/substituição, consumo de sessões e concorrência. UTF-8 sem BOM e finais de linha foram preservados.
- Limitações: revisão não isolada; sem validação integrada ou crash real. Não há garantia de durabilidade física após queda de energia, coordenação entre processos ou recuperação de dados já corrompidos.
- Identificação mantida: **Mark LVII**, conforme PROJECT-POLICY.md.

Evidência técnica: .ai/changes/change-002/REVIEW.md e .ai/changes/change-002/DEVELOP.md.

## change-001 — confirmação da abertura do VS Code

- A abertura só é anunciada como confirmada após observar uma janela do VS Code associada ao caminho completo do projeto. Sem evidência suficiente, o agente informa que a abertura não foi confirmada e preserva o trabalho de código salvo.
- stdout e stderr dos subprocessos desse fluxo têm limite de 64 KiB por stream, com leitura incremental. Excesso interrompe a tentativa, sem anunciar sucesso ou tentar outro candidato; os subprocessos próprios são encerrados e seus pipes fechados.
- Validação: 29 testes passaram, incluindo limite exato, primeiro byte excedente, dois streams ativos, timeout e encerramento. UTF-8 sem BOM e finais de linha foram preservados.
- Limitações: revisão não isolada e sem teste manual do editor ou integração completa da aplicação. Títulos sem caminho completo e perfis sem observação continuam não verificados.
- Identificação mantida: **Mark LVII**. Nenhuma nova versão, tag ou release atribuída.

Evidência técnica: `.ai/changes/change-001/REVIEW-REVISION-002.md` e `.ai/changes/change-001/DEVELOP-REVISION-002.md`.
