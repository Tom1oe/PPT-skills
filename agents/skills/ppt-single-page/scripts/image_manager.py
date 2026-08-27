"""
图片管理器模块（元数据驱动模式）
不再生成占位图片文件，仅维护图片任务清单（元数据）。
支持：任务创建 → 状态追踪 → 比例匹配 → 居中裁切 → 填充。
"""

import os
import json
import math
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Tuple
from enum import Enum

from PIL import Image


# ============================================================
# 常量
# ============================================================

# 标准宽高比 → (宽, 高) 映射表
ASPECT_RATIO_MAP: Dict[str, Tuple[int, int]] = {
    "1:1":  (1024, 1024),
    "3:4":  (768, 1024),
    "4:3":  (1024, 768),
    "9:16": (576, 1024),
    "16:9": (1024, 576),
    "2:3":  (682, 1024),
    "3:2":  (1024, 682),
}


class TaskStatus(str, Enum):
    """图片任务状态"""
    PENDING = "pending"          # 等待生成
    GENERATING = "generating"    # 生成中
    DONE = "done"               # 已完成
    FAILED = "failed"           # 失败
    SKIPPED = "skipped"         # 跳过


# ============================================================
# 数据类
# ============================================================

@dataclass
class ImageTask:
    """图片任务元数据（不包含实际文件）"""
    id: str                              # 任务ID（通常等于zone_id）
    zone_id: str                         # 关联的布局区域ID
    left: float                          # 区域左边距（英寸）
    top: float                           # 区域上边距（英寸）
    width: float                         # 区域宽度（英寸）
    height: float                        # 区域高度（英寸）
    image_type: str = "photo"            # photo | chart | icon | decorator
    aspect_ratio: str = ""               # 匹配的标准比例
    target_width: int = 0                # 目标像素宽度
    target_height: int = 0              # 目标像素高度
    description: str = ""                # 图片描述（用于生图 prompt）
    style_prompt: str = ""               # 风格提示词后缀
    status: TaskStatus = TaskStatus.PENDING
    image_path: Optional[str] = None     # 生成后的图片文件路径
    error: Optional[str] = None          # 错误信息

    def to_dict(self) -> dict:
        d = asdict(self)
        d["status"] = self.status.value
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "ImageTask":
        d = dict(d)
        d["status"] = TaskStatus(d.get("status", "pending"))
        return cls(**d)


# ============================================================
# 图片管理器
# ============================================================

class ImageManager:
    """
    图片管理器 — 元数据驱动模式。
    不生成任何占位文件，只维护任务清单。
    """

    def __init__(self, output_dir: str = "./output_images"):
        self.output_dir = output_dir
        self.tasks: Dict[str, ImageTask] = {}
        os.makedirs(output_dir, exist_ok=True)

    # ----------------------------------------------------------
    # 任务创建
    # ----------------------------------------------------------

    def create_task(
        self,
        zone_id: str,
        left: float,
        top: float,
        width: float,
        height: float,
        image_type: str = "photo",
        description: str = "",
        style_prompt: str = "",
        preferred_ratio: str = "",
    ) -> ImageTask:
        """创建图片任务（纯元数据，不生成文件）"""
        # 匹配最佳标准比例
        if preferred_ratio and preferred_ratio in ASPECT_RATIO_MAP:
            ratio = preferred_ratio
            target_w, target_h = ASPECT_RATIO_MAP[ratio]
        else:
            ratio = self._match_ratio(width, height)
            # 检查标准比例与实际区域比例的偏差
            actual_ratio = width / height if height > 0 else 1.0
            std_w, std_h = ASPECT_RATIO_MAP.get(ratio, (1024, 1024))
            std_ratio = std_w / std_h
            deviation = abs(actual_ratio - std_ratio) / max(std_ratio, 0.01)

            if deviation > 0.1:
                # 偏差超过10%，使用区域实际尺寸（按96dpi换算像素）
                target_w = max(100, int(width * 96))
                target_h = max(100, int(height * 96))
                ratio = f"{width:.1f}:{height:.1f}"
            else:
                target_w, target_h = std_w, std_h

        task = ImageTask(
            id=f"img_{zone_id}",
            zone_id=zone_id,
            left=left,
            top=top,
            width=width,
            height=height,
            image_type=image_type,
            aspect_ratio=ratio,
            target_width=target_w,
            target_height=target_h,
            description=description,
            style_prompt=style_prompt,
            status=TaskStatus.PENDING,
        )
        self.tasks[task.id] = task
        return task

    # ----------------------------------------------------------
    # 状态管理
    # ----------------------------------------------------------

    def mark_generating(self, task_id: str):
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.GENERATING

    def mark_failed(self, task_id: str, error: str = ""):
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.FAILED
            self.tasks[task_id].error = error

    def mark_skipped(self, task_id: str):
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.SKIPPED

    def fill_image(
        self,
        task_id: str,
        image_path: str,
        crop_to_fit: bool = True,
    ) -> Optional[str]:
        """
        将生成的图片填入任务。
        如果 crop_to_fit=True，执行居中裁切以匹配目标比例。
        """
        if task_id not in self.tasks:
            return None

        task = self.tasks[task_id]

        if crop_to_fit and os.path.exists(image_path):
            cropped_path = self._center_crop(
                image_path, task.target_width, task.target_height, task_id)
            if cropped_path:
                image_path = cropped_path

        task.image_path = image_path
        task.status = TaskStatus.DONE
        return image_path

    # ----------------------------------------------------------
    # 查询
    # ----------------------------------------------------------

    def get_task(self, task_id: str) -> Optional[ImageTask]:
        return self.tasks.get(task_id)

    def get_by_type(self, image_type: str) -> List[ImageTask]:
        return [t for t in self.tasks.values() if t.image_type == image_type]

    def get_by_status(self, status: TaskStatus) -> List[ImageTask]:
        return [t for t in self.tasks.values() if t.status == status]

    def get_pending_tasks(self) -> List[ImageTask]:
        return self.get_by_status(TaskStatus.PENDING)

    def get_done_tasks(self) -> List[ImageTask]:
        return self.get_by_status(TaskStatus.DONE)

    def all_done(self) -> bool:
        """检查所有任务是否都已完成（done 或 skipped）"""
        return all(
            t.status in (TaskStatus.DONE, TaskStatus.SKIPPED)
            for t in self.tasks.values()
        )

    def get_resolution(self, task_id: str) -> Tuple[int, int]:
        task = self.tasks.get(task_id)
        if task:
            return task.target_width, task.target_height
        return 1024, 1024

    def get_summary(self) -> dict:
        by_type: Dict[str, int] = {}
        by_status: Dict[str, int] = {}
        for t in self.tasks.values():
            by_type[t.image_type] = by_type.get(t.image_type, 0) + 1
            by_status[t.status.value] = by_status.get(t.status.value, 0) + 1
        return {
            "total": len(self.tasks),
            "by_type": by_type,
            "by_status": by_status,
        }

    # ----------------------------------------------------------
    # 任务清单导出/导入（断点续传支持）
    # ----------------------------------------------------------

    def export_tasks(self, filepath: Optional[str] = None) -> str:
        """导出任务清单为 JSON 文件"""
        if filepath is None:
            filepath = os.path.join(self.output_dir, "image_tasks.json")
        data = {
            "output_dir": self.output_dir,
            "total": len(self.tasks),
            "tasks": [t.to_dict() for t in self.tasks.values()],
        }
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filepath

    def import_tasks(self, filepath: str) -> int:
        """从 JSON 文件导入任务清单（用于断点续传）"""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        count = 0
        for task_data in data.get("tasks", []):
            task = ImageTask.from_dict(task_data)
            self.tasks[task.id] = task
            count += 1
        return count

    # ----------------------------------------------------------
    # 内部方法
    # ----------------------------------------------------------

    @staticmethod
    def _match_ratio(width_inches: float, height_inches: float) -> str:
        """将任意宽高比匹配到最接近的标准比例"""
        if height_inches == 0:
            return "16:9"
        actual = width_inches / height_inches

        best_ratio = "1:1"
        best_diff = float("inf")
        for name, (w, h) in ASPECT_RATIO_MAP.items():
            std = w / h
            diff = abs(actual - std)
            if diff < best_diff:
                best_diff = diff
                best_ratio = name
        return best_ratio

    def _center_crop(
        self,
        image_path: str,
        target_w: int,
        target_h: int,
        task_id: str,
    ) -> Optional[str]:
        """居中裁切图片到目标比例"""
        try:
            img = Image.open(image_path)
            src_w, src_h = img.size
            target_ratio = target_w / target_h
            src_ratio = src_w / src_h

            if abs(src_ratio - target_ratio) < 0.02:
                # 比例已匹配，只需缩放
                img = img.resize((target_w, target_h), Image.LANCZOS)
            elif src_ratio > target_ratio:
                # 图片更宽，裁两侧
                new_w = int(src_h * target_ratio)
                left = (src_w - new_w) // 2
                img = img.crop((left, 0, left + new_w, src_h))
                img = img.resize((target_w, target_h), Image.LANCZOS)
            else:
                # 图片更高，裁上下
                new_h = int(src_w / target_ratio)
                top = (src_h - new_h) // 2
                img = img.crop((0, top, src_w, top + new_h))
                img = img.resize((target_w, target_h), Image.LANCZOS)

            output = os.path.join(self.output_dir, f"{task_id}_cropped.png")
            img.save(output, "PNG")
            return output
        except Exception as e:
            print(f"   ⚠️ 裁切失败 ({task_id}): {e}")
            return None
