import os, glob

base = r'c:\Users\Wander - Rosangela\Desktop\site de receitas'
count = 0

old_str1 = '© 2026 Quero Rango (querorango.com) — Todos os direitos reservados.'
new_str1 = '© 2026 Quero Rango (querorango.com) — Todos os direitos reservados. • Desenvolvido por Wander Santos'

old_str2 = '© 2026 Quero Rango'
for root, dirs, files in os.walk(base):
    if '.git' in root or 'node_modules' in root: continue
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                content = fp.read()
            if 'Desenvolvido por Wander Santos' not in content:
                if old_str1 in content:
                    content = content.replace(old_str1, new_str1)
                    with open(p, 'w', encoding='utf-8') as fp:
                        fp.write(content)
                    count += 1

print(f'HTMLs atualizados: {count}')
