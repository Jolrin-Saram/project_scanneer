# YOLO Detection Analysis Tool - Project Summary

완성된 YOLO 객체 검출 성능 분석 도구의 전체 개요입니다.

---

## 📋 프로젝트 개요

**목적**: YOLO4/YOLO8 기반 객체 검출 모델의 성능을 자동으로 분석, 평가, 보고하는 통합 도구

**주요 특징**:
- ✅ 완전 자동화된 파이프라인 (모델 로드 → 검출 → 분석 → 리포팅)
- ✅ Ground Truth 주석 기반 정확한 성능 메트릭 계산
- ✅ GPU/CUDA 자동 감지 및 최적화
- ✅ 멀티 프로젝트 환경 지원 (프로젝트 자동 발견)
- ✅ 다양한 출력 형식 (그래프 + Excel 리포트)

---

## 📁 생성된 파일 구조

### 핵심 모듈 (src 폴더)

| 파일명 | 역할 | 주요 기능 |
|--------|------|---------|
| **project_scanner.py** | 프로젝트 발견 | D:\project 내 모든 Python 프로젝트 자동 스캔 |
| **system_detector.py** | 시스템 정보 수집 | GPU/CUDA/CPU 자동 감지, 시스템 사양 파악 |
| **generate_requirements.py** | 요구사항 생성 | 시스템 사양에 맞는 requirements.txt 자동 생성 |
| **integrated_setup.py** | 환경 셋업 | 5단계 자동 설정 프로세스 (스캔→감지→생성→생성→설치) |
| **detector.py** | 객체 검출 | YOLO 모델 로드 및 이미지 처리 |
| **ground_truth_loader.py** | 주석 로드 | Ground Truth JSON 파일 로드 및 검증 |
| **analyzer.py** | 성능 분석 | Precision/Recall/AP/mAP 등 메트릭 계산 |
| **visualizer.py** | 시각화 | 성능 메트릭 그래프 자동 생성 |
| **reporter.py** | 리포팅 | Excel 파일로 상세 분석 결과 내보내기 |

### 메인 실행 파일

| 파일명 | 역할 |
|--------|------|
| **setup.py** | 통합 환경 셋업 (Python) |
| **setup_windows.bat** | Windows 배치 파일 |
| **main.py** | YOLO 분석 도구 메인 스크립트 |

### 문서 및 설정

| 파일명 | 설명 |
|--------|------|
| **README.md** | 사용자 가이드 및 시작하기 |
| **ANNOTATION_FORMAT.md** | Ground Truth 주석 형식 설명 |
| **requirements_template.txt** | Python 패키지 템플릿 |
| **PROJECT_SUMMARY.md** | 이 파일 |

---

## 🔄 전체 워크플로우

```
1. 초기 설정 (새 컴퓨터)
   ↓
2. setup.py 또는 setup_windows.bat 실행
   ├─ [STEP 1] 프로젝트 스캔 (project_scanner.py)
   ├─ [STEP 2] 시스템 감지 (system_detector.py)
   ├─ [STEP 3] Requirements 생성 (generate_requirements.py)
   ├─ [STEP 4] 가상환경 생성
   └─ [STEP 5] 패키지 설치
   ↓
3. 가상환경 활성화
   ↓
4. main.py 실행
   ├─ [STEP 1] 모델 로드 (detector.py)
   ├─ [STEP 2] 객체 검출 (detector.py)
   ├─ [STEP 3] 성능 분석 (ground_truth_loader.py + analyzer.py)
   ├─ [STEP 4] 그래프 생성 (visualizer.py)
   └─ [STEP 5] Excel 리포트 (reporter.py)
   ↓
5. 결과 확인
   ├─ outputs/metrics_summary.png
   ├─ outputs/detection_rate.png
   ├─ outputs/class_distribution.png
   ├─ outputs/confidence_distribution.png
   ├─ outputs/file_type_distribution.png
   ├─ outputs/defect_type_distribution.png
   └─ outputs/YOLO_Analysis_Report_*.xlsx
```

---

## 🛠️ 각 모듈 상세 설명

### 1. Project Scanner (project_scanner.py)

**목적**: D:\project 내 모든 Python 프로젝트 자동 발견

**기능**:
- requirements.txt, setup.py, pyproject.toml 검색
- 프로젝트별 의존성 추출
- 프로젝트 구조 분석 및 JSON 리포트 생성

**출력**: `config/project_scan_report.json`

```python
from src.project_scanner import ProjectScanner
scanner = ProjectScanner('D:/project')
projects = scanner.scan()
scanner.save_report()
```

---

### 2. System Detector (system_detector.py)

**목적**: 현재 시스템의 GPU/CUDA/CPU 정보 자동 감지

**감지 항목**:
- OS/아키텍처
- CPU 정보 (이름, 코어, 스레드)
- GPU 정보 (NVIDIA GPU 감지, VRAM)
- CUDA 버전
- cuDNN 설치 여부
- PyTorch 설치 여부
- 시스템 메모리

**출력**: `config/system_config.json`

```python
from src.system_detector import SystemDetector
detector = SystemDetector()
info = detector.detect_all()
detector.print_summary()
detector.save_config()
```

---

### 3. Generate Requirements (generate_requirements.py)

**목적**: 모든 프로젝트의 의존성을 통합하여 requirements.txt 생성

**프로세스**:
1. 프로젝트 스캔 리포트 로드
2. 시스템 정보 로드
3. 모든 의존성 병합
4. 충돌 해결
5. CUDA 버전에 맞는 PyTorch 선택

**출력**: `requirements.txt` (자동 생성)

```python
from src.generate_requirements import RequirementsGenerator
gen = RequirementsGenerator(report_path, config_path)
gen.load_data()
gen.save_requirements()
```

---

### 4. Integrated Setup (integrated_setup.py)

**목적**: 1부터 3까지의 전체 프로세스를 자동화

**5단계 프로세스**:
1. 프로젝트 스캔
2. 시스템 감지
3. Requirements 생성
4. 가상환경 생성
5. 패키지 설치

---

### 5. Detector (detector.py)

**목적**: YOLO 모델을 로드하고 이미지에서 객체 검출

**주요 메서드**:
- `load_model()`: YOLO 모델 로드
- `detect_image()`: 단일 이미지 검출
- `detect_directory()`: 디렉토리 내 모든 이미지 검출
- `get_detection_summary()`: 검출 결과 요약

```python
from src.detector import YOLODetector
detector = YOLODetector('yolov8n.pt', confidence=0.5)
detector.load_model()
results = detector.detect_directory('inputs/')
summary = detector.get_detection_summary()
```

**검출 결과 형식**:
```python
{
    'image_name': 'image1.jpg',
    'image_size': {'width': 1920, 'height': 1080},
    'total_detections': 5,
    'detections': [
        {
            'class_name': 'dog',
            'confidence': 0.95,
            'bbox': {'x1': 100, 'y1': 150, 'x2': 400, 'y2': 500}
        },
        ...
    ]
}
```

---

### 6. Ground Truth Loader (ground_truth_loader.py)

**목적**: JSON 형식의 Ground Truth 주석 파일 로드

**기능**:
- JSON 주석 파일 파싱
- 주석 형식 검증
- 샘플 주석 생성

```python
from src.ground_truth_loader import GroundTruthLoader
loader = GroundTruthLoader('annotations/')
annotations = loader.load_annotations()
loader.print_annotation_summary()
```

**주석 파일 형식**:
```json
{
  "image_name": "image1.jpg",
  "objects": [
    {
      "class": "dog",
      "bbox": {"x1": 100, "y1": 150, "x2": 400, "y2": 500}
    }
  ]
}
```

---

### 7. Analyzer (analyzer.py)

**목적**: 검출 결과와 Ground Truth를 비교하여 성능 메트릭 계산

**계산 메트릭**:
- **Precision**: TP / (TP + FP)
- **Recall**: TP / (TP + FN)
- **F1 Score**: 조화 평균
- **IoU**: Intersection over Union
- **AP**: Average Precision
- **mAP**: mean Average Precision

```python
from src.analyzer import DetectionAnalyzer
analyzer = DetectionAnalyzer()
analyzer.load_ground_truth_from_dir('annotations/')
# predictions 추가...
results = analyzer.analyze_all(iou_threshold=0.5)
analyzer.print_results(results)
```

**결과 형식**:
```python
{
    'metrics': {
        'overall': {'precision': 0.85, 'recall': 0.92, ...},
        'per_class': {'dog': {...}, 'cat': {...}}
    },
    'ap_scores': {'dog': 0.92, 'cat': 0.85},
    'detection_rate': 92.5
}
```

---

### 8. Visualizer (visualizer.py)

**목적**: 분석 결과를 그래프로 시각화

**생성 그래프**:
1. `metrics_summary.png` - Precision/Recall/F1, TP/FP/FN, Per-class 메트릭
2. `detection_rate.png` - 원형 차트
3. `class_distribution.png` - 클래스별 객체 수
4. `confidence_distribution.png` - 신뢰도 분포
5. `file_type_distribution.png` - 파일 종류 분류
6. `defect_type_distribution.png` - 불량 유형 분류

```python
from src.visualizer import ResultVisualizer
viz = ResultVisualizer('outputs/')
files = viz.create_full_report(results, detector_summary)
```

---

### 9. Reporter (reporter.py)

**목적**: 분석 결과를 Excel 파일로 내보내기

**생성 시트**:
1. **Summary** - 전체 메트릭 요약
2. **Detection Results** - 이미지별 검출 결과
3. **Class Distribution** - 클래스별 객체 분포
4. **File Types** - 파일 종류 분류

```python
from src.reporter import ExcelReporter
reporter = ExcelReporter('outputs/')
path = reporter.generate_full_report(results, detections, summary)
```

---

## 📊 성능 메트릭 설명

### Confusion Matrix
- **TP (True Positive)**: 올바르게 검출된 객체
- **FP (False Positive)**: 잘못 검출된 객체
- **FN (False Negative)**: 놓친 객체

### Precision, Recall, F1
- **Precision**: 검출된 객체 중 정답의 비율 (오탐지 최소화)
- **Recall**: 실제 객체 중 검출된 비율 (누락 최소화)
- **F1 Score**: Precision과 Recall의 균형

### IoU (Intersection over Union)
```
IoU = 교집합 / 합집합
```
- 0.5는 일반적 기준 (COCO)
- 0.75는 엄격한 기준

### AP & mAP
- **AP**: 신뢰도 임계값을 변화시키며 계산한 Precision-Recall 곡선의 면적
- **mAP**: 모든 클래스의 AP의 평균

---

## 🚀 사용 방법 요약

### 처음 사용하기 (새 컴퓨터)

```bash
# 1. setup.py 또는 setup_windows.bat 실행 (한 번만)
# Windows:
D:\project\data-tools\setup_windows.bat

# 2. 가상환경 활성화
D:\project\project_venv\Scripts\activate.bat

# 3. 분석 실행
python main.py
```

### 이미지와 주석 준비

```
inputs/
├── image1.jpg
├── image2.jpg
└── image3.png

annotations/
├── image1.json
├── image2.json
└── image3.json
```

### 분석 옵션

```bash
# 기본 설정
python main.py

# 커스텀 모델
python main.py --model models/yolov8m.pt

# Ground Truth 주석 지정
python main.py --annotations D:/project/data-tools/annotations

# 신뢰도 및 IoU 조정
python main.py --confidence 0.6 --iou 0.45

# 모든 옵션 확인
python main.py --help
```

---

## 📈 출력 파일

### 그래프 (PNG)
- `outputs/metrics_summary.png` - 전체 성능 메트릭
- `outputs/detection_rate.png` - 검출률
- `outputs/detection_class_distribution.png` - 클래스 분포
- `outputs/confidence_distribution.png` - 신뢰도 분포
- `outputs/file_type_distribution.png` - 파일 종류
- `outputs/defect_type_distribution.png` - 불량 유형

### 리포트 (Excel)
- `outputs/YOLO_Analysis_Report_YYYYMMDD_HHMMSS.xlsx`
  - Summary 시트: 전체 메트릭
  - Detection Results 시트: 이미지별 결과
  - Class Distribution 시트: 클래스별 통계
  - File Types 시트: 파일 종류별 통계

---

## 🔧 커스터마이징 가이드

### 모델 변경

```python
# main.py에서
python main.py --model models/custom_model.pt
```

### 클래스명 변경

YOLO 모델의 클래스명은 자동으로 감지됩니다.
Ground Truth 주석에서 `class` 필드를 변경하세요.

### 신뢰도 임계값 조정

```python
# 낮은 임계값 = 더 많은 검출 (더 많은 오탐지)
python main.py --confidence 0.3

# 높은 임계값 = 더 적은 검출 (더 높은 정확도)
python main.py --confidence 0.8
```

### IoU 임계값 조정

```python
# 분석할 때 IoU 임계값 변경
# analyzer.py의 analyze_all() 호출 시
results = analyzer.analyze_all(iou_threshold=0.75)
```

---

## 🐛 문제 해결

### GPU 인식 안 됨
```bash
# PyTorch CUDA 재설치
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

### 메모리 부족
```bash
# 작은 모델 사용
python main.py --model yolov8n.pt

# 또는 이미지 크기 축소
# detector.py 수정 필요
```

### 모듈 import 오류
```bash
# 가상환경 다시 활성화
D:\project\project_venv\Scripts\activate.bat

# 또는 패키지 재설치
pip install -r requirements.txt
```

---

## 📚 다른 컴퓨터로 이전

```bash
# 1. D:\project\data-tools 폴더 복사
# 2. 새 컴퓨터에서 setup.py 실행
python setup.py
# 자동으로 시스템 사양에 맞춰 환경 구성됩니다!
```

---

## 🎯 향후 개선 계획

- [ ] COCO/Pascal VOC 형식 자동 변환
- [ ] 라벨링 도구 통합 (LabelImg, CVAT)
- [ ] 실시간 분석 대시보드
- [ ] 모델 비교 분석
- [ ] 하이퍼파라미터 최적화
- [ ] 클라우드 스토리지 연동
- [ ] REST API 제공
- [ ] Docker 이미지 제공

---

## 📝 라이선스 및 정보

- **개발 날짜**: 2024-10-29
- **Python 버전**: 3.8+
- **주요 의존성**: ultralytics, torch, opencv, pandas, matplotlib, openpyxl
- **라이선스**: MIT

---

## 📞 지원

문제가 발생하면:
1. README.md 참고
2. ANNOTATION_FORMAT.md 확인
3. 로그 메시지 분석
4. 파이썬 버전 및 패키지 버전 확인

---

**이 도구가 도움이 되길 바랍니다!** 🎉
