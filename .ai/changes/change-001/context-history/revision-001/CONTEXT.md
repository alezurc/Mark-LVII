# CONTEXT — change-001

## Intenção e proveniência

Pedido humano: “D006: verificar a abertura do VS Code antes de anunciar sucesso”. Fonte: conversa atual, após seleção explícita do finding D006 em `.ai/DISCOVERY.md` (run discovery-2026-11-17-01). Esta seleção define a intenção; não constitui aprovação de desenvolvimento.

Evidência CONFIRMED: `actions/dev_agent.py:300-319` inicia candidatos por Popen com shell=True, descarta stdout/stderr, espera 1,5 segundo e imprime sucesso sem observar resultado. Os chamadores em torno das linhas 566 e 1483 ignoram o bool retornado. CONFLICT: esse comportamento contraria AGENTS.md quanto a saída de processos e sucesso verificado. SHA-256 inicial de actions/dev_agent.py: `30c80e17cfaa3709f3e5c94faac13325b68d15f810ca756430b6dd716017dbdd`.

## Resultado esperado

O agente de código somente anuncia que o VS Code abriu o projeto quando observa uma janela do editor associada à pasta solicitada. Uma tentativa aceita pelo launcher, um exit code zero ou um processo genérico Code existente não bastam. Quando a observação for indisponível ou ambígua, comunicar abertura não verificada, sem transformar isso em falha do trabalho de código já concluído.

## Escopo exato

- `actions/dev_agent.py`: função _open_vscode, helpers locais estritamente necessários e seus dois chamadores; diagnóstico/log de abertura. Preservar o contrato bool (True somente para confirmação observada; False para falha ou não verificado, diferenciados no diagnóstico).
- `tests/test_dev_agent_vscode.py`: testes focais com unittest e mocks, sem executar o editor, acessar serviços ou ler chaves reais.

SCOPE.json lista estes mesmos arquivos, incluindo o teste novo. Nenhum alvo adicional de produto/documentação está previsto para CLOSE. Documentos de governança da change permanecem em sua pasta própria.

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

## Validação planejada

Na etapa DEVELOP: unittest isolado do arquivo novo; parsing dos arquivos alterados; revisão do diff e das mensagens dos dois chamadores. Não chamar modelos nem ferramentas com efeitos reais nos testes. Observação manual opcional de VS Code instalado só pode sustentar o perfil efetivamente observado; registrar como não executada se indisponível. A aceitação do comportamento conservador em perfis sem observador é provada por mocks; não depende de instalar/configurar outro sistema. REVIEW deve revalidar encoding/BOM e os critérios acima, sem inferir cobertura multiplataforma de um teste Windows.

## Restrições de execução e encoding

Usar somente stdlib e dependências já declaradas em requirements.txt; reutilizar observação disponível quando viável. Qt apenas por métodos thread-safe de player. Não modificar chaves/settings. Preservar bytes fora das edições localizadas, encoding, BOM e finais de linha do arquivo existente. Não há migração de encoding proposta. O teste novo será UTF-8 sem BOM. O runtime captura ENCODING-BASELINE.json na conclusão e recaptura no gate de aprovação; não editar esses artefatos manualmente.

## Riscos e incógnitas

- UNKNOWN: intenção original de encoding sem BOM. Inventário do Discovery indica bytes UTF-8 válidos; isso não comprova intenção de codepage. Preservar sem recodificação integral.
- UNKNOWN: disponibilidade e exatidão da associação janela/workspace em cada OS e configuração do editor. Sem evidência suficiente, retornar não verificado; não pesquisar ou instalar backends alternativos automaticamente.
- INFERRED: títulos homônimos e reuso de instância podem gerar falso positivo se usados isoladamente. Critério 1 exige associação inequívoca; critério 2 cobre falha conservadora.
- INFERRED: espera pelo launcher/observação pode atrasar a tarefa. Critério 6 exige limite total e testes de timeout.
- A inconsistência D006 é o defeito a resolver, não evidência de autorização de desenvolvimento. Os demais findings do Discovery continuam inalterados.

Nenhuma dependência externa material bloqueia a preparação deste contexto: indisponibilidade de observação tem resultado conservador definido. Se implementação exigir engenharia externa além destes limites, aplicar Boundary Stop Condition e parar o ramo afetado, sem contorno.

## Gate humano

Contexto preparado para avaliação humana. Aprovação: PENDING; referência de aprovação: NONE; implementação não iniciada. O comando de conclusão de CONTEXT não concede develop_authorized. Somente referência humana explícita no comando público approve pode conceder autorização conforme os gates do runtime.
