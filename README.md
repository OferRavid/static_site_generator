# Static Site Generator

A simple and modular static site generator built in Python and shell scripting. This project was created as part of the Boot.dev curriculum and demonstrates core concepts of file I/O, templating, process automation, and lightweight server deployment.

## Features

- Converts markdown-like content into static HTML pages
- Templating support for reusable layouts
- Shell scripts for building and testing the site
- Python development server for local previews
- Minimal dependencies, portable across environments

## Project Structure

- `content/` – Source files for pages
- `static/` – Static assets (CSS, images)
- `template.html` – HTML base template
- `src/` – Generator logic
- `build.sh` – Script to generate the static site
- `server.py` – Local dev server
- `test.sh` – Testing script to validate output

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/OferRavid/static_site_generator.git
   cd static_site_generator
   ```
2. Build the site:
   ```bash
   ./build.sh
   ```
3. Start the local server:
   ```bash
   python3 server.py
   ```
4. Visit http://localhost:8000 in your browser to view the generated site.

License
This project is licensed under the MIT License.   

---
   
Created by Ofer Ravid
