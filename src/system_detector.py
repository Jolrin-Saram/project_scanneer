"""
System Detector - GPU, CUDA, CPU 등 시스템 정보 수집
"""

import os
import json
import subprocess
import platform
from pathlib import Path
from typing import Dict, Any


class SystemDetector:
    """시스템 정보를 수집하는 클래스"""

    def __init__(self):
        """초기화"""
        self.system_info = {}

    def detect_all(self) -> Dict[str, Any]:
        """모든 시스템 정보 수집"""
        print("[*] Detecting system information...")

        self.system_info = {
            'platform': self._detect_platform(),
            'cpu': self._detect_cpu(),
            'gpu': self._detect_gpu(),
            'cuda': self._detect_cuda(),
            'cudnn': self._detect_cudnn(),
            'pytorch': self._detect_pytorch(),
            'memory': self._detect_memory(),
        }

        return self.system_info

    def _detect_platform(self) -> Dict[str, Any]:
        """플랫폼 정보 수집"""
        print("  [*] Detecting platform...")
        return {
            'system': platform.system(),
            'release': platform.release(),
            'machine': platform.machine(),
            'processor': platform.processor(),
        }

    def _detect_cpu(self) -> Dict[str, Any]:
        """CPU 정보 수집"""
        print("  [*] Detecting CPU...")
        try:
            if platform.system() == 'Windows':
                # Windows에서 CPU 정보
                result = subprocess.run(
                    ['wmic', 'cpu', 'get', 'name', '/value'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                cpu_name = result.stdout.split('=')[1].strip() if '=' in result.stdout else 'Unknown'

                # 코어 수
                import psutil
                cores = psutil.cpu_count(logical=False)
                threads = psutil.cpu_count(logical=True)

                return {
                    'name': cpu_name,
                    'cores': cores,
                    'threads': threads,
                }
            else:
                # Linux/Mac
                import psutil
                return {
                    'name': platform.processor(),
                    'cores': psutil.cpu_count(logical=False),
                    'threads': psutil.cpu_count(logical=True),
                }
        except Exception as e:
            print(f"    [!] Error detecting CPU: {e}")
            return {'name': 'Unknown', 'cores': 'Unknown', 'threads': 'Unknown'}

    def _detect_gpu(self) -> Dict[str, Any]:
        """GPU 정보 수집"""
        print("  [*] Detecting GPU...")
        gpu_info = {
            'has_nvidia_gpu': False,
            'gpu_name': 'None',
            'total_memory': 'Unknown',
            'available_memory': 'Unknown',
            'compute_capability': 'Unknown',
        }

        try:
            # nvidia-smi 명령어로 GPU 정보 수집
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=name,memory.total,memory.free,compute_cap', '--format=csv,noheader'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if lines:
                    parts = lines[0].split(',')
                    if len(parts) >= 4:
                        gpu_info['has_nvidia_gpu'] = True
                        gpu_info['gpu_name'] = parts[0].strip()
                        gpu_info['total_memory'] = parts[1].strip()
                        gpu_info['available_memory'] = parts[2].strip()
                        gpu_info['compute_capability'] = parts[3].strip()
                        print(f"    [+] NVIDIA GPU detected: {gpu_info['gpu_name']}")
        except FileNotFoundError:
            print("    [!] nvidia-smi not found. NVIDIA GPU tools may not be installed.")
        except Exception as e:
            print(f"    [!] Error detecting GPU: {e}")

        return gpu_info

    def _detect_cuda(self) -> Dict[str, Any]:
        """CUDA 정보 수집"""
        print("  [*] Detecting CUDA...")
        cuda_info = {
            'installed': False,
            'version': 'Unknown',
            'path': 'Unknown',
        }

        try:
            result = subprocess.run(
                ['nvidia-smi'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                # nvidia-smi 출력에서 CUDA 버전 추출
                for line in result.stdout.split('\n'):
                    if 'CUDA Version' in line:
                        cuda_version = line.split(':')[-1].strip()
                        cuda_info['installed'] = True
                        cuda_info['version'] = cuda_version
                        print(f"    [+] CUDA version: {cuda_version}")
                        break

            # CUDA_PATH 환경변수 확인
            cuda_path = os.environ.get('CUDA_PATH')
            if cuda_path:
                cuda_info['path'] = cuda_path
        except Exception as e:
            print(f"    [!] Error detecting CUDA: {e}")

        return cuda_info

    def _detect_cudnn(self) -> Dict[str, Any]:
        """cuDNN 정보 수집"""
        print("  [*] Detecting cuDNN...")
        cudnn_info = {
            'installed': False,
            'version': 'Unknown',
            'path': 'Unknown',
        }

        try:
            # cuDNN을 찾기 위해 일반적인 경로 확인
            possible_paths = [
                os.environ.get('CUDNN_PATH'),
                os.path.join(os.environ.get('CUDA_PATH', ''), 'include'),
                'C:\\Program Files\\NVIDIA GPU Computing Toolkit\\cuDNN',
                '/usr/local/cuda/include',
            ]

            for path in possible_paths:
                if path and os.path.exists(path):
                    # cudnn.h 파일 찾기
                    cudnn_h = os.path.join(path, 'cudnn.h')
                    if os.path.exists(cudnn_h):
                        cudnn_info['path'] = path
                        cudnn_info['installed'] = True
                        print(f"    [+] cuDNN found at: {path}")
                        break

        except Exception as e:
            print(f"    [!] Error detecting cuDNN: {e}")

        return cudnn_info

    def _detect_pytorch(self) -> Dict[str, Any]:
        """PyTorch 설치 여부 및 버전"""
        print("  [*] Detecting PyTorch...")
        pytorch_info = {
            'installed': False,
            'version': 'Unknown',
            'cuda_support': False,
        }

        try:
            import torch
            pytorch_info['installed'] = True
            pytorch_info['version'] = torch.__version__
            pytorch_info['cuda_support'] = torch.cuda.is_available()
            print(f"    [+] PyTorch version: {torch.__version__}")
            if torch.cuda.is_available():
                print(f"    [+] CUDA is available for PyTorch")
        except ImportError:
            print("    [!] PyTorch not installed")

        return pytorch_info

    def _detect_memory(self) -> Dict[str, Any]:
        """메모리 정보 수집"""
        print("  [*] Detecting memory...")
        memory_info = {
            'total_gb': 'Unknown',
            'available_gb': 'Unknown',
        }

        try:
            import psutil
            memory = psutil.virtual_memory()
            memory_info['total_gb'] = round(memory.total / (1024**3), 2)
            memory_info['available_gb'] = round(memory.available / (1024**3), 2)
            print(f"    [+] Total RAM: {memory_info['total_gb']} GB")
        except Exception as e:
            print(f"    [!] Error detecting memory: {e}")

        return memory_info

    def get_cuda_pytorch_requirement(self) -> str:
        """시스템 CUDA 버전에 맞는 PyTorch 요구사항 생성"""
        cuda_version = self.system_info.get('cuda', {}).get('version', 'Unknown')

        # CUDA 버전에 따른 PyTorch 설치 옵션
        cuda_mapping = {
            '12.4': 'torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124',
            '12.1': 'torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121',
            '11.8': 'torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118',
            '11.7': 'torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117',
            '11.6': 'torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu116',
            'CPU': 'torch torchvision torchaudio',  # CPU only
        }

        # 정확한 버전 매칭
        for key, value in cuda_mapping.items():
            if key in cuda_version:
                return value

        # 기본값: CPU only
        print("[!] CUDA version not recognized, defaulting to CPU-only PyTorch")
        return cuda_mapping['CPU']

    def save_config(self, output_path: str = None):
        """시스템 정보를 JSON으로 저장"""
        if output_path is None:
            output_path = "D:/project/data-tools/config/system_config.json"

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.system_info, f, indent=2, ensure_ascii=False)

        print(f"[+] System config saved to {output_path}")
        return output_path

    def print_summary(self):
        """시스템 정보 요약 출력"""
        print("\n" + "="*60)
        print("SYSTEM INFORMATION SUMMARY")
        print("="*60)

        # Platform
        platform_info = self.system_info.get('platform', {})
        print(f"\nPlatform:")
        print(f"  OS: {platform_info.get('system')} {platform_info.get('release')}")
        print(f"  Architecture: {platform_info.get('machine')}")

        # CPU
        cpu_info = self.system_info.get('cpu', {})
        print(f"\nCPU:")
        print(f"  Name: {cpu_info.get('name')}")
        print(f"  Cores: {cpu_info.get('cores')}")
        print(f"  Threads: {cpu_info.get('threads')}")

        # Memory
        memory_info = self.system_info.get('memory', {})
        print(f"\nMemory:")
        print(f"  Total: {memory_info.get('total_gb')} GB")
        print(f"  Available: {memory_info.get('available_gb')} GB")

        # GPU
        gpu_info = self.system_info.get('gpu', {})
        print(f"\nGPU:")
        if gpu_info.get('has_nvidia_gpu'):
            print(f"  GPU: {gpu_info.get('gpu_name')}")
            print(f"  Total Memory: {gpu_info.get('total_memory')}")
            print(f"  Compute Capability: {gpu_info.get('compute_capability')}")
        else:
            print(f"  GPU: Not detected (CPU only)")

        # CUDA
        cuda_info = self.system_info.get('cuda', {})
        print(f"\nCUDA:")
        if cuda_info.get('installed'):
            print(f"  Version: {cuda_info.get('version')}")
            print(f"  Path: {cuda_info.get('path')}")
        else:
            print(f"  CUDA: Not installed or not detected")

        # cuDNN
        cudnn_info = self.system_info.get('cudnn', {})
        print(f"\ncuDNN:")
        if cudnn_info.get('installed'):
            print(f"  Path: {cudnn_info.get('path')}")
        else:
            print(f"  cuDNN: Not installed or not detected")

        # PyTorch
        pytorch_info = self.system_info.get('pytorch', {})
        print(f"\nPyTorch:")
        if pytorch_info.get('installed'):
            print(f"  Version: {pytorch_info.get('version')}")
            print(f"  CUDA Support: {pytorch_info.get('cuda_support')}")
        else:
            print(f"  PyTorch: Not installed")

        print("\n" + "="*60 + "\n")


def main():
    """메인 실행 함수"""
    detector = SystemDetector()
    detector.detect_all()
    detector.print_summary()
    detector.save_config()


if __name__ == "__main__":
    main()
