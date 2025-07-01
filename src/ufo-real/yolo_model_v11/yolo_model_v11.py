# -*- coding: utf-8 -*-
"""
YOLO Module:
Imagerecognition aint pretty...
"""

import os
import sys
from typing import Optional

import cv2
from ultralytics import YOLO  # type: ignore # pylint: disable=import-error
from components import Camera, Obstacle, Pylon, VisualNode
from basic import Colour as co


class ImageDetection:
    """Fassade Class to use the YOLO Model you want."""

    # accepted image formats
    img_ext_list = [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG", ".bmp", ".BMP"]

    model_path: str
    camera: Camera
    thresh: float
    resolution: tuple[int, int]
    model: YOLO
    labels: dict[int, str]

    bbox_colors = [
        co.bgr("DUSTY_STEEL_BLUE"),
        co.bgr("WARM_ORANGE"),
        co.bgr("SOFT_CORAL_RED"),
        co.bgr("MINTY_TEAL"),
        co.bgr("OLIVE_GREEN"),
        co.bgr("GOLDEN_SAND"),
        co.bgr("DUSTY_MAUVE"),
        co.bgr("SOFT_PINK_LAVENDER"),
        co.bgr("WARM_TAUPE"),
        co.bgr("LIGHT_WARM_GRAY"),
    ]

    def __init__(
        self,
        model_path: str,
        camera: Camera,
        thresh: float,
        resolution: Optional[str] = None,
    ) -> None:
        self.model_path = model_path
        self.camera = camera
        self.thresh = thresh

        if resolution:  # custom user resolution for better perfomance
            self.resolution = (
                int(resolution.split("x")[0]),
                int(resolution.split("x")[1]),
            )
        else:  # nativ camera resolution for quality
            self.resolution = (camera.get_width, camera.get_height)

        # Check if model file exists and is valid
        if not os.path.exists(model_path):
            model_path = "YOLO_Model_v11\\my_model.pt"  # default in case of misspelling

        # Load the model into memory (takes time) and get label-map
        self.model = YOLO(model_path, task="detect")
        self.labels = self.model.names

    def __str__(self) -> str:
        return (
            "Image Detection Config:\n"
            + "-----------------------\n"
            + f"- Model:\t({self.model_path}\n"
            + f"- Camera:\t{self.camera}\n"
            + f"- Threshhold:\t{self.thresh * 100}%\n"
            + f"- Labels:\t{self.labels}\n"
        )

    def yolo_detect_by_image( # pylint: disable=too-many-locals
        self,
        pic_path: str,
    ) -> tuple[list[VisualNode], list[Obstacle], cv2.typing.MatLike]:
        """let the system recognize all the objects in a given picture"""

        # check to see if the pic_path is usable
        if os.path.isfile(pic_path):
            _, ext = os.path.splitext(pic_path)
            if ext not in self.img_ext_list:
                print(f"File extension {ext} is not supported.")
                sys.exit(0)
        else:
            print("Given path is not a file.")
            sys.exit(0)

        frame = cv2.imread(pic_path)  # pylint: disable=no-member
        frame = cv2.resize(frame, self.resolution) # pylint: disable=no-member

        # Run inference on frame
        results = self.model(frame, verbose=False)

        # Extract results
        detections = results[0].boxes

        # SELF ADDED Node-List
        nodes: list[VisualNode] = []
        pylons: list[Pylon] = []
        obstacles: list[Obstacle] = []

        # Go through each detection and get bbox coords, confidence, and class
        for d in detections:
            # Get bounding box coordinates
            # Ultralytics returns results in Tensor format, which have to be
            # converted to a regular Python array
            xyxy_tensor = detections[
                d
            ].xyxy.cpu()  # Detections in Tensor format in CPU memory
            xyxy = xyxy_tensor.numpy().squeeze()  # Convert tensors to Numpy array
            xmin, ymin, xmax, ymax = xyxy.astype(
                int
            )  # Extract individual coordinates and convert to int

            # Get bounding box class ID, name and confidence
            classidx = int(detections[d].cls.item())
            classname = self.labels[classidx]
            conf = detections[d].conf.item()

            # Draw box if confidence threshold is high enough
            if conf > self.thresh:
                # SELF ADDED CODE
                if classname == "nodes":
                    center_width = int((xmin + xmax) / 2)
                    center_height = int((ymin + ymax) / 2)
                    nodes.append(
                        VisualNode.position_only(str(d), (center_width, center_height))
                    )
                elif classname == "pylon":
                    pylons.append(Pylon(xmin, ymin, xmax, ymax))
                elif classname == "obstacle":
                    obstacles.append(Obstacle(xmin, ymin, xmax, ymax))

        # SELF ADDED CODE - append all the pylon visual nodes
        # - can't be first because that causes a bug somewhere else TODO
        for p in pylons:
            nodes.append(self.camera.compute_hidden_node_image_position(p))

        return (nodes, obstacles, frame)
