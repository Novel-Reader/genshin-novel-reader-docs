# Genshin-novel-reader-doc

原神小说阅读器的每个组件在 Github 上有独立的源代码库

- 小说阅读器（javascript 版本）：https://github.com/Novel-Reader/Genshin-novel-reader
- 小说服务器：https://github.com/Novel-Reader/Genshin-novel-reader-express-server
- 小说阅读器（typescript 版）：https://github.com/Novel-Reader/novel-reader-ts
- 文档源代码：https://github.com/Novel-Reader/Genshin-novel-reader-doc
- 文档编译后代码：https://github.com/Novel-Reader/Novel-Reader.github.io

## 版本说明

1.0 版本之前，服务器代码和阅读器代码都保存在一个存储库中，即 https://github.com/Novel-Reader/Genshin-novel-reader

1.0 之后，实现了前后端代码分离：

前端代码 https://github.com/Novel-Reader/Genshin-novel-reader

后端代码 https://github.com/Novel-Reader/Genshin-novel-reader-express-server

同时支持了前端 typescript 版本 https://github.com/Novel-Reader/novel-reader-ts

## 工具脚本

所有脚本均从仓库根目录运行。安装项目 Python 依赖：

```bash
pip install -r requirements.txt
```

### Markdown 格式化

`tools/format-markdown.py` 使用 mdformat 格式化 Markdown，默认处理 `README.md` 和 `docs/` 下的所有 Markdown 文件：

```bash
python3 tools/format-markdown.py
```

可指定文件或目录；添加 `--check` 只检查格式，不修改文件：

```bash
python3 tools/format-markdown.py docs/v2/5.3-change-log.md
python3 tools/format-markdown.py --check
```

### 图片重命名

`tools/rename-image.py` 将指定目录中至少包含两个下划线的文件，重命名为首尾下划线之间的文字并添加 `.png` 后缀。缺少下划线的文件会跳过；如果目标文件名冲突，脚本会报错且不执行重命名。

```bash
python3 tools/rename-image.py docs/screenshots
```

### 图片压缩

`tools/compress-image.py` 使用 OpenCV 压缩图片。当前脚本固定读取运行目录中的 `test.png`，并输出 `new_test.png`，目标大小为 100 KB；如需处理其他文件或调整目标大小，请修改脚本中的 `main()` 调用。

```bash
python3 tools/compress-image.py
```
