"""
风格主题定义模块
提供多种美术风格的颜色方案、字体方案、装饰元素和生图提示词。
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ColorPalette:
    """颜色方案"""
    primary: str          # 主色
    secondary: str        # 辅色
    accent: str           # 强调色
    background: str       # 背景色
    surface: str          # 表面色（卡片等）
    text_primary: str     # 主文字色
    text_secondary: str   # 辅文字色
    text_light: str       # 浅色文字（用于深色背景上）
    border: str           # 边框色
    gradient_start: str   # 渐变起始色
    gradient_end: str     # 渐变结束色


@dataclass
class FontConfig:
    """字体方案"""
    title_font: str           # 标题字体
    body_font: str            # 正文字体
    title_size_pt: int = 36   # 主标题字号
    subtitle_size_pt: int = 24  # 副标题字号
    heading_size_pt: int = 20   # 小标题字号
    body_size_pt: int = 14      # 正文字号
    caption_size_pt: int = 11   # 注释字号
    number_size_pt: int = 48    # 大数字字号
    title_bold: bool = True
    body_bold: bool = False


@dataclass
class DecoratorConfig:
    """装饰元素配置"""
    has_background_image: bool = False
    background_image_prompt: str = ""
    background_opacity: float = 0.3
    has_gradient_overlay: bool = False
    has_geometric_shapes: bool = False
    has_wave_decoration: bool = False
    has_line_decorations: bool = False
    corner_radius: int = 0           # 卡片圆角(px), 0=直角
    shadow_enabled: bool = False
    icon_style: str = "outlined"     # outlined | filled | minimal


@dataclass
class StyleTheme:
    """完整的风格主题"""
    name: str
    display_name: str
    description: str
    colors: ColorPalette
    fonts: FontConfig
    decorators: DecoratorConfig
    image_prompt_suffix: str = ""    # 生图时附加的风格提示词


# ============================================================
# 预设风格主题
# ============================================================

BUSINESS_BLUE = StyleTheme(
    name="business_blue",
    display_name="商务蓝",
    description="蓝灰色系商务风格，搭配山脉/城市背景，简洁专业",
    colors=ColorPalette(
        primary="#3D6B8E",
        secondary="#5A8BA8",
        accent="#2C5F7C",
        background="#F5F7FA",
        surface="#FFFFFF",
        text_primary="#2D3748",
        text_secondary="#4A5568",
        text_light="#FFFFFF",
        border="#CBD5E0",
        gradient_start="#3D6B8E",
        gradient_end="#5A8BA8",
    ),
    fonts=FontConfig(
        title_font="微软雅黑",
        body_font="微软雅黑",
        title_size_pt=36,
        subtitle_size_pt=20,
        heading_size_pt=18,
        body_size_pt=12,
        number_size_pt=48,
    ),
    decorators=DecoratorConfig(
        has_background_image=True,
        background_image_prompt="majestic snow-capped mountain range with blue sky, professional photography",
        background_opacity=0.25,
        has_gradient_overlay=True,
        has_line_decorations=True,
        corner_radius=4,
        shadow_enabled=True,
        icon_style="outlined",
    ),
    image_prompt_suffix="professional corporate style, blue-grey color palette, clean and elegant, high quality",
)

NATURE_GREEN = StyleTheme(
    name="nature_green",
    display_name="水墨绿",
    description="绿色水墨风格，中国风山水元素，文雅大气",
    colors=ColorPalette(
        primary="#5B7B5B",
        secondary="#7A9A7A",
        accent="#4A6A4A",
        background="#F8FAF5",
        surface="#FFFFFF",
        text_primary="#2D3B2D",
        text_secondary="#4A5B4A",
        text_light="#FFFFFF",
        border="#C5D5C0",
        gradient_start="#5B7B5B",
        gradient_end="#A8C8A0",
    ),
    fonts=FontConfig(
        title_font="微软雅黑",
        body_font="微软雅黑",
        title_size_pt=36,
        subtitle_size_pt=20,
        heading_size_pt=18,
        body_size_pt=12,
        number_size_pt=48,
    ),
    decorators=DecoratorConfig(
        has_background_image=True,
        background_image_prompt="Chinese ink wash painting style green mountains with flowing clouds, traditional art",
        background_opacity=0.2,
        has_gradient_overlay=True,
        has_wave_decoration=True,
        corner_radius=0,
        icon_style="minimal",
    ),
    image_prompt_suffix="Chinese ink wash painting style, green tones, elegant and traditional, artistic",
)

TECH_DARK = StyleTheme(
    name="tech_dark",
    display_name="科技暗黑",
    description="深色科技风格，渐变光效和几何图形，现代感强",
    colors=ColorPalette(
        primary="#6C63FF",
        secondary="#4ECDC4",
        accent="#FF6B6B",
        background="#0F0F1A",
        surface="#1A1A2E",
        text_primary="#E8E8F0",
        text_secondary="#A0A0B8",
        text_light="#FFFFFF",
        border="#2A2A3E",
        gradient_start="#6C63FF",
        gradient_end="#4ECDC4",
    ),
    fonts=FontConfig(
        title_font="微软雅黑",
        body_font="微软雅黑",
        title_size_pt=40,
        subtitle_size_pt=22,
        heading_size_pt=18,
        body_size_pt=13,
        number_size_pt=52,
    ),
    decorators=DecoratorConfig(
        has_gradient_overlay=True,
        has_geometric_shapes=True,
        corner_radius=12,
        shadow_enabled=True,
        icon_style="filled",
    ),
    image_prompt_suffix="futuristic dark tech style, neon glow effects, geometric shapes, modern digital art",
)

MINIMAL_LIGHT = StyleTheme(
    name="minimal_light",
    display_name="极简白",
    description="极简主义白色风格，大量留白，细线条，优雅干净",
    colors=ColorPalette(
        primary="#333333",
        secondary="#666666",
        accent="#E74C3C",
        background="#FAFAFA",
        surface="#FFFFFF",
        text_primary="#1A1A1A",
        text_secondary="#666666",
        text_light="#FFFFFF",
        border="#E0E0E0",
        gradient_start="#FAFAFA",
        gradient_end="#F0F0F0",
    ),
    fonts=FontConfig(
        title_font="微软雅黑",
        body_font="微软雅黑",
        title_size_pt=38,
        subtitle_size_pt=18,
        heading_size_pt=16,
        body_size_pt=12,
        number_size_pt=56,
        title_bold=False,
    ),
    decorators=DecoratorConfig(
        has_line_decorations=True,
        corner_radius=0,
        icon_style="outlined",
    ),
    image_prompt_suffix="minimalist clean style, white background, elegant simplicity, modern design",
)

WARM_CORPORATE = StyleTheme(
    name="warm_corporate",
    display_name="暖色商务",
    description="温暖色调商务风格，亲和力强，适合团队和文化主题",
    colors=ColorPalette(
        primary="#C08552",
        secondary="#D4A574",
        accent="#8B5E3C",
        background="#FDF8F3",
        surface="#FFFFFF",
        text_primary="#3D2B1F",
        text_secondary="#6B4F3A",
        text_light="#FFFFFF",
        border="#E6D5C3",
        gradient_start="#C08552",
        gradient_end="#D4A574",
    ),
    fonts=FontConfig(
        title_font="微软雅黑",
        body_font="微软雅黑",
        title_size_pt=36,
        subtitle_size_pt=20,
        heading_size_pt=18,
        body_size_pt=12,
        number_size_pt=48,
    ),
    decorators=DecoratorConfig(
        has_gradient_overlay=True,
        corner_radius=8,
        shadow_enabled=True,
        icon_style="filled",
    ),
    image_prompt_suffix="warm corporate style, golden brown tones, friendly and professional, high quality",
)

GRADIENT_MODERN = StyleTheme(
    name="gradient_modern",
    display_name="渐变现代",
    description="多彩渐变现代风格，玻璃态设计，适合产品和营销",
    colors=ColorPalette(
        primary="#7F5AF0",
        secondary="#2CB67D",
        accent="#FF8906",
        background="#16161A",
        surface="rgba(255,255,255,0.08)",
        text_primary="#FFFFFE",
        text_secondary="#94A1B2",
        text_light="#FFFFFE",
        border="rgba(255,255,255,0.12)",
        gradient_start="#7F5AF0",
        gradient_end="#2CB67D",
    ),
    fonts=FontConfig(
        title_font="微软雅黑",
        body_font="微软雅黑",
        title_size_pt=42,
        subtitle_size_pt=22,
        heading_size_pt=18,
        body_size_pt=13,
        number_size_pt=52,
    ),
    decorators=DecoratorConfig(
        has_gradient_overlay=True,
        has_geometric_shapes=True,
        corner_radius=16,
        shadow_enabled=True,
        icon_style="filled",
    ),
    image_prompt_suffix="modern gradient style, vibrant colors, glassmorphism, premium digital design",
)


# ============================================================
# 风格注册表
# ============================================================

THEME_REGISTRY: dict[str, StyleTheme] = {
    "business_blue": BUSINESS_BLUE,
    "nature_green": NATURE_GREEN,
    "tech_dark": TECH_DARK,
    "minimal_light": MINIMAL_LIGHT,
    "warm_corporate": WARM_CORPORATE,
    "gradient_modern": GRADIENT_MODERN,
}

# 内容类型 → 推荐风格映射
AUTO_STYLE_MAP: dict[str, str] = {
    "cover": "business_blue",
    "content": "business_blue",
    "data": "tech_dark",
    "mixed": "warm_corporate",
    "comparison": "minimal_light",
    "timeline": "nature_green",
}


def get_theme(name: str) -> StyleTheme:
    """获取指定名称的风格主题"""
    if name not in THEME_REGISTRY:
        raise ValueError(
            f"未知的风格主题: {name}。"
            f"可选项: {list(THEME_REGISTRY.keys())}"
        )
    return THEME_REGISTRY[name]


def get_auto_theme(page_type: str) -> StyleTheme:
    """根据页面类型自动推荐风格主题"""
    theme_name = AUTO_STYLE_MAP.get(page_type, "business_blue")
    return THEME_REGISTRY[theme_name]


def list_themes() -> list[dict]:
    """列出所有可用风格主题"""
    return [
        {
            "name": t.name,
            "display_name": t.display_name,
            "description": t.description,
        }
        for t in THEME_REGISTRY.values()
    ]
