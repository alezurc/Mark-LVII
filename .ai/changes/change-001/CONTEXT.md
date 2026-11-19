# CONTEXT — change-001

Revisão 002 — correção do achado R001/P2 após REVIEW_CHANGES_REQUESTED. Esta revisão substitui o contexto operacional anterior para a próxima aprovação; não altera decisões históricas. Cópia exata da revisão anterior: `context-history/revision-001/CONTEXT.md`, SHA-256 registrado no histórico desta revisão. REVIEW.md e DEVELOP.md anteriores permanecem como evidência histórica, sem reclassificar o resultado anterior.

## Intenção e proveniência

Pedido humano: “D006: verificar a abertura do VS Code antes de anunciar sucesso”. Fonte: conversa atual, após seleção explícita do finding D006 em `.ai/DISCOVERY.md` (run discovery-2026-11-17-01). Esta seleção define a intenção; não constitui aprovação de desenvolvimento.

Evidência histórica de D006: a versão inicial de `actions/dev_agent.py:300-319` usava Popen com shell=True, DEVNULL e sucesso presumido após 1,5 segundo; seus chamadores ignoravam o bool. SHA-256 original: `30c80e17cfaa3709f3e5c94faac13325b68d15f810ca756430b6dd716017dbdd`. Esse é o defeito original, não uma descrição do código atual.

Evidência atual CONFIRMED: a implementação entregue em DEVELOP verifica janela e usa argv sem shell, mas `_open_vscode` e `_vscode_observe` ainda usam captura integral via subprocess.run(capture_output=True). REVIEW.md registra R001/P2 OPEN: não há limite de bytes durante captura. A decisão humana registrada em REVIEW_CHANGES_REQUESTED tem referência literal “Autorizado a correção do achado P2”. Ela solicita correção; não substitui o novo gate de aprovação de contexto.

Ponto de partida desta revisão: actions/dev_agent.py SHA-256 `3d48b90554a97c7903774a404da94c831d8f607b507d3e08b5e5aab367f88c85`; tests/test_dev_agent_vscode.py SHA-256 `3c9e22694e1d20f7dfb9379c6ae2b7bc44b5f059ec72c0e9375716963d8c921a`.

## Resultado esperado

O agente de código somente anuncia que o VS Code abriu o projeto quando observa uma janela do editor associada à pasta solicitada. Uma tentativa aceita pelo launcher, um exit code zero ou um processo genérico Code existente não bastam. Quando a observação for indisponível ou ambígua, comunicar abertura não verificada, sem transformar isso em falha do trabalho de código já concluído.

## Escopo exato

- `actions/dev_agent.py`: função _open_vscode, helpers locais estritamente necessários e seus dois chamadores; diagnóstico/log de abertura. Preservar o contrato bool (True somente para confirmação observada; False para falha ou não verificado, diferenciados no diagnóstico).
- `tests/test_dev_agent_vscode.py`: testes focais com unittest e mocks, sem executar o editor, acessar serviços ou ler chaves reais.

SCOPE.json mantém estes mesmos arquivos; o teste já existe após o primeiro DEVELOP. O delta desta revisão limita-se à captura dos subprocessos do fluxo VS Code, seus helpers locais, mensagens necessárias e testes de regressão. Preservar os comportamentos de verificação de janela e dos chamadores já entregues. Nenhum alvo adicional de produto/documentação está previsto para CLOSE. Documentos de governança da change permanecem em sua pasta própria.

Fora do escopo: execução dos projetos gerados, instalação de dependências, escolha de modelos, refatoração geral do dev_agent, outras ações, controles Qt, configuração de credenciais, política Git e demais findings. Não alterar core/desktop ou helpers compartilhados; pode-se consultar APIs existentes sem editá-las. Se forem necessárias alterações adicionais, revisar contexto pelo mecanismo apropriado antes de implementação.

## Critérios de aceitação

1. Sucesso exige observação posterior à solicitação de uma janela do VS Code com associação verificável à pasta alvo normalizada. A verificação aceita janela já existente quando ela corresponde ao alvo; não exige um processo novo. Associação baseada somente em nome de pasta ambíguo não confirma sucesso.
2. Comando aceito sem janela correspondente, processo de outro projeto e observação indisponível/negada resultam em diagnóstico não verificado e retorno False. Nenhum log ou mensagem ao usuário afirma que o editor abriu nesses casos.
3. Executável ausente, exit code não zero e timeout produzem diagnóstico claro, preservando o trabalho de código e sem exceção escapar do helper. Falhas anteriores de candidatos ficam diagnosticadas; tentativas alternativas são limitadas.
4. stdout/stderr são capturados e registrados quando houver conteúdo, com limites de tamanho e sem espera ilimitada. Não usar DEVNULL para esconder erros. Logs não incluem credenciais ou conteúdo do projeto.
5. Argumentos de pasta com espaços ou caracteres especiais chegam ao launcher como dados. Evitar interpretação de shell desnecessária; tratar wrappers .cmd de Windows explicitamente quando aplicável, sem construir comando com texto não escapado.
6. Observação e lançamento possuem deadline total explícito e finito; testes simulam o relógio para provar encerramento. Nenhum widget Qt é criado/tocado a partir da ferramenta.
7. Ambos os chamadores usam o resultado para apresentar diagnóstico de editor consistente; falha em abrir o editor não invalida alterações/testes do projeto. Sucesso na tarefa de código não deve ser confundido com sucesso na abertura do editor.
8. Testes focais cobrem janela correta nova e existente, outro projeto, pasta homônima ambígua, processo sem janela, indisponibilidade de observação, ausência do comando, saída com erro, timeout, fallback limitado e caminho com espaços/caracteres especiais. Verificar também que os chamadores não anunciam abertura sem confirmação.
9. Aplicar teto de **65.536 bytes (64 KiB) por stream**, separadamente para stdout e stderr, em cada subprocesso do lançamento e da observação. Ler em blocos de no máximo 8.192 bytes; o armazenamento retido deve respeitar o teto, com no máximo um bloco transitório por leitor. Não capturar integralmente para só depois truncar. Não transferir a captura ilimitada para arquivo temporário ou fila sem limite. O orçamento agregado deve permanecer proporcional ao número fixo de leitores e candidatos, sem crescimento com o volume total emitido.
10. Ao detectar bytes além do teto, interromper a tentativa, encerrar e colher o subprocesso observado e concluir seus leitores, sem wait/join ilimitado. Registrar stream afetado, limite e truncamento, sem conteúdo bruto, credenciais ou texto do projeto. Retornar False: excesso de saída não confirma abertura. Não iniciar novas tentativas após excesso. Não terminar processos GUI do editor já abertos; limitar o encerramento aos subprocessos CLI/probe criados por esta operação. Cleanup faz parte do orçamento temporal finito; se uma confirmação não puder ser obtida nesse prazo, reportar não verificado.
11. Até o teto, manter classificação por status/timeout e a observação posterior à tentativa concluída. Exatamente 65.536 bytes e EOF não constituem excesso; o primeiro byte adicional deve acioná-lo. Evitar deadlock quando os dois streams produzem simultaneamente, quando um fecha antes do outro ou quando há silêncio. Preservar o deadline compartilhado de oito segundos e os limites dos candidatos.
12. Testar stdout e stderr abaixo, no limite e acima do teto, incluindo emissão simultânea, excesso contínuo, silêncio/timeout, falha de início, cleanup e proteção de logs. Asserções devem demonstrar leitura incremental e retenção limitada durante captura, não somente tamanho do log final. Reexecutar os 19 testes anteriores e adaptá-los às interfaces internas necessárias sem remover cobertura comportamental. Pode-se acrescentar um subprocesso Python local controlado como fixture, com timeout estrito e sem GUI/rede/chaves, para verificar drenagem e encerramento reais; mocks continuam obrigatórios para o editor e o relógio.

## Validação planejada

Na etapa DEVELOP: unittest isolado do arquivo de testes, incluindo os cenários R001 dos critérios 9–12; parsing dos arquivos alterados; revisão do diff, do armazenamento retido e do cleanup. Não chamar modelos, editor real ou serviços externos nos testes. A fixture Python local, se usada, somente emite dados sintéticos sob limites estritos. Observação manual opcional de VS Code instalado só pode sustentar o perfil efetivamente observado; registrar como não executada se indisponível. A aceitação do comportamento conservador em perfis sem observador é provada por mocks; não depende de instalar/configurar outro sistema. REVIEW deve revalidar encoding/BOM e os critérios acima, sem inferir cobertura multiplataforma de um teste Windows.

## Restrições de execução e encoding

Usar somente stdlib e dependências já declaradas em requirements.txt; reutilizar observação disponível quando viável. Qt apenas por métodos thread-safe de player. Não modificar chaves/settings. Preservar bytes fora das edições localizadas, encoding, BOM e finais de linha dos dois arquivos existentes: fonte com CRLF e teste com LF, ambos UTF-8 sem BOM. Não há migração de encoding proposta; ENCODING-POLICY.json permanece sem migrations/unknown_decisions. O runtime recaptura ENCODING-BASELINE.json na conclusão e no novo gate de aprovação; não editar esses artefatos manualmente. Snapshots anteriores ficam no histórico para manter proveniência.

## Riscos e incógnitas

- UNKNOWN: intenção original de encoding sem BOM. Inventário do Discovery indica bytes UTF-8 válidos; isso não comprova intenção de codepage. Preservar sem recodificação integral.
- UNKNOWN: disponibilidade e exatidão da associação janela/workspace em cada OS e configuração do editor. Sem evidência suficiente, retornar não verificado; não pesquisar ou instalar backends alternativos automaticamente.
- INFERRED: títulos homônimos e reuso de instância podem gerar falso positivo se usados isoladamente. Critério 1 exige associação inequívoca; critério 2 cobre falha conservadora.
- INFERRED: espera pelo launcher/observação pode atrasar a tarefa. Critério 6 exige limite total e testes de timeout.
- CONFIRMED: R001 ainda está aberto na entrada desta revisão; limitar apenas o log não limita a memória da captura. Critérios 9–12 definem a correção verificável, ainda não implementada.
- INFERRED: dois pipes e cleanup concorrente podem provocar deadlock ou leitores residuais. Exigir limites de leitura, sincronização e encerramento verificáveis nos testes. Não completar DEVELOP com workers próprios ainda executando.
- A inconsistência D006 é o defeito a resolver, não evidência de autorização de desenvolvimento. Os demais findings do Discovery continuam inalterados.

Nenhuma dependência externa material bloqueia a preparação deste contexto: indisponibilidade de observação tem resultado conservador definido. Se implementação exigir engenharia externa além destes limites, aplicar Boundary Stop Condition e parar o ramo afetado, sem contorno.

## Gate humano

Revisão 002 preparada para avaliação humana. Nova aprovação: PENDING; nova referência de aprovação: NONE; correção de R001 não iniciada. A primeira implementação e sua aprovação permanecem históricas; REVIEW_CHANGES_REQUESTED revogou develop_authorized. O comando de conclusão de CONTEXT não concede autorização nova. Somente referência humana explícita no comando público approve pode concedê-la conforme os gates do runtime. Não reaproveitar automaticamente a referência de changes-requested como aprovação desta revisão.
