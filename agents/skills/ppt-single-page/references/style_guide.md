# 美术风格参考文档

## 风格总览

| 风格 | 色系 | 适合场景 | 关键词 |
|------|------|---------|--------|
| business_blue | 蓝灰色 | 年度汇报、商务报告 | 专业、稳重、清晰 |
| nature_green | 绿色水墨 | 工作总结、文化主题 | 文雅、自然、大气 |
| tech_dark | 深色科技 | 技术方案、产品发布 | 现代、科技、酷炫 |
| minimal_light | 极简白 | 简约风格、创意展示 | 干净、优雅、留白 |
| warm_corporate | 暖色商务 | 团队建设、文化宣传 | 温暖、亲和、专业 |
| gradient_modern | 渐变现代 | 产品展示、市场营销 | 活力、时尚、高级 |

---

## 1. business_blue — 商务蓝

### 配色方案
- 主色: `#3D6B8E` (深蓝灰)
- 辅色: `#5A8BA8` (中蓝)
- 强调色: `#2C5F7C` (深蓝)
- 背景: `#F5F7FA` (浅灰白)
- 文字主色: `#2D3748`
- 文字辅色: `#4A5568`

### 装饰特点
- 山脉/城市天际线背景图
- 简洁的线条分隔
- 轻微阴影和圆角卡片
- 带编号的小图标

### 生图提示词模板
```
{内容描述}, professional corporate style, blue-grey color palette,
clean and elegant, high quality photography, soft lighting
```

### 字体搭配
- 标题: 微软雅黑 Bold 36pt
- 正文: 微软雅黑 Regular 12pt

---

## 2. nature_green — 水墨绿

### 配色方案
- 主色: `#5B7B5B` (苍绿)
- 辅色: `#7A9A7A` (浅绿)
- 背景: `#F8FAF5` (米白)
- 文字主色: `#2D3B2D`

### 装饰特点
- 中国风水墨山水背景
- 波浪流线装饰
- 直角设计（无圆角）
- 极简图标风格

### 生图提示词模板
```
{内容描述}, Chinese ink wash painting style, green tones,
elegant and traditional, artistic, soft watercolor effect
```

---

## 3. tech_dark — 科技暗黑

### 配色方案
- 主色: `#6C63FF` (紫蓝)
- 辅色: `#4ECDC4` (青绿)
- 强调色: `#FF6B6B` (暖红)
- 背景: `#0F0F1A` (深黑)
- 表面色: `#1A1A2E`

### 装饰特点
- 渐变光效
- 几何图形装饰
- 大圆角 (12px)
- 阴影效果
- 填充式图标

### 生图提示词模板
```
{内容描述}, futuristic dark tech style, neon glow effects,
geometric shapes, modern digital art, dark background
```

---

## 4. minimal_light — 极简白

### 配色方案
- 主色: `#333333` (深灰)
- 辅色: `#666666` (中灰)
- 强调色: `#E74C3C` (红色点缀)
- 背景: `#FAFAFA` (纯白)

### 装饰特点
- 大量留白
- 细线条分隔
- 直角设计
- 线框图标
- 非粗体标题

### 生图提示词模板
```
{内容描述}, minimalist clean style, white background,
elegant simplicity, modern design, high contrast
```

---

## 5. warm_corporate — 暖色商务

### 配色方案
- 主色: `#C08552` (暖棕)
- 辅色: `#D4A574` (浅金)
- 背景: `#FDF8F3` (暖白)
- 文字主色: `#3D2B1F`

### 装饰特点
- 温暖渐变
- 中等圆角 (8px)
- 阴影效果
- 填充式图标

### 生图提示词模板
```
{内容描述}, warm corporate style, golden brown tones,
friendly and professional, high quality, natural lighting
```

---

## 6. gradient_modern — 渐变现代

### 配色方案
- 主色: `#7F5AF0` (紫色)
- 辅色: `#2CB67D` (翠绿)
- 强调色: `#FF8906` (橙色)
- 背景: `#16161A` (深黑)

### 装饰特点
- 多彩渐变
- 几何图形
- 大圆角 (16px)
- 玻璃态效果
- 填充式图标

### 生图提示词模板
```
{内容描述}, modern gradient style, vibrant colors,
glassmorphism, premium digital design, colorful
```

---

## 风格自动推荐规则

| 内容类型 | 推荐风格 |
|---------|---------|
| cover (封面) | business_blue |
| content (内容) | business_blue |
| data (数据) | tech_dark |
| mixed (混合) | warm_corporate |
| comparison (对比) | minimal_light |
| timeline (时间轴) | nature_green |

---

## AI 生图参数规范与避坑指南

> [!WARNING]
> 调用 ImageGen / 生图模型时，`size` 参数**必须传显式像素尺寸**（如 `1440x2560`）或命名尺寸（`2K`/`3K`/`4K`），**绝对不可传入 `"3:4"` 或 `"16:9"` 这种比例字符串**，否则会导致 `IMAGE_SIZE_INVALID`。

### 常用比例与 ImageGen 像素对照

| 期望比例 | ImageGen `size` 传参 | 常见适用场景 |
|:---|:---|:---|
| **1:1** | `2048x2048` | 方形产品特写、徽标、头像 |
| **3:4** | `1920x2560` | 竖向人物立绘、海报型展示图 |
| **4:3** | `2560x1920` | 传统配图、插画 |
| **9:16** | `1440x2560` | 移动端界面、手机长幅海报 |
| **16:9** | `2560x1440` | 宽屏全幅背景、科技全景大图 |
| **2:3** | `1706x2560` | 竖向海报摄影 |
| **3:2** | `2560x1706` | 横向摄影风景图 |

