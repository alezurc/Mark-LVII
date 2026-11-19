# Retomada 002 — DEP-004-001 — instalação delimitada de PyQt6

Data: 2026-11-19 (America/Sao_Paulo).
Humano: usuário responsável pelo projeto nesta conversa.
Referência literal: “sim”, em resposta a “Autoriza instalar o PyQt6 nesse Python e verificar sua compatibilidade para retomar o desenvolvimento?”.
Objetivo/escopo: instalar PyQt6 no Python disponível, sem ambiente virtual, e verificar compatibilidade/importação dos componentes da interface. Não instalar automaticamente outros pacotes.
Vínculo: BOUNDARY-STOP-DEP-004-001.md e RESUMPTION-DEP-004-001.md. Ambos preservados.
Limite: instalação de PyQt6 e suas dependências transitivas; uma verificação de importação, com repetição pelo mecanismo oficial em caso de Acesso negado. Parar em incompatibilidade/dependência adicional ausente.

## Evidência

Comando: python -m pip install PyQt6
Tentativa normal: Acesso negado antes de iniciar Python.
Repetição autorizada via mecanismo oficial: exit code 0.
Instalados: PyQt6 6.12.1, PyQt6-Qt6 6.12.0, PyQt6-sip 13.13.1, pelos wheels selecionados pelo pip. PATH não foi alterado.

Comando de verificação: python -c "import sys; from PyQt6.QtCore import PYQT_VERSION_STR, QT_VERSION_STR; from PyQt6.QtWidgets import QApplication; print('Python:', sys.version); print('PyQt:', PYQT_VERSION_STR, 'Qt:', QT_VERSION_STR); import ui; print('UI import available')"
Tentativa normal: Acesso negado antes de iniciar Python.
Repetição autorizada via mecanismo oficial: exit code 1.
Python: 3.15.2; PyQt: 6.12.1; Qt: 6.12.0.
Importações PyQt6.QtCore/PyQt6.QtWidgets: sucesso.
Import ui: ModuleNotFoundError: No module named 'psutil', em ui.py:21.

## Disposição vinculada

CONFIRMED: ausência anterior de PyQt6 resolvida para import dos módulos Qt neste Python. Isso não prova funcionamento da interface completa ou critérios da change-004.
CONFIRMED: psutil ausente neste Python impede importação de ui e evidência obrigatória AC8.
UNKNOWN: outras dependências e comportamento completo da aplicação; não investigar automaticamente após a parada.
Categoria: EXTERNAL_DEPENDENCY, mesma preparação de ambiente DEP-004-001.
Consequência material: DEVELOP permanece incompleto; sem evidência Qt da aplicação, REVIEW/CLOSE dependentes permanecem bloqueados.
Responsável: usuário responsável pelo ambiente do projeto.
Limite: autorização de instalar PyQt6 não concede instalação de psutil ou do requirements.txt inteiro.
Próxima ação humana: autorizar preparação delimitada das dependências declaradas do projeto, ou preparar ambiente e autorizar nova verificação.
Condição objetiva de retomada: autorização explícita para resolver dependências adicionais, seguida de import ui e perfil de testes Qt disponíveis; sem alterar critérios/produto fora do SCOPE aprovado.
reopen_authorization_ref para expansão adicional: NONE.

Nenhum arquivo de produto alterado, nenhum lease adquirido, nenhum teste da implementação executado. Estado runtime não foi editado. A parada original permanece como registro histórico, com PyQt6 resolvido parcialmente por esta retomada e a lacuna psutil agora identificada.