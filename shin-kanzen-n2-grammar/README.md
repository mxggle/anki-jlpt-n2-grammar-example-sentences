# 新完全掌握N2语法例句卡牌

## 卡牌统计

- **总卡牌数**: 约688张（1376行数据，包含标题行和分隔符）
- **音频文件数**: 531个MP3文件
- **语法点覆盖**: N2全部语法点
- **详细程度**: 包含逐词精解、语法分析和例句发音

## 文件说明

### notes.csv
包含所有卡牌的数据，字段包括：
- 牌组名称（Deck）
- 例句（Sentence）
- 语法点（Grammar Point）
- 课程编号（Lesson）
- 带高亮的例句（Sentence with Highlight）
- 假名标注（Reading）
- 中文翻译（Translation）
- 音频文件名（Audio）
- 语法接续（Grammar Formation）
- 语法解释（中日双语）
- 逐词精解（Detailed Word Analysis）
- 标签（Tags）

### medias/
包含所有例句的音频文件（MP3格式），按课程和序号命名：
- 格式: `lesson_XX_sub_XX_line_XXX.mp3`
- 编码: MP3
- 采样率: 标准质量

### templates/
包含Anki卡牌的模板文件：
- **Japanese Grammar Enhanced Model++-Japanese Grammar Card.html**: 卡牌HTML模板
- **Japanese Grammar Enhanced Model++-styles.css**: 卡牌样式表

## 导入说明

1. 在Anki中选择"文件" → "导入"
2. 选择 `notes.csv` 文件
3. 设置字段分隔符为"逗号"
4. 确认字段映射正确
5. 导入完成后，确保媒体文件同步

## 卡牌特性

### 正面
- 完整例句（关键语法点高亮显示）
- 课程编号
- 提示：需要填写的语法点

### 背面
- 完整例句（带语法高亮）
- 假名标注
- 中文翻译
- 音频播放按钮
- 语法点说明
- 语法接续方式
- 详细的逐词精解
- 句子结构分析

## 学习建议

1. **循序渐进**: 按照Lesson编号顺序学习
2. **听力训练**: 多听音频，培养语感
3. **理解优先**: 仔细阅读逐词精解
4. **活学活用**: 尝试用学到的语法点造句
5. **定期复习**: 利用Anki的SRS算法

## 技术规格

- **字符编码**: UTF-8
- **CSV分隔符**: 逗号(,)
- **HTML转义**: 已处理
- **音频格式**: MP3
- **模板系统**: Anki标准模板

## 更新日志

查看主仓库的 CHANGELOG.md（如果有）或 Releases 页面了解更新内容。

## 问题反馈

如果遇到问题，请在主仓库提交 Issue，并提供：
- Anki版本
- 操作系统
- 问题描述
- 截图（如适用）
