"""
detector.py
YOLOv8-based object detector for VisionAssist.

Wraps Ultralytics YOLOv8n for real-time webcam inference, with:
- class filtering (only run inference for the class we're searching for)
- confidence thresholding
- lightweight inference size for speed
- returns clean structured detections for navigator.py to consume
"""
import cv2
import torch
from ultralytics import YOLO


class Detector:
    def __init__(
        self,
        model_path: str = "models/yolov8n.pt",
        conf_threshold: float = 0.45,
        iou_threshold: float = 0.45,
        infer_size: int = 416,  # smaller = faster, 416 is a good speed/accuracy tradeoff for webcam
    ):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = YOLO(model_path)
        self.model.to(self.device)

        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.infer_size = infer_size

        # COCO class name -> id map, built once from the model itself
        self.class_names = self.model.names  # dict: {0: 'person', 39: 'bottle', ...}
        self.name_to_id = {v: k for k, v in self.class_names.items()}

        # Half precision only helps on GPU; skip on CPU
        self.half = self.device == "cuda"

    def detect(self, frame, target_class_ids=None):
        """
        Run detection on a single frame.

        Args:
            frame: BGR image (numpy array) from OpenCV
            target_class_ids: optional list of COCO class ids to restrict detection to

        Returns:
            List of dicts sorted by confidence (highest first):
            [{"class_name", "class_id", "conf", "box", "center", "box_height", "frame_shape"}]
        """
        h, w = frame.shape[:2]

        results = self.model.predict(
            source=frame,
            imgsz=self.infer_size,
            conf=self.conf_threshold,
            iou=self.iou_threshold,
            classes=target_class_ids,  # None = all classes, or restrict to requested ones
            half=self.half,
            device=self.device,
            verbose=False,
        )

        detections = []
        result = results[0]

        if result.boxes is not None and len(result.boxes) > 0:
            boxes = result.boxes.xyxy.cpu().numpy()
            confs = result.boxes.conf.cpu().numpy()
            cls_ids = result.boxes.cls.cpu().numpy().astype(int)

            for box, conf, cls_id in zip(boxes, confs, cls_ids):
                x1, y1, x2, y2 = box
                cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

                detections.append({
                    "class_name": self.class_names[cls_id],
                    "class_id": int(cls_id),
                    "conf": float(conf),
                    "box": (float(x1), float(y1), float(x2), float(y2)),
                    "center": (float(cx), float(cy)),
                    "box_height": float(y2 - y1),  # used by navigator.py for distance estimate
                    "frame_shape": (h, w),
                })

        detections.sort(key=lambda d: d["conf"], reverse=True)
        return detections

    def class_id_for_name(self, name: str):
        """Look up a COCO class id from its name (used by object_mapper.py)."""
        return self.name_to_id.get(name)

    def draw_detections(self, frame, detections, highlight_class=None):
        """Draw bounding boxes + labels on a frame for the demo recording."""
        for det in detections:
            x1, y1, x2, y2 = map(int, det["box"])
            label = f'{det["class_name"]} {det["conf"]:.2f}'

            is_target = highlight_class is not None and det["class_name"] == highlight_class
            color = (0, 0, 255) if is_target else (0, 200, 0)  # red = target, green = others
            thickness = 3 if is_target else 1

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
            cv2.putText(
                frame, label, (x1, max(y1 - 8, 12)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2,
            )

        return frame


# Quick standalone test: python src/detector.py
if __name__ == "__main__":
    detector = Detector()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        dets = detector.detect(frame)
        frame = detector.draw_detections(frame, dets)

        cv2.imshow("VisionAssist - Detector Test", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
