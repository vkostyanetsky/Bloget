# Bloget 💬 📃 📢 
 
[![pylint](https://github.com/vkostyanetsky/BlogBuilder/actions/workflows/pylint.yml/badge.svg)](https://github.com/vkostyanetsky/BlogBuilder/actions/workflows/pylint.yml) [![black](https://github.com/vkostyanetsky/BlogBuilder/actions/workflows/black.yml/badge.svg)](https://github.com/vkostyanetsky/BlogBuilder/actions/workflows/black.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This script generates static files for my [Russian](https://kostyanetsky.ru) and [English](https://kostyanetsky.me) blogs. Since I made it for personal use, I didn't write detailed usage instructions.

If you have any questions, feel free to contact me or [open an issue](https://github.com/vkostyanetsky/Bloget/issues/new).

## 🙂 How to use?

Clone the repo first.

### Build Tailwind CSS

From the repository root:

```bash
npm install
npm run tailwind:build
```

> [!tip]
> You can run `npm run tailwind:watch` while developing.

### Build the blog and run a local web server

Assume:
- Bloget repo: C:\Blog\Bloget
- Input content: C:\Blog\Input
- Output folder: C:\Blog\Output

Run:

```bash
cd C:\Blog\Input
bloget build `
    --url=http://localhost:8085 `
    --output=C:\Blog\Output `
    --public=C:\Blog\Bloget\public `
    --templates=C:\Blog\Bloget\templates `
    --webserver
```
