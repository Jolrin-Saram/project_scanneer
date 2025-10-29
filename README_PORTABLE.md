# Project Scanner - Portable GUI Version

포터블 형태의 프로젝트 스캐너 GUI 도구

## 사용 방법

### 실행
1. `run_scanner.bat` 를 더블클릭하여 실행
2. GUI 창이 열리면 스캔할 폴더를 선택
3. "스캔 시작" 버튼 클릭

### 빌드 방법 (개발자용)
1. Python 3.8+ 설치
2. 필수 패키지 설치: `pip install -r requirements.txt`
3. `build_portable.bat` 실행
4. `portable_build/bin/ProjectScanner.exe` 생성됨

## 폴더 구조

```
project_scanner_portable/
├── bin/                      # 실행 파일 위치
│   └── ProjectScanner.exe
├── config/                   # 설정 파일
│   ├── gui_settings.json     # GUI 설정
│   └── project_scan_report.json
├── outputs/                  # 스캔 결과
│   ├── *.json               # JSON 리포트
│   └── *.xlsx               # Excel 분석 보고서
├── program_data/            # 로그 및 캐시
│   └── logs/
├── src/                      # 소스 코드
├── run_scanner.bat          # 실행 스크립트 (클릭!)
├── build_portable.bat       # 빌드 스크립트
├── requirements.txt         # Python 패키지
└── README.md
```

## 특징

✅ 포터블 형태 - USB/외장 하드에서 바로 실행
✅ GUI 인터페이스 - 편리한 폴더 선택
✅ 실시간 진행 상황 표시
✅ 자동 설정 저장 - 마지막 폴더 경로 기억
✅ JSON & Excel 리포트 생성

## 지원 환경

- Windows 7+
- Python 3.8+ (개발/빌드시)

## 문제 해결

### "ProjectScanner.exe not found" 오류
→ 먼저 `build_portable.bat` 를 실행하여 exe를 생성하세요

### GUI가 나타나지 않음
→ 명령 프롬프트에서 error 메시지 확인
→ requirements.txt의 패키지가 모두 설치되었는지 확인

## 라이선스

MIT License
