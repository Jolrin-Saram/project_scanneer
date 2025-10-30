# -*- coding: utf-8 -*-
"""
GUI Project Scanner
Portable Version
"""

import PySimpleGUI as sg
import json
import os
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    PROGRAM_DIR = Path(sys._MEIPASS)
else:
    PROGRAM_DIR = Path(__file__).parent

CONFIG_DIR = PROGRAM_DIR.parent / "config"
OUTPUT_DIR = PROGRAM_DIR.parent / "outputs"

CONFIG_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

CONFIG_FILE = CONFIG_DIR / "gui_settings.json"

sys.path.insert(0, str(PROGRAM_DIR / "src"))
from project_scanner import ProjectScanner

sg.theme('DarkBlue3')

def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {'last_root': str(PROGRAM_DIR.parent)}

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False)

config = load_config()

layout = [
    [sg.Text('Project Scanner GUI', font=('Arial', 14, 'bold'))],
    [sg.Frame('Scan Settings', [
        [sg.Text('Folder:', size=(12, 1)), 
         sg.InputText(config['last_root'], key='-PATH-', size=(45, 1)),
         sg.FolderBrowse()],
    ])],
    [sg.Frame('Execution', [
        [sg.Button('Scan', size=(12, 2)), sg.Button('Clear', size=(12, 2)), sg.Button('Exit', size=(12, 2))],
        [sg.Multiline(size=(70, 20), disabled=True, key='-OUTPUT-')],
    ])],
    [sg.Frame('Results', [
        [sg.Text('Projects: '), sg.Text('0', key='-PROJ-', size=(5, 1))],
        [sg.Text('Dependencies: '), sg.Text('0', key='-DEPS-', size=(5, 1))],
    ])]
]

window = sg.Window('Project Scanner', layout, size=(700, 600))

while True:
    event, values = window.read()
    
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    
    if event == 'Scan':
        path = values['-PATH-']
        if not os.path.isdir(path):
            sg.popup_error('Invalid path')
            continue
        
        window['-OUTPUT-'].update('')
        window['-OUTPUT-'].print('[*] Scanning...')
        
        try:
            scanner = ProjectScanner(path)
            scanner.scan()
            
            window['-PROJ-'].update(str(len(scanner.projects)))
            window['-DEPS-'].update(str(len(scanner.get_all_dependencies())))
            
            for proj in scanner.projects:
                window['-OUTPUT-'].print(f"Found: {proj['name']}")
            
            report_path = OUTPUT_DIR / "scan_report.json"
            report = {
                'root': path,
                'projects': len(scanner.projects),
                'dependencies': len(scanner.get_all_dependencies()),
            }
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False)
            
            window['-OUTPUT-'].print('[+] Done!')
            config['last_root'] = path
            save_config(config)
        except Exception as e:
            window['-OUTPUT-'].print(f'[!] Error: {e}')
    
    if event == 'Clear':
        window['-OUTPUT-'].update('')
        window['-PROJ-'].update('0')
        window['-DEPS-'].update('0')

window.close()
