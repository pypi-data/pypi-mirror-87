from typing import List, Optional, Tuple

from pydantic import BaseModel


class DMInputParams(BaseModel):
    scale: float
    size: Tuple[int, int]
    mean: Optional[Tuple[float, ...]]
    swapRB: Optional[bool]
    crop: Optional[bool]

    class Config:
        allow_population_by_field_name = True
        fields = {"swapRB": "swap_rb"}


class DetectDefaults(BaseModel):
    confThreshold: Optional[float] = 0.5
    nmsThreshold: Optional[float] = 0.5

    class Config:
        allow_population_by_field_name = True
        fields = {
            "confThreshold": "confidence_threshold",
            "nmsThreshold": "nms_threshold",
        }


class DrawDefaults(BaseModel):
    color: Optional[Tuple[int, int, int]] = (255, 0, 0)
    label_format: Optional[str] = "{} | {:.1%}"
    offset: Optional[Tuple[int, int]] = (30, 30)
    font_const: Optional[int] = 3
    thickness: Optional[int] = 2


class DetectionModelConfig(BaseModel):
    name: str
    description: Optional[str]
    weights_path: str
    config_path: str
    classes_path: str
    input_params: DMInputParams
    detect_defaults: Optional[DetectDefaults] = DetectDefaults()
    draw_defaults: Optional[DrawDefaults] = DrawDefaults()
    class_offset: Optional[int] = 0


class YasodConfig(BaseModel):
    version: int
    detection_models: List[DetectionModelConfig]
