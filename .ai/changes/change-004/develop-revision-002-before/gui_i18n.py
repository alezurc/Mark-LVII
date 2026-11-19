"""Desktop UI messages and explicit, weakly held Qt text bindings.

Only Text values opt into localization. Ordinary strings (user content, paths,
provider names and plugin metadata) always pass through unchanged.
"""
from __future__ import annotations

import string
import weakref

LANGUAGES = (("en", "English"), ("pt-BR", "Português (Brasil)"))
_language = "en"
_bindings = weakref.WeakKeyDictionary()
_listeners = []
PT_BR = {'The test itself failed: {error}': 'O teste falhou: {error}', '   (optional)': '   (opcional)',
 '   ★ recommended': '   ★ recomendado',
 ' and ': ' e ',
 ' under Windows Defender Firewall → Inbound Rules.': ' no Windows Defender Firewall → Regras de '
                                                      'Entrada.',
 ' · held back in quiet hours': ' · suspensa no horário silencioso',
 '#00d4ff   (custom hex colour)': '#00d4ff   (cor hexadecimal personalizada)',
 'A 3-D reactor core that turns with the state and moves with your voice. Tap to switch to the animated head.': 'Um '
                                                                                                                'núcleo '
                                                                                                                'de '
                                                                                                                'reator '
                                                                                                                '3D '
                                                                                                                'que '
                                                                                                                'gira '
                                                                                                                'conforme '
                                                                                                                'o '
                                                                                                                'estado '
                                                                                                                'e '
                                                                                                                'se '
                                                                                                                'move '
                                                                                                                'com '
                                                                                                                'sua '
                                                                                                                'voz. '
                                                                                                                'Clique '
                                                                                                                'para '
                                                                                                                'exibir '
                                                                                                                'o '
                                                                                                                'rosto '
                                                                                                                'animado.',
 'ANSWER': 'RESPONDER',
 'ASSISTANT NAME': 'NOME DO ASSISTENTE',
 'ASSISTANT VOICE': 'VOZ DO ASSISTENTE',
 'All three set. SAVE & APPLY reconnects; the conversation is kept.': 'Os três estão configurados. '
                                                                      'SALVAR E APLICAR reconecta '
                                                                      'e mantém a conversa.',
 'An animated head that speaks your words and shows what JARVIS is doing. Tap to switch to the reactor core.': 'Um '
                                                                                                               'rosto '
                                                                                                               'animado '
                                                                                                               'que '
                                                                                                               'fala '
                                                                                                               'e '
                                                                                                               'mostra '
                                                                                                               'o '
                                                                                                               'que '
                                                                                                               'JARVIS '
                                                                                                               'está '
                                                                                                               'fazendo. '
                                                                                                               'Clique '
                                                                                                               'para '
                                                                                                               'exibir '
                                                                                                               'o '
                                                                                                               'núcleo '
                                                                                                               'do '
                                                                                                               'reator.',
 'Applying reconnects the session. Your conversation is kept.': 'Aplicar reconecta a sessão. Sua '
                                                                'conversa é mantida.',
 'Auto-detected: {v0}': 'Detectado automaticamente: {v0}',
 'BRIEFING': 'RESUMO',
 'BROKEN': 'COM ERRO',
 'Background task': 'Tarefa em segundo plano',
 'CANCEL': 'CANCELAR',
 'CHECKING': 'VERIFICANDO',
 'CLOSE': 'FECHAR',
 'CODE AGENT': 'AGENTE DE CÓDIGO',
 'COMMAND': 'COMANDO',
 'COMMUNICATIONS': 'COMUNICAÇÕES',
 'CONNECTED': 'CONECTADO',
 'CONNECTING': 'CONECTANDO',
 'CONTROLS': 'CONTROLES',
 'Carries out': 'Executa',
 'Change it by voice — "move the briefing to 08:30", "turn the check-in off", "remind me every Friday at 17:00".': 'Altere '
                                                                                                                   'por '
                                                                                                                   'voz '
                                                                                                                   '— '
                                                                                                                   '"mude '
                                                                                                                   'o '
                                                                                                                   'resumo '
                                                                                                                   'para '
                                                                                                                   '08:30", '
                                                                                                                   '"desative '
                                                                                                                   'o '
                                                                                                                   'check-in", '
                                                                                                                   '"lembre-me '
                                                                                                                   'toda '
                                                                                                                   'sexta '
                                                                                                                   'às '
                                                                                                                   '17:00".',
 'Choose what powers the conversation. Gemini is the default and needs nothing set up here.': 'Escolha '
                                                                                              'o '
                                                                                              'que '
                                                                                              'alimenta '
                                                                                              'a '
                                                                                              'conversa. '
                                                                                              'Gemini '
                                                                                              'é o '
                                                                                              'padrão '
                                                                                              'e '
                                                                                              'não '
                                                                                              'precisa '
                                                                                              'de '
                                                                                              'configuração '
                                                                                              'aqui.',
 'Code is written by whatever answers background requests above.': 'O código é escrito pelo modelo '
                                                                   'das solicitações em segundo '
                                                                   'plano acima.',
 'Configure J.A.R.V.I.S. before first boot.': 'Configure J.A.R.V.I.S. antes de iniciar.',
 'Controls — the everyday switches': 'Controles — opções do dia a dia',
 'Could not save interface language: {error}': 'Não foi possível salvar o idioma da interface: '
                                               '{error}',
 'DEFAULT': 'PADRÃO',
 'DEFAULT  (follow system)': 'PADRÃO  (seguir o sistema)',
 'DISCONNECTED': 'DESCONECTADO',
 'DISMISS': 'DISPENSAR',
 'DONE': 'CONCLUÍDO',
 'DROP A FILE OR FOLDER  ·  OR CLICK': 'SOLTE UM ARQUIVO OU PASTA  ·  OU CLIQUE',
 'Dismiss': 'Dispensar',
 'Document': 'Documento',
 'ENGINE': 'MOTOR',
 'ENGINE · {engine}': 'MOTOR · {engine}',
 'ERR: Auto-start failed — {v0}': 'ERR: Falha na inicialização automática — {v0}',
 'ERR: Config save failed — {v0}': 'ERR: Falha ao salvar configuração — {v0}',
 'ERR: Confirmation failed — {v0}': 'ERR: Falha na confirmação — {v0}',
 'ERR: Push-to-talk failed — {v0}': 'ERR: Falha no pressionar para falar — {v0}',
 'ERR: Shortcut failed — {v0}': 'ERR: Falha no atalho — {v0}',
 'EXPLAIN': 'EXPLICAR',
 'F4 MUTE   ·   F11 FULLSCREEN   ·   ESC INTERRUPT   ·   BY FATIHMAKES': 'F4 SILENCIAR   ·   F11 '
                                                                         'TELA CHEIA   ·   ESC '
                                                                         'INTERROMPER   ·   POR '
                                                                         'FATIHMAKES',
 'FAILED': 'FALHOU',
 'FILE: {v0} ({v1}) loaded': 'FILE: {v0} ({v1}) carregado',
 'FILES': 'ARQUIVOS',
 'FINISH  →': 'CONCLUIR  →',
 'FIX': 'CORRIGIR',
 'FIXING': 'CORRIGINDO',
 'FOLDER: {v0} ({v1} files) loaded': 'FOLDER: {v0} ({v1} arquivos) carregada',
 'Forget this': 'Esquecer este item',
 'Fullscreen  [F11]': 'Tela cheia  [F11]',
 'GEMINI API KEY': 'CHAVE DE API DO GEMINI',
 'Gemini Live. Nothing on this panel changes the conversation.': 'Gemini Live. Este painel não '
                                                                 'altera a conversa.',
 'Gemini only  —  the way it has always been': 'Somente Gemini  —  configuração original',
 'HEARING': 'RECONHECIMENTO',
 'Hold a key to talk instead of streaming the mic continuously.': 'Segure uma tecla para falar em '
                                                                  'vez de transmitir o microfone '
                                                                  'continuamente.',
 'IDLE': 'EM ESPERA',
 'INITIALISING': 'INICIALIZANDO',
 'INPUT': 'ENTRADA',
 'INSTALL {v0}': 'INSTALAR {v0}',
 'INTERFACE LANGUAGE': 'IDIOMA DA INTERFACE',
 'INTERRUPT': 'INTERROMPER',
 'Key expires in  {v0:02d}:{v1:02d}': 'A chave expira em  {v0:02d}:{v1:02d}',
 'LISTENING': 'OUVINDO',
 'LIVE': 'AO VIVO',
 'LOG': 'REGISTRO',
 'Last: {last} — {result}': 'Última: {last} — {result}',
 'Left as it is, these keep using Gemini and stop working when its text quota runs out.': 'Sem '
                                                                                          'alterações, '
                                                                                          'continuam '
                                                                                          'usando '
                                                                                          'Gemini '
                                                                                          'e param '
                                                                                          'quando '
                                                                                          'a cota '
                                                                                          'de '
                                                                                          'texto '
                                                                                          'acaba.',
 'MEMORY': 'MEMÓRIA',
 'MIC ACTIVE': 'MIC ATIVO',
 'MIC MUTED': 'MIC SILENCIADO',
 'MIC · LIVE': 'MIC · ATIVO',
 'MIC · MUTED': 'MIC · SILENCIADO',
 'MICROPHONE': 'MICROFONE',
 'MICROPHONE — what JARVIS hears you with': 'MICROFONE — como JARVIS ouve você',
 'MUTED': 'SILENCIADO',
 'Microphone stays closed until you hold the key — nothing is sent while you are not holding it.': 'O '
                                                                                                   'microfone '
                                                                                                   'fica '
                                                                                                   'fechado '
                                                                                                   'até '
                                                                                                   'você '
                                                                                                   'segurar '
                                                                                                   'a '
                                                                                                   'tecla '
                                                                                                   '— '
                                                                                                   'nada '
                                                                                                   'é '
                                                                                                   'enviado '
                                                                                                   'enquanto '
                                                                                                   'ela '
                                                                                                   'estiver '
                                                                                                   'solta.',
 'Mute or unmute the microphone  [F4]': 'Silenciar ou ativar o microfone  [F4]',
 'NETWORK': 'REDE',
 'NEW KEY': 'NOVA CHAVE',
 'NEXT  →': 'PRÓXIMA  →',
 'NO KEY — USE A LOCAL MODEL': 'SEM CHAVE — USAR MODELO LOCAL',
 'Next: {next}': 'Próxima: {next}',
 'No background tasks yet.': 'Ainda não há tarefas em segundo plano.',
 'No configurable plugins are installed.\nDrop a plugin that needs settings (like the 3D-printer suite) into the plugins folder and it will show up here.': 'Nenhum '
                                                                                                                                                            'plugin '
                                                                                                                                                            'configurável '
                                                                                                                                                            'instalado.\n'
                                                                                                                                                            'Coloque '
                                                                                                                                                            'um '
                                                                                                                                                            'plugin '
                                                                                                                                                            'que '
                                                                                                                                                            'precise '
                                                                                                                                                            'de '
                                                                                                                                                            'configuração '
                                                                                                                                                            '(como '
                                                                                                                                                            'o '
                                                                                                                                                            'de '
                                                                                                                                                            'impressora '
                                                                                                                                                            '3D) '
                                                                                                                                                            'na '
                                                                                                                                                            'pasta '
                                                                                                                                                            'plugins '
                                                                                                                                                            'para '
                                                                                                                                                            'exibi-lo '
                                                                                                                                                            'aqui.',
 'No file loaded': 'Nenhum arquivo carregado',
 'No plugins found in /plugins.': 'Nenhum plugin encontrado em /plugins.',
 'No routines yet. Ask for one by voice — "every weekday at 08:30, tell me the weather".': 'Ainda '
                                                                                           'não há '
                                                                                           'rotinas. '
                                                                                           'Peça '
                                                                                           'por '
                                                                                           'voz — '
                                                                                           '"todo '
                                                                                           'dia '
                                                                                           'útil '
                                                                                           'às '
                                                                                           '08:30, '
                                                                                           'diga a '
                                                                                           'previsão '
                                                                                           'do '
                                                                                           'tempo".',
 'None': 'Nenhum',
 'None found.': 'Nenhum resultado.',
 'Nothing stored yet.': 'Ainda não há informações salvas.',
 'Nothing to check for this one.': 'Nada para verificar neste provedor.',
 'Nothing to list for this one.': 'Nada para listar neste provedor.',
 'Nothing to set up. Your voice goes to Gemini and comes back as speech over one connection, with the transcript and every tool call on the same wire.': 'Nada '
                                                                                                                                                         'para '
                                                                                                                                                         'configurar. '
                                                                                                                                                         'Sua '
                                                                                                                                                         'voz '
                                                                                                                                                         'vai '
                                                                                                                                                         'ao '
                                                                                                                                                         'Gemini '
                                                                                                                                                         'e '
                                                                                                                                                         'volta '
                                                                                                                                                         'como '
                                                                                                                                                         'fala '
                                                                                                                                                         'na '
                                                                                                                                                         'mesma '
                                                                                                                                                         'conexão, '
                                                                                                                                                         'com '
                                                                                                                                                         'transcrição '
                                                                                                                                                         'e '
                                                                                                                                                         'chamadas '
                                                                                                                                                         'de '
                                                                                                                                                         'ferramentas.',
 'OFF': 'DESLIGADO',
 'ON': 'LIGADO',
 'OPERATING SYSTEM': 'SISTEMA OPERACIONAL',
 'OUTPUT VOLUME': 'VOLUME DE SAÍDA',
 'One connection carries your voice, its voice, the transcript and the tools together. The fastest option — about half a second to the first word.': 'Uma '
                                                                                                                                                     'conexão '
                                                                                                                                                     'transporta '
                                                                                                                                                     'sua '
                                                                                                                                                     'voz, '
                                                                                                                                                     'a '
                                                                                                                                                     'resposta, '
                                                                                                                                                     'a '
                                                                                                                                                     'transcrição '
                                                                                                                                                     'e '
                                                                                                                                                     'as '
                                                                                                                                                     'ferramentas. '
                                                                                                                                                     'A '
                                                                                                                                                     'opção '
                                                                                                                                                     'mais '
                                                                                                                                                     'rápida '
                                                                                                                                                     '— '
                                                                                                                                                     'cerca '
                                                                                                                                                     'de '
                                                                                                                                                     'meio '
                                                                                                                                                     'segundo '
                                                                                                                                                     'até '
                                                                                                                                                     'a '
                                                                                                                                                     'primeira '
                                                                                                                                                     'palavra.',
 'Only {v0} is missing — it will run, but you will type instead of speak, or read instead of listen.': 'Falta '
                                                                                                       'apenas '
                                                                                                       '{v0} '
                                                                                                       '— '
                                                                                                       'funcionará, '
                                                                                                       'mas '
                                                                                                       'você '
                                                                                                       'digitará '
                                                                                                       'em '
                                                                                                       'vez '
                                                                                                       'de '
                                                                                                       'falar '
                                                                                                       'ou '
                                                                                                       'lerá '
                                                                                                       'em '
                                                                                                       'vez '
                                                                                                       'de '
                                                                                                       'ouvir.',
 'Or enter manually:': 'Ou digite manualmente:',
 'PICTURE': 'IMAGEM',
 'PLANNING': 'PLANEJANDO',
 'PLATFORM': 'PLATAFORMA',
 'PROCESSES': 'PROCESSOS',
 'PROCESSING': 'PROCESSANDO',
 'PROTOCOL · {protocol}': 'PROTOCOLO · {protocol}',
 'Personal AI Assistant': 'Assistente pessoal de IA',
 'Phone connected — JARVIS ready': 'Celular conectado — JARVIS pronto',
 "Pick MY OWN SETUP above to run it on your own machine, or through another company's model.": 'Escolha '
                                                                                               'MINHA '
                                                                                               'CONFIGURAÇÃO '
                                                                                               'acima '
                                                                                               'para '
                                                                                               'executar '
                                                                                               'no '
                                                                                               'seu '
                                                                                               'computador '
                                                                                               'ou '
                                                                                               'com '
                                                                                               'um '
                                                                                               'modelo '
                                                                                               'de '
                                                                                               'outra '
                                                                                               'empresa.',
 'Playing a tone…': 'Reproduzindo um tom…',
 'QUEUED': 'NA FILA',
 'QUIZ': 'QUESTIONÁRIO',
 'QUIZ: {v0} — {v1}/{v2} correct': 'QUIZ: {v0} — {v1}/{v2} corretas',
 'READING': 'LENDO',
 'READY': 'PRONTO',
 'RELEASE TO LOAD': 'SOLTE PARA CARREGAR',
 'REQUEST': 'PEDIDO',
 'ROUTINE': 'ROTINA',
 'ROUTINES': 'ROTINAS',
 "Reading a document, looking at your screen, writing code — the assistant's own requests, not the conversation. These use Gemini's text quota, which runs out before the voice does. Sending them somewhere else keeps them working, and changes nothing you hear.": 'Ler '
                                                                                                                                                                                                                                                                      'documentos, '
                                                                                                                                                                                                                                                                      'ver '
                                                                                                                                                                                                                                                                      'a '
                                                                                                                                                                                                                                                                      'tela, '
                                                                                                                                                                                                                                                                      'escrever '
                                                                                                                                                                                                                                                                      'código '
                                                                                                                                                                                                                                                                      '— '
                                                                                                                                                                                                                                                                      'solicitações '
                                                                                                                                                                                                                                                                      'do '
                                                                                                                                                                                                                                                                      'assistente, '
                                                                                                                                                                                                                                                                      'além '
                                                                                                                                                                                                                                                                      'da '
                                                                                                                                                                                                                                                                      'conversa. '
                                                                                                                                                                                                                                                                      'Usam '
                                                                                                                                                                                                                                                                      'a '
                                                                                                                                                                                                                                                                      'cota '
                                                                                                                                                                                                                                                                      'de '
                                                                                                                                                                                                                                                                      'texto '
                                                                                                                                                                                                                                                                      'do '
                                                                                                                                                                                                                                                                      'Gemini, '
                                                                                                                                                                                                                                                                      'que '
                                                                                                                                                                                                                                                                      'acaba '
                                                                                                                                                                                                                                                                      'antes '
                                                                                                                                                                                                                                                                      'da '
                                                                                                                                                                                                                                                                      'de '
                                                                                                                                                                                                                                                                      'voz. '
                                                                                                                                                                                                                                                                      'Usar '
                                                                                                                                                                                                                                                                      'outro '
                                                                                                                                                                                                                                                                      'provedor '
                                                                                                                                                                                                                                                                      'mantém '
                                                                                                                                                                                                                                                                      'essas '
                                                                                                                                                                                                                                                                      'funções '
                                                                                                                                                                                                                                                                      'sem '
                                                                                                                                                                                                                                                                      'alterar '
                                                                                                                                                                                                                                                                      'o '
                                                                                                                                                                                                                                                                      'que '
                                                                                                                                                                                                                                                                      'você '
                                                                                                                                                                                                                                                                      'ouve.',
 'SETUP': 'CONFIGURAÇÃO',
 'SKIPPED': 'IGNORADO',
 'SPEAKERS': 'ALTO-FALANTES',
 'SPEAKERS — what JARVIS talks through': 'ALTO-FALANTES — por onde JARVIS fala',
 'SPEAKING': 'FALANDO',
 'STATUS': 'ESTADO',
 'STEPS — newest first': 'ETAPAS — mais recentes primeiro',
 'STOPPED': 'INTERROMPIDO',
 'SUMMARISE': 'RESUMIR',
 "SYS: '{v0}' could not be shown — this Qt build does not read that image format.": 'SYS: Não foi '
                                                                                    'possível '
                                                                                    "exibir '{v0}' "
                                                                                    '— esta versão '
                                                                                    'do Qt não lê '
                                                                                    'esse formato.',
 'SYS: Audio devices updated.': 'SYS: Dispositivos de áudio atualizados.',
 'SYS: Auto-start {v0}.': 'SYS: Inicialização automática {v0}.',
 'SYS: Could not generate remote key.': 'SYS: Não foi possível gerar a chave remota.',
 'SYS: Dashboard not running — remote unavailable.': 'SYS: Painel remoto parado — acesso remoto '
                                                     'indisponível.',
 'SYS: Desktop shortcut created.': 'SYS: Atalho da área de trabalho criado.',
 'SYS: Engine settings saved — reconnecting.': 'SYS: Configuração do motor salva — reconectando.',
 'SYS: HUD switched to the animated face.': 'SYS: HUD alterado para o rosto animado.',
 'SYS: HUD switched to the reactor core.': 'SYS: HUD alterado para o núcleo do reator.',
 'SYS: Identity updated — {v0}': 'SYS: Identidade atualizada — {v0}',
 'SYS: Initialised. OS={v0}. {v1} online.': 'SYS: Inicializado. SO={v0}. {v1} conectado.',
 'SYS: Microphone active.': 'SYS: Microfone ativo.',
 'SYS: Microphone muted.': 'SYS: Microfone silenciado.',
 'SYS: Provider settings unavailable: {v0}': 'SYS: Configuração de provedores indisponível: {v0}',
 'SYS: Remote key generated — manual: {v0}': 'SYS: Chave remota gerada — acesso manual: {v0}',
 'SYS: Routine not changed — {v0}': 'SYS: Rotina não alterada — {v0}',
 'SYS: The providers folder is not installed — the assistant runs on Gemini Live.': 'SYS: A pasta '
                                                                                    'providers não '
                                                                                    'está '
                                                                                    'instalada — o '
                                                                                    'assistente '
                                                                                    'usa Gemini '
                                                                                    'Live.',
 'SYS: The video could not be played{v0}.': 'SYS: Não foi possível reproduzir o vídeo{v0}.',
 'SYS: UI colour applied — {v0}': 'SYS: Cor da interface aplicada — {v0}',
 'SYS: Video playback is not available in this Qt install.': 'SYS: A reprodução de vídeo não está '
                                                             'disponível nesta instalação do Qt.',
 'SYS: Voice set — {v0}': 'SYS: Voz definida — {v0}',
 'SYSTEMS': 'SISTEMAS',
 'Same as background requests': 'Igual às solicitações em segundo plano',
 'Same as conversation': 'Igual à conversa',
 'Saved ✓': 'Salvo ✓',
 'Says': 'Diz',
 'Scan with phone camera to connect instantly': 'Leia com a câmera do celular para conectar',
 'Send  [Enter]': 'Enviar  [Enter]',
 'Setup — things you set once': 'Configuração — preferências iniciais',
 'Speak now…': 'Fale agora…',
 'State: {state}{quiet} · ran {runs} times': 'Estado: {state}{quiet} · executada {runs} vezes',
 'Stop the assistant mid-sentence  [ESC]': 'Interromper a fala do assistente  [ESC]',
 'System default': 'Padrão do sistema',
 'TASKS': 'TAREFAS',
 'TEMP': 'TEMP.',
 'TEST': 'TESTAR',
 'TESTING': 'TESTANDO',
 'THINKING': 'RACIOCINANDO',
 'TRANSLATE': 'TRADUZIR',
 'Testing…': 'Testando…',
 'The document does not settle:': 'O documento não esclarece:',
 'The model that plans, writes and fixes projects when you ask the assistant to build something. Saved to Desktop/JarvisProjects.': 'O '
                                                                                                                                    'modelo '
                                                                                                                                    'que '
                                                                                                                                    'planeja, '
                                                                                                                                    'escreve '
                                                                                                                                    'e '
                                                                                                                                    'corrige '
                                                                                                                                    'projetos '
                                                                                                                                    'quando '
                                                                                                                                    'você '
                                                                                                                                    'pede '
                                                                                                                                    'ao '
                                                                                                                                    'assistente '
                                                                                                                                    'para '
                                                                                                                                    'criar '
                                                                                                                                    'algo. '
                                                                                                                                    'Salvos '
                                                                                                                                    'em '
                                                                                                                                    'Desktop/JarvisProjects.',
 'Try Gemini first  —  faster': 'Tentar Gemini primeiro  —  mais rápido',
 'Try the other one first  —  keeps more on your machine': 'Tentar o outro primeiro  —  mantém '
                                                           'mais dados no computador',
 'Type a command or question…': 'Digite um comando ou pergunta…',
 'UI COLOUR  —  drag the handle': 'COR DA INTERFACE  —  arraste o controle',
 'UPTIME': 'TEMPO ATIVO',
 'Uses the model you chose for ② THINKING.': 'Usa o modelo escolhido em ② RACIOCÍNIO.',
 'Uses the settings under BACKGROUND REQUESTS.': 'Usa as opções de SOLICITAÇÕES EM SEGUNDO PLANO.',
 'VIDEO': 'VÍDEO',
 'VOICE': 'VOZ',
 'VOICE INTERFACE': 'INTERFACE DE VOZ',
 'WAIT': 'AGUARDE',
 'WAITING': 'AGUARDANDO',
 'WRITING': 'ESCREVENDO',
 'When: {when}': 'Quando: {when}',
 'YOUR NAME  (leave blank for default sir / efendim)': 'SEU NOME  (em branco: sir / efendim)',
 'Your choice of hearing, thinking and speaking. Can run entirely on this computer, with nothing leaving it. Slower: 1.5 to 4 seconds.': 'Escolha '
                                                                                                                                         'reconhecimento '
                                                                                                                                         'de '
                                                                                                                                         'voz, '
                                                                                                                                         'raciocínio '
                                                                                                                                         'e '
                                                                                                                                         'fala. '
                                                                                                                                         'Pode '
                                                                                                                                         'funcionar '
                                                                                                                                         'só '
                                                                                                                                         'neste '
                                                                                                                                         'computador, '
                                                                                                                                         'sem '
                                                                                                                                         'enviar '
                                                                                                                                         'dados. '
                                                                                                                                         'Mais '
                                                                                                                                         'lento: '
                                                                                                                                         '1,5 '
                                                                                                                                         'a '
                                                                                                                                         '4 '
                                                                                                                                         'segundos.',
 'checking…': 'verificando…',
 'disabled': 'desativada',
 'e.g.  Tony   (leave blank for auto)': 'ex.: Tony   (em branco: automático)',
 'enabled': 'ativada',
 'installing {package} — this can take a minute…': 'instalando {package} — pode levar um minuto…',
 'new ': 'novo ',
 'next {time} · {description}': 'próxima {time} · {description}',
 'no': 'não',
 'off': 'desligada',
 'on': 'ligada',
 'pip failed': 'falha no pip',
 'reading…': 'carregando…',
 'reads the answer out loud': 'lê a resposta em voz alta',
 'turns what you say into words': 'transforma sua fala em palavras',
 'understands, decides, uses your tools': 'compreende, decide e usa suas ferramentas',
 'yes': 'sim',
 'your answer': 'sua resposta',
 '{count} model(s) found on this server — pick one above.': '{count} modelo(s) encontrados neste '
                                                            'servidor — escolha acima.',
 '{mark}  Code with {name}{star}': '{mark}  Programar com {name}{star}',
 '{mark}  Fall back to {name}': '{mark}  Usar {name} como alternativa',
 '{name}  (not connected)': '{name}  (desconectado)',
 '{v0}   (optional)': '{v0}   (opcional)',
 '{v0}  {v1}  ·  {v2}  ·  Tell {v3} what to do with it': '{v0}  {v1}  ·  {v2}  ·  Diga a {v3} o '
                                                         'que fazer com ele',
 '{v0}  {v1}  ·  {v2} files  ·  Tell {v3} what to change in it': '{v0}  {v1}  ·  {v2} arquivos  ·  '
                                                                 'Diga a {v3} o que alterar',
 '{v0}  ·  PERSONAL AI SYSTEM': '{v0}  ·  SISTEMA PESSOAL DE IA',
 '{v0} ACTIVE': '{v0} ATIVAS',
 '{v0} ON': '{v0} LIGADAS',
 '{v0} stored facts — newest first. Nothing here is sent anywhere; it lives in memory/long_term.json on this machine.': '{v0} '
                                                                                                                        'informações '
                                                                                                                        'salvas '
                                                                                                                        '— '
                                                                                                                        'mais '
                                                                                                                        'recentes '
                                                                                                                        'primeiro. '
                                                                                                                        'Nada '
                                                                                                                        'é '
                                                                                                                        'enviado; '
                                                                                                                        'os '
                                                                                                                        'dados '
                                                                                                                        'ficam '
                                                                                                                        'em '
                                                                                                                        'memory/long_term.json '
                                                                                                                        'neste '
                                                                                                                        'computador.',
 '— default —': '— padrão —',
 '— not set —': '— não configurado —',
 "…  noted — I'll go over this one with you": '…  anotado — vou analisar esta resposta com você',
 '↻ REFRESH': '↻ ATUALIZAR',
 '⊞  CREATE DESKTOP SHORTCUT': '⊞  CRIAR ATALHO',
 '⌃ LESS': '⌃ MENOS',
 '⌄ MORE': '⌄ MAIS',
 '▶  VIDEO': '▶  VÍDEO',
 '▸  APPLY': '▸  APLICAR',
 '▸  APPLY CHANGES': '▸  APLICAR ALTERAÇÕES',
 '▸  CONFIRM': '▸  CONFIRMAR',
 '▸  INITIALISE SYSTEMS': '▸  INICIALIZAR SISTEMAS',
 '▸  SAVE': '▸  SALVAR',
 '▸  SAVE  &&  APPLY': '▸  SALVAR  E  APLICAR',
 '◈  CAMERA FEED': '◈  CÂMERA',
 '◈  CLIPBOARD DETECTED': '◈  ÁREA DE TRANSFERÊNCIA',
 '◈  INITIALISATION REQUIRED': '◈  INICIALIZAÇÃO NECESSÁRIA',
 '◈  REMOTE ACCESS': '◈  ACESSO REMOTO',
 '◈  VISUAL INPUT': '◈  ENTRADA VISUAL',
 '◉  AUTO-START: OFF': '◉  INICIAR COM WINDOWS: NÃO',
 '◉  AUTO-START: ON': '◉  INICIAR COM WINDOWS: SIM',
 '◉  HUD: REACTOR CORE': '◉  HUD: NÚCLEO DO REATOR',
 '◉  REMOTE CONTROL': '◉  CONTROLE REMOTO',
 '☀  MORNING BRIEF: OFF': '☀  RESUMO MATINAL: NÃO',
 '☀  MORNING BRIEF: ON': '☀  RESUMO MATINAL: SIM',
 '⚙  CUSTOMISE ASSISTANT': '⚙  PERSONALIZAR ASSISTENTE',
 '⚙  PLUGIN SETTINGS': '⚙  CONFIGURAR PLUGINS',
 '⚠  CONFIRM': '⚠  CONFIRMAÇÃO',
 '⚠  Windows is blocking incoming connections to this copy of Python, so your phone cannot reach this page. Restart JARVIS and accept the Windows prompt, or remove the rules named ': '⚠  '
                                                                                                                                                                                       'O '
                                                                                                                                                                                       'Windows '
                                                                                                                                                                                       'bloqueia '
                                                                                                                                                                                       'conexões '
                                                                                                                                                                                       'de '
                                                                                                                                                                                       'entrada '
                                                                                                                                                                                       'deste '
                                                                                                                                                                                       'Python, '
                                                                                                                                                                                       'impedindo '
                                                                                                                                                                                       'o '
                                                                                                                                                                                       'acesso '
                                                                                                                                                                                       'pelo '
                                                                                                                                                                                       'celular. '
                                                                                                                                                                                       'Reinicie '
                                                                                                                                                                                       'JARVIS '
                                                                                                                                                                                       'e '
                                                                                                                                                                                       'aceite '
                                                                                                                                                                                       'a '
                                                                                                                                                                                       'solicitação '
                                                                                                                                                                                       'do '
                                                                                                                                                                                       'Windows '
                                                                                                                                                                                       'ou '
                                                                                                                                                                                       'remova '
                                                                                                                                                                                       'as '
                                                                                                                                                                                       'regras '
                                                                                                                                                                                       'chamadas ',
 '⚠  ② THINKING is not set — without it the assistant falls back to Gemini Live and says so in the log.': '⚠  '
                                                                                                          '② '
                                                                                                          'RACIOCÍNIO '
                                                                                                          'não '
                                                                                                          'configurado '
                                                                                                          '— '
                                                                                                          'o '
                                                                                                          'assistente '
                                                                                                          'usará '
                                                                                                          'Gemini '
                                                                                                          'Live '
                                                                                                          'e '
                                                                                                          'avisará '
                                                                                                          'no '
                                                                                                          'registro.',
 '⚡  BACKGROUND REQUESTS': '⚡  SOLICITAÇÕES EM SEGUNDO PLANO',
 '⛶  FULLSCREEN  [F11]': '⛶  TELA CHEIA  [F11]',
 '✓  correct': '✓  correto',
 '✓  installed — close and reopen this panel': '✓  instalado — feche e reabra este painel',
 '✓  {count} available — pick one above.': '✓  {count} disponíveis — escolha acima.',
 '✓  {count} available: {items}': '✓  {count} disponíveis: {items}',
 '✓  {count} found.': '✓  {count} encontrados.',
 '✕  CLOSE': '✕  FECHAR',
 '⬇  DOWNLOADING… (one-time)': '⬇  BAIXANDO… (uma vez)',
 '⬇  WAKE WORD: DOWNLOAD': '⬇  PALAVRA DE ATIVAÇÃO: BAIXAR',
 '🎙  WAKE WORD': '🎙  PALAVRA DE ATIVAÇÃO',
 '🎙  WAKE WORD: OFF': '🎙  ATIVAÇÃO POR VOZ: NÃO',
 '🎙  WAKE WORD: ON': '🎙  ATIVAÇÃO POR VOZ: SIM',
 '🎚  PUSH-TO-TALK: OFF': '🎚  PRESSIONAR PARA FALAR: NÃO',
 '🎚  PUSH-TO-TALK: {v0}': '🎚  PRESSIONAR PARA FALAR: {v0}',
 '🎧  AUDIO DEVICES': '🎧  DISPOSITIVOS DE ÁUDIO',
 '👂  WAKE NOW': '👂  ATIVAR AGORA',
 '📁  Choose a folder…  (for coding)': '📁  Escolher pasta…  (para programar)',
 '📄  Choose a file…': '📄  Escolher arquivo…',
 '🔇  SOUND OFF': '🔇  SOM DESLIGADO',
 '🔊  SOUND ON': '🔊  SOM LIGADO',
 '🔌  ENGINE  &  PROVIDERS': '🔌  MOTOR  E  PROVEDORES',
 '🔌  ENGINE && PROVIDERS': '🔌  MOTOR E PROVEDORES',
 '🖥  MY OWN SETUP': '🖥  MINHA CONFIGURAÇÃO',
 '😴  SLEEP NOW': '😴  DORMIR AGORA',
 '🛠  CODING': '🛠  PROGRAMAÇÃO',
 '🧑  HUD: ANIMATED FACE': '🧑  HUD: ROSTO ANIMADO',
 '🧠  MEMORY': '🧠  MEMÓRIA',
 '🧠  WHAT JARVIS REMEMBERS': '🧠  O QUE JARVIS LEMBRA',
 '🧩  PLUGIN MANAGER': '🧩  GERENCIAR PLUGINS',
 '🧩  PLUGINS': '🧩  PLUGINS'}


def normalize_language(value):
    return value if isinstance(value, str) and value in ("en", "pt-BR") else "en"


def get_language():
    return _language


def watch_language(callback):
    """Keep no window alive solely for language notifications."""
    _listeners.append(weakref.WeakMethod(callback))


def join_messages(separator, values):
    result = tr("")
    for index, value in enumerate(values):
        if index:
            result = result + separator
        result = result + value
    return result


class Text(str):
    def __new__(cls, source, values=None, uppercase=False):
        values = dict(values or {})
        obj = super().__new__(cls, _format(source, values, uppercase))
        obj.source, obj.values, obj.uppercase = source, values, uppercase
        return obj

    def upper(self):
        return Text(self.source, self.values, True)

    def __add__(self, other):
        return Text("{left}{right}", {"left": self, "right": other})

    def __radd__(self, other):
        return Text("{left}{right}", {"left": other, "right": self})


def _format(source, values, uppercase=False):
    template = PT_BR.get(source, source) if _language == "pt-BR" else source
    resolved = {key: render(value) if isinstance(value, Text) else value
                for key, value in values.items()}
    try:
        result = template.format(**resolved)
    except (KeyError, ValueError, IndexError, TypeError):
        try:
            result = source.format(**resolved)
        except (KeyError, ValueError, IndexError, TypeError):
            result = source
    return result.upper() if uppercase else result


def tr(source, **values):
    return Text(source, values)


def render(value):
    return _format(value.source, value.values, value.uppercase) if isinstance(value, Text) else value


def _remember(widget, key, value):
    bindings = _bindings.setdefault(widget, {})
    if isinstance(value, Text):
        bindings[key] = value
    else:
        bindings.pop(key, None)


def set_language(value):
    """Apply on the Qt main thread. Never persist or reconnect a voice session."""
    global _language
    from PyQt6.QtCore import QThread
    from PyQt6.QtWidgets import QApplication
    app = QApplication.instance()
    if app is not None and QThread.currentThread() != app.thread():
        raise RuntimeError("UI language must be changed on the Qt main thread")
    _language = normalize_language(value)
    for widget, bindings in list(_bindings.items()):
        for (method, index), message in list(bindings.items()):
            try:
                if method == "item":
                    blocked = widget.blockSignals(True)
                    try:
                        typed = widget.currentText() if widget.isEditable() else None
                        custom = (typed is not None and
                                  typed != widget.itemText(widget.currentIndex()))
                        widget.setItemText(index, render(message))
                        if custom:
                            widget.setEditText(typed)
                    finally:
                        widget.blockSignals(blocked)
                else:
                    # Bypass the binding setter so the original source survives.
                    getattr(super(_Localized, widget), method)(render(message))
            except RuntimeError:
                # Qt may have deleted the C++ object before Python's wrapper.
                _bindings.pop(widget, None)
                break
    if app is not None:
        for reference in list(_listeners):
            callback = reference()
            if callback is None:
                _listeners.remove(reference)
            else:
                callback()
        for widget in app.allWidgets():
            widget.update()  # Repaint explicitly tagged canvas text, no text scan.


def catalog_errors():
    formatter = string.Formatter()
    errors = []
    for source, translated in PT_BR.items():
        try:
            fields = lambda text: sorted((name, spec, conv) for _, name, spec, conv
                                         in formatter.parse(text) if name is not None)
            if fields(source) != fields(translated):
                errors.append(source)
        except ValueError:
            errors.append(source)
    return errors


# These aliases are imported only by GUI modules, never globally monkeypatched.
from PyQt6 import QtWidgets as _qt


class _Localized:
    def setAccessibleName(self, value):
        _remember(self, ("setAccessibleName", None), value)
        return super().setAccessibleName(render(value))

    def setText(self, value):
        _remember(self, ("setText", None), value)
        return super().setText(render(value))

    def setToolTip(self, value):
        _remember(self, ("setToolTip", None), value)
        return super().setToolTip(render(value))

    def setPlaceholderText(self, value):
        _remember(self, ("setPlaceholderText", None), value)
        return super().setPlaceholderText(render(value))


class QLabel(_Localized, _qt.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if args and isinstance(args[0], Text):
            self.setText(args[0])


class QPushButton(_Localized, _qt.QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if args and isinstance(args[0], Text):
            self.setText(args[0])


class QLineEdit(_Localized, _qt.QLineEdit):
    pass


class QComboBox(_Localized, _qt.QComboBox):
    def message_at(self, index):
        return _bindings.get(self, {}).get(("item", index), self.itemText(index))

    def addItem(self, text, *args):
        index = self.count()
        super().addItem(render(text), *args)
        _remember(self, ("item", index), text)

    def insertItem(self, index, text, *args):
        index = max(0, min(index, self.count()))
        bindings = _bindings.setdefault(self, {})
        for key in sorted(list(bindings), key=lambda key: key[1] or -1, reverse=True):
            if key[0] == "item" and key[1] >= index:
                bindings[("item", key[1] + 1)] = bindings.pop(key)
        super().insertItem(index, render(text), *args)
        _remember(self, ("item", index), text)

    def removeItem(self, index):
        if index < 0 or index >= self.count():
            return super().removeItem(index)
        bindings = _bindings.setdefault(self, {})
        bindings.pop(("item", index), None)
        for key in sorted(list(bindings), key=lambda key: key[1] or -1):
            if key[0] == "item" and key[1] > index:
                bindings[("item", key[1] - 1)] = bindings.pop(key)
        super().removeItem(index)

    def clear(self):
        bindings = _bindings.get(self, {})
        for key in list(bindings):
            if key[0] == "item":
                bindings.pop(key)
        super().clear()
