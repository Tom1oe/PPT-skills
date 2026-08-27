# PPT-skills: 智能单页 PPT 生成与排版引擎

基于 AI Agent / Python 的智能单页 PPT 生成工具，专为高质量排版、多场景版式布局、丰富美术风格与自动化质量校验设计。

---

## ✨ 核心特性

- 📐 **20 种经典版式布局**：覆盖结构目录、章节转场、金字塔层级、思维脑图发散、卫星轨道、阶梯进阶、冲刺目标、多宫格网格、时间轴与数据对比等全场景。
- 🎨 **6 种精选美术风格**：商务蓝、水墨绿、科技暗黑、极简白、暖色商务、渐变现代。
- 🖼️ **元数据驱动与无拉伸填充**：智能匹配标准比例（1:1, 3:4, 4:3, 9:16, 16:9, 2:3, 3:2），自动居中裁剪，避免图片拉伸形变。
- 🚀 **纯 Python 跨平台架构**：仅依赖 `python-pptx` 与 `Pillow`，零系统级 C 依赖（无需安装 cairo/cairosvg），100% 兼容 Windows / macOS / Linux。
- 🔍 **全自动化质量校验器**：自动检测文本框交叠 (IoU 算法)、文本溢出、图片越界与比例形变。
- 🤖 **平台生态友好**：原生适配中国电信星辰智能体 (TeleAgent) 工作空间与断点续传机制。

---

## 📁 目录结构

```
PPT-skills/
├── agents/
│   └── skills/
│       └── ppt-single-page/
│           ├── SKILL.md                  # Skill 规范定义与全流程指导
│           ├── requirements.txt          # 运行依赖
│           ├── scripts/
│           │   ├── generate_slide.py     # 主执行脚本 (CLI 入口)
│           │   ├── layout_engine.py      # 20 种版式布局引擎
│           │   ├── style_themes.py       # 6 种视觉风格与配色系统
│           │   ├── image_manager.py      # 元数据驱动的图片/图元管理器
│           │   ├── graphics_renderer.py  # 纯 Pillow 图形/图元渲染器
│           │   ├── chart_builder.py      # 数据图表生成器 (饼/柱/折线/环形/雷达)
│           │   └── validator.py          # 质量合规校验器 (重叠/形变/错位)
│           ├── examples/                 # 各版式示例输入 JSON
│           ├── references/               # 布局、风格、校验详细参考文档
│           └── resources/                # 推荐字体说明
├── .gitignore
└── README.md
```

---

## 🛠️ 快速上手

### 1. 安装依赖

```bash
pip install -r agents/skills/ppt-single-page/requirements.txt
```

### 2. 生成单页 PPT

```bash
python agents/skills/ppt-single-page/scripts/generate_slide.py \
  --input agents/skills/ppt-single-page/examples/example_input.json \
  --output output.pptx
```

### 3. 质量校验

```bash
python agents/skills/ppt-single-page/scripts/validator.py --input output.pptx
```

---

## 📄 开源协议

MIT License
