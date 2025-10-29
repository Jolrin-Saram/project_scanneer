"""
Project Scanner - D:\project 내 모든 Python 프로젝트 발견 및 분석
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any
import re


class ProjectScanner:
    """프로젝트를 스캔하고 구조를 분석하는 클래스"""

    def __init__(self, root_path: str):
        """
        Args:
            root_path: 스캔할 루트 경로 (e.g., 'D:/project')
        """
        self.root_path = Path(root_path)
        self.projects = []
        self.project_dependencies = {}

    def scan(self) -> List[Dict[str, Any]]:
        """
        D:\project 디렉토리를 재귀적으로 스캔하여 Python 프로젝트 발견

        Returns:
            프로젝트 정보 리스트
        """
        print(f"[*] Scanning projects in {self.root_path}...")

        for root, dirs, files in os.walk(self.root_path):
            # 숨겨진 폴더와 가상환경 폴더 제외
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['venv', 'env', '__pycache__', 'node_modules']]

            # Python 프로젝트 감지
            project_info = self._check_project(root, files)
            if project_info:
                self.projects.append(project_info)
                print(f"    [+] Found project: {project_info['name']} at {project_info['path']}")

        return self.projects

    def _check_project(self, root: str, files: List[str]) -> Dict[str, Any] or None:
        """
        특정 디렉토리가 Python 프로젝트인지 확인

        Args:
            root: 현재 디렉토리 경로
            files: 디렉토리 내 파일 리스트

        Returns:
            프로젝트 정보 또는 None
        """
        project_indicators = {
            'requirements.txt': self._parse_requirements,
            'setup.py': self._parse_setup_py,
            'pyproject.toml': self._parse_pyproject_toml,
            'Pipfile': self._parse_pipfile,
            'main.py': None,
            'app.py': None,
        }

        detected_type = None
        dependencies = []

        for indicator, parser in project_indicators.items():
            if indicator in files:
                if parser:
                    try:
                        dependencies = parser(os.path.join(root, indicator))
                    except Exception as e:
                        print(f"    [!] Error parsing {indicator}: {e}")
                        dependencies = []
                detected_type = indicator
                break

        # 프로젝트를 발견했으면 정보 반환
        if detected_type:
            project_name = os.path.basename(root)
            return {
                'name': project_name,
                'path': root,
                'type': detected_type,
                'dependencies': dependencies,
                'python_files': [f for f in files if f.endswith('.py')],
                'config_files': [f for f in files if f in project_indicators.keys()],
            }

        return None

    def _parse_requirements(self, filepath: str) -> List[str]:
        """requirements.txt 파싱"""
        packages = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # 주석과 빈 줄 제외
                    if line and not line.startswith('#'):
                        # 버전 정보 분리
                        package = re.split(r'[<>=!]', line)[0].strip()
                        if package:
                            packages.append(package)
        except Exception as e:
            print(f"    [!] Error reading {filepath}: {e}")

        return packages

    def _parse_setup_py(self, filepath: str) -> List[str]:
        """setup.py 파싱 (간단한 버전)"""
        packages = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # install_requires 찾기
                match = re.search(r'install_requires\s*=\s*\[(.*?)\]', content, re.DOTALL)
                if match:
                    deps_str = match.group(1)
                    # 문자열 추출
                    for dep in re.findall(r"['\"]([^'\"]+)['\"]", deps_str):
                        package = re.split(r'[<>=!]', dep)[0].strip()
                        if package:
                            packages.append(package)
        except Exception as e:
            print(f"    [!] Error reading {filepath}: {e}")

        return packages

    def _parse_pyproject_toml(self, filepath: str) -> List[str]:
        """pyproject.toml 파싱 (간단한 버전)"""
        packages = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # dependencies 섹션 찾기
                match = re.search(r'dependencies\s*=\s*\[(.*?)\]', content, re.DOTALL)
                if match:
                    deps_str = match.group(1)
                    for dep in re.findall(r"['\"]([^'\"]+)['\"]", deps_str):
                        package = re.split(r'[<>=!]', dep)[0].strip()
                        if package:
                            packages.append(package)
        except Exception as e:
            print(f"    [!] Error reading {filepath}: {e}")

        return packages

    def _parse_pipfile(self, filepath: str) -> List[str]:
        """Pipfile 파싱 (간단한 버전)"""
        packages = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # [packages] 섹션 찾기
                match = re.search(r'\[packages\](.*?)(?:\[|$)', content, re.DOTALL)
                if match:
                    packages_section = match.group(1)
                    for line in packages_section.split('\n'):
                        package = line.split('=')[0].strip()
                        if package and not package.startswith('#'):
                            packages.append(package)
        except Exception as e:
            print(f"    [!] Error reading {filepath}: {e}")

        return packages

    def get_all_dependencies(self) -> Dict[str, int]:
        """모든 프로젝트의 의존성 통합"""
        all_deps = {}

        for project in self.projects:
            for dep in project['dependencies']:
                all_deps[dep] = all_deps.get(dep, 0) + 1

        self.project_dependencies = all_deps
        return all_deps

    def save_report(self, output_path: str = None) -> str:
        """분석 결과를 JSON 리포트로 저장"""
        if output_path is None:
            output_path = os.path.join(self.root_path, 'project_scan_report.json')

        report = {
            'scan_root': str(self.root_path),
            'total_projects_found': len(self.projects),
            'projects': self.projects,
            'all_dependencies': self.get_all_dependencies(),
        }

        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"[+] Report saved to {output_path}")
        return output_path

    def print_summary(self):
        """요약 정보 출력"""
        print("\n" + "="*60)
        print("PROJECT SCAN SUMMARY")
        print("="*60)
        print(f"Total projects found: {len(self.projects)}")
        print(f"Total unique dependencies: {len(self.get_all_dependencies())}")

        print("\nProjects:")
        for i, project in enumerate(self.projects, 1):
            print(f"  {i}. {project['name']}")
            print(f"     Path: {project['path']}")
            print(f"     Type: {project['type']}")
            print(f"     Dependencies: {len(project['dependencies'])}")

        print("\nTop dependencies (used in multiple projects):")
        sorted_deps = sorted(self.project_dependencies.items(), key=lambda x: x[1], reverse=True)[:10]
        for dep, count in sorted_deps:
            print(f"  - {dep}: {count} project(s)")

        print("="*60 + "\n")


def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(
        description='Python 프로젝트 스캐너 - 지정된 디렉토리 내 모든 프로젝트를 재귀적으로 발견'
    )
    parser.add_argument(
        '--root',
        type=str,
        default='D:/project',
        help='스캔할 루트 디렉토리 경로 (기본값: D:/project)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='리포트 저장 경로 (기본값: root_path/project_scan_report.json)'
    )

    args = parser.parse_args()
    root_path = args.root

    print(f"
{'='*70}")
    print(f"프로젝트 스캐너 시작")
    print(f"{'='*70}")
    print(f"스캔 위치: {root_path}")

    # 프로젝트 스캔
    scanner = ProjectScanner(root_path)
    projects = scanner.scan()

    # 요약 출력
    scanner.print_summary()

    # 리포트 저장
    if args.output:
        output_path = args.output
    else:
        output_path = os.path.join(root_path, "project_scan_report.json")

    scanner.save_report(output_path)


if __name__ == "__main__":
    main()
