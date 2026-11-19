from pathlib import Path
import ast
p=Path('gui/providers_panel.py');s=p.read_bytes().decode('utf-8').replace('\r\n','\n')
s=s.replace('        b.setMinimumHeight(84)','        b.setMinimumHeight(126)')
s=s.replace("        b.setText(tr('{v0}\\n\\n{v1}', v0=title, v1=body))", '''        b.setAccessibleName(title)
        content = QVBoxLayout(b)
        content.setContentsMargins(12, 10, 12, 10)
        content.setSpacing(6)
        for message, colour in ((title, C.TEXT), (body, C.TEXT_DIM)):
            label = QLabel(message, b)
            label.setFont(hud_font(7))
            label.setWordWrap(True)
            label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            label.setStyleSheet(f"color: {colour}; background: transparent;")
            content.addWidget(label)
        content.addStretch()''')
ast.parse(s);p.write_bytes(s.replace('\n','\r\n').encode('utf-8'))