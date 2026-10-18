# MATH 285 — The Exponential Map

英文 PreTeXt 教材稿，依据同目录 Lecture 8 与 9 整理。三章依次介绍指数映射与局部坐标、群同态与 Lie 子群、矩阵指数与应用。包含完整证明、交叉引用、补充例题和六道附提示或答案的练习。

## 在 VS Code 中编辑和实时预览

1. 用 **File → Open Folder** 打开这个 `math285-pretext` 文件夹。
2. 安装推荐扩展 **PreTeXt-tools** (`oscarlevin.pretext-tools`)。
3. 编辑 `source/main.ptx` 或三个章节文件。通过命令面板搜索 **PreTeXt**，选择扩展的 **Instant Preview / Live Preview**。可用 **PreTeXt: Live Preview: Choose Scope** 切换当前文件和整个项目。预览命令名称会随扩展版本调整。
4. 实时预览适合写作；正式网页请按下面的构建流程生成。

官方扩展：https://marketplace.visualstudio.com/items?itemName=oscarlevin.pretext-tools

## 正式构建（macOS / Linux）

首次在项目终端执行：

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pretext build web
pretext view web
```

已经附带本次实际构建的 `output/web/`。正式预览应使用 `pretext view web` 提供的本地网址；不要依赖直接双击 HTML 文件。

以后在 VS Code 按 **Cmd+Shift+B** 构建网页，或运行任务 **PreTeXt: View web**。构建任务使用项目自己的 `.venv`，因此需先完成上述首次安装。扩展如找不到命令，请在已激活 `.venv` 的终端运行命令。

```sh
pretext build latex   # 导出排版用 LaTeX
pretext build print   # 生成 PDF；另需安装 TeX Live / MacTeX
```

本次已验证 XML schema、网页和 LaTeX 导出；没有验证 PDF 编译。Python 依赖固定为本次通过验证的组合，避免新版本依赖不兼容。

## 文件说明

- `source/main.ptx`：书名、前言、章节引用和参考文献。
- `source/01-flows-and-coordinates.ptx`：Lecture 8 主体。
- `source/02-homomorphisms-and-subgroups.ptx`：Lecture 9 的自然性、子群判别与唯一性。
- `source/03-matrix-exponentials.ptx`：Lecture 9 的矩阵指数、表示与经典矩阵群，以及补充练习。
- `publication/publication.ptx`：出版配置。
- `project.ptx`：网页、PDF、LaTeX 构建目标。
- `EDITORIAL.md`：来源映射、数学修订和发布前待补事项。

发布网页时，部署正式构建出的 `output/web/` 全部内容到静态网站托管服务即可。当前项目未上传或公开发布。

官方指南：https://pretextbook.org/doc/guide/html/tutorial-first-document.html

## 保存后自动编译与刷新

运行 VS Code 任务 **PreTeXt: Auto compile and preview**，保持任务运行。右侧 Simple Browser 打开 `http://127.0.0.1:8766/construction.html`。源文件会在停止输入约 1.2 秒后自动保存，后台随后编译，成功后预览自动刷新并尽量保留滚动位置。编译错误显示在 `.preview/build.log`。

项目重新打开时，若 VS Code 询问是否允许运行自动任务，选择允许即可。也可手动通过 Terminal → Run Task 启动该任务。

## 公开网站与更新

网站：https://swang0456.github.io/lie-groups/

本地编辑后，在 VS Code Source Control 中填写修改说明、Commit，再 Sync Changes。推送到 main 后，GitHub Actions 自动编译并发布，运行记录在仓库 Actions 页面。网页只在构建成功后发布。

本地自动保存只更新本机预览，公开网站在同步后更新。
