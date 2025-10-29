"""
GUI Project Scanner - PySimpleGUI 기반
포터블 형태로 외장 하드에서 실행 가능
"""

import PySimpleGUI as sg
import json
import os
import sys
from pathlib import Path
from datetime import datetime
import threading

# 현재 스크립트 위치 기반 상대 경로 설정
if getattr(sys, 'frozen', False):
    # PyInstaller로 패킹된 경우
    PROGRAM_DIR = Path(sys._MEIPASS)
else:
    # 일반 Python 실행
    PROGRAM_DIR = Path(__file__).parent

CONFIG_DIR = PROGRAM_DIR.parent / "config"
OUTPUT_DIR = PROGRAM_DIR.parent / "outputs"
DATA_DIR = PROGRAM_DIR.parent / "program_data"

# 디렉토리 생성
CONFIG_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

CONFIG_FILE = CONFIG_DIR / "gui_settings.json"
SCAN_REPORT_FILE = OUTPUT_DIR / "scan_report.json"

# PySimpleGUI 테마 설정
sg.theme('DarkBlue3')

# 설정 로드
def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {'last_root': str(PROGRAM_DIR.parent), 'window_size': (900, 700)}

# 설정 저장
def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

# ProjectScanner import
sys.path.insert(0, str(PROGRAM_DIR / "src"))
try:
    from project_scanner import ProjectScanner
except ImportError:
    sg.popup_error("Error: project_scanner 모듈을 찾을 수 없습니다")
    sys.exit(1)

# 전역 변수
current_config = load_config()
scan_results = None
scanning = False

def create_window():
    menu_def = [
        ['파일(&F)', ['설정(&S)', '종료(&E)']],
        ['도움말(&H)', ['정보(&A)']],
    ]
    
    layout = [
        [sg.Menu(menu_def, tearoff=False)],
        
        [sg.Text('프로젝트 스캐너 - 포터블 버전', font=('Arial', 16, 'bold'))],
        
        [sg.Frame('스캔 설정', [
            [sg.Text('스캔 폴더:', size=(15, 1)), 
             sg.InputText(current_config['last_root'], key='-SCAN_PATH-', size=(50, 1)),
             sg.FolderBrowse('찾아보기', size=(10, 1))],
            [sg.Text('', size=(15, 1)),
             sg.Checkbox('하위 폴더 포함', default=True, key='-RECURSIVE-'),
             sg.Checkbox('숨겨진 폴더 제외', default=True, key='-EXCLUDE_HIDDEN-')],
        ])],
        
        [sg.Frame('스캔 실행', [
            [sg.Button('스캔 시작', size=(15, 2), button_color=('white', 'green')),
             sg.Button('중지', size=(15, 2), button_color=('white', 'red'), disabled=True, key='-STOP-'),
             sg.Button('리포트 열기', size=(15, 2))],
            [sg.ProgressBar(100, orientation='h', size=(80, 20), key='-PROGRESS-')],
            [sg.Multiline(size=(95, 25), disabled=True, key='-OUTPUT-', font=('Courier', 9))],
        ])],
        
        [sg.Frame('결과 요약', [
            [sg.Column([
                [sg.Text('발견된 프로젝트: ', size=(20, 1)), sg.Text('0', key='-PROJECT_COUNT-', size=(10, 1))],
                [sg.Text('총 의존성: ', size=(20, 1)), sg.Text('0', key='-DEPS_COUNT-', size=(10, 1))],
                [sg.Text('스캔 위치: ', size=(20, 1)), sg.Text('None', key='-SCAN_LOCATION-', size=(50, 1))],
            ])],
        ])],
        
        [sg.Button('저장', size=(10, 1)), 
         sg.Button('초기화', size=(10, 1)), 
         sg.Button('종료', size=(10, 1))],
    ]
    
    window = sg.Window('프로젝트 스캐너 GUI', layout, 
                       size=current_config.get('window_size', (900, 700)),
                       finalize=True)
    return window

def scan_directory(root_path):
    global scan_results
    
    try:
        scanner = ProjectScanner(root_path)
        projects = scanner.scan()
        scan_results = {
            'scan_root': str(root_path),
            'total_projects': len(projects),
            'projects': projects,
            'dependencies': scanner.get_all_dependencies(),
            'timestamp': datetime.now().isoformat(),
        }
        
        # 리포트 저장
        with open(SCAN_REPORT_FILE, 'w', encoding='utf-8') as f:
            json.dump(scan_results, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    window = create_window()
    
    while True:
        event, values = window.read(timeout=100)
        
        if event == sg.WINDOW_CLOSED or event == '종료':
            break
        
        if event == '스캔 시작':
            root_path = values['-SCAN_PATH-']
            
            if not os.path.isdir(root_path):
                sg.popup_error('유효하지 않은 경로입니다')
                continue
            
            window['-OUTPUT-'].update('')
            window['-PROGRESS-'].update_bar(0)
            window['-SCAN_LOCATION-'].update(root_path)
            
            window['-OUTPUT-'].print('[*] 스캔 시작...')
            window['-OUTPUT-'].print(f'[*] 위치: {root_path}')
            
            # 스캔 실행
            if scan_directory(root_path):
                window['-OUTPUT-'].print('[+] 스캔 완료!')
                window['-PROJECT_COUNT-'].update(str(scan_results['total_projects']))
                window['-DEPS_COUNT-'].update(str(len(scan_results['dependencies'])))
                window['-PROGRESS-'].update_bar(100)
                
                for i, proj in enumerate(scan_results['projects'], 1):
                    window['-OUTPUT-'].print(f"  {i}. {proj['name']} ({proj['type']})")
            else:
                window['-OUTPUT-'].print('[!] 스캔 실패')
        
        if event == '리포트 열기':
            if SCAN_REPORT_FILE.exists():
                os.startfile(str(SCAN_REPORT_FILE))
            else:
                sg.popup('리포트가 없습니다. 먼저 스캔을 실행하세요')
        
        if event == '저장':
            config = {
                'last_root': values['-SCAN_PATH-'],
                'window_size': window.size,
            }
            save_config(config)
            sg.popup('설정이 저장되었습니다')
        
        if event == '초기화':
            window['-OUTPUT-'].update('')
            window['-PROJECT_COUNT-'].update('0')
            window['-DEPS_COUNT-'].update('0')
            window['-PROGRESS-'].update_bar(0)
        
        if event == '정보(&A)':
            sg.popup_ok(
                '프로젝트 스캐너 GUI v1.0
'
                '포터블 형태로 외장 하드에서 실행 가능
'
                '
'
                '설정은 자동으로 저장됩니다',
                title='정보'
            )
    
    window.close()

if __name__ == '__main__':
    main()
