"""
Integrated Setup - 프로젝트 발견부터 환경 구축까지 자동화
1. 프로젝트 스캔
2. 시스템 정보 수집
3. requirements.txt 생성
4. 가상환경 생성
5. 패키지 설치
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


class IntegratedSetup:
    """통합 환경 셋업을 관리하는 클래스"""

    def __init__(self, root_path: str = "D:/project"):
        """
        Args:
            root_path: 프로젝트 루트 경로
        """
        self.root_path = Path(root_path)
        self.data_tools_path = self.root_path / "data-tools"
        self.src_path = self.data_tools_path / "src"
        self.config_path = self.data_tools_path / "config"
        self.venv_path = self.root_path / "project_venv"

    def setup_all(self):
        """전체 셋업 실행"""
        print("\n" + "="*70)
        print("INTEGRATED SETUP - Automated Project Discovery & Environment Setup")
        print("="*70 + "\n")

        try:
            step_1_success = self.step_1_scan_projects()
            if not step_1_success:
                print("[!] Failed at Step 1: Project Scanning")
                return False

            step_2_success = self.step_2_detect_system()
            if not step_2_success:
                print("[!] Failed at Step 2: System Detection")
                return False

            step_3_success = self.step_3_generate_requirements()
            if not step_3_success:
                print("[!] Failed at Step 3: Requirements Generation")
                return False

            step_4_success = self.step_4_create_venv()
            if not step_4_success:
                print("[!] Failed at Step 4: Virtual Environment Creation")
                return False

            step_5_success = self.step_5_install_packages()
            if not step_5_success:
                print("[!] Failed at Step 5: Package Installation")
                return False

            self.print_completion_summary()
            return True

        except Exception as e:
            print(f"[!] Unexpected error during setup: {e}")
            return False

    def step_1_scan_projects(self) -> bool:
        """Step 1: 프로젝트 스캔"""
        print("\n[STEP 1/5] Scanning projects in D:/project...")
        print("-" * 70)

        try:
            # project_scanner.py 실행
            script_path = self.src_path / "project_scanner.py"
            if not script_path.exists():
                print(f"[!] project_scanner.py not found at {script_path}")
                return False

            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=60
            )

            print(result.stdout)
            if result.stderr:
                print("[!] Warnings/Errors:", result.stderr)

            # 리포트 파일 확인
            report_path = self.config_path / "project_scan_report.json"
            if not report_path.exists():
                print(f"[!] Project scan report not generated at {report_path}")
                return False

            print("[+] Step 1 completed successfully")
            return True

        except subprocess.TimeoutExpired:
            print("[!] Project scanning timed out")
            return False
        except Exception as e:
            print(f"[!] Error during project scanning: {e}")
            return False

    def step_2_detect_system(self) -> bool:
        """Step 2: 시스템 정보 수집"""
        print("\n[STEP 2/5] Detecting system information...")
        print("-" * 70)

        try:
            # system_detector.py 실행
            script_path = self.src_path / "system_detector.py"
            if not script_path.exists():
                print(f"[!] system_detector.py not found at {script_path}")
                return False

            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=60
            )

            print(result.stdout)
            if result.stderr:
                print("[!] Warnings/Errors:", result.stderr)

            # 설정 파일 확인
            config_path = self.config_path / "system_config.json"
            if not config_path.exists():
                print(f"[!] System config not generated at {config_path}")
                return False

            print("[+] Step 2 completed successfully")
            return True

        except subprocess.TimeoutExpired:
            print("[!] System detection timed out")
            return False
        except Exception as e:
            print(f"[!] Error during system detection: {e}")
            return False

    def step_3_generate_requirements(self) -> bool:
        """Step 3: requirements.txt 생성"""
        print("\n[STEP 3/5] Generating unified requirements.txt...")
        print("-" * 70)

        try:
            # generate_requirements.py 실행
            script_path = self.src_path / "generate_requirements.py"
            if not script_path.exists():
                print(f"[!] generate_requirements.py not found at {script_path}")
                return False

            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=60
            )

            print(result.stdout)
            if result.stderr:
                print("[!] Warnings/Errors:", result.stderr)

            # requirements.txt 확인
            req_path = self.data_tools_path / "requirements.txt"
            if not req_path.exists():
                print(f"[!] requirements.txt not generated at {req_path}")
                return False

            print("[+] Step 3 completed successfully")
            return True

        except subprocess.TimeoutExpired:
            print("[!] Requirements generation timed out")
            return False
        except Exception as e:
            print(f"[!] Error during requirements generation: {e}")
            return False

    def step_4_create_venv(self) -> bool:
        """Step 4: 가상환경 생성"""
        print("\n[STEP 4/5] Creating virtual environment...")
        print("-" * 70)

        try:
            # 기존 가상환경 삭제
            if self.venv_path.exists():
                print(f"[*] Removing existing virtual environment at {self.venv_path}...")
                shutil.rmtree(self.venv_path)

            # 가상환경 생성
            print(f"[*] Creating virtual environment at {self.venv_path}...")
            result = subprocess.run(
                [sys.executable, "-m", "venv", str(self.venv_path)],
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                print(f"[!] Failed to create virtual environment")
                print(f"Error: {result.stderr}")
                return False

            # 가상환경 확인
            if not self.venv_path.exists():
                print(f"[!] Virtual environment creation failed")
                return False

            print(f"[+] Virtual environment created at {self.venv_path}")
            print("[+] Step 4 completed successfully")
            return True

        except subprocess.TimeoutExpired:
            print("[!] Virtual environment creation timed out")
            return False
        except Exception as e:
            print(f"[!] Error creating virtual environment: {e}")
            return False

    def step_5_install_packages(self) -> bool:
        """Step 5: 패키지 설치"""
        print("\n[STEP 5/5] Installing packages...")
        print("-" * 70)

        try:
            # pip 업그레이드
            print("[*] Upgrading pip...")
            pip_path = self.venv_path / ("Scripts" if sys.platform == "win32" else "bin") / ("pip.exe" if sys.platform == "win32" else "pip")

            result = subprocess.run(
                [str(pip_path), "install", "--upgrade", "pip", "setuptools", "wheel"],
                capture_output=True,
                text=True,
                timeout=180
            )

            if result.returncode != 0:
                print(f"[!] Failed to upgrade pip")
                print(f"Error: {result.stderr}")
                # 계속 진행

            # requirements.txt 설치
            req_path = self.data_tools_path / "requirements.txt"
            if not req_path.exists():
                print(f"[!] requirements.txt not found at {req_path}")
                return False

            print(f"[*] Installing packages from {req_path}...")
            result = subprocess.run(
                [str(pip_path), "install", "-r", str(req_path)],
                capture_output=True,
                text=True,
                timeout=600  # 10분 타임아웃
            )

            print(result.stdout)
            if result.stderr:
                print("[*] Installation warnings/info:")
                print(result.stderr)

            if result.returncode != 0:
                print(f"[!] Package installation failed")
                print(f"[*] Try manually running: {pip_path} install -r {req_path}")
                return False

            print("[+] Step 5 completed successfully")
            return True

        except subprocess.TimeoutExpired:
            print("[!] Package installation timed out")
            print("[*] Try manually installing packages with:")
            print(f"    {self.venv_path}\\Scripts\\pip install -r {self.data_tools_path}\\requirements.txt")
            return False
        except Exception as e:
            print(f"[!] Error installing packages: {e}")
            return False

    def print_completion_summary(self):
        """완료 요약 출력"""
        print("\n" + "="*70)
        print("SETUP COMPLETED SUCCESSFULLY")
        print("="*70)

        print(f"\nProject Root: {self.root_path}")
        print(f"Data Tools: {self.data_tools_path}")
        print(f"Virtual Environment: {self.venv_path}")
        print(f"Configuration: {self.config_path}")

        print("\n[+] Project Discovery: ✓ Completed")
        print("    - All projects in D:/project have been scanned")
        print("    - Report: data-tools/config/project_scan_report.json")

        print("\n[+] System Detection: ✓ Completed")
        print("    - System information collected")
        print("    - Config: data-tools/config/system_config.json")

        print("\n[+] Requirements Generation: ✓ Completed")
        print("    - Unified requirements.txt generated")
        print("    - File: data-tools/requirements.txt")

        print("\n[+] Virtual Environment: ✓ Created")
        print(f"    - Location: {self.venv_path}")

        print("\n[+] Package Installation: ✓ Completed")
        print("    - All dependencies installed")

        print("\n" + "-"*70)
        print("NEXT STEPS:")
        print("-"*70)

        if sys.platform == "win32":
            print(f"\n1. Activate virtual environment (Windows):")
            print(f"   {self.venv_path}\\Scripts\\activate.bat")
        else:
            print(f"\n1. Activate virtual environment (Linux/Mac):")
            print(f"   source {self.venv_path}/bin/activate")

        print(f"\n2. Run YOLO analysis tool:")
        print(f"   python {self.data_tools_path}/main.py")

        print(f"\n3. Test with sample images:")
        print(f"   Place images in: {self.data_tools_path}/inputs")
        print(f"   Results will be in: {self.data_tools_path}/outputs")

        print("\n" + "="*70 + "\n")

    def get_activation_command(self) -> str:
        """가상환경 활성화 명령어 반환"""
        if sys.platform == "win32":
            return str(self.venv_path / "Scripts" / "activate.bat")
        else:
            return f"source {self.venv_path / 'bin' / 'activate'}"


def main():
    """메인 실행 함수"""
    setup = IntegratedSetup()
    success = setup.setup_all()

    if success:
        print("[+] All setup steps completed successfully!")
        sys.exit(0)
    else:
        print("[!] Setup failed. Please review the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
