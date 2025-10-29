"""
Analyzer - 객체 검출 성능 분석 모듈 (Precision, Recall, AP, mAP 등)
Ground Truth 주석을 기반으로 정확한 성능 메트릭 계산
"""

import numpy as np
from typing import Dict, List, Tuple, Any
from collections import defaultdict
import os
from pathlib import Path


class DetectionAnalyzer:
    """객체 검출 성능을 분석하는 클래스"""

    def __init__(self):
        """초기화"""
        self.ground_truth = {}  # {image_name: [{'class': str, 'bbox': {...}}]}
        self.predictions = {}   # {image_name: [{'class': str, 'bbox': {...}, 'confidence': float}]}
        self.metrics = {}

    def add_ground_truth(self, image_name: str, annotations: List[Dict]):
        """
        ground truth 추가

        Args:
            image_name: 이미지 이름
            annotations: 주석 리스트 [{'class': 'dog', 'bbox': {'x1': 0, 'y1': 0, 'x2': 100, 'y2': 100}}]
        """
        self.ground_truth[image_name] = annotations

    def load_ground_truth_from_dir(self, annotation_dir: str) -> bool:
        """
        주석 디렉토리에서 ground truth 로드

        Args:
            annotation_dir: 주석 파일이 있는 디렉토리

        Returns:
            성공 여부
        """
        try:
            from ground_truth_loader import GroundTruthLoader

            loader = GroundTruthLoader(annotation_dir)
            loaded_annotations = loader.load_annotations()

            if not loaded_annotations:
                print("[!] No annotations loaded")
                return False

            # 로드한 주석을 ground truth로 설정
            for image_name, annotations in loaded_annotations.items():
                # 주석 형식 정규화
                normalized_annotations = []
                for ann in annotations:
                    if isinstance(ann, dict):
                        # 'class' 또는 'label' 필드 지원
                        class_name = ann.get('class') or ann.get('label') or 'Unknown'
                        bbox = ann.get('bbox', {})

                        normalized_annotations.append({
                            'class': class_name,
                            'bbox': bbox,
                        })

                self.add_ground_truth(image_name, normalized_annotations)

            self.has_ground_truth = True
            print(f"[+] Loaded ground truth for {len(loaded_annotations)} images")
            return True

        except ImportError:
            print("[!] ground_truth_loader module not found")
            return False
        except Exception as e:
            print(f"[!] Error loading ground truth: {e}")
            return False

    def add_predictions(self, image_name: str, detections: List[Dict]):
        """
        예측 결과 추가

        Args:
            image_name: 이미지 이름
            detections: 검출 결과 리스트 [{'class': 'dog', 'bbox': {...}, 'confidence': 0.95}]
        """
        self.predictions[image_name] = detections

    def calculate_iou(self, box1: Dict, box2: Dict) -> float:
        """
        IoU (Intersection over Union) 계산

        Args:
            box1, box2: {'x1': float, 'y1': float, 'x2': float, 'y2': float}

        Returns:
            IoU 값 (0.0-1.0)
        """
        x1_inter = max(box1['x1'], box2['x1'])
        y1_inter = max(box1['y1'], box2['y1'])
        x2_inter = min(box1['x2'], box2['x2'])
        y2_inter = min(box1['y2'], box2['y2'])

        if x2_inter < x1_inter or y2_inter < y1_inter:
            return 0.0

        inter_area = (x2_inter - x1_inter) * (y2_inter - y1_inter)

        box1_area = (box1['x2'] - box1['x1']) * (box1['y2'] - box1['y1'])
        box2_area = (box2['x2'] - box2['x1']) * (box2['y2'] - box2['y1'])

        union_area = box1_area + box2_area - inter_area

        if union_area == 0:
            return 0.0

        return inter_area / union_area

    def match_predictions_with_ground_truth(self, iou_threshold: float = 0.5) -> Dict[str, Any]:
        """
        예측과 ground truth 매칭

        Args:
            iou_threshold: IoU 임계값

        Returns:
            매칭 결과
        """
        matches = defaultdict(list)
        tp = 0  # True Positives
        fp = 0  # False Positives
        fn = 0  # False Negatives

        class_tp = defaultdict(int)
        class_fp = defaultdict(int)
        class_fn = defaultdict(int)

        for image_name in self.predictions:
            predictions = self.predictions.get(image_name, [])
            ground_truths = self.ground_truth.get(image_name, [])

            matched_gt = set()

            # 예측된 각 객체에 대해
            for pred in predictions:
                pred_class = pred['class']
                pred_bbox = pred['bbox']
                best_iou = 0
                best_gt_idx = -1

                # Ground truth와의 최고 IoU 찾기
                for gt_idx, gt in enumerate(ground_truths):
                    if gt_idx not in matched_gt and gt['class'] == pred_class:
                        iou = self.calculate_iou(pred_bbox, gt['bbox'])
                        if iou > best_iou:
                            best_iou = iou
                            best_gt_idx = gt_idx

                if best_iou >= iou_threshold and best_gt_idx != -1:
                    tp += 1
                    class_tp[pred_class] += 1
                    matched_gt.add(best_gt_idx)
                    matches[image_name].append({
                        'prediction': pred,
                        'ground_truth': ground_truths[best_gt_idx],
                        'iou': best_iou,
                        'match': 'TP'
                    })
                else:
                    fp += 1
                    class_fp[pred_class] += 1
                    matches[image_name].append({
                        'prediction': pred,
                        'ground_truth': None,
                        'iou': best_iou,
                        'match': 'FP'
                    })

            # 매칭되지 않은 ground truth
            for gt_idx, gt in enumerate(ground_truths):
                if gt_idx not in matched_gt:
                    fn += 1
                    class_fn[gt['class']] += 1

        return {
            'total_tp': tp,
            'total_fp': fp,
            'total_fn': fn,
            'class_tp': dict(class_tp),
            'class_fp': dict(class_fp),
            'class_fn': dict(class_fn),
            'matches': dict(matches),
        }

    def calculate_metrics(self, matches: Dict[str, Any]) -> Dict[str, Any]:
        """
        Precision, Recall, F1 Score 계산

        Args:
            matches: 매칭 결과

        Returns:
            메트릭 딕셔너리
        """
        tp = matches['total_tp']
        fp = matches['total_fp']
        fn = matches['total_fn']

        metrics = {
            'overall': {},
            'per_class': {},
        }

        # 전체 메트릭
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        metrics['overall']['precision'] = precision
        metrics['overall']['recall'] = recall
        metrics['overall']['f1_score'] = f1_score
        metrics['overall']['tp'] = tp
        metrics['overall']['fp'] = fp
        metrics['overall']['fn'] = fn

        # 클래스별 메트릭
        all_classes = set(list(matches['class_tp'].keys()) + list(matches['class_fp'].keys()) + list(matches['class_fn'].keys()))

        for class_name in all_classes:
            class_tp = matches['class_tp'].get(class_name, 0)
            class_fp = matches['class_fp'].get(class_name, 0)
            class_fn = matches['class_fn'].get(class_name, 0)

            class_precision = class_tp / (class_tp + class_fp) if (class_tp + class_fp) > 0 else 0
            class_recall = class_tp / (class_tp + class_fn) if (class_tp + class_fn) > 0 else 0
            class_f1 = 2 * (class_precision * class_recall) / (class_precision + class_recall) \
                if (class_precision + class_recall) > 0 else 0

            metrics['per_class'][class_name] = {
                'precision': class_precision,
                'recall': class_recall,
                'f1_score': class_f1,
                'tp': class_tp,
                'fp': class_fp,
                'fn': class_fn,
            }

        return metrics

    def calculate_ap(self, matches: Dict[str, Any], iou_threshold: float = 0.5) -> Dict[str, float]:
        """
        AP (Average Precision) 계산 (COCO 스타일)

        Args:
            matches: 매칭 결과
            iou_threshold: IoU 임계값

        Returns:
            클래스별 AP 값
        """
        class_ap = {}

        all_classes = set(list(matches['class_tp'].keys()) + list(matches['class_fp'].keys()))

        for class_name in all_classes:
            # 해당 클래스의 모든 예측과 ground truth 수집
            class_predictions = []
            total_ground_truth = 0

            for image_name, image_matches in matches['matches'].items():
                for match in image_matches:
                    if match['prediction']['class'] == class_name:
                        class_predictions.append({
                            'confidence': match['prediction'].get('confidence', 0),
                            'is_tp': match['match'] == 'TP',
                        })

                total_ground_truth += matches['class_fn'].get(class_name, 0)

            total_ground_truth += matches['class_tp'].get(class_name, 0)

            if total_ground_truth == 0 or not class_predictions:
                class_ap[class_name] = 0.0
                continue

            # 신뢰도로 정렬
            class_predictions.sort(key=lambda x: x['confidence'], reverse=True)

            # Precision-Recall 곡선 계산
            tp_count = 0
            fp_count = 0
            precisions = []
            recalls = []

            for pred in class_predictions:
                if pred['is_tp']:
                    tp_count += 1
                else:
                    fp_count += 1

                precision = tp_count / (tp_count + fp_count)
                recall = tp_count / total_ground_truth

                precisions.append(precision)
                recalls.append(recall)

            # AP 계산 (간단한 버전)
            class_ap[class_name] = np.mean(precisions) if precisions else 0.0

        return class_ap

    def get_detection_rate(self, total_objects: int = None) -> float:
        """
        객체 검출률 계산

        Args:
            total_objects: 전체 객체 수 (None이면 ground truth 기반)

        Returns:
            검출률 (%)
        """
        if total_objects is None:
            total_objects = sum(len(ann) for ann in self.ground_truth.values())

        if total_objects == 0:
            return 0.0

        total_detected = sum(len(pred) for pred in self.predictions.values())

        return (total_detected / total_objects) * 100

    def analyze_all(self, iou_threshold: float = 0.5) -> Dict[str, Any]:
        """
        전체 분석 수행

        Args:
            iou_threshold: IoU 임계값

        Returns:
            모든 분석 결과
        """
        matches = self.match_predictions_with_ground_truth(iou_threshold)
        metrics = self.calculate_metrics(matches)
        ap_scores = self.calculate_ap(matches, iou_threshold)

        return {
            'matches': matches,
            'metrics': metrics,
            'ap_scores': ap_scores,
            'detection_rate': self.get_detection_rate(),
            'iou_threshold': iou_threshold,
        }

    def print_results(self, results: Dict[str, Any]):
        """분석 결과 출력"""
        print("\n" + "="*70)
        print("DETECTION ANALYSIS RESULTS")
        print("="*70)

        # 전체 메트릭
        overall = results['metrics']['overall']
        print(f"\nOverall Metrics:")
        print(f"  Precision: {overall['precision']:.4f}")
        print(f"  Recall: {overall['recall']:.4f}")
        print(f"  F1 Score: {overall['f1_score']:.4f}")
        print(f"  TP: {overall['tp']}, FP: {overall['fp']}, FN: {overall['fn']}")

        # 클래스별 메트릭
        if results['metrics']['per_class']:
            print(f"\nPer-Class Metrics:")
            for class_name, class_metrics in results['metrics']['per_class'].items():
                print(f"  {class_name}:")
                print(f"    Precision: {class_metrics['precision']:.4f}")
                print(f"    Recall: {class_metrics['recall']:.4f}")
                print(f"    F1 Score: {class_metrics['f1_score']:.4f}")

        # AP 점수
        if results['ap_scores']:
            print(f"\nAverage Precision (AP) @ IoU={results['iou_threshold']}:")
            for class_name, ap in results['ap_scores'].items():
                print(f"  {class_name}: {ap:.4f}")

        # mAP
        mAP = np.mean(list(results['ap_scores'].values())) if results['ap_scores'] else 0
        print(f"\nmAP (mean Average Precision): {mAP:.4f}")

        # 검출률
        print(f"\nDetection Rate: {results['detection_rate']:.2f}%")

        print("="*70 + "\n")


def main():
    """테스트 코드"""
    analyzer = DetectionAnalyzer()

    # 샘플 ground truth 추가
    analyzer.add_ground_truth('image1.jpg', [
        {'class': 'dog', 'bbox': {'x1': 10, 'y1': 20, 'x2': 100, 'y2': 150}},
        {'class': 'cat', 'bbox': {'x1': 120, 'y1': 30, 'x2': 200, 'y2': 180}},
    ])

    # 샘플 예측 추가
    analyzer.add_predictions('image1.jpg', [
        {'class': 'dog', 'bbox': {'x1': 12, 'y1': 22, 'x2': 102, 'y2': 152}, 'confidence': 0.95},
        {'class': 'cat', 'bbox': {'x1': 125, 'y1': 35, 'x2': 205, 'y2': 185}, 'confidence': 0.85},
    ])

    # 분석 실행
    results = analyzer.analyze_all()

    # 결과 출력
    analyzer.print_results(results)


if __name__ == "__main__":
    main()
