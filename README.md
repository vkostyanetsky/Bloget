# Bloget 💬 📃 📢 
 
[![pylint](https://github.com/vkostyanetsky/BlogBuilder/actions/workflows/pylint.yml/badge.svg)](https://github.com/vkostyanetsky/BlogBuilder/actions/workflows/pylint.yml) [![black](https://github.com/vkostyanetsky/BlogBuilder/actions/workflows/black.yml/badge.svg)](https://github.com/vkostyanetsky/BlogBuilder/actions/workflows/black.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This script generates static files for my [Russian](https://kostyanetsky.ru) and [English](https://kostyanetsky.me) blogs. Since I made it for personal use, I didn't write detailed usage instructions.

If you have any questions, feel free to contact me or [open an issue](https://github.com/vkostyanetsky/Bloget/issues/new).

## 🙂 How to use?

To build a blog from `C:\Blogs\ru` and start a web-server to test the result: 

```
cd C:\Blogs\ru
bloget build --url=http://localhost:8085 --output=C:\Blogs\test --assets=C:\Blogs\assets --templates=C:\Blogs\templates --webserver
```

To push changes in `C:\Blogs\ru` to GitHub: 

```
cd C:\Blogs\ru
git add .
git commit -m "Content update"
git push
```