# Source for the GitHub Pages site

Edit the markdown here. Do not edit the generated `.html` files.

| Source | Page |
|---|---|
| `experiment.md` | `../index.html` |
| `rft-dataset.md` | `../rft-dataset.html` |
| `hardware.md` | `../compute.html` |

Rebuild:

```bash
pip install markdown
python3 docs/build.py
```

The build writes the `.html` files next to `docs/build.py` and adds `.nojekyll`,
so GitHub Pages serves the files without Jekyll. The pages load no external
scripts, stylesheets or fonts.
