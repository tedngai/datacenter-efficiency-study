import re, ast, os
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, "add_rows5.py")
s = open(p, encoding="utf-8").read()
s2 = re.sub(r',("https?://[^"]*")', r',url=\1', s)
open(p, "w", encoding="utf-8").write(s2)
ast.parse(s2)
print("syntax OK")
