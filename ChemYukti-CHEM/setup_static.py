"""
Run this once to copy the ChemYukti logo to the static folder:
    python setup_static.py
"""
import shutil, os

src = os.path.join(os.path.dirname(__file__), "chemyukti logo.png")
dst = os.path.join(os.path.dirname(__file__), "app", "static", "img", "chemyukti-logo.png")
os.makedirs(os.path.dirname(dst), exist_ok=True)
shutil.copy2(src, dst)
print(f"Copied logo to {dst}")
