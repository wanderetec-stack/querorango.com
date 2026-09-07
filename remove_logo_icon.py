import os, re

base = r'c:\Users\Wander - Rosangela\Desktop\site de receitas'
count = 0

# Regex para remover o span com o icone
pattern_icon = re.compile(r'<span class=\"nav-logo-icon\">.*?</span>\s*', re.DOTALL)
pattern_footer_emoji = re.compile(r'<div class=\"footer-logo\">\s*🍊\s*', re.DOTALL)
pattern_title_emoji = re.compile(r'Quero Rango\s*🍊\s*\|', re.DOTALL)

for root, dirs, files in os.walk(base):
    if '.git' in root or 'node_modules' in root: continue
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                content = fp.read()
            
            new_content = content
            new_content = pattern_icon.sub('', new_content)
            new_content = pattern_footer_emoji.sub('<div class=\"footer-logo\">', new_content)
            new_content = pattern_title_emoji.sub('Quero Rango |', new_content)
            # Caso tenha sobrado algum emoji direto no logo
            new_content = new_content.replace('🍊 Quero Rango', 'Quero Rango')
            new_content = new_content.replace('🍊Quero Rango', 'Quero Rango')
            
            if new_content != content:
                with open(p, 'w', encoding='utf-8') as fp:
                    fp.write(new_content)
                count += 1

print(f'HTMLs limpos (removido icone do logo): {count}')
