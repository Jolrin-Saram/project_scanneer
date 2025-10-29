# 포터블 GUI 프로젝트 스캐너 - 완전 설정 가이드

## 📦 포터블 패키지 구조

완성된 포터블 패키지 구조:

```
project_scanner_portable/
├── bin/                              # 실행 파일
│   └── ProjectScanner.exe           # GUI 애플리케이션 (PyInstaller로 생성)
│
├── src/                              # 소스 코드
│   ├── gui_scanner.py               # GUI 메인 애플리케이션
│   ├── project_scanner.py           # 프로젝트 스캔 엔진
│   ├── file_classifier.py           # 파일 분류 기능
│   ├── analyzer.py                  # 의존성 분석
│   ├── detector.py                  # YOLO 감지 (옵션)
│   ├── visualizer.py                # 시각화
│   └── reporter.py                  # Excel 리포트 생성
│
├── config/                           # 설정 저장소
│   ├── gui_settings.json            # GUI 마지막 설정 (자동 저장)
│   └── project_scan_report.json     # 최근 스캔 결과
│
├── outputs/                          # 스캔 결과 저장
│   ├── scan_report.json             # JSON 형식 리포트
│   ├── *.xlsx                       # Excel 분석 보고서
│   └── *.png                        # 그래프 이미지
│
├── program_data/                     # 프로그램 데이터
│   └── logs/                        # 로그 파일
│
├── run_scanner.bat                   # ⭐ 실행 파일 (더블클릭!)
├── build_portable.bat                # 빌드 파일 (개발자용)
├── prepare_portable.bat              # 배포 준비 스크립트
├── portable_config.json              # 포터블 설정
├── scanner_icon.ico                  # 애플리케이션 아이콘
├── README_PORTABLE.md                # 이 파일
└── requirements.txt                  # Python 의존성 (개발용)
```

## 🚀 빠른 시작

### Option 1: 미리 빌드된 exe 사용 (권장)
1. 폴더 전체를 USB나 외장 하드로 복사
2. `run_scanner.bat` 더블클릭
3. GUI가 열리면 스캔할 폴더 선택
4. "스캔 시작" 버튼 클릭

### Option 2: 직접 빌드하기 (개발자용)

#### 필수 요구사항
- Windows 7 이상
- Python 3.8 이상
- pip (Python 패키지 관리자)

#### 빌드 단계

1️⃣ **Python 패키지 설치**
```bash
cd project_scanner_portable
pip install -r requirements.txt
```

2️⃣ **exe 생성**
```bash
build_portable.bat
```
- 3~5분 소요
- `portable_build/bin/ProjectScanner.exe` 생성됨

3️⃣ **배포 패키지 준비**
```bash
prepare_portable.bat
```
- `ProjectScanner_Portable_v1.0/` 폴더 생성
- 모든 필요 파일 자동 포함

4️⃣ **배포**
```bash
run_scanner.bat
```
- GUI 애플리케이션 실행

## 💻 GUI 기능

### 메인 화면
- **스캔 폴더 선택**: "찾아보기" 버튼으로 폴더 선택
- **옵션**:
  - 하위 폴더 포함: 재귀적 스캔 활성화
  - 숨겨진 폴더 제외: .git, .venv 등 제외

### 스캔 실행
- **스캔 시작**: 선택한 폴더 스캔 시작
- **진행 상황**: 프로그레스 바로 실시간 표시
- **로그 출력**: 발견된 프로젝트 목록 표시

### 결과 확인
- **발견된 프로젝트**: 찾은 Python 프로젝트 개수
- **총 의존성**: 모든 프로젝트의 라이브러리 개수
- **스캔 위치**: 마지막으로 스캔한 경로

### 버튼
- **리포트 열기**: 최근 JSON 리포트를 탐색기에서 열기
- **저장**: 현재 설정 저장 (자동으로도 저장됨)
- **초기화**: 모든 결과 초기화

## 📁 자동 저장 기능

GUI는 다음 정보를 자동으로 저장합니다:
- **마지막 스캔 경로**: 다음 실행시 자동 로드
- **윈도우 크기**: 이전 사이즈 유지
- **스캔 결과**: JSON 파일로 저장

저장 위치: `config/gui_settings.json`

## 🔧 포터블 특징

✅ **외장 드라이브 호환**
- 상대 경로 사용으로 드라이브 독립성 보장
- 어느 폴더에 배치해도 동작

✅ **Python 미설치 환경 지원**
- PyInstaller로 생성된 standalone exe
- 별도 Python 설치 불필요

✅ **자동 설정 관리**
- 마지막 설정 자동 저장
- 초기 실행시 기본값 자동 적용

✅ **로그 관리**
- 스캔 결과 자동 저장
- `program_data/logs/` 에 기록

## 🐛 문제 해결

### "ProjectScanner.exe not found" 오류
**원인**: exe 파일이 없음
**해결**:
```bash
build_portable.bat
```
를 실행하여 exe 생성

### GUI가 바로 종료됨
**원인**: Python 모듈 누락 또는 경로 오류
**해결**:
1. `requirements.txt`의 모든 패키지 설치 확인
2. `src/project_scanner.py` 파일 존재 확인
3. GUI 콘솔 출력 확인 (오류 메시지 보기)

### "스캔 위치 오류" 또는 "유효하지 않은 경로"
**원인**: 존재하지 않는 폴더 선택
**해결**: 
1. 폴더 존재 확인
2. "찾아보기" 버튼으로 유효한 폴더 재선택

### 결과가 저장되지 않음
**원인**: `outputs/` 폴더 없음 또는 권한 부족
**해결**:
1. `outputs/` 폴더 수동 생성
2. 폴더 권한 확인 (읽기/쓰기)

## 📊 리포트 형식

### JSON 리포트 (`scan_report.json`)
```json
{
  "scan_root": "D:\projects",
  "total_projects": 3,
  "projects": [
    {
      "name": "project1",
      "path": "D:\projects\project1",
      "type": "requirements.txt",
      "dependencies": ["numpy", "pandas", ...],
      "python_files": ["main.py", "utils.py"],
      "config_files": ["requirements.txt"]
    }
  ],
  "dependencies": {
    "numpy": 2,
    "pandas": 1,
    ...
  },
  "timestamp": "2024-10-30T08:30:00"
}
```

### Excel 리포트 (옵션)
- 프로젝트 목록
- 의존성 분석
- 파일 분류
- 그래프 및 차트

## 🎯 사용 시나리오

### 시나리오 1: 새 프로젝트 폴더 분석
```
1. run_scanner.bat 실행
2. 폴더 선택: C:
ew_projects
3. "스캔 시작" 클릭
4. outputs/scan_report.json 확인
```

### 시나리오 2: 외장 하드에서 실행
```
1. 포터블 폴더를 USB로 복사
2. 다른 컴퓨터에 USB 연결
3. run_scanner.bat 실행
4. 자동으로 마지막 설정 로드
```

### 시나리오 3: 여러 프로젝트 비교
```
1. run_scanner.bat 실행
2. 첫 번째 폴더 스캔 → outputs/scan_report.json 저장
3. config 폴더의 파일 별도 저장
4. 다른 폴더 스캔
5. JSON 비교
```

## 📝 개발자 노트

### GUI 커스터마이징
`src/gui_scanner.py` 수정:
- 테마 변경: `sg.theme('DarkBlue3')` → 다른 테마 선택
- 레이아웃 수정: layout 배열 편집
- 색상 변경: button_color, background_color 등

### 새 기능 추가
1. `src/` 에 새 모듈 추가
2. `gui_scanner.py` 에서 import
3. `build_portable.bat` 에서 --add-data 옵션 추가
4. `build_portable.bat` 재실행

### Python 콘솔 출력 보기
```bash
python src/gui_scanner.py
```
- GUI 대신 콘솔에서 직접 실행
- 오류 메시지 상세 확인

## 📞 지원

문제 발생시:
1. README_PORTABLE.md 읽기 (이 문서)
2. `src/gui_scanner.py` 로그 확인
3. requirements.txt 패키지 재설치

## 📜 라이선스

MIT License - 자유롭게 수정/배포 가능

---

**마지막 업데이트**: 2024-10-30
**버전**: 1.0.0
**상태**: ✅ 포터블 패키징 완료
