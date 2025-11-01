# 新完全掌握N2语法例句 (Shin Kanzen Master Grammar N2)

这是一个基于《新完全掌握日本语能力考试N2级语法》教材的Anki记忆卡牌项目。

## 📸 卡牌预览

<div align="center">
  <table>
    <tr>
      <td width="50%">
        <img src="https://github.com/user-attachments/assets/11f65318-2a92-4474-a417-3348624c3b26" alt="卡牌正面" />
        <p align="center"><em>卡牌正面 - 语法高亮</em></p>
      </td>
      <td width="50%">
        <img src="https://github.com/user-attachments/assets/fbc19941-fb20-4615-b8d0-75ed23256db1" alt="卡牌背面" />
        <p align="center"><em>卡牌背面 - 假名与翻译</em></p>
      </td>
    </tr>
    <tr>
      <td width="50%">
        <img src="https://github.com/user-attachments/assets/a2cf57b9-57b3-45f3-9dc3-66f6133992e5" alt="语法接续" />
        <p align="center"><em>语法接续说明</em></p>
      </td>
      <td width="50%">
        <img src="https://github.com/user-attachments/assets/fc0ada2f-564d-4986-8b7e-743be2c85b29" alt="逐词精解" />
        <p align="center"><em>逐词详细精解</em></p>
      </td>
    </tr>
  </table>
</div>

## 项目简介

本项目包含了《新完全掌握N2语法》书中的所有例句，每个句子都配有详细的语法解释、词汇分析和音频发音。适合准备JLPT N2考试的学习者系统地掌握N2语法点。

## Anki卡牌信息

- **Anki卡牌ID**: 1584745637
- **卡牌链接**: https://ankiweb.net/shared/info/1584745637
- **难度级别**: JLPT N2
- **内容来源**: 新完全掌握日本语能力考试N2级语法

## 项目结构

```
.
├── README.md                          # 本文件
├── LICENSE                            # 开源许可证（CC BY-NC 4.0）
├── .gitignore                         # Git忽略文件
└── shin-kanzen-n2-grammar/           # 主卡牌目录
    ├── notes.csv                      # 卡牌数据（CSV格式）
    ├── medias/                        # 音频文件目录（包含例句发音）
    └── templates/                     # Anki卡牌模板
        ├── Japanese Grammar Enhanced Model++-Japanese Grammar Card.html
        └── Japanese Grammar Enhanced Model++-styles.css
```

## 卡牌内容

每张卡牌包含以下信息：

- **例句**: 日语原文例句
- **语法点**: 标注的语法点（高亮显示）
- **课号**: 对应教材的课程编号
- **假名标注**: 完整的假名注音
- **中文翻译**: 例句的中文翻译
- **音频**: 例句的日语发音（MP3格式）
- **语法接续**: 该语法点的接续方式
- **语法解释**: 详细的语法说明（中日双语）
- **逐词精解**: 句子中每个词的详细解释
- **标签**: N2标签用于分类

## 使用方法

### 导入到Anki

1. 下载Anki桌面版: https://apps.ankiweb.net/
2. 从AnkiWeb下载本卡牌: https://ankiweb.net/shared/info/1584745637
3. 双击下载的`.apkg`文件，Anki会自动导入

### 从源文件导入

如果你想从本项目的源文件导入：

1. 克隆或下载本仓库
2. 打开Anki
3. 点击“文件” → “导入”
4. 选择`shin-kanzen-n2-grammar/notes.csv`文件
5. 确保`shin-kanzen-n2-grammar/medias/`文件夹中的音频文件在Anki的媒体文件夹中

## 学习建议

1. **按课程顺序学习**: 卡牌按照教材的课程顺序组织（Lesson 01开始）
2. **注意语法接续**: 每个语法点都标注了具体的接续方式
3. **利用音频**: 充分利用例句音频练习听力和发音
4. **理解逐词精解**: 仔细阅读逐词精解部分，理解句子结构
5. **定期复习**: 利用Anki的间隔重复算法定期复习

## 语法覆盖范围

本卡牌涵盖了N2级别的所有主要语法点，包括但不限于：

- 时间相关语法（～際に、～最中だ、～うちに等）
- 条件假设语法
- 原因理由语法
- 目的手段语法
- 授受关系语法
- 敬语表达
- 其他N2必考语法点

## 数据格式说明

`notes.csv`文件采用逗号分隔格式，包含以下字段：

1. Deck（牌组名）
2. Sentence（例句）
3. Grammar Point（语法点）
4. Lesson（课程）
5. Sentence with Highlight（带高亮的例句）
6. Reading（假名标注）
7. Translation（中文翻译）
8. Audio（音频文件）
9. Grammar Formation（语法接续）
10. 其他辅助信息字段

## 技术特性

- **响应式设计**: 卡牌模板支持手机和电脑端
- **语法高亮**: 关键语法点在例句中高亮显示
- **富文本格式**: 支持HTML格式的详细解释
- **标签系统**: 便于筛选和分类学习

## 下载发布版

从 [Releases](https://github.com/mxggle/anki-jlpt-n2-grammar-example-sentences/releases) 页面下载最新的 `.apkg` 文件，直接导入Anki使用。

注意：**请下载 `.apkg` 文件，不要下载源代码 zip 文件**。

## 贡献

欢迎贡献！如果你发现了错误或有改进建议：

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 许可证

本项目采用 [CC BY-NC 4.0](LICENSE) 许可证。

- ✅ 允许分享和修改
- ❌ 禁止商业使用
- 🔗 必须注明出处

内容基于《新完全掌握日本语能力考试N2级语法》教材，仅供学习交流使用。

## 相关资源

- [JLPT官方网站](https://www.jlpt.jp/)
- [Anki官方网站](https://apps.ankiweb.net/)
- [新完全掌握系列教材](https://www.3anet.co.jp/)

---

祝学习顺利！がんばって！
# anki-jlpt-n2-grammar-example-sentences
