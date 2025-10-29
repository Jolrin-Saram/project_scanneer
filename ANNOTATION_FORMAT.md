# Ground Truth Annotation Format Guide

YOLO 검출 성능 분석을 위한 주석(Ground Truth) 파일 형식 설명입니다.

## 개요

주석 파일은 **JSON 형식**이며, 각 이미지별로 별도의 파일로 저장됩니다.

## 파일 구조

```
D:\project\data-tools\
├── inputs/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── image3.png
├── annotations/
│   ├── image1.json
│   ├── image2.json
│   └── image3.json
└── outputs/
```

## JSON 형식

### 기본 형식

```json
{
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
    }
  ]
}
```

### 필드 설명

#### 최상위 필드 (선택사항)

- **image_name** (string): 이미지 파일명
- **image_size** (object): 이미지 크기 정보
  - **width** (int): 이미지 너비 (픽셀)
  - **height** (int): 이미지 높이 (픽셀)

#### objects 배열 필드

**각 객체는 다음 필드를 포함해야 합니다:**

- **class** (string, 필수): 객체 클래스명
  - 예: "dog", "cat", "bird", "defect_type_1" 등
  - 영문자, 숫자, 언더스코어(_) 사용 권장

- **bbox** (object, 필수): 바운딩 박스 좌표
  - **x1** (float, int): 좌상단 X 좌표
  - **y1** (float, int): 좌상단 Y 좌표
  - **x2** (float, int): 우하단 X 좌표
  - **y2** (float, int): 우하단 Y 좌표

**선택사항 필드:**

- **id** (int): 객체 ID (고유식별자)
- **confidence** (float): 주석자 확신도 (0.0-1.0)
- **difficult** (boolean): 어려운 케이스 표시
- **occluded** (boolean): 부분적으로 가려짐 표시

## 예제

### 예제 1: 동물 객체 검출

파일명: `dog_image.json`

```json
{
  "image_name": "dog_image.jpg",
  "image_size": {
    "width": 1024,
    "height": 768
  },
  "objects": [
    {
      "id": 1,
      "class": "dog",
      "bbox": {
        "x1": 150,
        "y1": 200,
        "x2": 450,
        "y2": 650
      },
      "confidence": 0.95
    },
    {
      "id": 2,
      "class": "dog",
      "bbox": {
        "x1": 600,
        "y1": 100,
        "x2": 900,
        "y2": 500
      },
      "confidence": 0.92
    }
  ]
}
```

### 예제 2: 불량 객체 검출 (산업용)

파일명: `product_001.json`

```json
{
  "image_name": "product_001.jpg",
  "image_size": {
    "width": 1280,
    "height": 960
  },
  "objects": [
    {
      "id": 1,
      "class": "scratch",
      "bbox": {
        "x1": 100,
        "y1": 200,
        "x2": 300,
        "y2": 250
      },
      "difficult": false
    },
    {
      "id": 2,
      "class": "dent",
      "bbox": {
        "x1": 500,
        "y1": 400,
        "x2": 700,
        "y2": 600
      },
      "occluded": true
    }
  ]
}
```

### 예제 3: 객체가 없는 이미지

파일명: `empty_image.json`

```json
{
  "image_name": "empty_image.jpg",
  "objects": []
}
```

## 주석 파일 생성 방법

### 수동 생성

1. 텍스트 에디터 (VS Code, Sublime Text 등)에서 위 형식대로 작성
2. 파일을 `annotations` 폴더에 저장
3. 파일명은 이미지명과 동일하되 확장자는 `.json`

### 자동 생성 스크립트

```python
import json
import os

def create_annotation_template(image_path, output_dir):
    """
    이미지로부터 주석 템플릿 생성
    """
    from PIL import Image

    image_name = os.path.basename(image_path)
    base_name = os.path.splitext(image_name)[0]

    # 이미지 크기 확인
    img = Image.open(image_path)
    width, height = img.size

    # 템플릿 생성
    annotation = {
        "image_name": image_name,
        "image_size": {
            "width": width,
            "height": height
        },
        "objects": []
    }

    # JSON 파일 저장
    output_path = os.path.join(output_dir, f"{base_name}.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(annotation, f, indent=2, ensure_ascii=False)

    print(f"[+] Template created: {output_path}")
```

### CVAT, LabelImg 등에서 변환

다른 라벨링 도구에서 생성한 주석을 JSON으로 변환할 수 있습니다.

**Pascal VOC XML → JSON 변환 예제:**

```python
import xml.etree.ElementTree as ET
import json
import os

def convert_voc_to_json(xml_path, output_dir):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    image_name = root.find('filename').text
    size = root.find('size')

    annotation = {
        "image_name": image_name,
        "image_size": {
            "width": int(size.find('width').text),
            "height": int(size.find('height').text)
        },
        "objects": []
    }

    for obj in root.findall('object'):
        class_name = obj.find('name').text
        bndbox = obj.find('bndbox')

        annotation["objects"].append({
            "class": class_name,
            "bbox": {
                "x1": int(bndbox.find('xmin').text),
                "y1": int(bndbox.find('ymin').text),
                "x2": int(bndbox.find('xmax').text),
                "y2": int(bndbox.find('ymax').text)
            }
        })

    base_name = os.path.splitext(image_name)[0]
    output_path = os.path.join(output_dir, f"{base_name}.json")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(annotation, f, indent=2, ensure_ascii=False)
```

## 검증

주석 파일의 유효성을 확인하려면:

```python
from src.ground_truth_loader import GroundTruthLoader

loader = GroundTruthLoader('D:/project/data-tools/annotations')
annotations = loader.load_annotations()

# 요약 출력
loader.print_annotation_summary()

# 개별 주석 검증
for image_name, objects in annotations.items():
    for obj in objects:
        valid, msg = loader.validate_annotation(obj)
        if not valid:
            print(f"[!] Invalid annotation in {image_name}: {msg}")
```

## 주의사항

1. **파일명 일치**: 주석 파일명(확장자 제외)은 이미지 파일명과 동일해야 합니다.
   - ✅ image1.jpg → image1.json
   - ❌ image1.jpg → img1.json

2. **좌표 범위**: 바운딩 박스 좌표는 이미지 범위 내에 있어야 합니다.
   - 0 ≤ x1, x2 ≤ width
   - 0 ≤ y1, y2 ≤ height

3. **좌표 순서**: x1 < x2, y1 < y2 이어야 합니다.

4. **클래스명**: 일관성 있는 클래스명을 사용하세요.
   - ✅ "dog", "cat", "bird" (소문자)
   - ❌ "Dog", "DOG", "Dog " (대소문자 또는 공백 포함)

5. **UTF-8 인코딩**: JSON 파일은 UTF-8 인코딩으로 저장하세요.

## 샘플 생성

다음 명령으로 샘플 주석 파일을 생성할 수 있습니다:

```bash
python -c "from src.ground_truth_loader import GroundTruthLoader; loader = GroundTruthLoader(); loader.create_sample_annotation()"
```

생성된 파일: `D:\project\data-tools\annotations\sample_annotation.json`

## 분석 실행

주석 파일이 준비되면 다음 명령으로 분석을 실행합니다:

```bash
# 주석 디렉토리 자동 감지
python main.py

# 또는 명시적으로 주석 디렉토리 지정
python main.py --annotations D:/project/data-tools/annotations
```

분석 결과에 다음 메트릭이 포함됩니다:
- Precision (정확도)
- Recall (재현율)
- F1 Score
- Average Precision (AP)
- mean Average Precision (mAP)
- Confusion Matrix (TP, FP, FN)

---

더 자세한 정보는 README.md를 참고하세요.
