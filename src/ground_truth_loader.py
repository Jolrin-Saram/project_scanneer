"""
Ground Truth Loader - 주석 데이터 로드 및 파싱 모듈
JSON 형식의 주석 파일을 읽어 검출 결과와 비교
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any


class GroundTruthLoader:
    """Ground Truth 주석 데이터를 로드하고 파싱하는 클래스"""

    def __init__(self, annotation_dir: str = None):
        """
        Args:
            annotation_dir: 주석 파일이 있는 디렉토리
        """
        self.annotation_dir = annotation_dir or "D:/project/data-tools/annotations"
        self.ground_truths = {}
        os.makedirs(self.annotation_dir, exist_ok=True)

    def load_annotations(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        주석 디렉토리에서 모든 JSON 주석 파일 로드

        Returns:
            이미지별 주석 딕셔너리
        """
        print(f"[*] Loading annotations from {self.annotation_dir}...")

        annotation_files = list(Path(self.annotation_dir).glob('*.json'))

        if not annotation_files:
            print(f"[!] No JSON annotation files found in {self.annotation_dir}")
            return {}

        for annotation_file in annotation_files:
            try:
                with open(annotation_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # 파일 이름에서 이미지 이름 추출
                image_name = annotation_file.stem

                # 주석 형식 확인
                if isinstance(data, dict) and 'objects' in data:
                    self.ground_truths[image_name] = data['objects']
                elif isinstance(data, list):
                    self.ground_truths[image_name] = data
                else:
                    print(f"    [!] Unknown annotation format in {annotation_file.name}")
                    continue

                print(f"    [+] Loaded {annotation_file.name}: {len(self.ground_truths[image_name])} objects")

            except json.JSONDecodeError as e:
                print(f"    [!] Failed to parse {annotation_file.name}: {e}")
            except Exception as e:
                print(f"    [!] Error loading {annotation_file.name}: {e}")

        print(f"[+] Loaded annotations for {len(self.ground_truths)} images")
        return self.ground_truths

    def load_annotation_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        특정 주석 파일 로드

        Args:
            file_path: 주석 파일 경로

        Returns:
            주석 리스트
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if isinstance(data, dict) and 'objects' in data:
                return data['objects']
            elif isinstance(data, list):
                return data
            else:
                print(f"[!] Unknown annotation format in {file_path}")
                return []

        except Exception as e:
            print(f"[!] Error loading annotation file {file_path}: {e}")
            return []

    def get_annotations_for_image(self, image_name: str) -> List[Dict[str, Any]]:
        """
        특정 이미지의 주석 가져오기

        Args:
            image_name: 이미지 이름 (확장자 제외)

        Returns:
            주석 리스트
        """
        # 확장자 제거
        base_name = os.path.splitext(image_name)[0]
        return self.ground_truths.get(base_name, [])

    def create_sample_annotation(self, output_path: str = None) -> str:
        """
        샘플 주석 파일 생성

        Args:
            output_path: 저장 경로

        Returns:
            생성된 파일 경로
        """
        if output_path is None:
            output_path = os.path.join(self.annotation_dir, 'sample_annotation.json')

        sample_annotation = {
            "image_name": "image1.jpg",
            "image_size": {
                "width": 1920,
                "height": 1080
            },
            "objects": [
                {
                    "id": 1,
                    "class": "dog",
                    "bbox": {
                        "x1": 100,
                        "y1": 150,
                        "x2": 400,
                        "y2": 500
                    }
                },
                {
                    "id": 2,
                    "class": "cat",
                    "bbox": {
                        "x1": 600,
                        "y1": 200,
                        "x2": 900,
                        "y2": 600
                    }
                },
                {
                    "id": 3,
                    "class": "bird",
                    "bbox": {
                        "x1": 1200,
                        "y1": 100,
                        "x2": 1400,
                        "y2": 300
                    }
                }
            ]
        }

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(sample_annotation, f, indent=2, ensure_ascii=False)

        print(f"[+] Sample annotation created at {output_path}")
        return output_path

    def validate_annotation(self, annotation: Dict[str, Any]) -> Tuple[bool, str]:
        """
        주석 형식 유효성 검사

        Args:
            annotation: 검증할 주석

        Returns:
            (유효 여부, 메시지)
        """
        required_fields = ['class', 'bbox']

        if isinstance(annotation, dict):
            # 필수 필드 확인
            for field in required_fields:
                if field not in annotation:
                    return False, f"Missing required field: {field}"

            # bbox 형식 확인
            bbox = annotation['bbox']
            required_bbox_fields = ['x1', 'y1', 'x2', 'y2']
            for field in required_bbox_fields:
                if field not in bbox:
                    return False, f"Missing bbox field: {field}"

                if not isinstance(bbox[field], (int, float)):
                    return False, f"Invalid bbox value type for {field}"

            return True, "Valid annotation"
        else:
            return False, "Annotation must be a dictionary"

    def print_annotation_summary(self):
        """주석 요약 출력"""
        print("\n" + "="*70)
        print("GROUND TRUTH ANNOTATION SUMMARY")
        print("="*70)

        print(f"\nTotal images with annotations: {len(self.ground_truths)}")

        # 클래스별 객체 수
        class_count = {}
        for image_name, annotations in self.ground_truths.items():
            for annotation in annotations:
                class_name = annotation.get('class', 'Unknown')
                class_count[class_name] = class_count.get(class_name, 0) + 1

        print(f"\nClass Distribution:")
        for class_name, count in sorted(class_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  {class_name}: {count}")

        print(f"\nTotal objects: {sum(class_count.values())}")
        print("="*70 + "\n")


def main():
    """테스트 코드"""
    loader = GroundTruthLoader()

    # 샘플 주석 생성
    sample_path = loader.create_sample_annotation()

    # 주석 로드
    annotations = loader.load_annotations()

    # 요약 출력
    loader.print_annotation_summary()


if __name__ == "__main__":
    main()
