"""
Detector - YOLO4/YOLO8 모델을 사용한 객체 검출 모듈
파일명 기반 지능형 분류 기능 포함
"""

import os
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime
from file_classifier import FileClassifier


class YOLODetector:
    """YOLO 모델을 사용하여 객체를 검출하는 클래스"""

    def __init__(self, model_path: str, confidence: float = 0.5, iou: float = 0.45):
        """
        Args:
            model_path: YOLO 모델 경로 (예: 'yolov8n.pt')
            confidence: 신뢰도 임계값 (0.0-1.0)
            iou: NMS IOU 임계값 (0.0-1.0)
        """
        self.model_path = model_path
        self.confidence = confidence
        self.iou = iou
        self.model = None
        self.device = None
        self.class_names = {}
        self.detections = []
        self.file_classifier = FileClassifier()  # 파일명 분류기 초기화

    def load_model(self) -> bool:
        """YOLO 모델 로드"""
        print(f"[*] Loading YOLO model from {self.model_path}...")

        try:
            from ultralytics import YOLO
            import torch

            # GPU 여부 확인
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
            print(f"    [+] Using device: {self.device}")

            # 모델 로드
            self.model = YOLO(self.model_path)
            print(f"    [+] Model loaded successfully: {self.model_path}")

            # 클래스 이름 추출
            if hasattr(self.model, 'names'):
                self.class_names = self.model.names
                print(f"    [+] Classes: {len(self.class_names)}")

            return True

        except ImportError as e:
            print(f"    [!] Error: ultralytics not installed: {e}")
            return False
        except Exception as e:
            print(f"    [!] Error loading model: {e}")
            return False

    def detect_image(self, image_path: str) -> Dict[str, Any]:
        """
        단일 이미지 객체 검출

        Args:
            image_path: 이미지 파일 경로

        Returns:
            검출 결과 딕셔너리
        """
        if self.model is None:
            print("[!] Model not loaded. Please load model first.")
            return {}

        if not os.path.exists(image_path):
            print(f"[!] Image file not found: {image_path}")
            return {}

        try:
            # 이미지 로드
            image = cv2.imread(image_path)
            if image is None:
                print(f"[!] Failed to load image: {image_path}")
                return {}

            height, width = image.shape[:2]

            # 객체 검출
            results = self.model(image_path, conf=self.confidence, iou=self.iou, device=self.device)

            # 결과 처리
            detections = []
            if results and len(results) > 0:
                for result in results:
                    if result.boxes is not None:
                        for box in result.boxes:
                            detection = {
                                'class_id': int(box.cls.item()),
                                'class_name': self.class_names.get(int(box.cls.item()), 'Unknown'),
                                'confidence': float(box.conf.item()),
                                'bbox': {
                                    'x1': float(box.xyxy[0][0].item()),
                                    'y1': float(box.xyxy[0][1].item()),
                                    'x2': float(box.xyxy[0][2].item()),
                                    'y2': float(box.xyxy[0][3].item()),
                                },
                            }
                            detections.append(detection)

            result_dict = {
                'image_path': image_path,
                'image_name': os.path.basename(image_path),
                'image_size': {'width': width, 'height': height},
                'timestamp': datetime.now().isoformat(),
                'detections': detections,
                'total_detections': len(detections),
                'unique_classes': len(set([d['class_id'] for d in detections])),
            }

            self.detections.append(result_dict)
            return result_dict

        except Exception as e:
            print(f"[!] Error detecting objects in {image_path}: {e}")
            return {}

    def detect_directory(self, directory_path: str, image_extensions: List[str] = None) -> List[Dict[str, Any]]:
        """
        디렉토리 내 모든 이미지 객체 검출

        Args:
            directory_path: 이미지가 있는 디렉토리 경로
            image_extensions: 처리할 이미지 확장자 (기본값: jpg, jpeg, png, bmp, tiff)

        Returns:
            모든 검출 결과 리스트
        """
        if image_extensions is None:
            image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']

        print(f"\n[*] Detecting objects in {directory_path}...")

        if not os.path.isdir(directory_path):
            print(f"[!] Directory not found: {directory_path}")
            return []

        image_files = []
        for ext in image_extensions:
            image_files.extend(Path(directory_path).glob(f'*{ext}'))
            image_files.extend(Path(directory_path).glob(f'*{ext.upper()}'))

        image_files = list(set(image_files))  # 중복 제거
        total_images = len(image_files)

        if total_images == 0:
            print(f"[!] No image files found in {directory_path}")
            return []

        print(f"    [+] Found {total_images} image(s)")

        # 파일명 기반 분류
        image_filenames = [f.name for f in image_files]
        self.file_classifier.classify_files(image_filenames)
        self.file_classifier.get_classification_groups()
        self.file_classifier.get_classification_stats()

        print(f"    [+] File classification completed")
        print(f"        - Classification types: {len(self.file_classifier.classification_groups)}")

        all_results = []
        for idx, image_file in enumerate(sorted(image_files), 1):
            print(f"    [{idx}/{total_images}] Processing {image_file.name}...", end=' ')
            result = self.detect_image(str(image_file))
            if result:
                # 파일 분류 정보 추가
                file_classification = self.file_classifier.classifications.get(image_file.name, 'Unknown')
                result['file_classification'] = file_classification
                all_results.append(result)
                print(f"✓ ({result['total_detections']} objects, {file_classification})")
            else:
                print("✗ Failed")

        return all_results

    def draw_detections(self, image_path: str, detections: List[Dict], output_path: str = None) -> bool:
        """
        이미지에 검출 결과 그리기

        Args:
            image_path: 원본 이미지 경로
            detections: 검출 결과 리스트
            output_path: 결과 이미지 저장 경로

        Returns:
            성공 여부
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                print(f"[!] Failed to load image: {image_path}")
                return False

            # 검출 결과 그리기
            for detection in detections:
                bbox = detection['bbox']
                class_name = detection['class_name']
                confidence = detection['confidence']

                x1, y1 = int(bbox['x1']), int(bbox['y1'])
                x2, y2 = int(bbox['x2']), int(bbox['y2'])

                # 바운딩 박스 그리기
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # 라벨 그리기
                label = f"{class_name} {confidence:.2f}"
                cv2.putText(image, label, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # 결과 저장
            if output_path is None:
                output_path = image_path.replace('.jpg', '_detected.jpg').replace('.png', '_detected.png')

            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
            cv2.imwrite(output_path, image)
            print(f"    [+] Detection visualization saved to {output_path}")
            return True

        except Exception as e:
            print(f"[!] Error drawing detections: {e}")
            return False

    def get_detection_summary(self) -> Dict[str, Any]:
        """검출 결과 요약"""
        summary = {
            'total_images': len(self.detections),
            'total_objects': sum(d['total_detections'] for d in self.detections),
            'avg_objects_per_image': 0,
            'class_distribution': {},
            'file_classification_stats': {},  # 파일명 분류별 통계
            'file_classification_distribution': {},  # 파일명 분류별 객체 수
            'confidence_stats': {
                'min': 1.0,
                'max': 0.0,
                'avg': 0.0,
            },
            'detection_rate': 0.0,  # 객체가 검출된 이미지 비율
        }

        if not self.detections:
            return summary

        # 평균 객체 수
        summary['avg_objects_per_image'] = summary['total_objects'] / summary['total_images']

        # 클래스 분포
        for detection_result in self.detections:
            for detection in detection_result['detections']:
                class_name = detection['class_name']
                summary['class_distribution'][class_name] = \
                    summary['class_distribution'].get(class_name, 0) + 1

        # 신뢰도 통계
        all_confidences = []
        for detection_result in self.detections:
            for detection in detection_result['detections']:
                all_confidences.append(detection['confidence'])

        if all_confidences:
            summary['confidence_stats']['min'] = min(all_confidences)
            summary['confidence_stats']['max'] = max(all_confidences)
            summary['confidence_stats']['avg'] = sum(all_confidences) / len(all_confidences)

        # 검출률 (객체가 검출된 이미지 비율)
        images_with_objects = sum(1 for d in self.detections if d['total_detections'] > 0)
        summary['detection_rate'] = (images_with_objects / summary['total_images'] * 100) if summary['total_images'] > 0 else 0

        # 파일명 분류별 통계
        file_classification_count = {}
        file_classification_objects = {}

        for detection_result in self.detections:
            file_class = detection_result.get('file_classification', 'Unknown')
            file_classification_count[file_class] = file_classification_count.get(file_class, 0) + 1
            file_classification_objects[file_class] = file_classification_objects.get(file_class, 0) + detection_result['total_detections']

        summary['file_classification_stats'] = file_classification_count
        summary['file_classification_distribution'] = file_classification_objects

        return summary

    def clear_detections(self):
        """검출 결과 초기화"""
        self.detections = []
        print("[*] Detection results cleared")


def main():
    """테스트 코드"""
    # YOLO8 nano 모델 사용
    detector = YOLODetector('yolov8n.pt', confidence=0.5)

    if detector.load_model():
        # 샘플 이미지 디렉토리 검출
        results = detector.detect_directory('D:/project/data-tools/inputs')

        # 요약 출력
        summary = detector.get_detection_summary()
        print("\nDetection Summary:")
        print(f"  Total images: {summary['total_images']}")
        print(f"  Total objects: {summary['total_objects']}")
        print(f"  Detection rate: {summary['detection_rate']:.2f}%")
        print(f"  Class distribution: {summary['class_distribution']}")


if __name__ == "__main__":
    main()
