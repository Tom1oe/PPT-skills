"""
布局引擎模块
提供 10+ 种预设布局模板，每种布局由一组 Zone 组成。
所有坐标基于 13.333" × 7.5" 标准 16:9 宽屏幻灯片。
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


# 幻灯片标准尺寸（英寸）
SLIDE_WIDTH = 13.333
SLIDE_HEIGHT = 7.5

# 标准边距
MARGIN_LEFT = 0.6
MARGIN_RIGHT = 0.6
MARGIN_TOP = 0.5
MARGIN_BOTTOM = 0.4

# 内容区域
CONTENT_LEFT = MARGIN_LEFT
CONTENT_WIDTH = SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
CONTENT_TOP = MARGIN_TOP
CONTENT_HEIGHT = SLIDE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM


class ZoneType(Enum):
    TEXT = "text"
    IMAGE = "image"
    CHART = "chart"
    ICON = "icon"
    DECORATOR = "decorator"
    NUMBER = "number"
    BACKGROUND = "background"


class TextAlign(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class VerticalAlign(Enum):
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"


@dataclass
class Zone:
    """布局区域定义"""
    id: str                                # 唯一标识
    zone_type: ZoneType                    # 区域类型
    left: float                            # 左边距（英寸）
    top: float                             # 上边距（英寸）
    width: float                           # 宽度（英寸）
    height: float                          # 高度（英寸）
    z_order: int = 0                       # 层级（越大越在上面）
    aspect_ratio: Optional[str] = None     # 图片目标比例
    text_align: TextAlign = TextAlign.LEFT
    vertical_align: VerticalAlign = VerticalAlign.TOP
    font_size_key: str = "body"            # title|subtitle|heading|body|caption|number
    is_bold: Optional[bool] = None
    color_key: str = "text_primary"        # 引用 ColorPalette 中的颜色键
    content_key: str = ""                  # 映射到输入内容中的字段
    placeholder_label: str = ""            # 占位文字


@dataclass
class LayoutTemplate:
    """布局模板"""
    name: str
    display_name: str
    description: str
    page_types: list[str]                  # 适用的页面类型
    zones: list[Zone] = field(default_factory=list)
    min_items: int = 0                     # 最少内容项数
    max_items: int = 99                    # 最多内容项数


# ============================================================
# 预设布局模板
# ============================================================

def _cover_fullimage() -> LayoutTemplate:
    """封面页 — 全幅背景图 + 居中标题"""
    return LayoutTemplate(
        name="cover_fullimage",
        display_name="全幅封面",
        description="全幅背景图片 + 大标题居中，适合章节首页",
        page_types=["cover"],
        zones=[
            Zone(id="bg_image", zone_type=ZoneType.BACKGROUND,
                 left=0, top=0, width=SLIDE_WIDTH, height=SLIDE_HEIGHT,
                 z_order=0, aspect_ratio="16:9", content_key="background_image"),
            Zone(id="overlay", zone_type=ZoneType.DECORATOR,
                 left=0, top=0, width=SLIDE_WIDTH, height=SLIDE_HEIGHT,
                 z_order=1),
            Zone(id="section_number", zone_type=ZoneType.NUMBER,
                 left=SLIDE_WIDTH * 0.55, top=1.5, width=3.0, height=2.0,
                 z_order=2, font_size_key="number", color_key="text_light",
                 text_align=TextAlign.RIGHT, content_key="section_number"),
            Zone(id="title", zone_type=ZoneType.TEXT,
                 left=SLIDE_WIDTH * 0.35, top=3.0, width=5.5, height=1.5,
                 z_order=3, font_size_key="title", color_key="text_light",
                 text_align=TextAlign.CENTER, content_key="title"),
            Zone(id="subtitle", zone_type=ZoneType.TEXT,
                 left=SLIDE_WIDTH * 0.35, top=4.5, width=5.5, height=0.8,
                 z_order=3, font_size_key="caption", color_key="text_light",
                 text_align=TextAlign.CENTER, content_key="subtitle"),
        ],
    )


def _cover_split() -> LayoutTemplate:
    """封面页 — 左图右文分割布局"""
    split = SLIDE_WIDTH * 0.5
    return LayoutTemplate(
        name="cover_split",
        display_name="分割封面",
        description="左侧大图 + 右侧标题文字，适合年度报告首页",
        page_types=["cover"],
        zones=[
            Zone(id="left_image", zone_type=ZoneType.IMAGE,
                 left=0, top=0, width=split, height=SLIDE_HEIGHT,
                 z_order=0, content_key="hero_image"),
            Zone(id="decorative_text_top", zone_type=ZoneType.TEXT,
                 left=split + 0.5, top=0.8, width=4.0, height=1.0,
                 z_order=2, font_size_key="subtitle", color_key="text_secondary",
                 content_key="decorative_text"),
            Zone(id="section_number", zone_type=ZoneType.NUMBER,
                 left=split + 4.5, top=1.8, width=2.0, height=1.5,
                 z_order=1, font_size_key="number", color_key="primary",
                 text_align=TextAlign.RIGHT, content_key="section_number"),
            Zone(id="title", zone_type=ZoneType.TEXT,
                 left=split + 0.8, top=3.5, width=5.0, height=1.5,
                 z_order=2, font_size_key="title", color_key="text_primary",
                 content_key="title"),
            Zone(id="subtitle", zone_type=ZoneType.TEXT,
                 left=split + 0.8, top=5.0, width=5.0, height=0.6,
                 z_order=2, font_size_key="caption", color_key="text_secondary",
                 content_key="subtitle"),
            Zone(id="bottom_text", zone_type=ZoneType.TEXT,
                 left=split + 0.8, top=5.8, width=4.0, height=1.0,
                 z_order=2, font_size_key="caption", color_key="text_secondary",
                 content_key="footer_text"),
        ],
    )


def _content_sidebar() -> LayoutTemplate:
    """内容页 — 左侧窄栏 + 右侧主内容区"""
    sidebar_w = 3.5
    return LayoutTemplate(
        name="content_sidebar",
        display_name="侧栏内容页",
        description="左侧图片/装饰 + 右侧文字内容列表",
        page_types=["content", "mixed"],
        zones=[
            Zone(id="sidebar_image", zone_type=ZoneType.IMAGE,
                 left=0.4, top=1.5, width=3.0, height=4.0,
                 z_order=1, aspect_ratio="3:4", content_key="sidebar_image"),
            Zone(id="page_number", zone_type=ZoneType.TEXT,
                 left=0.5, top=0.3, width=0.8, height=0.5,
                 z_order=2, font_size_key="heading", color_key="primary",
                 content_key="page_number"),
            Zone(id="page_title", zone_type=ZoneType.TEXT,
                 left=1.5, top=0.3, width=5.0, height=0.6,
                 z_order=2, font_size_key="heading", color_key="text_primary",
                 content_key="title"),
            Zone(id="sidebar_title", zone_type=ZoneType.TEXT,
                 left=0.4, top=5.8, width=3.0, height=0.5,
                 z_order=2, font_size_key="heading", color_key="text_primary",
                 text_align=TextAlign.CENTER, content_key="sidebar_title"),
            Zone(id="sidebar_desc", zone_type=ZoneType.TEXT,
                 left=0.4, top=6.3, width=3.0, height=0.8,
                 z_order=2, font_size_key="caption", color_key="text_secondary",
                 text_align=TextAlign.CENTER, content_key="sidebar_desc"),
            # 右侧列表项（最多3个）
            Zone(id="item_1", zone_type=ZoneType.TEXT,
                 left=4.5, top=1.5, width=8.0, height=1.5,
                 z_order=2, font_size_key="body", color_key="text_primary",
                 content_key="items[0]"),
            Zone(id="item_2", zone_type=ZoneType.TEXT,
                 left=4.5, top=3.2, width=8.0, height=1.5,
                 z_order=2, font_size_key="body", color_key="text_primary",
                 content_key="items[1]"),
            Zone(id="item_3", zone_type=ZoneType.TEXT,
                 left=4.5, top=4.9, width=8.0, height=1.5,
                 z_order=2, font_size_key="body", color_key="text_primary",
                 content_key="items[2]"),
        ],
        min_items=1,
        max_items=3,
    )


def _content_grid_2x3() -> LayoutTemplate:
    """内容展示 — 2行×3列网格"""
    col_w = 3.6
    row_h = 2.6
    gap_x = 0.5
    gap_y = 0.4
    start_x = 0.8
    start_y = 1.4
    zones = [
        Zone(id="page_number", zone_type=ZoneType.TEXT,
             left=0.5, top=0.3, width=0.8, height=0.5,
             z_order=2, font_size_key="heading", color_key="primary",
             content_key="page_number"),
        Zone(id="page_title", zone_type=ZoneType.TEXT,
             left=1.5, top=0.3, width=6.0, height=0.6,
             z_order=2, font_size_key="heading", color_key="text_primary",
             content_key="title"),
    ]
    for row in range(2):
        for col in range(3):
            idx = row * 3 + col
            x = start_x + col * (col_w + gap_x)
            y = start_y + row * (row_h + gap_y)
            zones.extend([
                Zone(id=f"card_{idx}_number", zone_type=ZoneType.NUMBER,
                     left=x, top=y, width=0.8, height=0.5,
                     z_order=3, font_size_key="heading", color_key="primary",
                     content_key=f"items[{idx}].number"),
                Zone(id=f"card_{idx}_title", zone_type=ZoneType.TEXT,
                     left=x + 0.9, top=y, width=col_w - 1.0, height=0.5,
                     z_order=3, font_size_key="heading", color_key="text_primary",
                     content_key=f"items[{idx}].title"),
                Zone(id=f"card_{idx}_desc", zone_type=ZoneType.TEXT,
                     left=x, top=y + 0.6, width=col_w, height=row_h - 0.8,
                     z_order=3, font_size_key="body", color_key="text_secondary",
                     content_key=f"items[{idx}].description"),
                Zone(id=f"card_{idx}_icon", zone_type=ZoneType.ICON,
                     left=x + col_w - 0.8, top=y + row_h - 0.8, width=0.6, height=0.6,
                     z_order=3, aspect_ratio="1:1",
                     content_key=f"items[{idx}].icon"),
            ])
    return LayoutTemplate(
        name="content_grid_2x3",
        display_name="六宫格内容页",
        description="2行×3列网格布局，每格含编号+标题+描述+图标",
        page_types=["content"],
        zones=zones,
        min_items=3,
        max_items=6,
    )


def _content_centered() -> LayoutTemplate:
    """内容页 — 中心环形/辐射状布局"""
    cx, cy = SLIDE_WIDTH / 2, SLIDE_HEIGHT / 2 + 0.3
    r = 2.5
    import math
    zones = [
        Zone(id="page_number", zone_type=ZoneType.TEXT,
             left=0.5, top=0.3, width=0.8, height=0.5,
             z_order=2, font_size_key="heading", color_key="primary",
             content_key="page_number"),
        Zone(id="page_title", zone_type=ZoneType.TEXT,
             left=1.5, top=0.3, width=6.0, height=0.6,
             z_order=2, font_size_key="heading", color_key="text_primary",
             content_key="title"),
        # 中心圆
        Zone(id="center_circle", zone_type=ZoneType.DECORATOR,
             left=cx - 1.2, top=cy - 1.2, width=2.4, height=2.4,
             z_order=2),
        Zone(id="center_title", zone_type=ZoneType.TEXT,
             left=cx - 1.0, top=cy - 0.4, width=2.0, height=0.8,
             z_order=3, font_size_key="heading", color_key="primary",
             text_align=TextAlign.CENTER, content_key="center_title"),
    ]
    # 6个周围要点（环形分布）
    for i in range(6):
        angle = math.radians(-90 + i * 60)
        px = cx + r * math.cos(angle) - 1.2
        py = cy + r * math.sin(angle) - 0.5
        zones.extend([
            Zone(id=f"point_{i}_title", zone_type=ZoneType.TEXT,
                 left=px, top=py, width=2.4, height=0.4,
                 z_order=3, font_size_key="body", color_key="text_primary",
                 text_align=TextAlign.CENTER, is_bold=True,
                 content_key=f"items[{i}].title"),
            Zone(id=f"point_{i}_desc", zone_type=ZoneType.TEXT,
                 left=px, top=py + 0.4, width=2.4, height=0.6,
                 z_order=3, font_size_key="caption", color_key="text_secondary",
                 text_align=TextAlign.CENTER,
                 content_key=f"items[{i}].description"),
        ])
    return LayoutTemplate(
        name="content_centered",
        display_name="环形辐射页",
        description="中心主题 + 周围6个要点环形分布",
        page_types=["content"],
        zones=zones,
        min_items=3,
        max_items=6,
    )


def _data_chart() -> LayoutTemplate:
    """数据展示 — 左文右图表"""
    return LayoutTemplate(
        name="data_chart",
        display_name="图表展示页",
        description="左侧文字说明 + 右侧数据图表",
        page_types=["data"],
        zones=[
            Zone(id="page_number", zone_type=ZoneType.TEXT,
                 left=0.5, top=0.3, width=0.8, height=0.5,
                 z_order=2, font_size_key="heading", color_key="primary",
                 content_key="page_number"),
            Zone(id="page_title", zone_type=ZoneType.TEXT,
                 left=1.5, top=0.3, width=6.0, height=0.6,
                 z_order=2, font_size_key="heading", color_key="text_primary",
                 content_key="title"),
            Zone(id="text_block", zone_type=ZoneType.TEXT,
                 left=0.8, top=1.5, width=5.5, height=5.0,
                 z_order=2, font_size_key="body", color_key="text_primary",
                 content_key="description"),
            Zone(id="chart_area", zone_type=ZoneType.CHART,
                 left=7.0, top=1.2, width=5.5, height=5.5,
                 z_order=2, aspect_ratio="1:1",
                 content_key="chart"),
        ],
    )


def _data_stats() -> LayoutTemplate:
    """数据统计 — 多个统计卡片"""
    zones = [
        Zone(id="page_number", zone_type=ZoneType.TEXT,
             left=0.5, top=0.3, width=0.8, height=0.5,
             z_order=2, font_size_key="heading", color_key="primary",
             content_key="page_number"),
        Zone(id="page_title", zone_type=ZoneType.TEXT,
             left=1.5, top=0.3, width=6.0, height=0.6,
             z_order=2, font_size_key="heading", color_key="text_primary",
             content_key="title"),
        Zone(id="text_block_1", zone_type=ZoneType.TEXT,
             left=0.8, top=1.3, width=5.5, height=1.8,
             z_order=2, font_size_key="body", color_key="text_primary",
             content_key="items[0]"),
        Zone(id="text_block_2", zone_type=ZoneType.TEXT,
             left=0.8, top=3.8, width=5.5, height=1.8,
             z_order=2, font_size_key="body", color_key="text_primary",
             content_key="items[1]"),
    ]
    # 右侧2个统计环形图
    for i in range(2):
        x = 7.5 + i * 3.0
        zones.extend([
            Zone(id=f"stat_{i}_chart", zone_type=ZoneType.CHART,
                 left=x, top=2.0, width=2.2, height=2.2,
                 z_order=2, aspect_ratio="1:1",
                 content_key=f"stats[{i}].chart"),
            Zone(id=f"stat_{i}_value", zone_type=ZoneType.TEXT,
                 left=x, top=4.4, width=2.2, height=0.6,
                 z_order=3, font_size_key="heading", color_key="primary",
                 text_align=TextAlign.CENTER,
                 content_key=f"stats[{i}].value"),
            Zone(id=f"stat_{i}_label", zone_type=ZoneType.TEXT,
                 left=x, top=5.0, width=2.2, height=0.5,
                 z_order=3, font_size_key="caption", color_key="text_secondary",
                 text_align=TextAlign.CENTER,
                 content_key=f"stats[{i}].label"),
        ])
    return LayoutTemplate(
        name="data_stats",
        display_name="数据统计页",
        description="左侧文字 + 右侧环形统计图卡片",
        page_types=["data"],
        zones=zones,
        min_items=1,
        max_items=2,
    )


def _content_grid_2x2() -> LayoutTemplate:
    """内容展示 — 2行×2列大卡片"""
    col_w = 5.5
    row_h = 2.8
    gap_x = 0.8
    gap_y = 0.4
    start_x = 0.8
    start_y = 1.4
    zones = [
        Zone(id="page_title", zone_type=ZoneType.TEXT,
             left=0.8, top=0.3, width=8.0, height=0.7,
             z_order=2, font_size_key="heading", color_key="text_primary",
             content_key="title"),
    ]
    for row in range(2):
        for col in range(2):
            idx = row * 2 + col
            x = start_x + col * (col_w + gap_x)
            y = start_y + row * (row_h + gap_y)
            zones.extend([
                Zone(id=f"card_{idx}_image", zone_type=ZoneType.IMAGE,
                     left=x, top=y, width=2.2, height=2.2,
                     z_order=2, aspect_ratio="1:1",
                     content_key=f"items[{idx}].image"),
                Zone(id=f"card_{idx}_title", zone_type=ZoneType.TEXT,
                     left=x + 2.5, top=y + 0.2, width=2.8, height=0.5,
                     z_order=3, font_size_key="heading", color_key="primary",
                     content_key=f"items[{idx}].title"),
                Zone(id=f"card_{idx}_desc", zone_type=ZoneType.TEXT,
                     left=x + 2.5, top=y + 0.8, width=2.8, height=1.8,
                     z_order=3, font_size_key="body", color_key="text_secondary",
                     content_key=f"items[{idx}].description"),
            ])
    return LayoutTemplate(
        name="content_grid_2x2",
        display_name="四宫格内容页",
        description="2行×2列大卡片，含图片+标题+描述",
        page_types=["content", "mixed"],
        zones=zones,
        min_items=2,
        max_items=4,
    )


def _timeline() -> LayoutTemplate:
    """时间轴布局"""
    zones = [
        Zone(id="page_title", zone_type=ZoneType.TEXT,
             left=0.8, top=0.3, width=8.0, height=0.7,
             z_order=2, font_size_key="heading", color_key="text_primary",
             content_key="title"),
        # 水平时间轴线
        Zone(id="timeline_line", zone_type=ZoneType.DECORATOR,
             left=0.8, top=3.6, width=11.7, height=0.06,
             z_order=1),
    ]
    # 最多5个节点
    for i in range(5):
        x = 1.2 + i * 2.4
        y_above = 1.5
        y_below = 4.0
        # 奇偶交错上下
        if i % 2 == 0:
            text_y, text_h = y_above, 1.8
        else:
            text_y, text_h = y_below, 1.8
        zones.extend([
            Zone(id=f"node_{i}_dot", zone_type=ZoneType.DECORATOR,
                 left=x + 0.8, top=3.4, width=0.4, height=0.4,
                 z_order=3),
            Zone(id=f"node_{i}_title", zone_type=ZoneType.TEXT,
                 left=x, top=text_y, width=2.0, height=0.5,
                 z_order=3, font_size_key="body", color_key="primary",
                 text_align=TextAlign.CENTER, is_bold=True,
                 content_key=f"items[{i}].title"),
            Zone(id=f"node_{i}_desc", zone_type=ZoneType.TEXT,
                 left=x, top=text_y + 0.5, width=2.0, height=text_h - 0.5,
                 z_order=3, font_size_key="caption", color_key="text_secondary",
                 text_align=TextAlign.CENTER,
                 content_key=f"items[{i}].description"),
        ])
    return LayoutTemplate(
        name="timeline",
        display_name="时间轴页",
        description="水平时间轴，节点上下交错",
        page_types=["timeline"],
        zones=zones,
        min_items=3,
        max_items=5,
    )


def _comparison() -> LayoutTemplate:
    """对比布局 — 左右对比"""
    half_w = (SLIDE_WIDTH - 2.0) / 2
    return LayoutTemplate(
        name="comparison",
        display_name="对比页",
        description="左右对比两栏布局",
        page_types=["comparison"],
        zones=[
            Zone(id="page_title", zone_type=ZoneType.TEXT,
                 left=0.8, top=0.3, width=11.0, height=0.7,
                 z_order=2, font_size_key="heading", color_key="text_primary",
                 text_align=TextAlign.CENTER, content_key="title"),
            Zone(id="divider", zone_type=ZoneType.DECORATOR,
                 left=SLIDE_WIDTH / 2 - 0.03, top=1.3, width=0.06, height=5.5,
                 z_order=1),
            # 左栏
            Zone(id="left_image", zone_type=ZoneType.IMAGE,
                 left=0.8, top=1.3, width=half_w - 0.5, height=2.5,
                 z_order=2, aspect_ratio="16:9", content_key="left.image"),
            Zone(id="left_title", zone_type=ZoneType.TEXT,
                 left=0.8, top=4.0, width=half_w - 0.5, height=0.5,
                 z_order=2, font_size_key="heading", color_key="primary",
                 text_align=TextAlign.CENTER, content_key="left.title"),
            Zone(id="left_desc", zone_type=ZoneType.TEXT,
                 left=0.8, top=4.6, width=half_w - 0.5, height=2.2,
                 z_order=2, font_size_key="body", color_key="text_secondary",
                 content_key="left.description"),
            # 右栏
            Zone(id="right_image", zone_type=ZoneType.IMAGE,
                 left=SLIDE_WIDTH / 2 + 0.3, top=1.3, width=half_w - 0.5, height=2.5,
                 z_order=2, aspect_ratio="16:9", content_key="right.image"),
            Zone(id="right_title", zone_type=ZoneType.TEXT,
                 left=SLIDE_WIDTH / 2 + 0.3, top=4.0, width=half_w - 0.5, height=0.5,
                 z_order=2, font_size_key="heading", color_key="primary",
                 text_align=TextAlign.CENTER, content_key="right.title"),
            Zone(id="right_desc", zone_type=ZoneType.TEXT,
                 left=SLIDE_WIDTH / 2 + 0.3, top=4.6, width=half_w - 0.5, height=2.2,
                 z_order=2, font_size_key="body", color_key="text_secondary",
                 content_key="right.description"),
        ],
    )


def _section_divider() -> LayoutTemplate:
    """章节分隔页 — 大号编号 + 标题"""
    return LayoutTemplate(
        name="section_divider",
        display_name="章节分隔页",
        description="大号章节编号 + 标题 + 装饰背景，用于章节过渡",
        page_types=["cover"],
        zones=[
            Zone(id="bg_image", zone_type=ZoneType.BACKGROUND,
                 left=0, top=0, width=SLIDE_WIDTH, height=SLIDE_HEIGHT,
                 z_order=0, aspect_ratio="16:9", content_key="background_image"),
            Zone(id="overlay", zone_type=ZoneType.DECORATOR,
                 left=SLIDE_WIDTH * 0.5, top=0, width=SLIDE_WIDTH * 0.5, height=SLIDE_HEIGHT,
                 z_order=1),
            Zone(id="section_number", zone_type=ZoneType.NUMBER,
                 left=SLIDE_WIDTH * 0.6, top=2.0, width=4.0, height=2.5,
                 z_order=2, font_size_key="number", color_key="primary",
                 text_align=TextAlign.LEFT, content_key="section_number"),
            Zone(id="title", zone_type=ZoneType.TEXT,
                 left=SLIDE_WIDTH * 0.55, top=4.2, width=5.0, height=1.5,
                 z_order=2, font_size_key="title", color_key="text_primary",
                 content_key="title"),
            Zone(id="subtitle", zone_type=ZoneType.TEXT,
                 left=SLIDE_WIDTH * 0.55, top=5.7, width=5.0, height=0.8,
                 z_order=2, font_size_key="caption", color_key="text_secondary",
                 content_key="subtitle"),
        ],
    )


def _mixed_media() -> LayoutTemplate:
    """混合页 — 图文混排"""
    return LayoutTemplate(
        name="mixed_media",
        display_name="图文混排页",
        description="多图+多文本自由组合，适合内容丰富的页面",
        page_types=["mixed", "content"],
        zones=[
            Zone(id="page_title", zone_type=ZoneType.TEXT,
                 left=0.8, top=0.3, width=8.0, height=0.7,
                 z_order=2, font_size_key="heading", color_key="text_primary",
                 content_key="title"),
            Zone(id="text_block", zone_type=ZoneType.TEXT,
                 left=0.8, top=1.3, width=5.0, height=2.0,
                 z_order=2, font_size_key="body", color_key="text_primary",
                 content_key="description"),
            # 左下图
            Zone(id="image_1", zone_type=ZoneType.IMAGE,
                 left=0.8, top=3.8, width=3.5, height=3.0,
                 z_order=2, aspect_ratio="4:3", content_key="images[0]"),
            # 右上图
            Zone(id="image_2", zone_type=ZoneType.IMAGE,
                 left=6.5, top=1.3, width=6.0, height=3.0,
                 z_order=2, aspect_ratio="16:9", content_key="images[1]"),
            # 中部文字
            Zone(id="text_block_2", zone_type=ZoneType.TEXT,
                 left=4.8, top=3.8, width=3.5, height=3.0,
                 z_order=2, font_size_key="body", color_key="text_secondary",
                 content_key="text_block_2"),
            # 右下图标列表
            Zone(id="icon_list", zone_type=ZoneType.ICON,
                 left=8.8, top=4.8, width=3.7, height=2.0,
                 z_order=2, aspect_ratio="16:9",
                 content_key="icon_list"),
        ],
    )


def _catalog_grid() -> LayoutTemplate:
    """目录索引页 — 左侧竖排标题 + 右侧2x2章节网格"""
    return LayoutTemplate(
        name="catalog_grid",
        display_name="目录索引页",
        description="左侧竖排目录标题 + 右侧 4 个章节卡片，适合汇报目录",
        page_types=["catalog", "content"],
        min_items=2,
        max_items=4,
        zones=[
            Zone(id="left_bar", zone_type=ZoneType.DECORATOR,
                 left=1.0, top=1.2, width=1.6, height=5.0, z_order=0),
            Zone(id="catalog_title", zone_type=ZoneType.TEXT,
                 left=1.1, top=1.5, width=1.4, height=4.5,
                 z_order=1, font_size_key="title", color_key="text_primary",
                 text_align=TextAlign.CENTER, content_key="title"),
            # 2x2 章节卡片
            Zone(id="part_1", zone_type=ZoneType.TEXT,
                 left=3.8, top=1.5, width=4.0, height=2.0,
                 z_order=1, font_size_key="heading", color_key="text_primary",
                 content_key="items[0]"),
            Zone(id="part_2", zone_type=ZoneType.TEXT,
                 left=8.5, top=1.5, width=4.0, height=2.0,
                 z_order=1, font_size_key="heading", color_key="text_primary",
                 content_key="items[1]"),
            Zone(id="part_3", zone_type=ZoneType.TEXT,
                 left=3.8, top=4.0, width=4.0, height=2.0,
                 z_order=1, font_size_key="heading", color_key="text_primary",
                 content_key="items[2]"),
            Zone(id="part_4", zone_type=ZoneType.TEXT,
                 left=8.5, top=4.0, width=4.0, height=2.0,
                 z_order=1, font_size_key="heading", color_key="text_primary",
                 content_key="items[3]"),
        ],
    )


def _section_header() -> LayoutTemplate:
    """章节转场页 — 居中几何框架 + 实色标签 + 大章节标题"""
    return LayoutTemplate(
        name="section_header",
        display_name="章节转场页",
        description="几何框架 + 居中 PART 标签与大号章节标题，用于篇章过渡",
        page_types=["section", "cover"],
        zones=[
            Zone(id="center_box", zone_type=ZoneType.DECORATOR,
                 left=2.5, top=1.8, width=8.333, height=3.8, z_order=0),
            Zone(id="part_badge", zone_type=ZoneType.DECORATOR,
                 left=4.667, top=2.2, width=4.0, height=0.9, z_order=1),
            Zone(id="part_text", zone_type=ZoneType.TEXT,
                 left=4.667, top=2.25, width=4.0, height=0.8,
                 z_order=2, font_size_key="heading", color_key="text_light",
                 text_align=TextAlign.CENTER, content_key="section_number"),
            Zone(id="section_title", zone_type=ZoneType.TEXT,
                 left=2.667, top=3.4, width=8.0, height=1.6,
                 z_order=2, font_size_key="title", color_key="text_primary",
                 text_align=TextAlign.CENTER, content_key="title"),
        ],
    )


def _pyramid_hierarchy() -> LayoutTemplate:
    """金字塔层级页 — 左侧条目清单 + 右侧分层金字塔"""
    return LayoutTemplate(
        name="pyramid_hierarchy",
        display_name="金字塔层级页",
        description="左侧 3-4 个层级说明 + 右侧分层三角形金字塔，适合层级架构分析",
        page_types=["data", "content"],
        min_items=2,
        max_items=4,
        zones=[
            Zone(id="title", zone_type=ZoneType.TEXT,
                 left=0.8, top=0.5, width=10.0, height=0.8,
                 z_order=1, font_size_key="heading", color_key="text_primary",
                 content_key="title"),
            # 左侧条目
            Zone(id="level_1", zone_type=ZoneType.TEXT,
                 left=0.8, top=1.8, width=5.5, height=1.3,
                 z_order=1, font_size_key="body", color_key="text_primary",
                 content_key="items[0]"),
            Zone(id="level_2", zone_type=ZoneType.TEXT,
                 left=0.8, top=3.4, width=5.5, height=1.3,
                 z_order=1, font_size_key="body", color_key="text_primary",
                 content_key="items[1]"),
            Zone(id="level_3", zone_type=ZoneType.TEXT,
                 left=0.8, top=5.0, width=5.5, height=1.3,
                 z_order=1, font_size_key="body", color_key="text_primary",
                 content_key="items[2]"),
            # 右侧金字塔图元
            Zone(id="pyramid_chart", zone_type=ZoneType.CHART,
                 left=7.4, top=1.6, width=5.0, height=5.0,
                 z_order=1, aspect_ratio="1:1", content_key="pyramid"),
        ],
    )


def _central_radial_lightbulb() -> LayoutTemplate:
    """中心发散/思维脑图页 — 中心核心主题 + 四角发散要点"""
    return LayoutTemplate(
        name="central_radial_lightbulb",
        display_name="思维发散中枢页",
        description="中心核心概念/灯泡/问号 + 四周 4 个节点连线发散，适合问题拆解与根因分析",
        page_types=["content", "data"],
        min_items=3,
        max_items=4,
        zones=[
            Zone(id="title", zone_type=ZoneType.TEXT,
                 left=0.8, top=0.5, width=10.0, height=0.8,
                 z_order=1, font_size_key="heading", color_key="text_primary",
                 content_key="title"),
            # 中心主视觉/发散节点
            Zone(id="center_hub", zone_type=ZoneType.DECORATOR,
                 left=4.667, top=1.8, width=4.0, height=4.8,
                 z_order=1),
            # 四周文本框
            Zone(id="branch_top_left", zone_type=ZoneType.TEXT,
                 left=0.8, top=1.8, width=3.6, height=2.0,
                 z_order=2, font_size_key="body", color_key="text_primary",
                 content_key="items[0]"),
            Zone(id="branch_top_right", zone_type=ZoneType.TEXT,
                 left=8.9, top=1.8, width=3.6, height=2.0,
                 z_order=2, font_size_key="body", color_key="text_primary",
                 content_key="items[1]"),
            Zone(id="branch_bottom_left", zone_type=ZoneType.TEXT,
                 left=0.8, top=4.5, width=3.6, height=2.0,
                 z_order=2, font_size_key="body", color_key="text_primary",
                 content_key="items[2]"),
            Zone(id="branch_bottom_right", zone_type=ZoneType.TEXT,
                 left=8.9, top=4.5, width=3.6, height=2.0,
                 z_order=2, font_size_key="body", color_key="text_primary",
                 content_key="items[3]"),
        ],
    )


def _planetary_orbit() -> LayoutTemplate:
    """卫星轨道/核心能力页 — 左侧多维卫星环绕 + 右侧详情说明卡"""
    return LayoutTemplate(
        name="planetary_orbit",
        display_name="多维卫星轨道页",
        description="左侧核心大圆+周围5-6个能力小圆卫星环绕 + 右侧详情说明面板，适合能力模型展示",
        page_types=["content", "data"],
        min_items=4,
        max_items=6,
        zones=[
            Zone(id="title", zone_type=ZoneType.TEXT,
                 left=0.8, top=0.5, width=10.0, height=0.8,
                 z_order=1, font_size_key="heading", color_key="text_primary",
                 content_key="title"),
            # 左侧环形轨道视觉
            Zone(id="orbit_visual", zone_type=ZoneType.DECORATOR,
                 left=1.0, top=1.6, width=5.5, height=5.2,
                 z_order=1),
            # 右侧卡片面板
            Zone(id="panel_bg", zone_type=ZoneType.DECORATOR,
                 left=7.2, top=1.6, width=5.3, height=5.2,
                 z_order=0),
            Zone(id="panel_content", zone_type=ZoneType.TEXT,
                 left=7.5, top=2.0, width=4.7, height=4.5,
                 z_order=1, font_size_key="body", color_key="text_primary",
                 content_key="items[0]"),
        ],
    )


def _stepped_stairs() -> LayoutTemplate:
    """阶梯进阶页 — 3-4 个台阶自左下向右上上升 + 底部说明"""
    return LayoutTemplate(
        name="stepped_stairs",
        display_name="阶梯进阶发展页",
        description="自左下向右上台阶式上升阶梯 + 节点说明，适合成长路径、技术演进",
        page_types=["timeline", "content"],
        min_items=3,
        max_items=4,
        zones=[
            Zone(id="title", zone_type=ZoneType.TEXT,
                 left=0.8, top=0.5, width=10.0, height=0.8,
                 z_order=1, font_size_key="heading", color_key="text_primary",
                 content_key="title"),
            # 阶梯视觉
            Zone(id="stairs_chart", zone_type=ZoneType.CHART,
                 left=1.5, top=1.5, width=10.333, height=3.5,
                 z_order=0, aspect_ratio="16:9", content_key="stairs"),
            # 底部 4 栏说明
            Zone(id="step_desc_1", zone_type=ZoneType.TEXT,
                 left=1.0, top=5.2, width=2.6, height=1.8,
                 z_order=1, font_size_key="caption", color_key="text_primary",
                 content_key="items[0]"),
            Zone(id="step_desc_2", zone_type=ZoneType.TEXT,
                 left=3.9, top=5.2, width=2.6, height=1.8,
                 z_order=1, font_size_key="caption", color_key="text_primary",
                 content_key="items[1]"),
            Zone(id="step_desc_3", zone_type=ZoneType.TEXT,
                 left=6.8, top=5.2, width=2.6, height=1.8,
                 z_order=1, font_size_key="caption", color_key="text_primary",
                 content_key="items[2]"),
            Zone(id="step_desc_4", zone_type=ZoneType.TEXT,
                 left=9.7, top=5.2, width=2.6, height=1.8,
                 z_order=1, font_size_key="caption", color_key="text_primary",
                 content_key="items[3]"),
        ],
    )


def _process_arrow() -> LayoutTemplate:
    """流程冲刺页 — 左侧流程步骤 + 右侧终点目标大圆"""
    return LayoutTemplate(
        name="process_arrow",
        display_name="流程冲刺目标页",
        description="多步骤流程朝向终点目标大徽标，适合阶段推进与冲刺目标",
        page_types=["timeline", "content"],
        min_items=3,
        max_items=6,
        zones=[
            Zone(id="title", zone_type=ZoneType.TEXT,
                 left=0.8, top=0.5, width=10.0, height=0.8,
                 z_order=1, font_size_key="heading", color_key="text_primary",
                 content_key="title"),
            # 流程条目左侧
            Zone(id="step_1", zone_type=ZoneType.TEXT,
                 left=1.0, top=1.8, width=6.5, height=1.2,
                 z_order=1, font_size_key="body", color_key="text_primary",
                 content_key="items[0]"),
            Zone(id="step_2", zone_type=ZoneType.TEXT,
                 left=1.0, top=3.2, width=6.5, height=1.2,
                 z_order=1, font_size_key="body", color_key="text_primary",
                 content_key="items[1]"),
            Zone(id="step_3", zone_type=ZoneType.TEXT,
                 left=1.0, top=4.6, width=6.5, height=1.2,
                 z_order=1, font_size_key="body", color_key="text_primary",
                 content_key="items[2]"),
            # 右侧终点徽标
            Zone(id="goal_circle", zone_type=ZoneType.DECORATOR,
                 left=8.5, top=2.2, width=3.8, height=3.8,
                 z_order=0),
            Zone(id="goal_text", zone_type=ZoneType.TEXT,
                 left=8.8, top=3.5, width=3.2, height=1.2,
                 z_order=1, font_size_key="heading", color_key="text_primary",
                 text_align=TextAlign.CENTER, content_key="footer_text"),
        ],
    )


def _two_options_circle() -> LayoutTemplate:
    """双圆方案对比页 — 左侧双错落大圆 + 右侧条目清单"""
    return LayoutTemplate(
        name="two_options_circle",
        display_name="双方案对比页",
        description="左侧双错落大圆方案 + 右侧详细条目清单，适合方案/定价/对比",
        page_types=["comparison", "content"],
        min_items=2,
        max_items=4,
        zones=[
            Zone(id="title", zone_type=ZoneType.TEXT,
                 left=0.8, top=0.5, width=10.0, height=0.8,
                 z_order=1, font_size_key="heading", color_key="text_primary",
                 content_key="title"),
            # 左侧双圆
            Zone(id="circle_opt_1", zone_type=ZoneType.TEXT,
                 left=1.2, top=1.8, width=2.8, height=2.8,
                 z_order=1, font_size_key="heading", color_key="text_primary",
                 text_align=TextAlign.CENTER, content_key="items[0]"),
            Zone(id="circle_opt_2", zone_type=ZoneType.TEXT,
                 left=2.6, top=3.6, width=2.8, height=2.8,
                 z_order=1, font_size_key="heading", color_key="text_primary",
                 text_align=TextAlign.CENTER, content_key="items[1]"),
            # 右侧条目列表
            Zone(id="desc_list", zone_type=ZoneType.TEXT,
                 left=6.2, top=1.8, width=6.2, height=4.8,
                 z_order=1, font_size_key="body", color_key="text_primary",
                 content_key="items[2]"),
        ],
    )


# ============================================================
# 布局注册表
# ============================================================

LAYOUT_REGISTRY: dict[str, LayoutTemplate] = {}


def _register_all():
    factories = [
        _cover_fullimage,
        _cover_split,
        _catalog_grid,
        _section_header,
        _content_sidebar,
        _content_grid_2x3,
        _content_grid_2x2,
        _content_centered,
        _pyramid_hierarchy,
        _central_radial_lightbulb,
        _planetary_orbit,
        _stepped_stairs,
        _process_arrow,
        _two_options_circle,
        _data_chart,
        _data_stats,
        _timeline,
        _comparison,
        _section_divider,
        _mixed_media,
    ]
    for factory in factories:
        layout = factory()
        LAYOUT_REGISTRY[layout.name] = layout


_register_all()


def get_layout(name: str) -> LayoutTemplate:
    """根据名称获取布局模板"""
    if name not in LAYOUT_REGISTRY:
        raise ValueError(
            f"未知的布局: {name}。可选项: {list(LAYOUT_REGISTRY.keys())}"
        )
    return LAYOUT_REGISTRY[name]


def select_layout(page_type: str, item_count: int = 0,
                  has_chart: bool = False) -> LayoutTemplate:
    """根据页面类型和内容特征自动选择布局"""
    candidates = [
        layout for layout in LAYOUT_REGISTRY.values()
        if page_type in layout.page_types
        and layout.min_items <= item_count <= layout.max_items
    ]
    if not candidates:
        candidates = [
            layout for layout in LAYOUT_REGISTRY.values()
            if page_type in layout.page_types
        ]
    if not candidates:
        # 兜底使用分割封面
        return LAYOUT_REGISTRY["cover_split"]

    # 如果有图表数据优先选 data 布局
    if has_chart:
        data_layouts = [c for c in candidates if "data" in c.name]
        if data_layouts:
            return data_layouts[0]

    return candidates[0]


def list_layouts() -> list[dict]:
    """列出所有可用布局"""
    return [
        {
            "name": l.name,
            "display_name": l.display_name,
            "description": l.description,
            "page_types": l.page_types,
            "min_items": l.min_items,
            "max_items": l.max_items,
        }
        for l in LAYOUT_REGISTRY.values()
    ]
