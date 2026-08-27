---
name: ppt-single-page
name_cn: 单页PPT智能生成
description: >-
  当用户需要根据文档内容生成单页 PPT 时使用此技能。支持多种布局模板（封面页、
  内容网格、数据展示、时间轴、对比页等）和多种美术风格（商务蓝、水墨绿、科技暗黑、
  极简白等）。可用 Pillow 绘制简单图形/图表，也可调用 AI 生图工具生成高质量图片。
  所有图片生成完成后进行文字重叠、图片错位、比例形变的自动校验。
  最终输出一页高质量 .pptx 文件到 TeleAgent 工作空间。
description_cn: >-
  根据文档内容与需求自动分析、选择或定制版式、应用美术风格、生成图表与AI配图，
  并在组装完成后执行文字重叠、图片错位与比例形变的自动化校验，输出高质量单页 PPTX。
---

# PPT 单页智能生成

根据文档内容自动分析、选择布局、应用美术风格、生成图片，并校验输出质量，最终生成一页精美的 PPTX 文件。

## 前置条件

确保已安装所需 Python 依赖（纯 Python，跨平台兼容 Windows/macOS/Linux）：

```bash
pip install -r requirements.txt
# 等价于: pip install python-pptx Pillow
```

> **注意**：无需任何 `cairosvg` 或 `brew install cairo` 等系统级 C 依赖。

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
   - `catalog` — 目录索引页（章节与板块导航）
   - `section` — 章节过渡页（PART 篇章转场）
   - `content` — 内容页（标题 + 多个要点/段落）
   - `data` — 数据展示页（包含图表、统计数字、金字塔）
   - `mixed` — 图文混排页（图片和文字穿插）
   - `comparison` — 对比页（两栏或多栏对比、双圆方案）
   - `timeline` — 时间线/进阶页（时序事件、阶梯上升、流程冲刺）
3. 统计元素数量：标题数、文本段落数、图片需求数、图表需求数。
4. 输出 `ContentAnalysis` 结构。

**输入示例参考**: [example_input.json](./examples/example_input.json)

---

### Phase 2 — 布局选择

根据内容分析结果，从布局模板库中选择最佳布局。

1. 读取布局引擎 [layout_engine.py](./scripts/layout_engine.py)。
2. 根据以下决策因素选择布局：
   - 页面类型 → 对应布局族（支持 20 种经典版式）
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

**元数据驱动模式**：只记录任务信息，不生成多余占位文件。

使用 [image_manager.py](./scripts/image_manager.py) 为每个图片区域创建任务记录：

```python
task = image_manager.create_task(
    zone_id="hero_image",
    left=0.0, top=0.0,
    width=6.667, height=7.5,
    image_type="photo",
    description="智能手机产品特写，极简科技感光影",
    style_prompt="professional tech product photography, sleek modern",
    preferred_ratio="3:4",
)
```

任务清单会自动导出为 `image_tasks.json`，支持断点续传。

> [!WARNING]
> **生图参数重要警告**：  
> 当调用 ImageGen / 生图模型工具时，`size` 参数**只接受命名尺寸（2K/3K/4K）或显式像素值（如 `1440x2560`）**，且总像素数必须 ≥ 3,686,400。  
> **绝对不可传入 `"3:4"` 或 `"16:9"` 这种比例字符串**，否则会直接触发 `IMAGE_SIZE_INVALID` 错误！

约定的标准图片比例与生图尺寸对照表：

| 比例 | ImageGen 生图尺寸 (`size` 参数) | 裁切/缩放参考分辨率 | 适用场景 |
|:---|:---|:---|:---|
| **1:1** | `2048x2048` | 1024 × 1024 | 方形产品图、头像、图标徽标 |
| **3:4** | `1920x2560` | 768 × 1024 | 竖向人物立绘、竖向产品海报 |
| **4:3** | `2560x1920` | 1024 × 768 | 横向展示图、传统文档插图 |
| **9:16** | `1440x2560` | 576 × 1024 | 竖向手机全幅、移动端界面 |
| **16:9** | `2560x1440` | 1024 × 576 | 横向全屏背景、宽屏展示大图 |
| **2:3** | `1706x2560` | 682 × 1024 | 竖向摄影图、海报图 |
| **3:2** | `2560x1706` | 1024 × 682 | 横向单反摄影、全景图 |

---

### Phase 5 — 执行图片生成

按类型分别处理：

- **`icon`（图标）** → [graphics_renderer.py](./scripts/graphics_renderer.py)
  - 使用 Pillow 直接绘制（纯 Python，无需 SVG 中间转换）
  - 支持圆形编号、几何图形、发散节点等

- **`chart`（数据图表与图元）** → [chart_builder.py](./scripts/chart_builder.py) / [graphics_renderer.py](./scripts/graphics_renderer.py)
  - 支持：环形进度图、饼图、柱状图、折线图、雷达图、金字塔层级、阶梯上升图等
  - 传入数据、尺寸和颜色方案

- **`photo`（AI 美术图片）** → 调用生图工具
  - 构建 Prompt = 内容描述 + 风格提示词后缀
  - **`size` 参数必须传入上表【ImageGen 生图尺寸】列的显式像素值（如 `1440x2560`），不可传比例字符串**
  - 图片生成后调用 `image_manager.fill_image(task.id, img_path)` 进行后处理与记录

- **`decorator`（装饰元素）** → [graphics_renderer.py](./scripts/graphics_renderer.py)
  - 渐变背景、半透明遮罩、发散中枢、微立体圆角卡片、线条等

#### 图片后处理（防形变）

对每张生成的图片：
1. 读取实际生成的分辨率
2. 使用 `_center_crop` 进行**居中裁切**以精确适配 PPTX 目标区域比例，**严禁直接拉伸变形**
3. 缩放到目标高清分辨率嵌入

---

### Phase 6 — 组装 PPTX

使用 [generate_slide.py](./scripts/generate_slide.py) 在**所有图片与图表生成就绪后**一次性延迟组装。

1. 创建 Presentation 对象（16:9 宽屏，标准尺寸 13.333" × 7.5"）
2. 添加空白幻灯片并应用主题背景色
3. 按 `z_order` 从低到高依次添加图层：
   - 背景层 / 装饰层 → Pillow 绘制的透明 PNG
   - 图片 / 图表 → 裁切后的高清图片
   - 文本框 → 设置段落文字、字体、字号、颜色、对齐方式
4. 保存 PPTX 到 TeleAgent 工作空间

#### 💡 自定义布局模式 (Custom Layout Mode)

当预设的 20 种布局模板不完全契合特定的定制化需求（例如：“左侧大手机产品图 + 右侧 6 行紧凑卖点列表”或特定图文微排版）时，可直接编写独立的 Python 生成脚本：

1. **复用调色板与规范**：从 `style_themes.py` 导入 `get_theme()` 获取统一配色与字体配置。
2. **纯 python-pptx 编排**：直接调用 `shapes.add_textbox()`、`shapes.add_picture()` 创建精确坐标的图文排版。
3. **Pillow 辅助渲染**：使用 `graphics_renderer.py` / Pillow 快速生成局部图标或圆角背景卡片。
4. **临时脚本管理**：自定义脚本可保存在 `.temp/` 或工作空间中执行。
5. **必须执行质量校验**：生成后**必须**调用 `validator.py` 确保无重叠与无形变。

---

### Phase 7 — 质量合规校验

使用 [validator.py](./scripts/validator.py) 对生成的 PPTX 进行全自动质量校验。

#### 核心检测项

1. **文字重叠检测 (Text Overlap)**
   - 提取所有文本框的 bounding box 计算 IoU
   - 检测任意文本框交叠（IoU > 5% 判定为 Error，0% < IoU ≤ 5% 判定为 Warning）
   - 检测文本行数与高度是否溢出边界

2. **图片错位检测 (Image Alignment)**
   - 检查图片是否超出 13.333" × 7.5" 可视区域（允许负边距 ≤ 0.1"）
   - 检查图片尺寸是否过小 (< 0.3")

3. **比例形变检测 (Aspect Distortion)**
   - 计算嵌入比例 vs 图片原始像素比例
   - 偏差 > 2% 报错提示形变

#### 常见校验失败修复对照表

| 失败类型 | 常见原因 | 修复方法 |
|:---|:---|:---|
| **`text_overlap` (error)** | 标题与副标题垂直间距不足（IoU > 5%） | 增大垂直间距，标题与副标题之间**至少保留 0.15" 间隙** |
| **`text_overlap` (warning)** | 列表项小标题与描述文本框重叠 | 合并在同一文本框中多段落显示，或留出 **≥ 0.06" 间隙** |
| **`text_overlap` (warning)** | 列表末项与底部页脚文字重叠 | 减小行高、适当压缩字号或将页脚整体下移至 `top=6.8"` 以后 |
| **`aspect_distortion`** | 图片嵌入尺寸比例与原始图片偏差 > 2% | 检查是否开启居中裁切（`crop_to_fit=True`），避免拉伸 |

> **经验法则**：垂直堆叠文本框之间**至少留出 0.1" 间隙**；文本框的 `height` 参数按需设置，避免设置过大导致 bounding box 虚高产生假性重叠报警。

**校验详细参考**: [validation_guide.md](./references/validation_guide.md)

---

## 快速开始

```bash
# 1. 安装依赖（仅需两个纯 Python 库）
pip install -r requirements.txt

# 2. 标准流程生成
python scripts/generate_slide.py --input examples/example_input.json

# 3. 指定输出与恢复
python scripts/generate_slide.py --input examples/example_input.json --output ./TeleAgent的工作空间/my_slide.pptx --resume

# 4. 执行校验
python scripts/validator.py --input ./TeleAgent的工作空间/output.pptx
```

## 注意事项

- 所有坐标基于 **13.333" × 7.5"** 标准 16:9 宽屏尺寸
- 图形绘制使用 Pillow（纯 Python），**跨平台零系统级依赖**
- 调用生图工具时，**`size` 参数传入显式像素尺寸（如 `1440x2560`），不可传比例字符串**
- 图片填充一律使用 **居中裁切** 模式，避免拉伸形变
- 中文字体优先使用「微软雅黑」或「思源黑体」，详见 [fonts.md](./resources/fonts.md)
- PPTX 默认输出到 `./TeleAgent的工作空间/`，可通过 `TELEAGENT_WORKSPACE` 环境变量自定义
- 支持 **断点续传**：遇中断可使用 `--resume` 参数无缝恢复生成进度
