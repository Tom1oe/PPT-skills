---
name: ppt-single-page
description: >-
  当用户需要根据文档内容生成单页 PPT 时使用此技能。支持多种布局模板（封面页、
  内容网格、数据展示、时间轴、对比页等）和多种美术风格（商务蓝、水墨绿、科技暗黑、
  极简白等）。可用 Pillow 绘制简单图形/图表，也可调用 AI 生图工具生成高质量图片。
  所有图片生成完成后进行文字重叠、图片错位、比例形变的自动校验。
  最终输出一页高质量 .pptx 文件到 TeleAgent 工作空间。
---

# PPT 单页智能生成

根据文档内容自动分析、选择布局、应用美术风格、生成图片，并校验输出质量，最终生成一页精美的 PPTX 文件。

## 前置条件

确保已安装所需 Python 依赖（纯 Python，跨平台兼容 Windows/macOS/Linux）：

```bash
pip install -r requirements.txt
# 等价于: pip install python-pptx Pillow
```

> **注意**：不再需要 `cairosvg` 或 `brew install cairo` 等系统级依赖。

## 输出路径

生成的文件默认放置在 **TeleAgent 工作空间**：

```
./TeleAgent的工作空间/
├── output.pptx              # 生成的 PPT 文件
├── images/                   # 图片文件目录
│   ├── img_xxx_chart.png     # 图表
│   ├── img_xxx_icon.png      # 图标
│   └── img_xxx_fallback.png  # 渐变占位（待AI图片替换）
└── image_tasks.json          # 图片任务清单
```

可通过环境变量 `TELEAGENT_WORKSPACE` 自定义路径：

```bash
export TELEAGENT_WORKSPACE="./my_workspace"
```

## 工作流程

按照以下 7 个阶段顺序执行。**每个阶段的详细参考文档在 `references/` 目录中**。

---

### Phase 1 — 内容分析

分析用户提供的文档内容，确定页面类型和所需元素。

1. 解析输入内容（支持 JSON 结构化数据、Markdown、纯文本）。
2. 识别内容类型：
   - `cover` — 封面/章节页（有大标题、副标题、装饰背景）
   - `content` — 内容页（标题 + 多个要点/段落）
   - `data` — 数据展示页（包含图表、统计数字）
   - `mixed` — 图文混排页（图片和文字穿插）
   - `comparison` — 对比页（两栏或多栏对比）
   - `timeline` — 时间线页（按时序排列的事件）
3. 统计元素数量：标题数、文本段落数、图片需求数、图表需求数。
4. 输出 `ContentAnalysis` 结构。

**输入示例参考**: [example_input.json](./examples/example_input.json)

---

### Phase 2 — 布局选择

根据内容分析结果，从布局模板库中选择最佳布局。

1. 读取布局引擎 [layout_engine.py](./scripts/layout_engine.py)。
2. 根据以下决策因素选择布局：
   - 页面类型 → 对应布局族
   - 元素数量 → 决定网格密度
   - 图片需求 → 决定图片区域比例
3. 每个布局由一组 **Zone** 组成，每个 Zone 定义了区域类型、位置、尺寸和属性。
4. 可根据实际内容微调 Zone 的位置和大小。

**布局详细参考**: [layout_guide.md](./references/layout_guide.md)

---

### Phase 3 — 风格应用

根据用户指定或自动推荐的美术风格，生成完整的视觉方案。

1. 读取风格主题 [style_themes.py](./scripts/style_themes.py)。
2. 如果用户未指定风格，根据内容类型自动推荐：
   - 商务报告 → `business_blue` 或 `warm_corporate`
   - 技术方案 → `tech_dark`
   - 文化/总结 → `nature_green`
   - 产品/营销 → `gradient_modern`
   - 创意展示 → `minimal_light`
3. 获取风格配置：颜色方案、字体方案、装饰元素、生图风格提示词。

**风格详细参考**: [style_guide.md](./references/style_guide.md)

---

### Phase 4 — 创建图片任务

**元数据驱动模式**：只记录任务信息，不生成占位文件。

使用 [image_manager.py](./scripts/image_manager.py) 为每个图片区域创建任务记录：

```python
task = image_manager.create_task(
    zone_id="hero_image",
    left=0.0, top=0.0,
    width=6.667, height=7.5,
    image_type="photo",
    description="蓝天白云下的雪山风景",
    style_prompt="professional corporate style",
    preferred_ratio="9:16",
)
```

任务清单会自动导出为 `image_tasks.json`，支持断点续传。

约定的标准图片比例及对应分辨率：

| 比例 | 宽 × 高 (px) | 适用场景 |
|------|-------------|---------|
| 1:1 | 1024 × 1024 | 头像、图标、方形图片 |
| 3:4 | 768 × 1024 | 竖向人物、竖向场景 |
| 4:3 | 1024 × 768 | 传统照片、文档插图 |
| 9:16 | 576 × 1024 | 竖向全幅、手机风格 |
| 16:9 | 1024 × 576 | 横向全幅、宽屏背景 |
| 2:3 | 682 × 1024 | 竖向海报 |
| 3:2 | 1024 × 682 | 横向照片 |

---

### Phase 5 — 执行图片生成

按类型分别处理：

- **`icon`（图标）** → [graphics_renderer.py](./scripts/graphics_renderer.py)
  - 使用 Pillow 直接绘制（无需 SVG 中间格式）
  - 支持圆形图标、数字图标、几何装饰等

- **`chart`（数据图表）** → [chart_builder.py](./scripts/chart_builder.py)
  - 使用 Pillow 直接绘制：环形图、饼图、柱状图、折线图、雷达图
  - 传入数据、尺寸和颜色方案

- **`photo`（AI 美术图片）** → 调用 `generate_image` 工具
  - 构建 Prompt = 内容描述 + 风格提示词后缀
  - 传入 AspectRatio 参数（从标准比例中选择）
  - 生成后调用 `image_manager.fill_image()` 填充

- **`decorator`（装饰元素）** → [graphics_renderer.py](./scripts/graphics_renderer.py)
  - 渐变背景、半透明遮罩、波浪线、几何图形等

#### 图片后处理

对每张生成的图片：
1. 检查实际宽高比是否匹配目标比例
2. 如不匹配，进行居中裁切（crop）而非拉伸（stretch）
3. 缩放到目标像素尺寸

---

### Phase 6 — 组装 PPTX（延迟组装）

使用 [generate_slide.py](./scripts/generate_slide.py) 在**所有图片就绪后**一次性组装。

1. 创建 Presentation 对象（16:9 宽屏，13.333" × 7.5"）
2. 添加空白幻灯片
3. 按 z_order 从低到高依次添加元素：
   - 装饰层 → Pillow 绘制的 PNG
   - 图片/图表 → 已完成任务的图片文件
   - 文本框 → 设置段落样式、字体、对齐
4. 保存到 TeleAgent 工作空间

---

### Phase 7 — 校验

使用 [validator.py](./scripts/validator.py) 对生成的 PPTX 进行自动化质量校验。

#### 校验项

1. **文字重叠检测**
   - 提取所有文本框的 bounding box
   - 检测任意两个文本框是否交叠（IoU 阈值 > 5%）
   - 检测文本是否溢出文本框边界

2. **图片错位检测**
   - 图片是否完全在幻灯片可视区域内
   - 图片位置与布局定义的偏差 < 0.1 英寸

3. **比例形变检测**
   - 图片嵌入尺寸的宽高比 vs 原始图片的宽高比
   - 允许偏差 < 2%

#### 校验结果

```python
{
    "passed": True/False,
    "errors": [...],      # 必须修复
    "warnings": [...],    # 建议修复
    "suggestions": [...]  # 优化建议
}
```

如果校验不通过，根据错误信息调整布局或重新生成对应的图片。

**校验详细参考**: [validation_guide.md](./references/validation_guide.md)

---

## 快速开始

```bash
# 安装依赖（仅需两个纯 Python 包）
pip install -r requirements.txt

# 使用示例输入生成 PPT
python scripts/generate_slide.py --input examples/example_input.json

# 指定输出路径
python scripts/generate_slide.py --input examples/example_input.json --output my_slide.pptx

# 从中断处恢复
python scripts/generate_slide.py --input examples/example_input.json --resume

# 单独校验
python scripts/validator.py --input output.pptx
```

## 注意事项

- 所有坐标基于 **13.333" × 7.5"** 标准宽屏尺寸
- 图形绘制使用 Pillow（纯 Python），**无需任何系统级依赖**
- AI 生图时使用 `generate_image` 工具，传入最接近的标准比例
- 图片填充使用 **居中裁切** 模式，避免拉伸形变
- 中文字体推荐使用「微软雅黑」或「思源黑体」，详见 [fonts.md](./resources/fonts.md)
- PPTX 默认输出到 `./TeleAgent的工作空间/`，可通过 `TELEAGENT_WORKSPACE` 环境变量自定义
- 支持 **断点续传**：中断后使用 `--resume` 参数恢复进度
