from pathlib import Path

# Compute local path to serve
serve_path = str(Path(__file__).with_name("serve").resolve())

# Serve directory for JS/CSS files
serve = {"__cdao": serve_path}

# List of JS files to load (usually from the serve path above)
scripts = ["__cdao/cdao.umd.js"]

# List of CSS files to load (usually from the serve path above)
# styles = ["__cdao/style.css"]

# List of Vue plugins to install/load
vue_use = ["cdao"]
