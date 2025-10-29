"""
Project Scanner
"""
import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any
import re

class ProjectScanner:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.projects = []
        self.project_dependencies = {}

    def scan(self) -> List[Dict[str, Any]]:
        print(f"[*] Scanning projects in {self.root_path}...")
        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['venv', 'env', '__pycache__', 'node_modules']]
            project_info = self._check_project(root, files)
            if project_info:
                self.projects.append(project_info)
                print(f"    [+] Found: {project_info['name']}")
        return self.projects

    def _check_project(self, root: str, files: List[str]) -> Dict[str, Any] or None:
        indicators = ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile', 'main.py', 'app.py']
        detected = None
        deps = []
        for ind in indicators:
            if ind in files:
                if ind == 'requirements.txt':
                    deps = self._parse_req(os.path.join(root, ind))
                detected = ind
                break
        if detected:
            return {
                'name': os.path.basename(root),
                'path': root,
                'type': detected,
                'dependencies': deps,
                'python_files': [f for f in files if f.endswith('.py')],
                'config_files': [f for f in files if f in indicators],
            }
        return None

    def _parse_req(self, filepath: str) -> List[str]:
        packages = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        pkg = line.split('==')[0].split('>=')[0].split('<=')[0].split('>')[0].split('<')[0].split('!=')[0].strip()
                        if pkg:
                            packages.append(pkg)
        except Exception as e:
            print(f"    [!] Error: {e}")
        return packages

    def get_all_dependencies(self) -> Dict[str, int]:
        all_deps = {}
        for proj in self.projects:
            for dep in proj['dependencies']:
                all_deps[dep] = all_deps.get(dep, 0) + 1
        self.project_dependencies = all_deps
        return all_deps

    def save_report(self, path: str = None) -> str:
        if path is None:
            path = os.path.join(self.root_path, 'project_scan_report.json')
        report = {
            'scan_root': str(self.root_path),
            'total_projects': len(self.projects),
            'projects': self.projects,
            'dependencies': self.get_all_dependencies(),
        }
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"[+] Saved to {path}")
        return path

    def print_summary(self):
        print("")
        print("=" * 60)
        print("SCAN SUMMARY")
        print("=" * 60)
        print(f"Projects found: {len(self.projects)}")
        print(f"Dependencies: {len(self.get_all_dependencies())}")
        for i, p in enumerate(self.projects, 1):
            print(f"  {i}. {p['name']} ({p['type']})")
        print("=" * 60)
        print("")

def main():
    parser = argparse.ArgumentParser(description='Project Scanner')
    parser.add_argument('--root', default='D:/project', help='Root directory')
    parser.add_argument('--output', default=None, help='Output path')
    args = parser.parse_args()
    
    print("")
    print("="*70)
    print("PROJECT SCANNER")
    print("="*70)
    print(f"Scanning: {args.root}")
    
    scanner = ProjectScanner(args.root)
    scanner.scan()
    scanner.print_summary()
    
    out = args.output or os.path.join(args.root, 'project_scan_report.json')
    scanner.save_report(out)

if __name__ == "__main__":
    main()
