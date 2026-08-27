# 校验规则参考文档

## 概述

校验器 (`validator.py`) 在 PPTX 生成完成后自动运行，检测三大类质量问题。
所有检测基于元素的 Bounding Box（边界框）计算。

## 1. 文字重叠检测

### 检测原理

提取每个包含文字的文本框的 bounding box `(left, top, width, height)`，
对所有文本框对计算 **IoU（交并比）**：

```
IoU = 交集面积 / (A面积 + B面积 - 交集面积)
```

### 判定规则

| IoU 范围 | 级别 | 说明 |
|----------|------|------|
| > 5% | ❌ error | 严重重叠，必须修复 |
| > 0% 且 ≤ 5% | ⚠️ warning | 轻微重叠，建议修复 |
| = 0% | ✅ pass | 无重叠 |

### 文本溢出检测

额外检查文本内容是否超出文本框容量：

- 根据字号估算每行可容纳字符数
- 计算所需行数和高度
- 如果所需高度 > 可用高度 × 1.1，则报告溢出

| 溢出比 | 级别 | 说明 |
|--------|------|------|
| > 1.5 | ❌ error | 严重溢出 |
| > 1.1 | ⚠️ warning | 轻微溢出 |

### 修复策略

1. **缩小字号** — 减小 font_size_key 到更小的字号级别
2. **扩大文本框** — 调整 Zone 的 width/height
3. **减少内容** — 精简文字
4. **换用更紧凑的布局** — 如从 2x3 改为侧栏布局

---

## 2. 图片错位检测

### 检测项

#### 边界检测
检查图片是否超出幻灯片可视区域 (13.333" × 7.5")：

| 超出方向 | 允许偏差 | 级别 |
|----------|----------|------|
| 左侧超出 | -0.1" | ❌ error |
| 上方超出 | -0.1" | ❌ error |
| 右侧超出 | +0.1" | ❌ error |
| 下方超出 | +0.1" | ⚠️ warning |

> **注**: 有意的出血设计（图片边缘超出幻灯片）在封面背景中是允许的。

#### 尺寸检测
检查图片是否过小：

| 条件 | 级别 |
|------|------|
| width < 0.3" 或 height < 0.3" | ⚠️ warning |

### 修复策略

1. **调整坐标** — 修改 Zone 的 left/top
2. **调整尺寸** — 修改 Zone 的 width/height
3. **检查图片裁切** — 确认 center_crop 逻辑正确

---

## 3. 比例形变检测

### 检测原理

对比图片的两个比例：
- **原始比例** = 图片文件的 width / height
- **嵌入比例** = PPTX 中 shape 的 width / height

### 判定规则

```
偏差 = |嵌入比例 - 原始比例| / 原始比例
```

| 偏差 | 级别 | 说明 |
|------|------|------|
| > 10% | ❌ error | 严重形变，图片被拉伸 |
| > 2% 且 ≤ 10% | ⚠️ warning | 轻微形变 |
| ≤ 2% | ✅ pass | 比例正常 |

### 修复策略

1. **居中裁切** — 使用 `image_manager.fill_image(crop_to_fit=True)` 裁切图片到目标比例
2. **重新选择比例** — 选择与占位区域更匹配的标准比例
3. **调整占位区域** — 修改 Zone 的 width/height 以匹配图片原始比例

---

## 阈值配置

所有阈值可在 `validator.py` 头部修改：

```python
TEXT_OVERLAP_IOU_THRESHOLD = 0.05   # 文本框重叠 IoU 阈值
POSITION_DEVIATION_INCHES = 0.1     # 位置偏差阈值（英寸）
ASPECT_RATIO_TOLERANCE = 0.02       # 比例偏差容忍度 (2%)
```

## 校验报告格式

```json
{
  "passed": true,
  "total_issues": 2,
  "errors": [],
  "warnings": [
    {
      "category": "text_overflow",
      "message": "文本框 'item_3' 内容可能溢出",
      "element": "item_3",
      "details": {"overflow_ratio": 1.15}
    }
  ],
  "suggestions": [
    {
      "category": "aspect_distortion",
      "message": "无法检测图片 'bg_image' 的原始比例"
    }
  ]
}
```
