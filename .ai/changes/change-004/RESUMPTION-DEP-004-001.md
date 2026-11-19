# Retomada delimitada — DEP-004-001

Data: 2026-11-19 (America/Sao_Paulo).
Humano: usuário responsável pelo projeto nesta conversa.
Referência literal: “sim autorizo e não uso um ambiente virtual”.
Vínculo: BOUNDARY-STOP-DEP-004-001.md; autorização responde à pergunta explícita de verificar novamente o Python disponível, sem instalar pacotes, e retomar implementação somente se PyQt6 estiver disponível.
Objetivo/escopo: uma verificação de versão e import PyQt6.QtWidgets usando python disponível no PATH, cwd D:\Trabalho_Pessoal\Mark-LVII. Sem ambiente virtual, instalação, mudança de PATH ou busca de outro interpretador.
Evidência esperada: versão Python e import Qt bem-sucedido.
Limite/ponto de parada: uma verificação, com uma repetição oficial em caso de Acesso negado; parar se dependência faltar.

## Resultado

Comando: python -c "import sys; print(sys.version); import PyQt6.QtWidgets; print('PyQt6 available')"
Tentativa normal: ferramenta não conseguiu iniciar Python, Acesso negado.
Repetição pelo mecanismo oficial de permissão: Python 3.15.2 iniciou; exit code 1; ModuleNotFoundError: No module named 'PyQt6'.
CONFIRMED: PyQt6 indisponível neste Python nesta verificação. UNKNOWN: disponibilidade em outros interpretadores, que não foram procurados.
A condição objetiva de retomada do DEVELOP não foi satisfeita. Nenhum arquivo de produto alterado, nenhum pacote instalado, nenhum lease adquirido e nenhum teste da implementação executado. Lifecycle e autorização de produto não foram alterados.

A parada original e sua evidência permanecem preservadas. A autorização foi utilizada apenas no escopo acima; não autoriza preparar dependências. O ramo volta a ficar parado sob DEP-004-001. Próxima ação humana: autorizar instalação delimitada de PyQt6 e dependências necessárias ao perfil de testes, ou preparar o ambiente e autorizar nova verificação. Sem investigação adicional automática.