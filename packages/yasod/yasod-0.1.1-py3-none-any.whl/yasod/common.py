from typing import List, NamedTuple

from numpy import float32, int32
from numpy.core.multiarray import ndarray


class Detection(NamedTuple):
    class_id: int32
    confidence: float32
    box: ndarray


class Detections(NamedTuple):
    class_ids: ndarray
    confidences: ndarray
    boxes: ndarray


def flatten_detections(detections: Detections) -> List[Detection]:
    return [
        Detection(*d)
        for d in zip(
            detections.class_ids.flatten(),
            detections.confidences.flatten(),
            detections.boxes,
        )
    ]
