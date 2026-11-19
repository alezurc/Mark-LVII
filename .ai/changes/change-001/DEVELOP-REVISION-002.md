# DEVELOP — revisão 002 — change-001

Correção de R001/P2 implementada sob CONTEXT revisão 002 e sua nova aprovação. Os relatórios DEVELOP.md e REVIEW.md anteriores permanecem intactos como evidência histórica. Este registro não constitui nova revisão técnica nem decisão humana de REVIEW.

## Alteração

Somente `actions/dev_agent.py` e `tests/test_dev_agent_vscode.py`, conforme APPROVED-SCOPE.json. O fluxo VS Code agora usa `_vscode_capture` no launcher e no observador, substituindo subprocess.run(capture_output=True) nesses pontos. Nenhum outro subprocesso de dev_agent foi alterado.

Cada stream tem buffer fixo de 65.536 bytes. Resultados/exceções usam memoryview sobre esses buffers, sem cópia integral. Leitura incremental de no máximo 8.192 bytes; ao encher o buffer, solicita um byte para distinguir EOF de excesso. Não há queue, spool, arquivo temporário ou thread leitora. Windows usa PeekNamedPipe antes de os.read; plataformas POSIX usam descriptor não bloqueante. A memória de captura permanece proporcional ao número fixo de streams/tentativas, não ao volume emitido.

Excesso gera OverflowError identificado pelo stream e interrompe toda a operação: sem fallback posterior, sem confirmação de janela e com log de limite/truncamento e contagens, sem conteúdo bruto. Os subprocessos CLI/probe próprios são encerrados se necessário, aguardados com timeout e ambos os pipes fechados em finally. Nenhum processo de editor já existente é alvo de encerramento. Há reserva dentro do timeout de cada captura para cleanup; o deadline compartilhado da operação continua em oito segundos. Falhas/timeout preservam o resultado conservador.

Lançamento por argv/URI sem shell, detecção de janela e comportamento dos dois chamadores foram preservados. Não houve Qt, serviço externo, dependência ou mudança de settings.

## Validação

`python -B tests/test_dev_agent_vscode.py`: **29 testes PASS**, em 1,375 s de execução da suíte nesta validação. Executado por permissão oficial após python não resolvido no PATH restrito; sem substituição de intérprete ou modificação de PATH.

Preservados os 19 cenários anteriores. Acrescentados 10 testes com subcasos para:

- stdout e stderr vazios, abaixo do limite, exatamente 65.536 bytes e 65.537 bytes;
- dois streams ativos no limite e produção contínua além do limite;
- leitura incremental com asserção de pedido/retorno até 8.192 bytes, pedido de um byte adicional e backing buffers de exatamente 65.536 bytes;
- silêncio/timeout, ausência de executável, fechamento antecipado de um stream e ausência de communicate/captura integral;
- interrupção sem fallback ou sucesso falso quando launcher/observador excede o teto; proteção dos logs contra conteúdo sintético sensível;
- subprocessos de fixture encerrados e pipes fechados em sucesso, excesso e timeout, sem threads leitoras residuais.

Fixtures são subprocessos Python locais controlados que somente emitem dados sintéticos ou aguardam sob timeout. Editor/modelos/rede/chaves reais não foram usados. O payload de detecção de janela continua testado com fonte de processos/janelas falsa. Parsing dos dois arquivos é executado pela suíte. Não se alega teste manual do editor ou validação completa da aplicação.

`git -c core.whitespace=cr-at-eol diff --check`: PASS. UTF-8 validado estritamente em ambos os alvos, sem BOM; CRLF do fonte e LF do teste preservados. Não há migração de encoding. UNKNOWN sobre intenção histórica sem BOM permanece; a validação comprova bytes e preservação, não intenção.

## Evidência

SHA-256 final:

- actions/dev_agent.py: `a037c36d50dac943fe18168fe9a3e278f7c94e4d159ae8c0554ee31ace344d8c`
- tests/test_dev_agent_vscode.py: `e87a0e53312e8c12073d87642e268b936445b3ff74cd38aa5194dd425a0885ce`

ENCODING-BASELINE.json aprovado preservado, hash `cc365165afe8fdec0612111cb5d75c9f41277da5a962ce5de43cb8db382fd619`. Artefatos de runtime não foram editados manualmente.

Lease desta sessão: `769631f0-7fa4-47f0-9c4c-697e104988a1`, adquirido por begin-stage e validado por check-stage antes das escritas. Todos os testes/fixtures terminaram. A correção de R001 está entregue para reavaliação; seu finding histórico OPEN não foi reescrito nem convertido em aprovação automática. As limitações já documentadas de títulos sem caminho e observação multiplataforma continuam. Nenhuma condição material nova de boundary foi identificada; não houve investigação externa.

Concluir somente DEVELOP pelo launcher canônico; não iniciar REVIEW automaticamente.
