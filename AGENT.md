# AGENT.md — 新完全掌握N2语法例句 Anki 打包流程文档

> 本文档面向 AI Agent 和开发者，描述整个 Anki 卡牌打包系统的架构、约束条件和常见修改方式。
> **修改前必读**，否则可能导致用户 Anki 数据库中出现重复卡片。

---

## 项目结构

```
Shin Kanzen Master Grammar N2/
├── AGENT.md                          # 本文档
├── package_anki.py                   # 主打包脚本（Python）
├── Shin_Kanzen_Master_Grammar_N2_v1.6.0.apkg  # 输出文件（运行后生成）
├── JLPT_N2.apkg                      # 参考原始包（勿删）
└── shin-kanzen-n2-grammar/
    ├── notes.csv                     # 所有卡片数据（22列 CSV）
    ├── medias/                       # 所有音频文件（531个 MP3）
    │   └── lesson_XX_sub_XX_line_XXX.mp3
    └── templates/
        ├── Japanese Grammar Enhanced Model++-Japanese Grammar Card.html  # 卡片 HTML 模板
        └── Japanese Grammar Enhanced Model++-styles.css                 # 卡片样式
```

---

## ⚠️ 关键约束：不能随意修改的固定值

这些值必须与原始 `JLPT_N2.apkg` 完全一致，**否则 Anki 会把新卡片当作全新卡片导入，造成重复**。

### 1. Model ID（Note Type ID）

```python
MODEL_ID = 1607392322
```

- 来源：从 `JLPT_N2.apkg` 的 SQLite 数据库 `col` 表 `models` 字段中读取
- Anki 用此 ID 来判断是否为同一个 Note Type
- **绝对不能修改**

### 2. GUID 格式

```
n2-line-{LineNumber}
# 例如: n2-line-1, n2-line-2, ..., n2-line-531
```

- `LineNumber` 来自 CSV 的 `col[20]`
- Anki 用 GUID 来判断是否为同一张笔记（笔记 = 一组字段数据）
- GUID 不匹配 → 重复导入；GUID 匹配 → 更新已有卡片
- **格式不能更改**；新增卡片时 LineNumber 必须唯一且连续

### 3. 字段顺序（20个字段，顺序固定）

| 索引 | 字段名 | 对应 CSV 列 |
|------|--------|------------|
| 0 | `FrontSentence` | `col[1]` |
| 1 | `GrammarPattern` | `col[2]` |
| 2 | `LessonInfo` | `col[3]` |
| 3 | `BackSentence` | `col[4]` |
| 4 | `ReadingFurigana` | `col[5]` |
| 5 | `Translation` | `col[6]` |
| 6 | `AudioFile` | `col[7]` |
| 7 | `GrammarFormation` | `col[8]` |
| 8 | `RichGrammarFormation` | `col[9]` |
| 9 | `StyleNotes` | `col[10]` |
| 10 | `ExplanationJapanese` | `col[11]` |
| 11 | `ExplanationChinese` | `col[12]` |
| 12 | `EnglishMeaning` | `col[13]` |
| 13 | `ChineseMeaning` | `col[14]` |
| 14 | `AdditionalNotes` | `col[15]` |
| 15 | `AdditionalNotesZh` | `col[16]` |
| 16 | `VocabularyNotes` | `col[17]` |
| 17 | `DetailedExplanation` | `col[18]` |
| 18 | `Level` | `col[19]` |
| 19 | `LineNumber` | `col[20]` |

---

## CSV 数据格式（notes.csv）

### 元数据头（前4行，以 `#` 开头，自动跳过）

```
#separator:comma
#html:true
#deck column:1       # col[0] 是牌组名
#tags column:22      # col[21] 是标签
```

### 完整列映射（共22列，0-indexed）

| 列索引 | 内容 | 示例 |
|--------|------|------|
| `col[0]` | 牌组名 | `新完全掌握N2语法例句::Lesson 01` |
| `col[1]` | FrontSentence（题目句，含`【…】`占位符） | `この整理券は、商品受け取りの【…】、必要です。` |
| `col[2]` | GrammarPattern（语法点名称） | `～際（に）` |
| `col[3]` | LessonInfo（课程编号） | `第1課 - 1` |
| `col[4]` | BackSentence（含高亮 span 的完整句） | `...` |
| `col[5]` | ReadingFurigana（带假名注音） | `この 整理券[せいりけん]は...` |
| `col[6]` | Translation（中文翻译） | `这张排号单在领取商品时需要用到` |
| `col[7]` | AudioFile（音频标签） | `[sound:lesson_01_sub_01_line_001.mp3]` |
| `col[8]` | GrammarFormation（接续规则纯文本） | `名ーの・動ー辞書形/た形 ＋際（に）` |
| `col[9]` | RichGrammarFormation（带 HTML 的接续规则） | `<div class="grammar-connection">...` |
| `col[10]` | StyleNotes（文体标注） | `硬い言い方` |
| `col[11]` | ExplanationJapanese（日语简释） | `～とき` |
| `col[12]` | ExplanationChinese（中文简释） | `……时候。书面语。` |
| `col[13]` | EnglishMeaning（英文释义，可为空） | `` |
| `col[14]` | ChineseMeaning（中文释义，可为空） | `` |
| `col[15]` | AdditionalNotes（补充说明，日文） | `主に行為や出来事を...` |
| `col[16]` | AdditionalNotesZh（补充说明，中文） | `主要接在表达行为...` |
| `col[17]` | VocabularyNotes（词汇注释，可为空） | `` |
| `col[18]` | DetailedExplanation（逐词精解，HTML） | `<h3>句子结构分析</h3>...` |
| `col[19]` | Level（JLPT 级别） | `1 N2` |
| `col[20]` | LineNumber（行号，也是 GUID 的来源） | `1` |
| `col[21]` | Tags（Anki 标签） | `5` |

---

## 打包脚本说明（package_anki.py）

### 运行方式

```bash
cd "Shin Kanzen Master Grammar N2"
python3 package_anki.py
```

### 依赖

```bash
pip install genanki
```

### 核心逻辑

1. **读取 CSS 和 HTML 模板**（`templates/` 目录）
2. **定义 Model**（固定 `MODEL_ID = 1607392322`，20个字段，顺序固定）
3. **逐行读取 `notes.csv`**，跳过 `#` 开头的元数据行
4. **使用 `safe_get(row, index)`** 安全读取每列（越界返回 `''`）
5. **构建 GUID**：`f'n2-line-{line_number}'`（`line_number = col[20]`）
6. **按 `col[0]` 分组**，为每个 Lesson 创建独立子牌组
7. **收集音频文件**：从 `col[7]` 解析 `[sound:xxx.mp3]` 并检查文件是否存在
8. **输出**：`Shin_Kanzen_Master_Grammar_N2_v1.6.0.apkg`

---

## 卡片模板说明（HTML 模板）

### 模板文件路径

```
shin-kanzen-n2-grammar/templates/Japanese Grammar Enhanced Model++-Japanese Grammar Card.html
```

### 模板结构

```
[div.card-front]       ← 正面（Anki 出题时显示）
[script]               ← 翻译持久化逻辑
[div.card-back]        ← 背面（翻牌后显示）
```

> ⚠️ 注意：`package_anki.py` 通过查找第一个 `<div class="card-back">` 来分割正面和背面模板。
> **不要在正面部分使用 `<div class="card-back">`**，否则分割会出错。

### 翻译持久化功能（localStorage）

卡片正面有一个翻译切换按钮，状态通过 `localStorage` 在卡片之间持久化：

- **Key**：`n2_translation_visible`
- **值**：`'true'` 或 `'false'`（字符串）
- **默认**：隐藏（首次加载时 `localStorage` 为 `null`）
- **作用域**：同一个 Anki session 内持久（重启 Anki 后重置）

#### 修改默认展开状态

在 `<script>` 中修改这一行：

```javascript
// 默认隐藏（改为 saved === 'true' 为首次默认隐藏，改为 true 为首次默认展开）
applyState(saved === 'true');

// 如需首次默认展开：
applyState(saved !== 'false');
```

---

## 常见修改任务

### ✅ 添加新卡片

1. 在 `notes.csv` 末尾追加新行
2. `col[0]`：对应牌组名（如 `新完全掌握N2语法例句::Lesson 27`）
3. `col[20]`（LineNumber）：必须是全局唯一的递增数字（当前最大是 531，新增从 532 开始）
4. 对应音频文件放入 `shin-kanzen-n2-grammar/medias/`
5. 运行 `python3 package_anki.py` 重新打包

### ✅ 修改卡片样式

编辑 `templates/Japanese Grammar Enhanced Model++-styles.css`，然后重新打包。
样式修改不影响 GUID 或 Model ID，不会产生重复。

### ✅ 修改卡片模板布局

编辑 `templates/Japanese Grammar Enhanced Model++-Japanese Grammar Card.html`。
注意：
- 正面内容在 `<div class="card-front">` 之内
- 背面内容在 `<div class="card-back">` 之内
- `<script>` 块放在两者之间（Anki 会在正面和背面都执行）

### ✅ 修改输出文件名

修改 `package_anki.py` 最后的：

```python
output_file = 'Shin_Kanzen_Master_Grammar_N2_v1.6.0.apkg'
```

### ✅ 新增字段

> ⚠️ 高风险操作！

新增字段会改变 Model 结构。需要：
1. 在 `package_anki.py` 的 `fields=[]` 列表末尾追加新字段（**只能追加到末尾**，不能插入中间）
2. 在 CSV 对应列填充数据
3. 在 HTML 模板中用 `{{新字段名}}` 引用
4. 重新打包
5. 在 Anki 导入时选择"更新笔记模板"

---

## 验证打包结果

可以用以下脚本快速验证输出文件是否正确：

```python
import zipfile, sqlite3, json, os

os.makedirs('_verify', exist_ok=True)
with zipfile.ZipFile('Shin_Kanzen_Master_Grammar_N2_v1.6.0.apkg', 'r') as z:
    z.extractall('_verify')

for name in ['collection.anki21', 'collection.anki2']:
    db = f'_verify/{name}'
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        models = json.loads(cur.execute("SELECT models FROM col").fetchone()[0])
        for mid, m in models.items():
            print(f"Model ID: {mid}")           # 期望: 1607392322
            print(f"Fields: {len(m['flds'])}")  # 期望: 20
        cur.execute("SELECT COUNT(*) FROM notes")
        print(f"Notes: {cur.fetchone()[0]}")    # 期望: 531（或更多）
        cur.execute("SELECT guid FROM notes LIMIT 3")
        print(f"GUIDs: {[r[0] for r in cur.fetchall()]}")  # 期望: ['n2-line-1', ...]
        conn.close()
        break

import shutil; shutil.rmtree('_verify')
```

---

## 导入 Anki 时的推荐设置

| 设置项 | 推荐值 |
|--------|--------|
| 合并笔记模板 | 打开（On） |
| 更新笔记/模板 | 始终（Always） |
| 学习进度 | 会自动保留 |

---

## 历史变更记录

| 版本 | 变更内容 |
|------|---------|
| v1.6.0 | 功能更新：卡片正面新增翻译切换按钮，可自由控制显示/隐藏 |
| v1.5.0 | 修复 MODEL_ID（1584745637 → 1607392322）；修复 GUID 格式（hash → n2-line-N）；字段从13个扩展到20个；添加翻译状态跨卡持久化（localStorage） |
