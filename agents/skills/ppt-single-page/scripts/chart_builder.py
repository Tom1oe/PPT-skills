"""
图表构建器模块（纯 Pillow 实现）
支持：环形图、饼图、柱状图、折线图、雷达图。
跨平台兼容：Windows / macOS / Linux，仅需 pip install Pillow。
"""

import math
import os
from typing import Optional, List, Tuple

from PIL import Image, ImageDraw, ImageFont


# ============================================================
# 颜色辅助
# ============================================================

def _hex_to_rgba(hex_color: str, opacity: float = 1.0) -> Tuple[int, int, int, int]:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 6:
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    else:
        r, g, b = 100, 100, 100
    return (r, g, b, int(opacity * 255))


# 默认配色板
DEFAULT_COLORS = [
    "#3D6B8E", "#5A8BA8", "#6C63FF", "#4ECDC4",
    "#FF6B6B", "#C08552", "#7F5AF0", "#2CB67D",
    "#FF8906", "#E74C3C", "#9B59B6", "#1ABC9C",
]


def _get_font(size: int) -> ImageFont.ImageFont:
    """获取字体，兼容不同平台"""
    font_paths = [
        "arial.ttf",                                    # Windows
        "/System/Library/Fonts/Helvetica.ttc",          # macOS
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux (Debian/Ubuntu)
        "/usr/share/fonts/TTF/DejaVuSans.ttf",          # Linux (Arch)
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except (IOError, OSError):
            continue
    return ImageFont.load_default()


def _save(img: Image.Image, path: str):
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    img.save(path, "PNG")


# ============================================================
# 环形图 (Donut Chart)
# ============================================================

def build_donut_chart(
    width: int,
    height: int,
    output_path: str,
    value: float = 68,
    max_value: float = 100,
    color: str = "#3D6B8E",
    bg_ring_color: str = "#E8EDF2",
    text_color: str = "#2D3748",
    label: str = "",
    ring_width_ratio: float = 0.18,
) -> str:
    """生成环形进度图"""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = width // 2, height // 2
    radius = int(min(width, height) * 0.4)
    ring_width = int(radius * ring_width_ratio * 2)
    bbox = [cx - radius, cy - radius, cx + radius, cy + radius]

    # 背景环
    draw.arc(bbox, 0, 360, fill=_hex_to_rgba(bg_ring_color), width=ring_width)

    # 进度弧
    pct = min(value / max_value, 1.0)
    sweep = pct * 360
    start = -90  # 从顶部开始
    draw.arc(bbox, start, start + sweep, fill=_hex_to_rgba(color), width=ring_width)

    # 中心文字
    text = label if label else f"{int(value)}%"
    font_size = max(12, radius // 2)
    font = _get_font(font_size)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - text_bbox[1]),
              text, fill=_hex_to_rgba(text_color), font=font)

    _save(img, output_path)
    return output_path


# ============================================================
# 饼图 (Pie Chart)
# ============================================================

def build_pie_chart(
    width: int,
    height: int,
    output_path: str,
    data: List[dict] = None,
    colors: Optional[List[str]] = None,
) -> str:
    """生成饼图"""
    if not data:
        data = [{"label": "A", "value": 40}, {"label": "B", "value": 35},
                {"label": "C", "value": 25}]
    if not colors:
        colors = DEFAULT_COLORS

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = width // 2, height // 2
    radius = int(min(width, height) * 0.38)
    bbox = [cx - radius, cy - radius, cx + radius, cy + radius]

    total = sum(d.get("value", 0) for d in data)
    if total == 0:
        total = 1

    start_angle = -90
    for i, item in enumerate(data):
        value = item.get("value", 0)
        sweep = (value / total) * 360
        color = _hex_to_rgba(colors[i % len(colors)])
        draw.pieslice(bbox, start_angle, start_angle + sweep, fill=color)
        start_angle += sweep

    _save(img, output_path)
    return output_path


# ============================================================
# 柱状图 (Bar Chart)
# ============================================================

def build_bar_chart(
    width: int,
    height: int,
    output_path: str,
    data: List[dict] = None,
    colors: Optional[List[str]] = None,
    show_labels: bool = True,
) -> str:
    """生成柱状图"""
    if not data:
        data = [{"label": "Q1", "value": 65}, {"label": "Q2", "value": 80},
                {"label": "Q3", "value": 55}, {"label": "Q4", "value": 90}]
    if not colors:
        colors = DEFAULT_COLORS

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 图表区域
    margin_left = int(width * 0.12)
    margin_right = int(width * 0.08)
    margin_top = int(height * 0.1)
    margin_bottom = int(height * 0.18)

    chart_w = width - margin_left - margin_right
    chart_h = height - margin_top - margin_bottom

    max_val = max(d.get("value", 0) for d in data) if data else 1
    if max_val == 0:
        max_val = 1

    n = len(data)
    bar_total_w = chart_w / max(n, 1)
    bar_w = int(bar_total_w * 0.6)
    gap = int(bar_total_w * 0.2)

    # 绘制基线
    base_y = margin_top + chart_h
    draw.line([(margin_left, base_y), (margin_left + chart_w, base_y)],
              fill=(180, 180, 180, 255), width=1)

    font = _get_font(max(10, height // 20))

    for i, item in enumerate(data):
        value = item.get("value", 0)
        bar_h = int((value / max_val) * chart_h * 0.9)
        x0 = margin_left + int(i * bar_total_w) + gap
        y0 = base_y - bar_h
        x1 = x0 + bar_w
        y1 = base_y

        color = _hex_to_rgba(colors[i % len(colors)])
        # 圆角顶部
        draw.rounded_rectangle([x0, y0, x1, y1], radius=max(2, bar_w // 8), fill=color)

        if show_labels:
            label = item.get("label", "")
            lbbox = draw.textbbox((0, 0), label, font=font)
            lw = lbbox[2] - lbbox[0]
            draw.text((x0 + (bar_w - lw) // 2, base_y + 4),
                      label, fill=(120, 120, 120, 255), font=font)

    _save(img, output_path)
    return output_path


# ============================================================
# 折线图 (Line Chart)
# ============================================================

def build_line_chart(
    width: int,
    height: int,
    output_path: str,
    data: List[dict] = None,
    line_color: str = "#3D6B8E",
    show_dots: bool = True,
    show_fill: bool = True,
) -> str:
    """生成折线图"""
    if not data:
        data = [{"label": "1月", "value": 30}, {"label": "2月", "value": 50},
                {"label": "3月", "value": 40}, {"label": "4月", "value": 70},
                {"label": "5月", "value": 60}, {"label": "6月", "value": 85}]

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    margin_left = int(width * 0.1)
    margin_right = int(width * 0.05)
    margin_top = int(height * 0.1)
    margin_bottom = int(height * 0.15)

    chart_w = width - margin_left - margin_right
    chart_h = height - margin_top - margin_bottom

    max_val = max(d.get("value", 0) for d in data) if data else 1
    if max_val == 0:
        max_val = 1

    n = len(data)
    points = []
    for i, item in enumerate(data):
        x = margin_left + int(i * chart_w / max(n - 1, 1))
        y = margin_top + chart_h - int((item.get("value", 0) / max_val) * chart_h * 0.9)
        points.append((x, y))

    base_y = margin_top + chart_h
    lc = _hex_to_rgba(line_color)

    # 填充区域
    if show_fill and len(points) >= 2:
        fill_points = list(points) + [(points[-1][0], base_y), (points[0][0], base_y)]
        fill_color = _hex_to_rgba(line_color, 0.15)
        draw.polygon(fill_points, fill=fill_color)

    # 绘制折线
    if len(points) >= 2:
        draw.line(points, fill=lc, width=max(2, height // 80))

    # 绘制数据点
    if show_dots:
        dot_r = max(3, height // 50)
        for pt in points:
            draw.ellipse([pt[0] - dot_r, pt[1] - dot_r,
                         pt[0] + dot_r, pt[1] + dot_r], fill=lc)

    # 基线
    draw.line([(margin_left, base_y), (margin_left + chart_w, base_y)],
              fill=(180, 180, 180, 255), width=1)

    _save(img, output_path)
    return output_path


# ============================================================
# 雷达图 (Radar Chart)
# ============================================================

def build_radar_chart(
    width: int,
    height: int,
    output_path: str,
    data: List[dict] = None,
    color: str = "#3D6B8E",
    show_grid: bool = True,
) -> str:
    """生成雷达图"""
    if not data:
        data = [{"label": "技术", "value": 85}, {"label": "市场", "value": 70},
                {"label": "质量", "value": 90}, {"label": "效率", "value": 75},
                {"label": "创新", "value": 80}]

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = width // 2, height // 2
    radius = int(min(width, height) * 0.35)
    n = len(data)
    max_val = max(d.get("value", 0) for d in data) if data else 1
    if max_val == 0:
        max_val = 1

    def _angle(i):
        return -math.pi / 2 + (2 * math.pi * i / n)

    # 网格
    if show_grid:
        grid_color = (200, 200, 200, 100)
        for level in [0.25, 0.5, 0.75, 1.0]:
            r = radius * level
            grid_pts = []
            for i in range(n):
                a = _angle(i)
                grid_pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
            grid_pts.append(grid_pts[0])
            draw.line(grid_pts, fill=grid_color, width=1)
        # 轴线
        for i in range(n):
            a = _angle(i)
            draw.line([(cx, cy), (cx + radius * math.cos(a), cy + radius * math.sin(a))],
                      fill=grid_color, width=1)

    # 数据区域
    data_pts = []
    for i, item in enumerate(data):
        v = item.get("value", 0) / max_val
        a = _angle(i)
        r = radius * v
        data_pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))

    fill_color = _hex_to_rgba(color, 0.25)
    outline_color = _hex_to_rgba(color, 0.9)
    draw.polygon(data_pts, fill=fill_color, outline=outline_color)

    # 数据点
    dot_r = max(3, radius // 20)
    for pt in data_pts:
        draw.ellipse([pt[0] - dot_r, pt[1] - dot_r,
                     pt[0] + dot_r, pt[1] + dot_r],
                     fill=_hex_to_rgba(color))

    _save(img, output_path)
    return output_path


# ============================================================
# 统一入口
# ============================================================

def build_chart(
    chart_type: str,
    width: int,
    height: int,
    output_path: str,
    **kwargs,
) -> str:
    """统一图表构建入口"""
    builders = {
        "donut": build_donut_chart,
        "pie": build_pie_chart,
        "bar": build_bar_chart,
        "line": build_line_chart,
        "radar": build_radar_chart,
    }
    builder = builders.get(chart_type, build_donut_chart)
    return builder(width, height, output_path, **kwargs)
