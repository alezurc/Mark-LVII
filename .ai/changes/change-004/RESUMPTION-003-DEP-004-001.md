# Retomada 003 — DEP-004-001 — requirements.txt

Data: 2026-11-19 (America/Sao_Paulo).
Humano: usuário responsável pelo projeto nesta conversa.
Referência literal: “autorizo sim e gostaria de saber como posso resolver o problema de acesso negado”, em resposta à instalação das dependências declaradas em requirements.txt e verificação do ambiente para retomar o desenvolvimento.
Vínculos: BOUNDARY-STOP-DEP-004-001.md e retomadas anteriores, preservados.
Objetivo/escopo: python -m pip install -r requirements.txt no Python atual, sem ambiente virtual; verificar disponibilidade após sucesso. Não instalar toolchain de sistema, trocar interpretador ou alterar requisitos automaticamente.
Limite/ponto de parada: uma instalação com uma repetição pelo mecanismo oficial em caso de Acesso negado; parar em falha que exija capacidade fora da preparação de pacotes declarados.

## Evidência e resultado

Get-Command python: C:\Program Files\WindowsApps\PythonSoftwareFoundation.PythonManager_26.4.240.0_x64__3847v3x7pw1km\python.exe
Get-Command py: C:\Windows\py.exe (apenas metadado; não usado como fallback).
Python previamente confirmado: 3.15.2.
Comando: python -m pip install -r requirements.txt
Tentativa normal: Acesso negado antes de iniciar Python.
Repetição via permissão oficial: processo executou, pip resolveu/downloadou pacotes e construiu wheels de seis dependências, mas encerrou com exit code 1 antes de concluir a instalação agregada.
Erro material: Failed building wheel for pyyaml; Microsoft Visual C++ 14.0 or greater is required.
PyYAML selecionado: 6.0.3, distribuição fonte pyyaml-6.0.3.tar.gz. Dependência transitiva de uvicorn[standard] declarada no projeto.
Não afirmar instalação completa ou prontidão do ambiente. PyQt6 instalado na retomada anterior não é revertido. Nenhuma desinstalação/limpeza de cache efetuada.

## Disposição vinculada

Categoria primária: EXTERNAL_DEPENDENCY; capacidade adicional requerida pelo build de dependência no perfil atual.
CONFIRMED: este comando falhou no build PyYAML por requisito do compilador C++ reportado pelo processo. Não prova incompatibilidade intrínseca de Python 3.15 nem ausência de qualquer compilador em toda a máquina.
INFERRED: restrição do contexto de execução do Codex participa do Acesso negado, pois o mesmo comando e launcher executam com permissão ampliada. Regra exata UNKNOWN; não alterar ACL de WindowsApps nem sandbox/política automaticamente.
Materialidade/consequência: instalação agregada e perfil de testes da change-004 não disponíveis; DEVELOP não concluído, downstream dependente bloqueado.
Responsável: usuário responsável pelo ambiente do projeto.
Limite de responsabilidade: instalar Microsoft C++ Build Tools ou outro Python e mudar o perfil não está coberto pela autorização de pip install -r requirements.txt.
Próxima ação humana: escolher e autorizar preparação delimitada do toolchain exigido, ou indicar/autorizar outro perfil Python do projeto. Sem escolha automática, alteração de requirements.txt, pin improvisado ou bypass de build.
Condição objetiva de retomada: autorização explícita vinculada a DEP-004-001 para o próximo perfil de preparação, instalação de dependências bem-sucedida e verificação de importação/testes obrigatórios disponível.
reopen_authorization_ref para nova ampliação: NONE.
Nenhum arquivo de produto alterado, nenhum lease adquirido, nenhum teste de implementação executado. Lifecycle e aprovação permanecem preservados; este documento não registra conclusão de DEVELOP.