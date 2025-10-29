#!/usr/bin/env python
"""
Main Setup Script - D:\project 의 모든 프로젝트를 분석하고 통합 환경 구축
"""

import sys
import os

# src 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from integrated_setup import IntegratedSetup


def main():
    """메인 실행"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  YOLO Analysis Tool - Integrated Project Setup".center(68) + "║")
    print("║" + "  Automated Discovery, Configuration & Environment Setup".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    print()

    # 현재 디렉토리 확인
    data_tools_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(data_tools_dir)

    print(f"[*] Setup Location: {data_tools_dir}")
    print(f"[*] Project Root: {project_root}")
    print()

    # 통합 셋업 실행
    setup = IntegratedSetup(root_path=project_root)
    success = setup.setup_all()

    if success:
        print("\n[✓] Setup completed successfully!")
        print("\nTo activate the virtual environment, run:")
        if sys.platform == "win32":
            print(f"    {setup.venv_path}\\Scripts\\activate.bat")
        else:
            print(f"    source {setup.venv_path}/bin/activate")

        return 0
    else:
        print("\n[✗] Setup failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
