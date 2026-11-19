# DEVELOP — change-001

Implementação de D006 no escopo aprovado: `actions/dev_agent.py` e `tests/test_dev_agent_vscode.py`.

## Comportamento entregue

O launcher usa argv sem shell e URI de pasta. No Windows, wrappers code.cmd/code.bat são substituídos pelo Code.exe e cli.js da mesma instalação, com ELECTRON_RUN_AS_NODE, evitando interpretação da pasta pelo shell. Até três candidatos são tentados, com timeout por tentativa e deadline compartilhado de oito segundos para lançamento/observação.

Depois de uma tentativa concluída, uma observação de janelas/processos reutiliza core.appidentity em subprocesso Python sem GUI, com timeout. Somente processo Code/code.exe e campo de título correspondente ao caminho completo normalizado confirmam sucesso. Processo genérico, outra pasta, título com apenas basename, pasta homônima, erro de observação e timeout não confirmam. Janelas existentes podem confirmar após a solicitação. Em executável empacotado, não iniciar o próprio GUI como Python: retornar observação não confirmada.

stdout/stderr são capturados; o log registra stream e tamanho recebido, com status/timeout separado, sem retransmitir conteúdo arbitrário que possa expor credenciais ou texto do projeto. Não há DEVNULL neste fluxo. Os dois chamadores usam o bool e registram confirmação ou não confirmação sem invalidar trabalho de código salvo.

## Validação

- `python -B tests/test_dev_agent_vscode.py`: 19 testes PASS. Execução oficial permitida após falha de resolução de python no PATH restrito. Testes usam AST dos helpers/chamadores reais, mocks de subprocessos e execução do payload de observação com fonte de janelas falsa; sem import do produto, chaves, editor ou chamadas de modelos.
- Parsing de ambos os arquivos faz parte da carga do teste; PASS.
- `git -c core.whitespace=cr-at-eol diff --check`: PASS. A checagem padrão acusa CRLF como whitespace; nenhuma conversão foi aplicada para mascarar isso.
- UTF-8 validado estritamente, sem BOM; CRLF do fonte existente preservado. Teste novo UTF-8 sem BOM. Não houve migração ou alteração da política de encoding aprovada.
- Revisão do diff: somente os dois arquivos de produto/teste aprovados; documentos auxiliares ficam na pasta da change. Demais arquivos de governança já estavam untracked antes de DEVELOP.

Hashes SHA-256 finais:

- actions/dev_agent.py: `3d48b90554a97c7903774a404da94c831d8f607b507d3e08b5e5aab367f88c85`
- tests/test_dev_agent_vscode.py: `3c9e22694e1d20f7dfb9379c6ae2b7bc44b5f059ec72c0e9375716963d8c921a`

## Limites preservados

Teste manual do VS Code real não executado. Títulos padrão de VS Code geralmente não expõem o caminho completo; nesses casos a abertura permanece não verificada, mesmo que visualmente tenha ocorrido. core.appidentity não fornece títulos em todos os sistemas; não se alega confirmação multiplataforma. Nenhum ajuste do editor, backend alternativo, widget ou dependência nova foi introduzido. Limitações de observação são tratadas pelo resultado conservador definido no contexto, sem investigação externa ou expansão de escopo. UNKNOWN sobre intenção de encoding sem BOM permanece; bytes foram preservados fora das edições localizadas.

Execução exclusiva desta sessão: `ab043edf-a3c0-4cf0-bd32-f36b28c2d695`, adquirida via begin-stage; check-stage válido antes de cada lote de alterações. Nenhum worker de teste permanece ativo. Conclusão deve ser registrada pelo launcher canônico; nenhuma decisão REVIEW foi inferida.
