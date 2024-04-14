# Bloget 💬 📃 📢 
 
[![pylint](https://github.com/vkostyanetsky/BlogBuilder/actions/workflows/pylint.yml/badge.svg)](https://github.com/vkostyanetsky/BlogBuilder/actions/workflows/pylint.yml) [![black](https://github.com/vkostyanetsky/BlogBuilder/actions/workflows/black.yml/badge.svg)](https://github.com/vkostyanetsky/BlogBuilder/actions/workflows/black.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This script generates static files for my blogs in [Russian](https://kostyanetsky.ru) and [English](https://kostyanetsky.me). I expect no interest in it since I made it for personal purposes, so there are no detailed instructions on how to use it. 

If you have any questions, feel free to contact me or [open an issue](https://github.com/vkostyanetsky/Bloget/issues/new).

# 🙂 How to use?

To build a blog from `C:\Blogs\ru` and start a web-server to test the result: 

```
cd C:\Blogs\ru
bloget build --output=C:\Blogs\test --skin=C:\Blogs\skin --url=http://localhost:8085 --webserver
```

To push changes in `C:\Blogs\ru` to GitHub: 

```
cd C:\Blogs\ru
git add .
git commit -m "Content update"
git push
```