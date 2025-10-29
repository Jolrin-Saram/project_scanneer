"""
Generate Requirements - 프로젝트 스캔 결과와 시스템 정보를 기반으로
통합 requirements.txt 생성
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from packaging import version as pkg_version


class RequirementsGenerator:
    """requirements.txt를 생성하는 클래스"""

    def __init__(self, project_scan_report: str, system_config: str):
        """
        Args:
            project_scan_report: project_scanner가 생성한 JSON 리포트 경로
            system_config: system_detector가 생성한 JSON 설정 경로
        """
        self.project_scan_report = project_scan_report
        self.system_config = system_config
        self.projects_data = {}
        self.system_info = {}
        self.merged_dependencies = {}
        self.conflicting_packages = []

    def load_data(self) -> bool:
        """스캔 리포트와 시스템 정보 로드"""
        print("[*] Loading project scan report and system config...")

        try:
            # 프로젝트 스캔 리포트 로드
            if os.path.exists(self.project_scan_report):
                with open(self.project_scan_report, 'r', encoding='utf-8') as f:
                    self.projects_data = json.load(f)
                print(f"    [+] Loaded {len(self.projects_data.get('projects', []))} projects")
            else:
                print(f"    [!] Project scan report not found: {self.project_scan_report}")
                return False

            # 시스템 정보 로드
            if os.path.exists(self.system_config):
                with open(self.system_config, 'r', encoding='utf-8') as f:
                    self.system_info = json.load(f)
                print(f"    [+] Loaded system configuration")
            else:
                print(f"    [!] System config not found: {self.system_config}")
                return False

            return True
        except Exception as e:
            print(f"    [!] Error loading data: {e}")
            return False

    def merge_dependencies(self) -> Dict[str, List[str]]:
        """모든 프로젝트의 의존성 통합"""
        print("[*] Merging dependencies...")

        merged = {}
        projects = self.projects_data.get('projects', [])

        for project in projects:
            project_name = project.get('name', 'Unknown')
            dependencies = project.get('dependencies', [])

            for dep in dependencies:
                if dep not in merged:
                    merged[dep] = []
                merged[dep].append(project_name)

        self.merged_dependencies = merged
        print(f"    [+] Merged {len(merged)} unique dependencies")

        return merged

    def resolve_conflicts(self) -> List[str]:
        """의존성 충돌 해결 및 최종 패키지 리스트 생성"""
        print("[*] Resolving potential conflicts...")

        final_packages = []
        self.conflicting_packages = []

        # 특별 처리가 필요한 패키지들
        special_handling = {
            'torch': self._handle_torch,
            'tensorflow': self._handle_tensorflow,
            'keras': self._handle_keras,
            'cuda': self._skip_package,  # CUDA는 시스템에서 설치해야 함
            'cudnn': self._skip_package,
        }

        for package, used_by in self.merged_dependencies.items():
            if package.lower() in special_handling:
                result = special_handling[package.lower()](package, used_by)
                if result:
                    final_packages.append(result)
            else:
                final_packages.append(package)

        # 중복 제거
        final_packages = list(set(final_packages))
        final_packages.sort()

        print(f"    [+] Resolved to {len(final_packages)} final packages")
        if self.conflicting_packages:
            print(f"    [!] Found {len(self.conflicting_packages)} potential conflicts:")
            for pkg in self.conflicting_packages:
                print(f"       - {pkg}")

        return final_packages

    def _handle_torch(self, package: str, used_by: List[str]) -> str:
        """PyTorch 특별 처리"""
        print(f"    [*] Special handling for torch (used by {len(used_by)} project(s))")

        cuda_version = self.system_info.get('cuda', {}).get('version', 'Unknown')
        has_gpu = self.system_info.get('gpu', {}).get('has_nvidia_gpu', False)

        # CUDA 버전에 따른 설치 옵션
        if not has_gpu:
            return "torch"  # CPU only

        # CUDA 버전 추출 (예: "12.4" from "12.4")
        cuda_version_short = cuda_version.split('.')[0] + '.' + cuda_version.split('.')[1] \
            if len(cuda_version.split('.')) > 1 else cuda_version

        cuda_mapping = {
            '12.4': 'torch>=2.0.0',
            '12.1': 'torch>=2.0.0',
            '11.8': 'torch>=1.13.0,<2.2.0',
            '11.7': 'torch>=1.12.0,<2.1.0',
            '11.6': 'torch>=1.11.0,<2.0.0',
        }

        # 기본값
        for key in cuda_mapping:
            if key in cuda_version:
                return cuda_mapping[key]

        return "torch"

    def _handle_tensorflow(self, package: str, used_by: List[str]) -> str:
        """TensorFlow 특별 처리"""
        print(f"    [*] Special handling for tensorflow (used by {len(used_by)} project(s))")
        return "tensorflow>=2.10.0"

    def _handle_keras(self, package: str, used_by: List[str]) -> str:
        """Keras 특별 처리"""
        print(f"    [*] Special handling for keras (used by {len(used_by)} project(s))")
        return None  # TensorFlow에 포함되어 있음

    def _skip_package(self, package: str, used_by: List[str]) -> str:
        """패키지 건너뛰기"""
        print(f"    [*] Skipping {package} (should be installed via system)")
        return None

    def generate_requirements(self) -> List[str]:
        """최종 requirements.txt 생성"""
        print("[*] Generating final requirements...")

        # 기본 패키지들
        base_packages = [
            "numpy",
            "pandas",
            "matplotlib",
            "seaborn",
            "opencv-python",
            "pillow",
            "scipy",
            "scikit-learn",
            "openpyxl",
            "tqdm",
            "pyyaml",
            "requests",
        ]

        # YOLO 관련 패키지
        yolo_packages = [
            "ultralytics>=8.0.0",
            "roboflow",
        ]

        # 의존성 병합
        final_packages = self.resolve_conflicts()

        # 모든 패키지 통합
        all_packages = base_packages + yolo_packages + final_packages

        # 중복 제거 및 정렬
        all_packages = sorted(list(set(all_packages)))

        # None 값 제거
        all_packages = [pkg for pkg in all_packages if pkg is not None]

        print(f"    [+] Generated {len(all_packages)} total packages")

        return all_packages

    def save_requirements(self, output_path: str = None) -> str:
        """requirements.txt 파일로 저장"""
        if output_path is None:
            output_path = "D:/project/data-tools/requirements.txt"

        packages = self.generate_requirements()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # requirements.txt 생성
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Auto-generated requirements.txt\n")
            f.write("# Generated based on project scan and system detection\n")
            f.write(f"# CUDA Version: {self.system_info.get('cuda', {}).get('version', 'Unknown')}\n")
            f.write(f"# GPU Available: {self.system_info.get('gpu', {}).get('has_nvidia_gpu', False)}\n")
            f.write("\n")

            # GPU 관련 설정
            if self.system_info.get('gpu', {}).get('has_nvidia_gpu'):
                f.write("# GPU-enabled packages\n")
                f.write("# Uncomment the appropriate line for your CUDA version:\n")
                f.write("# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124\n")
                f.write("# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121\n")
                f.write("# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118\n")
                f.write("\n")

            for package in packages:
                f.write(f"{package}\n")

        print(f"[+] Requirements saved to {output_path}")
        return output_path

    def print_summary(self):
        """요약 정보 출력"""
        print("\n" + "="*60)
        print("REQUIREMENTS GENERATION SUMMARY")
        print("="*60)

        print(f"\nProjects analyzed: {len(self.projects_data.get('projects', []))}")
        print(f"Total dependencies found: {len(self.merged_dependencies)}")
        print(f"Resolved conflicts: {len(self.conflicting_packages)}")

        print(f"\nSystem configuration:")
        print(f"  OS: {self.system_info.get('platform', {}).get('system')}")
        print(f"  GPU: {'NVIDIA' if self.system_info.get('gpu', {}).get('has_nvidia_gpu') else 'None'}")
        print(f"  CUDA: {self.system_info.get('cuda', {}).get('version', 'Not installed')}")

        print("\n" + "="*60 + "\n")


def main():
    """메인 실행 함수"""
    project_scan_report = "D:/project/data-tools/config/project_scan_report.json"
    system_config = "D:/project/data-tools/config/system_config.json"

    generator = RequirementsGenerator(project_scan_report, system_config)

    if generator.load_data():
        generator.merge_dependencies()
        generator.save_requirements()
        generator.print_summary()
    else:
        print("[!] Failed to generate requirements")


if __name__ == "__main__":
    main()
