# 🔍 Project Scanner GUI - Portable Edition

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%207%2B-orange.svg)
![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen.svg)

포터블 형태의 **GUI 기반 프로젝트 스캐너**입니다. Python 설치 없이 USB나 외장 하드에서 바로 실행할 수 있습니다.

## ✨ 주요 특징

- 🖥️ **GUI 인터페이스**: PySimpleGUI 기반의 사용자 친화적 인터페이스
- 💾 **완전 포터블**: USB, 외장하드, 네트워크 드라이브에서 직접 실행
- 🚀 **설치 불필요**: Python 미설치 환경에서도 동작 (standalone exe)
- ⚙️ **자동 설정 저장**: 마지막 스캔 위치와 설정 자동 기억
- 📊 **자동 리포트 생성**: JSON 및 Excel 형식의 분석 리포트
- 🔄 **재귀적 스캔**: 프로젝트 폴더의 모든 하위 디렉토리 자동 탐색
- 📦 **의존성 분석**: Python 프로젝트의 모든 패키지 의존성 추출

## 🚀 빠른 시작

### 방법 1: 미리 빌드된 exe 사용 (권장)

1. **저장소 클론**
```bash
git clone https://github.com/Jolrin-Saram/project_scanneer.git
cd project_scanneer
```

2. **실행**
```bash
run_scanner.bat
```

3. **사용**
   - 폴더 선택 버튼으로 스캔할 폴더 선택
   - "스캔 시작" 버튼 클릭
   - 결과 확인

### 방법 2: 직접 빌드하기

#### 필수 요구사항
- Windows 7 이상
- Python 3.8+
- pip (Python 패키지 관리자)

#### 빌드 단계

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. exe 생성 (3~5분 소요)
build_portable.bat

# 3. 배포 패키지 준비
prepare_portable.bat

# 4. 실행
run_scanner.bat
```

**결과**: `portable_build/bin/ProjectScanner.exe` 생성됨 (60~80MB)

## 📖 사용 설명서

### 기능별 설명

#### 1. 폴더 선택
- **찾아보기** 버튼으로 스캔할 폴더 선택
- 자동으로 마지막 선택 위치 로드
- 모든 드라이브에서 선택 가능

#### 2. 스캔 옵션
- **하위 폴더 포함**: 재귀적으로 모든 하위 폴더 스캔
- **숨겨진 폴더 제외**: .git, .venv 등 자동 제외

#### 3. 스캔 실행
- **스캔 시작**: 선택한 폴더 분석 시작
- **진행 상황**: 프로그레스 바로 실시간 표시
- **로그 출력**: 발견된 프로젝트 목록 표시

#### 4. 결과 확인
- **발견된 프로젝트**: Python 프로젝트 개수
- **총 의존성**: 모든 라이브러리 개수
- **리포트 열기**: JSON 파일 자동 열기

#### 5. 설정 저장
- **저장** 버튼: 현재 설정 저장
- **초기화** 버튼: 모든 데이터 초기화
- 자동 저장: 프로그램 종료시 자동 저장

## 📁 폴더 구조

```
project_scanneer/
│
├── src/                          # 소스 코드
│   ├── gui_scanner.py            # GUI 애플리케이션 (⭐)
│   ├── project_scanner.py        # 스캔 엔진
│   ├── file_classifier.py        # 파일 분류
│   ├── analyzer.py               # 분석
│   ├── detector.py               # YOLO 감지
│   ├── visualizer.py             # 시각화
│   ├── reporter.py               # 리포트
│   └── ground_truth_loader.py    # 어노테이션
│
├── config/                       # 설정 저장소
├── outputs/                      # 결과 저장소
├── program_data/                 # 프로그램 데이터
├── portable_build/               # 빌드 출력
│
├── build_portable.bat            # PyInstaller 빌드
├── run_scanner.bat               # GUI 실행 (사용자용)
├── prepare_portable.bat          # 배포 준비
├── scanner_icon.ico              # 아이콘
├── portable_config.json          # 설정
│
├── README.md                     # 이 파일
├── PORTABLE_SETUP_GUIDE.md       # 상세 설정 가이드
├── BUILD_AND_DEPLOY_GUIDE.txt    # 빌드 가이드
├── PORTABLE_COMPLETE_SUMMARY.md  # 기능 요약
├── README_PORTABLE.md            # 포터블 설명
│
└── requirements.txt              # 패키지 목록
```

## 🔧 시스템 요구사항

### 최종 사용자
- Windows 7 이상
- 50MB 이상의 디스크 공간
- 인터넷 연결 (선택사항)

### 개발자 (빌드용)
- Windows 7 이상
- Python 3.8+
- pip 패키지 관리자

## 📦 포함된 패키지

```
PySimpleGUI        - GUI 프레임워크
PyInstaller        - exe 패키징
matplotlib         - 그래프 생성
numpy              - 수치 계산
pandas             - 데이터 분석
openpyxl           - Excel 생성
opencv-python      - 이미지 처리
scikit-learn       - 머신러닝
```

## 📊 프로젝트 발견 기능

자동으로 다음을 감지합니다:

- `requirements.txt` - pip 의존성
- `setup.py` - 설치 스크립트
- `pyproject.toml` - 모던 Python 프로젝트
- `Pipfile` - Pipenv 환경
- `main.py`, `app.py` - 메인 파일

## 🐛 문제 해결

### Q: "ProjectScanner.exe not found" 오류
**A:** 빌드를 실행하세요:
```bash
build_portable.bat
```

### Q: GUI가 바로 종료됨
**A:** 다음을 확인하세요:
1. `requirements.txt` 패키지 설치 확인
2. `src/` 폴더 파일 존재 확인
3. 명령 프롬프트에서 오류 메시지 확인

### Q: "유효하지 않은 경로" 오류
**A:** 
1. 폴더 존재 확인
2. "찾아보기"로 유효한 폴더 선택

### Q: 결과가 저장되지 않음
**A:**
1. `outputs/` 폴더 생성
2. 폴더 권한 확인

## 🎯 사용 시나리오

### 시나리오 1: 단일 프로젝트 분석
```
1. run_scanner.bat 실행
2. 프로젝트 폴더 선택
3. "스캔 시작" 클릭
4. outputs/scan_report.json 확인
```

### 시나리오 2: USB에서 여러 폴더 분석
```
1. USB에 프로젝트 저장
2. 다른 컴퓨터에서 run_scanner.bat 실행
3. 첫 번째 폴더 스캔
4. 결과 저장 후 다른 폴더 스캔
```

## 📈 성능

| 항목 | 상세 |
|------|------|
| exe 파일 크기 | 60~80 MB |
| 첫 실행 시간 | 2~3초 |
| 소규모 스캔 | <1초 |
| 중규모 스캔 | 1~5초 |
| 대규모 스캔 | 5~30초 |
| 메모리 사용량 | 100~300 MB |

## 📚 추가 문서

- [포터블 설정 가이드](PORTABLE_SETUP_GUIDE.md) - 상세 설정 방법
- [빌드 및 배포 가이드](BUILD_AND_DEPLOY_GUIDE.txt) - 단계별 빌드 가이드
- [기능 완성 요약](PORTABLE_COMPLETE_SUMMARY.md) - 구현된 기능 목록
- [포터블 설명](README_PORTABLE.md) - 포터블 구조 설명

## 📜 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

```
MIT License

Copyright (c) 2024 Project Scanner

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 👨‍💻 프로젝트 정보

- **이름**: Project Scanner GUI - Portable Edition
- **버전**: 1.0.0
- **상태**: ✅ Production Ready
- **마지막 업데이트**: 2024-10-30
- **플랫폼**: Windows 7+

## 🔄 업데이트 방법

### 기능 추가 후
```bash
# 1. 코드 수정
# 2. 재빌드
build_portable.bat

# 3. 배포 준비
prepare_portable.bat

# 4. GitHub 업로드
git add .
git commit -m "Update: [변경사항]"
git push origin main
```

## 🎉 주요 기능 체크리스트

- ✅ GUI 인터페이스 (PySimpleGUI)
- ✅ 포터블 exe 생성 (PyInstaller)
- ✅ 자동 설정 저장
- ✅ 프로젝트 자동 발견
- ✅ 의존성 분석
- ✅ JSON 리포트 생성
- ✅ Excel 리포트 생성 (선택)
- ✅ 완전한 문서화
- ✅ 배치 자동화 스크립트
- ✅ GitHub 배포

## 🙏 감사

- **PySimpleGUI**: GUI 프레임워크
- **PyInstaller**: exe 패키징 도구
- **Python 커뮤니티**: 모든 오픈소스 라이브러리

---

**즐거운 프로젝트 스캐닝을 하세요!** 🚀

이 프로젝트가 유용했다면 ⭐ Star 해주세요!

**GitHub**: https://github.com/Jolrin-Saram/project_scanneer.git
