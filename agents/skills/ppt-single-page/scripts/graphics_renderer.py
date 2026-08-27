"""
图形渲染器模块（纯 Pillow 实现）
替代原 svg_renderer.py，完全移除 cairosvg 系统级依赖。
支持：渐变背景、遮罩层、波浪装饰、几何图形、圆形/矩形、线条等。
跨平台兼容：Windows / macOS / Linux，仅需 pip install Pillow。
"""

import os
import math
from typing import Optional, Tuple, List

from PIL import Image, ImageDraw, ImageFont


# ============================================================
# 颜色辅助
# ============================================================

def hex_to_rgba(hex_color: str, opacity: float = 1.0) -> Tuple[int, int, int, int]:
    """将 hex 颜色转为 RGBA 元组"""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 6:
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    elif len(hex_color) == 3:
        r, g, b = int(hex_color[0]*2, 16), int(hex_color[1]*2, 16), int(hex_color[2]*2, 16)
    else:
        r, g, b = 200, 200, 200
    return (r, g, b, int(opacity * 255))


def _lerp_color(c1: Tuple[int, ...], c2: Tuple[int, ...], t: float) -> Tuple[int, ...]:
    """线性插值两个颜色"""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


# ============================================================
# 渐变背景
# ============================================================

def generate_gradient_background(
    width: int,
    height: int,
    start_color: str,
    end_color: str,
    direction: str = "diagonal",
    opacity: float = 1.0,
    output_path: Optional[str] = None,
) -> Image.Image:
    """生成渐变背景图片"""
    c1 = hex_to_rgba(start_color, opacity)
    c2 = hex_to_rgba(end_color, opacity)
    img = Image.new("RGBA", (width, height))

    for y in range(height):
        for x in range(width):
            if direction == "horizontal":
                t = x / max(width - 1, 1)
            elif direction == "vertical":
                t = y / max(height - 1, 1)
            else:  # diagonal
                t = (x / max(width - 1, 1) + y / max(height - 1, 1)) / 2
            color = _lerp_color(c1, c2, t)
            img.putpixel((x, y), color)

    if output_path:
        _save_image(img, output_path)
    return img


def generate_gradient_background_fast(
    width: int,
    height: int,
    start_color: str,
    end_color: str,
    direction: str = "diagonal",
    opacity: float = 1.0,
    output_path: Optional[str] = None,
) -> Image.Image:
    """快速渐变背景（逐行绘制，比逐像素快很多）"""
    c1 = hex_to_rgba(start_color, opacity)
    c2 = hex_to_rgba(end_color, opacity)
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)

    if direction == "vertical" or direction == "diagonal":
        for y in range(height):
            t = y / max(height - 1, 1)
            color = _lerp_color(c1, c2, t)
            draw.line([(0, y), (width, y)], fill=color)
    else:  # horizontal
        for x in range(width):
            t = x / max(width - 1, 1)
            color = _lerp_color(c1, c2, t)
            draw.line([(x, 0), (x, height)], fill=color)

    if output_path:
        _save_image(img, output_path)
    return img


# ============================================================
# 遮罩层
# ============================================================

def generate_overlay(
    width: int,
    height: int,
    color: str = "#000000",
    opacity: float = 0.5,
    output_path: Optional[str] = None,
) -> Image.Image:
    """生成半透明遮罩层"""
    rgba = hex_to_rgba(color, opacity)
    img = Image.new("RGBA", (width, height), rgba)
    if output_path:
        _save_image(img, output_path)
    return img


# ============================================================
# 装饰元素
# ============================================================

def generate_wave_decoration(
    width: int,
    height: int,
    color: str = "#3D6B8E",
    opacity: float = 0.15,
    output_path: Optional[str] = None,
) -> Image.Image:
    """生成波浪装饰"""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    rgba = hex_to_rgba(color, opacity)

    # 绘制多条波浪线
    for wave_offset in range(3):
        points = []
        base_y = height * (0.3 + wave_offset * 0.2)
        amplitude = height * 0.08
        for x in range(0, width + 1, 2):
            y = base_y + amplitude * math.sin(x * 0.02 + wave_offset * 1.5)
            points.append((x, int(y)))
        if len(points) >= 2:
            draw.line(points, fill=rgba, width=max(1, height // 60))

    if output_path:
        _save_image(img, output_path)
    return img


def generate_geometric_shapes(
    width: int,
    height: int,
    color: str = "#6C63FF",
    opacity: float = 0.08,
    output_path: Optional[str] = None,
) -> Image.Image:
    """生成几何图形装饰"""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    rgba = hex_to_rgba(color, opacity)

    # 圆形
    r = min(width, height) * 0.15
    draw.ellipse([width * 0.1 - r, height * 0.2 - r,
                  width * 0.1 + r, height * 0.2 + r], fill=rgba)
    # 矩形
    draw.rectangle([width * 0.7, height * 0.6,
                    width * 0.9, height * 0.8], fill=rgba)
    # 三角形
    cx, cy = width * 0.85, height * 0.15
    s = min(width, height) * 0.1
    draw.polygon([
        (cx, cy - s),
        (cx - s * 0.866, cy + s * 0.5),
        (cx + s * 0.866, cy + s * 0.5),
    ], fill=rgba)

    if output_path:
        _save_image(img, output_path)
    return img


# ============================================================
# 基础图形
# ============================================================

def generate_number_circle(
    size: int,
    number: str,
    bg_color: str = "#3D6B8E",
    text_color: str = "#FFFFFF",
    output_path: Optional[str] = None,
) -> Image.Image:
    """生成带数字/符号的圆形图标"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 绘制圆形背景
    margin = max(2, size // 20)
    draw.ellipse([margin, margin, size - margin, size - margin],
                 fill=hex_to_rgba(bg_color))

    # 绘制文字
    font_size = max(10, size // 3)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except (IOError, OSError):
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except (IOError, OSError):
            font = ImageFont.load_default()

    text_rgba = hex_to_rgba(text_color)
    bbox = draw.textbbox((0, 0), number, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (size - tw) // 2
    ty = (size - th) // 2 - bbox[1]
    draw.text((tx, ty), number, fill=text_rgba, font=font)

    if output_path:
        _save_image(img, output_path)
    return img


def generate_circle(
    size: int,
    border_color: str = "#3D6B8E",
    border_width: int = 3,
    fill_color: Optional[str] = None,
    output_path: Optional[str] = None,
) -> Image.Image:
    """生成圆形（可选填充）"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    m = border_width
    fill = hex_to_rgba(fill_color) if fill_color else None
    draw.ellipse([m, m, size - m, size - m],
                 fill=fill,
                 outline=hex_to_rgba(border_color),
                 width=border_width)
    if output_path:
        _save_image(img, output_path)
    return img


def generate_rounded_rect(
    width: int,
    height: int,
    bg_color: str = "#FFFFFF",
    border_color: Optional[str] = None,
    border_width: int = 1,
    radius: int = 8,
    opacity: float = 1.0,
    output_path: Optional[str] = None,
) -> Image.Image:
    """生成圆角矩形"""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    fill = hex_to_rgba(bg_color, opacity)
    outline = hex_to_rgba(border_color) if border_color else None
    draw.rounded_rectangle([0, 0, width - 1, height - 1],
                           radius=radius,
                           fill=fill,
                           outline=outline,
                           width=border_width)
    if output_path:
        _save_image(img, output_path)
    return img


# ============================================================
# 线条
# ============================================================

def generate_horizontal_line(
    width: int,
    height: int,
    color: str = "#3D6B8E",
    line_width: int = 3,
    output_path: Optional[str] = None,
) -> Image.Image:
    """生成水平线"""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    y = height // 2
    draw.line([(0, y), (width, y)], fill=hex_to_rgba(color), width=line_width)
    if output_path:
        _save_image(img, output_path)
    return img


def generate_vertical_line(
    width: int,
    height: int,
    color: str = "#E2E8F0",
    line_width: int = 2,
    output_path: Optional[str] = None,
) -> Image.Image:
    """生成垂直线"""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    x = width // 2
    draw.line([(x, 0), (x, height)], fill=hex_to_rgba(color), width=line_width)
    if output_path:
        _save_image(img, output_path)
    return img


# ============================================================
# 高级图表与结构图元 (Diagrams & Shapes)
# ============================================================

def generate_pyramid_diagram(
    width: int,
    height: int,
    levels: int = 3,
    labels: Optional[List[str]] = None,
    colors: Optional[List[str]] = None,
    output_path: Optional[str] = None,
) -> Image.Image:
    """生成分层金字塔/三角形层级图"""
    if labels is None:
        labels = ["33%", "66%", "99%"]
    if colors is None:
        colors = ["#3D6B8E", "#5A8BA8", "#8FB3C8", "#CBDCE6"]

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx = width // 2
    top_y = int(height * 0.08)
    bottom_y = int(height * 0.92)
    total_h = bottom_y - top_y
    layer_h = total_h / levels
    half_base = int(width * 0.42)

    font = ImageFont.load_default()

    for i in range(levels):
        y1 = top_y + i * layer_h
        y2 = top_y + (i + 1) * layer_h
        w1 = half_base * (i / levels)
        w2 = half_base * ((i + 1) / levels)

        pts = [
            (cx - w1, y1),
            (cx + w1, y1),
            (cx + w2, y2),
            (cx - w2, y2),
        ]
        color_hex = colors[i % len(colors)]
        draw.polygon(pts, fill=hex_to_rgba(color_hex, 0.9), outline=(255, 255, 255, 200))

        # 标注文本
        if i < len(labels):
            txt = labels[i]
            bbox = draw.textbbox((0, 0), txt, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text((cx - tw // 2, int((y1 + y2) / 2 - th // 2)), txt,
                      fill=(255, 255, 255, 255), font=font)

    if output_path:
        _save_image(img, output_path)
    return img


def generate_stepped_stairs(
    width: int,
    height: int,
    steps: int = 4,
    colors: Optional[List[str]] = None,
    output_path: Optional[str] = None,
) -> Image.Image:
    """生成阶梯上升/进阶路径图"""
    if colors is None:
        colors = ["#2C5F7C", "#3D6B8E", "#5A8BA8", "#8FB3C8"]

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    step_w = width / (steps + 1)
    step_h = height / (steps + 1)
    base_y = height * 0.88

    for i in range(steps):
        x = int((i + 0.5) * step_w)
        y = int(base_y - (i + 1) * step_h * 0.8)
        w = int(step_w * 0.85)
        h = int(base_y - y)
        c = colors[i % len(colors)]

        # 绘制立柱台阶
        draw.rounded_rectangle([x, y, x + w, base_y], radius=6, fill=hex_to_rgba(c, 0.85))

        # 顶部高亮小圆
        r = min(w, 40) // 2
        cx, cy = x + w // 2, y
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hex_to_rgba(c), outline=(255, 255, 255, 240), width=2)

    # 绘制上升趋势连接线
    line_pts = []
    for i in range(steps):
        x = int((i + 0.5) * step_w + step_w * 0.85 / 2)
        y = int(base_y - (i + 1) * step_h * 0.8)
        line_pts.append((x, y))
    if len(line_pts) >= 2:
        draw.line(line_pts, fill=(255, 255, 255, 200), width=3)

    if output_path:
        _save_image(img, output_path)
    return img


def generate_radial_hub(
    width: int,
    height: int,
    node_count: int = 4,
    center_label: str = "?",
    primary_color: str = "#3D6B8E",
    output_path: Optional[str] = None,
) -> Image.Image:
    """生成中心发散/思维脑图图元（中心大圆 + 周围连线节点）"""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = width // 2, height // 2
    center_r = int(min(width, height) * 0.22)
    node_r = int(min(width, height) * 0.1)
    orbit_r = int(min(width, height) * 0.38)

    # 绘制连线
    for i in range(node_count):
        angle = -math.pi / 2 + (2 * math.pi * i / node_count)
        nx = int(cx + orbit_r * math.cos(angle))
        ny = int(cy + orbit_r * math.sin(angle))
        draw.line([(cx, cy), (nx, ny)], fill=hex_to_rgba(primary_color, 0.4), width=3)
        # 节点小圆
        draw.ellipse([nx - node_r, ny - node_r, nx + node_r, ny + node_r],
                     fill=hex_to_rgba(primary_color, 0.9), outline=(255, 255, 255, 255), width=2)
        # 节点序号
        num_str = f"0{i+1}"
        draw.text((nx - 6, ny - 6), num_str, fill=(255, 255, 255, 255))

    # 绘制中心主圆
    draw.ellipse([cx - center_r, cy - center_r, cx + center_r, cy + center_r],
                 fill=hex_to_rgba(primary_color), outline=(255, 255, 255, 255), width=4)

    # 中心文本
    draw.text((cx - 8, cy - 10), center_label, fill=(255, 255, 255, 255))

    if output_path:
        _save_image(img, output_path)
    return img


# ============================================================
# 文件保存
# ============================================================

def _save_image(img: Image.Image, output_path: str):
    """保存图片到文件"""
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    img.save(output_path, "PNG")

