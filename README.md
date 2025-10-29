# YOLO Detection Analysis Tool

YOLO4/YOLO8 객체 검출 모델의 성능을 분석하고 평가하는 자동화 도구입니다.

## 주요 기능

- **자동 프로젝트 발견**: D:\project 내 모든 Python 프로젝트 자동 스캔
- **시스템 자동 감지**: GPU/CUDA/CPU 정보 자동 수집
- **동적 Requirements 생성**: 시스템 사양에 맞게 자동으로 requirements.txt 생성
- **객체 검출**: YOLO4/YOLO8 모델을 사용한 자동 객체 검출
- **성능 분석**: Precision, Recall, F1 Score, AP, mAP 계산
- **파일명 기반 분류**: 파일명 패턴을 인식하여 자동으로 그룹화
- **시각화**: 분석 결과를 그래프로 자동 생성
- **Excel 리포트**: 상세 분석 결과를 Excel 파일로 내보내기

## 폴더 구조

```
D:\project\data-tools/
├── models/              # YOLO 모델 저장 폴더
├── inputs/              # 테스트 이미지 저장 폴더
├── outputs/             # 분석 결과 저장 폴더 (자동 생성)
├── annotations/         # Ground Truth 주석 파일 (선택사항)
├── config/              # 설정 파일 및 스캔 리포트
├── src/                 # 소스 코드
│   ├── project_scanner.py       # 프로젝트 발견 및 분석
│   ├── system_detector.py       # 시스템 정보 수집
│   ├── generate_requirements.py # 통합 requirements 생성
│   ├── integrated_setup.py      # 전체 환경 셋업
│   ├── detector.py              # YOLO 객체 검출
│   ├── analyzer.py              # 성능 분석
│   ├── ground_truth_loader.py   # Ground Truth 주석 로드
│   ├── visualizer.py            # 시각화 (그래프 생성)
│   └── reporter.py              # Excel 리포트 생성
├── setup.py             # 메인 셋업 스크립트
├── setup_windows.bat    # Windows 배치 파일
├── main.py              # YOLO 분석 도구 메인 스크립트
├── requirements.txt     # 패키지 의존성 (자동 생성)
├── README.md            # 이 파일
└── ANNOTATION_FORMAT.md # 주석 형식 설명서
```

## 초기 설정 (새 컴퓨터)

### 단계 1: 프로젝트 폴더 복사
새로운 컴퓨터에 D:\project 폴더 전체를 복사합니다.

### 단계 2: 환경 자동 설정

**Windows에서:**
```bash
cd D:\project\data-tools
setup_windows.bat
```

**Linux/Mac에서:**
```bash
cd D:\project\data-tools
python setup.py
```

### 자동으로 수행되는 작업:
1. ✓ D:\project 내 모든 Python 프로젝트 발견 및 분석
2. ✓ GPU/CUDA/CPU 정보 자동 감지
3. ✓ 시스템 사양에 맞게 requirements.txt 자동 생성
4. ✓ 통합 가상환경 생성 (D:\project\project_venv)
5. ✓ 모든 의존성 자동 설치

### 단계 3: 가상환경 활성화

**Windows:**
```bash
D:\project\project_venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source D:\project\project_venv/bin/activate
```

## Ground Truth 주석 (선택사항)

더 정확한 성능 분석을 위해 **Ground Truth 주석**을 사용할 수 있습니다.

### 주석 파일 준비

주석 파일은 JSON 형식이며, `annotations` 폴더에 저장합니다:

```
D:\project\data-tools\
├── inputs/
│   ├── image1.jpg
│   └── image2.jpg
└── annotations/
    ├── image1.json
    └── image2.json
```

### 주석 형식 예제

파일명: `image1.json`

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

**⚠️ 중요: 주석 파일명(확장자 제외)은 이미지 파일명과 동일해야 합니다!**
- ✅ image1.jpg → image1.json
- ❌ image1.jpg → img1.json

**상세 형식 및 더 많은 예제는 [ANNOTATION_FORMAT.md](ANNOTATION_FORMAT.md) 참고**

### 주석 파일 검증

```bash
python -c "from src.ground_truth_loader import GroundTruthLoader; loader = GroundTruthLoader(); loader.print_annotation_summary()"
```

## 사용 방법

### 1. YOLO 모델 준비

모델을 `models` 폴더에 저장합니다:
```
D:\project\data-tools\models\
├── yolov8n.pt      # YOLO8 nano (권장)
├── yolov8m.pt      # YOLO8 medium
└── custom_model.pt # 커스텀 모델
```

또는 자동으로 다운로드됩니다 (인터넷 필요).

### 2. 테스트 이미지 준비

`inputs` 폴더에 이미지 파일을 추가합니다:
```
D:\project\data-tools\inputs\
├── image1.jpg
├── image2.png
├── image3.bmp
└── ...
```

### 3. 분석 실행

가상환경이 활성화된 상태에서:

```bash
# 기본 설정으로 실행 (yolov8n.pt, confidence=0.5)
python main.py

# 커스텀 모델 및 설정
python main.py --model models/yolov8m.pt --confidence 0.6 --iou 0.5

# Ground Truth 주석을 사용한 정확한 분석
python main.py --annotations D:/project/data-tools/annotations

# 모든 옵션 확인
python main.py --help
```

#### Ground Truth 기반 분석

주석 파일이 `annotations` 폴더에 있으면 자동으로 로드되어 다음 메트릭이 계산됩니다:

- **Precision**: TP / (TP + FP)
- **Recall**: TP / (TP + FN)
- **F1 Score**: Precision과 Recall의 조화 평균
- **Average Precision (AP)**: 신뢰도별 Precision-Recall 곡선의 면적
- **mean Average Precision (mAP)**: 모든 클래스의 AP 평균
- **Confusion Matrix**: TP, FP, FN 분석

#### 주석 없이 분석

주석 파일이 없으면 다음만 계산됩니다:
- 검출된 객체 수 및 분포
- 신뢰도 통계
- 파일 종류 분류

### 4. 결과 확인

분석이 완료되면 `outputs` 폴더에 다음이 생성됩니다:

- **metrics_summary.png** - 성능 메트릭 그래프
- **detection_rate.png** - 객체 검출률 차트
- **class_distribution.png** - 클래스별 분포
- **confidence_distribution.png** - 신뢰도 분포
- **file_type_distribution.png** - 파일 종류 분포
- **defect_type_distribution.png** - 불량 유형 분포
- **YOLO_Analysis_Report_*.xlsx** - 상세 Excel 리포트

## 커스텀 명령어

```bash
# 프로젝트 스캔만 실행
python src/project_scanner.py

# 시스템 정보만 확인
python src/system_detector.py

# 이미지에서 객체 검출만 수행
python -c "from src.detector import YOLODetector; d = YOLODetector('yolov8n.pt'); d.load_model(); d.detect_directory('inputs')"
```

## 성능 메트릭 설명

### Precision (정확도)
검출된 객체 중 실제 객체의 비율
- 공식: TP / (TP + FP)

### Recall (재현율)
실제 객체 중 검출된 객체의 비율
- 공식: TP / (TP + FN)

### F1 Score
Precision과 Recall의 조화 평균
- 공식: 2 * (Precision * Recall) / (Precision + Recall)

### Average Precision (AP)
신뢰도 임계값을 변화시키며 계산한 Precision-Recall 곡선의 면적

### mean Average Precision (mAP)
모든 클래스의 AP의 평균

### Detection Rate (검출률)
검출된 객체 / 전체 객체 수

## 시스템 요구사항

### 최소 사양:
- Python 3.8+
- 4GB RAM
- 2GB 디스크 공간

### GPU 가속 (권장):
- NVIDIA GPU (8GB+ VRAM 권장)
- CUDA 11.6+
- cuDNN

## 문제 해결

### 모델 로드 실패
```bash
# ultralytics 다시 설치
pip install --upgrade ultralytics
```

### GPU 인식 안 됨
```bash
# PyTorch CUDA 버전 확인
python -c "import torch; print(torch.cuda.is_available())"

# GPU 지원 PyTorch 재설치
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

### 메모리 부족
- 작은 모델 사용 (yolov8n.pt)
- 이미지 크기 축소
- 배치 크기 감소

## 다른 컴퓨터로 이전

1. D:\project\data-tools 폴더 전체 복사
2. 새 컴퓨터에서 setup.py 또는 setup_windows.bat 실행
3. 자동으로 시스템 사양에 맞춰 환경이 구성됩니다

## 개발자 정보

이 도구는 다음 라이브러리를 사용합니다:
- [ultralytics/YOLO](https://github.com/ultralytics/ultralytics) - YOLO 객체 검출
- [PyTorch](https://pytorch.org/) - 딥러닝 프레임워크
- [OpenCV](https://opencv.org/) - 이미지 처리
- [Matplotlib](https://matplotlib.org/) - 시각화
- [openpyxl](https://openpyxl.readthedocs.io/) - Excel 파일 처리
- [pandas](https://pandas.pydata.org/) - 데이터 분석

## 라이선스

MIT License

## 지원

문제가 발생하면 다음을 확인하세요:
1. Python 버전 확인: `python --version`
2. 의존성 설치 확인: `pip list`
3. 모델 파일 존재 확인: `ls models/`
4. 입력 이미지 존재 확인: `ls inputs/`

## 업데이트 기록

### v1.0 (2024-10-29)
- 초기 릴리스
- 프로젝트 자동 발견 기능
- 시스템 자동 감지 기능
- YOLO 객체 검출 및 분석
- 자동 시각화 및 Excel 리포트 생성
