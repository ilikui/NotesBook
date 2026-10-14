---
title: "Commit Message Guidelines"
tags:
  - Area
  - KM
---

# Commit Message Guidelines

本仓库提供 Git 提交信息格式的规范和示例，旨在提高提交信息的可读性和项目的可维护性。

## 常见的提交关键词

- **`feat`**：新功能 ： 
  ```plaintext
  feat: 添加用户登录功能
  ```
- **`fix`**：修复 bug
  ```plaintext
  fix: 修复登录页面的错误提示
  ```
- **`docs`**：文档变更
  ```plaintext
  docs: 更新 API 文档
  ```
- **`style`**：代码格式（不影响代码运行的变动）
  ```plaintext
  style: 调整代码格式，删除多余空格
  ```
- **`refactor`**：重构（即不是新增功能，也不是修复 bug 的代码变动）
  ```plaintext
  refactor: 重命名变量以提高代码可读性
  ```
- **`test`**：增加测试
  ```plaintext
  test: 添加用户登录功能的单元测试
  ```
- **`chore`**：构建过程或辅助工具的变动
  ```plaintext
  chore: 更新依赖包版本
  ```
- **`ci`**：持续集成相关配置
  ```plaintext
  ci: 修改 CI 配置文件以支持新的测试框架
  ```
- **`build`**：影响构建系统或外部依赖的更改
  ```plaintext
  build: 修改 webpack 配置文件以优化打包过程
  ```
- **`revert`**：回滚某个更早之前的提交
  ```plaintext
  revert: 回滚提交 1234567
  ```

## 提交信息格式

```plaintext
<type>: <subject>
<body>
```

- **type**：提交类型（如 feat, fix 等）
- **subject**：简要描述变更
- **body**：详细描述变更（可选）

## 示例

1. **性能优化相关的更改**
   ```plaintext
   perf: 优化数据库查询性能
   通过添加索引，减少了查询时间。
   ```

2. **配置文件的修改**
   ```plaintext
   chore: 更新 ESLint 配置
   调整了 ESLint 规则以适应新的代码风格要求。
   ```

3. **代码注释的修改**
   ```plaintext
   docs: 更新函数的注释
   ```

4. **变量名的修改**
   ```plaintext
   refactor: 重命名变量以提高代码可读性
   ```

5. **改变函数的外部行为**
   - 如果是新功能或增强功能：
     ```plaintext
     feat: 修改函数行为以支持新的输入参数
     ```
   - 如果是修复 bug：
     ```plaintext
     fix: 修改函数行为以修复边界条件处理错误
     ```

6. **为 Selenium 驱动的 Chrome 添加设置分辨率的参数**

   ```plaintext
   feat: 为 Selenium 驱动的 Chrome 添加设置分辨率的参数
   通过在启动参数中添加选项，支持在启动 Chrome 时设置窗口分辨率。
   ```

7. **更新项目依赖包**

   ```plaintext
   chore: 更新项目依赖包
   ```

8. **重命名函数以提高代码可读性**

   ```
   refactor: 重命名函数以提高代码可读性
   将 `calculate()` 函数重命名为 `calculateTotalPrice()` 以更好地反映其功能。
   ```

9. **提取重复代码到一个独立的函数**

   ```
   refactor: 提取重复代码到一个独立的函数
   将多处重复的数据库查询逻辑提取到 `queryDatabase()` 函数中。
   ```

10. **重构类结构以实现更好的封装**

   ```
   refactor: 重构类结构以实现更好的封装
   将类 `User` 中的部分方法移到一个新的类 `UserHelper` 中，以提高代码的模块化和可维护性。
   ```

11. **将长函数拆分为多个小函数**

    ```
    refactor: 将长函数拆分为多个小函数
    将 `processOrder()` 函数拆分为 `validateOrder()`, `calculateTotal()`, 和 `saveOrder()` 函数，以提高代码的可读性和复用性。
    ```

12. **移除未使用的代码**

    ```
    refactor: 移除未使用的代码
    移除了 `oldFeature()` 函数及其相关调用，因为该功能已被新的实现取代。
    ```

13. **重构条件判断逻辑**

    ```
    refactor: 重构条件判断逻辑
    将 `processData()` 函数中的复杂嵌套条件重构为多个简单的条件判断，以提高代码的可读性。
    ```

14. **docs**（文档变更）

    ```
    docs: 更新 README 文件
    添加了项目的安装和配置步骤，并修正了一些拼写错误。
    ```

15. **chore**（构建过程或辅助工具的变动）

    ```
    chore: 更新依赖包版本
    将项目中的依赖包版本更新到最新的稳定版本，以确保项目使用最新的库和修复已知的漏洞。
    ```

16. **build**（影响构建系统或外部依赖的更改）

    ```
    build: 修改 webpack 配置
    添加了新的插件以优化打包过程，并调整了输出目录结构。
    ```

---



在 Git 提交信息（Commit Message）中加入表情（Emoji）不仅能让项目的 Commit 历史美观有趣，更重要的是能通过视觉符号快速分类，让人一眼看出每次提交的目的。
目前国际上最通用、最流行的规范是 Gitmoji。

📄 Git 提交的标准结构

结合 Angular 提交规范与 Gitmoji，最推荐的日常提交格式如下：
text
<emoji> <type>(<scope>): <subject>

[body]

[footer]
请谨慎使用此类代码。
• 示例：✨ feat(auth): 增加微信登录功能
• 示例：🐛 fix(cart): 修复购物车商品数量计算错误的 Bug

🎨 常用 Gitmoji 分类速查表

以下是开发中最常用的表情规范，分为四大核心场景：

1. 功能与日常开发

• ✨ :sparkles: 新功能（Introducing new features）
• 🐛 :bug: 修复 Bug（Fixing a bug）
• 📝 :memo: 撰写文档（Writing docs）
• 💄 :lipstick: 更新 UI/样式文件（Updating the UI and style files）
• 🎨 :art: 改进代码结构/代码格式化（Improving structure / format of the code）

2. 性能与重构

• ⚡ :zap: 提升性能（Improving performance）
• ♻️ :recycle: 重构代码（Refactoring code）
• 🔥 :fire: 删除代码或文件（Removing code or files）
• 💥 :boom: 破坏性修改（Introducing breaking changes）

3. 测试与安全

• ✅ :white_check_mark: 增加或通过测试（Adding or passing tests）
• 🔒 :lock: 修复安全问题（Fixing security issues）
• 🚨 :alert: 移除编译器警告（Fixing compiler / linter warnings）

4. 工程与配置

• 🔧 :wrench: 修改配置文件（Changing configuration files）
• 📦 :package: 更新依赖包/发布新版本（Updating dependencies / packaging）
• 🚀 :rocket: 部署项目（Deploying stuff）
• 👷 :construction_worker: CI/CD 构建系统变动（CI build system）

🛠️ 自动化工具推荐（告别手动复制）

如果你觉得每次都要去查或者复制表情很麻烦，可以使用以下工具将其变成半自动化或强制规范：
1. gitmoji-cli (命令行工具)
	• 安装：npm i -g gitmoji-cli
	• 使用：在提交时使用 gitmoji -c 代替 git commit，它会提供一个交互式的表情选择列表。
2. VS Code 插件
	• 在 VS Code 插件市场搜索 Gitmoji，安装后可以在 Git 提交框旁直接点击图标选择表情输入。
3. Husky + Commitlint (团队强管控)
	• 可以在前端工程中配置 Git Hooks，结合 commitlint-config-gitmoji 插件，如果团队成员提交时不加表情，或者表情用错了，直接拦截并拒绝提交。
您目前是个人项目想尝试，还是想在团队团队项目中推行这一套规范呢？如果是团队项目，我可以为您提供一套基于 Husky 和 commitlint 的自动化配置代码。
