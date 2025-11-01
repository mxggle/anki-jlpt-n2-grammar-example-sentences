# 如何更新 AnkiWeb 卡牌描述

## 步骤说明

### 1. 登录 AnkiWeb

访问 https://ankiweb.net/ 并登录您的账号。

### 2. 进入卡牌管理页面

1. 点击页面顶部的 "Decks"
2. 找到您的卡牌 "新完全掌握N2语法例句" (ID: 1584745637)
3. 点击卡牌名称或 "Edit" 按钮

### 3. 更新描述

1. 在编辑页面找到 "Description" 字段
2. 打开项目根目录下的 `ankiweb-description.html` 文件
3. 复制全部HTML内容
4. 粘贴到 AnkiWeb 的 Description 文本框中
5. 点击 "Save" 保存

### 4. 预览检查

保存后访问卡牌页面，检查：
- ✅ 排版是否正确
- ✅ 链接是否可点击
- ✅ Emoji 是否正常显示
- ✅ 语法高亮是否生效

## 编辑 HTML 描述

如果需要修改描述内容：

1. 编辑 `ankiweb-description.html` 文件
2. 保存修改
3. 按照上述步骤重新上传到 AnkiWeb

### 常用修改示例

#### 更新版本号
```html
<p style="text-align: center; color: #666; font-size: 0.9em;">
<em>Version 1.1 | Last Updated: 2025-12 | AnkiWeb ID: 1584745637</em>
</p>
```

#### 更新卡牌统计
```html
<li>✅ <strong>约800张卡牌</strong> - 涵盖N2全部语法点</li>
<li>🎵 <strong>600个音频文件</strong> - 每个例句配有真人发音</li>
```

#### 添加新的语法课程
```html
<h3>第27课 - XXX</h3>
<ul>
<li>～XXX - XXX</li>
</ul>
```

## 注意事项

1. **保持HTML格式**：AnkiWeb支持基本的HTML标签
2. **避免JavaScript**：AnkiWeb不支持JavaScript
3. **测试显示效果**：建议先在本地HTML预览器中查看效果
4. **备份原始内容**：每次更新前保存一份备份
5. **版本控制**：使用Git提交每次修改

## 支持的HTML标签

AnkiWeb支持的常用标签：
- 标题：`<h1>` ~ `<h6>`
- 段落：`<p>`
- 列表：`<ul>`, `<ol>`, `<li>`
- 强调：`<strong>`, `<em>`, `<b>`, `<i>`
- 链接：`<a href="...">`
- 引用：`<blockquote>`
- 代码：`<code>`
- 分隔线：`<hr>`
- 样式：`style` 属性（内联样式）

## 本地预览

在浏览器中打开 `ankiweb-description.html` 即可预览效果。

或使用命令：
```bash
open ankiweb-description.html  # macOS
xdg-open ankiweb-description.html  # Linux
start ankiweb-description.html  # Windows
```

## 发布流程

完整的卡牌更新流程：

1. 修改卡牌内容（notes.csv, templates等）
2. 更新 `ankiweb-description.html`（如有需要）
3. 在Anki中导出新的 `.apkg` 文件
4. 上传 `.apkg` 到 AnkiWeb
5. 更新描述（使用本文档步骤）
6. 提交Git更改：
   ```bash
   git add .
   git commit -m "Update deck to version X.X"
   git push
   ```
7. 创建GitHub Release（如适用）

## 相关文件

- `ankiweb-description.html` - AnkiWeb描述（HTML格式）
- `README.md` - GitHub项目说明
- `shin-kanzen-n2-grammar/README.md` - 卡牌详细说明

---

最后更新：2025-11-01
