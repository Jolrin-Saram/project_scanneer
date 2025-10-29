"""
Visualizer - 분석 결과 시각화 모듈 (그래프, 차트)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from typing import Dict, List, Any
from pathlib import Path


class ResultVisualizer:
    """분석 결과를 시각화하는 클래스"""

    def __init__(self, output_dir: str = None):
        """
        Args:
            output_dir: 그래프 저장 디렉토리
        """
        self.output_dir = output_dir or "D:/project/data-tools/outputs"
        os.makedirs(self.output_dir, exist_ok=True)

        # 한글 폰트 설정
        self._setup_fonts()

    def _setup_fonts(self):
        """한글 폰트 설정"""
        try:
            # Windows 기본 한글 폰트
            plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False
        except:
            pass

    def plot_metrics_summary(self, results: Dict[str, Any]) -> str:
        """
        성능 메트릭 요약 그래프

        Args:
            results: 분석 결과

        Returns:
            저장된 파일 경로
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Detection Performance Metrics', fontsize=16, fontweight='bold')

        # 1. Overall Metrics (Precision, Recall, F1)
        overall = results['metrics']['overall']
        metrics = ['Precision', 'Recall', 'F1 Score']
        values = [overall['precision'], overall['recall'], overall['f1_score']]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

        axes[0, 0].bar(metrics, values, color=colors, alpha=0.7, edgecolor='black')
        axes[0, 0].set_ylabel('Score')
        axes[0, 0].set_title('Overall Metrics')
        axes[0, 0].set_ylim([0, 1.1])
        for i, v in enumerate(values):
            axes[0, 0].text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold')

        # 2. Confusion Matrix (TP, FP, FN)
        tp = overall['tp']
        fp = overall['fp']
        fn = overall['fn']
        confusion_values = [tp, fp, fn]
        confusion_labels = [f'TP\n{tp}', f'FP\n{fp}', f'FN\n{fn}']
        colors2 = ['#2ECC71', '#E74C3C', '#F39C12']

        axes[0, 1].bar(confusion_labels, confusion_values, color=colors2, alpha=0.7, edgecolor='black')
        axes[0, 1].set_ylabel('Count')
        axes[0, 1].set_title('Confusion Matrix')

        # 3. Per-Class Precision & Recall
        if results['metrics']['per_class']:
            class_names = list(results['metrics']['per_class'].keys())
            precisions = [results['metrics']['per_class'][c]['precision'] for c in class_names]
            recalls = [results['metrics']['per_class'][c]['recall'] for c in class_names]

            x = np.arange(len(class_names))
            width = 0.35

            axes[1, 0].bar(x - width/2, precisions, width, label='Precision', alpha=0.8, color='#3498DB')
            axes[1, 0].bar(x + width/2, recalls, width, label='Recall', alpha=0.8, color='#E67E22')
            axes[1, 0].set_ylabel('Score')
            axes[1, 0].set_title('Per-Class Metrics')
            axes[1, 0].set_xticks(x)
            axes[1, 0].set_xticklabels(class_names, rotation=45, ha='right')
            axes[1, 0].legend()
            axes[1, 0].set_ylim([0, 1.1])

        # 4. AP Scores
        if results['ap_scores']:
            ap_names = list(results['ap_scores'].keys())
            ap_values = list(results['ap_scores'].values())

            axes[1, 1].barh(ap_names, ap_values, color='#9B59B6', alpha=0.7, edgecolor='black')
            axes[1, 1].set_xlabel('AP Score')
            axes[1, 1].set_title('Average Precision (AP) by Class')
            axes[1, 1].set_xlim([0, 1.1])
            for i, v in enumerate(ap_values):
                axes[1, 1].text(v + 0.02, i, f'{v:.3f}', va='center', fontweight='bold')

        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'metrics_summary.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"[+] Metrics summary saved to {output_path}")
        return output_path

    def plot_detection_rate(self, detection_rate: float) -> str:
        """
        검출률 시각화

        Args:
            detection_rate: 검출률 (%)

        Returns:
            저장된 파일 경로
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        # 원형 차트
        sizes = [detection_rate, 100 - detection_rate]
        labels = [f'Detected\n{detection_rate:.1f}%', f'Not Detected\n{100-detection_rate:.1f}%']
        colors = ['#2ECC71', '#E74C3C']
        explode = (0.05, 0)

        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                            explode=explode, startangle=90, textprops={'fontsize': 12})

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax.set_title('Object Detection Rate', fontsize=14, fontweight='bold', pad=20)

        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'detection_rate.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"[+] Detection rate visualization saved to {output_path}")
        return output_path

    def plot_class_distribution(self, class_distribution: Dict[str, int], title: str = 'Class Distribution') -> str:
        """
        클래스 분포 시각화

        Args:
            class_distribution: 클래스별 객체 수 딕셔너리
            title: 그래프 제목

        Returns:
            저장된 파일 경로
        """
        if not class_distribution:
            print("[!] No class distribution data to visualize")
            return None

        fig, ax = plt.subplots(figsize=(12, 6))

        classes = list(class_distribution.keys())
        counts = list(class_distribution.values())
        colors = plt.cm.Set3(np.linspace(0, 1, len(classes)))

        bars = ax.bar(classes, counts, color=colors, alpha=0.8, edgecolor='black')

        # 값 표시
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold')

        ax.set_xlabel('Class', fontweight='bold')
        ax.set_ylabel('Count', fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        plt.xticks(rotation=45, ha='right')

        plt.tight_layout()
        output_path = os.path.join(self.output_dir, f'{title.lower().replace(" ", "_")}.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"[+] Class distribution saved to {output_path}")
        return output_path

    def plot_confidence_distribution(self, confidence_scores: List[float]) -> str:
        """
        신뢰도 분포 시각화

        Args:
            confidence_scores: 신뢰도 점수 리스트

        Returns:
            저장된 파일 경로
        """
        if not confidence_scores:
            print("[!] No confidence scores to visualize")
            return None

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.hist(confidence_scores, bins=30, color='#3498DB', alpha=0.7, edgecolor='black')

        ax.axvline(np.mean(confidence_scores), color='#E74C3C', linestyle='--', linewidth=2, label=f'Mean: {np.mean(confidence_scores):.3f}')
        ax.axvline(np.median(confidence_scores), color='#F39C12', linestyle='--', linewidth=2, label=f'Median: {np.median(confidence_scores):.3f}')

        ax.set_xlabel('Confidence Score', fontweight='bold')
        ax.set_ylabel('Frequency', fontweight='bold')
        ax.set_title('Confidence Score Distribution', fontsize=14, fontweight='bold', pad=20)
        ax.legend()

        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'confidence_distribution.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"[+] Confidence distribution saved to {output_path}")
        return output_path

    def plot_file_type_analysis(self, file_type_distribution: Dict[str, int]) -> str:
        """
        파일 종류 분류 시각화

        Args:
            file_type_distribution: 파일 종류별 수 딕셔너리

        Returns:
            저장된 파일 경로
        """
        if not file_type_distribution:
            print("[!] No file type data to visualize")
            return None

        fig, ax = plt.subplots(figsize=(10, 8))

        file_types = list(file_type_distribution.keys())
        counts = list(file_type_distribution.values())
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        colors = colors[:len(file_types)] + [plt.cm.Set2(i) for i in range(max(0, len(file_types) - 5))]

        wedges, texts, autotexts = ax.pie(counts, labels=file_types, colors=colors[:len(file_types)],
                                           autopct='%1.1f%%', startangle=90)

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax.set_title('File Type Distribution', fontsize=14, fontweight='bold', pad=20)

        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'file_type_distribution.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"[+] File type distribution saved to {output_path}")
        return output_path

    def plot_defect_type_analysis(self, defect_distribution: Dict[str, int]) -> str:
        """
        불량 유형(라벨) 분류 시각화

        Args:
            defect_distribution: 불량 유형별 수 딕셔너리

        Returns:
            저장된 파일 경로
        """
        return self.plot_class_distribution(defect_distribution, title='Defect Type Distribution')

    def plot_file_classification_analysis(self, file_classification_stats: Dict[str, int],
                                          file_classification_distribution: Dict[str, int] = None) -> str:
        """
        파일명 기반 분류 분석 시각화

        Args:
            file_classification_stats: 파일명 분류별 파일 수 딕셔너리
            file_classification_distribution: 파일명 분류별 객체 수 딕셔너리

        Returns:
            저장된 파일 경로
        """
        if not file_classification_stats:
            print("[!] No file classification data to visualize")
            return None

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # 1. 파일명 분류별 파일 수
        classifications = list(file_classification_stats.keys())
        file_counts = list(file_classification_stats.values())
        colors = plt.cm.Set3(np.linspace(0, 1, len(classifications)))

        axes[0].bar(classifications, file_counts, color=colors, alpha=0.8, edgecolor='black')
        axes[0].set_xlabel('File Classification', fontweight='bold')
        axes[0].set_ylabel('Number of Files', fontweight='bold')
        axes[0].set_title('Files by Classification Type', fontsize=12, fontweight='bold')
        axes[0].tick_params(axis='x', rotation=45)

        for i, v in enumerate(file_counts):
            axes[0].text(i, v + 0.1, str(v), ha='center', fontweight='bold')

        # 2. 파일명 분류별 객체 수
        if file_classification_distribution:
            object_counts = list(file_classification_distribution.values())
            axes[1].bar(classifications, object_counts, color=colors, alpha=0.8, edgecolor='black')
            axes[1].set_xlabel('File Classification', fontweight='bold')
            axes[1].set_ylabel('Number of Objects', fontweight='bold')
            axes[1].set_title('Objects Detected by Classification Type', fontsize=12, fontweight='bold')
            axes[1].tick_params(axis='x', rotation=45)

            for i, v in enumerate(object_counts):
                axes[1].text(i, v + 0.5, str(v), ha='center', fontweight='bold')
        else:
            axes[1].remove()
            fig.set_size_inches(10, 6)

        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'file_classification_analysis.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"[+] File classification analysis saved to {output_path}")
        return output_path

    def create_full_report(self, results: Dict[str, Any], detector_summary: Dict[str, Any] = None) -> List[str]:
        """
        전체 분석 리포트 생성

        Args:
            results: 분석 결과
            detector_summary: 검출기 요약 정보

        Returns:
            생성된 파일 경로 리스트
        """
        generated_files = []

        # 1. 메트릭 요약
        file1 = self.plot_metrics_summary(results)
        generated_files.append(file1)

        # 2. 검출률
        file2 = self.plot_detection_rate(results['detection_rate'])
        generated_files.append(file2)

        # 3. 클래스 분포
        if detector_summary and 'class_distribution' in detector_summary:
            file3 = self.plot_class_distribution(detector_summary['class_distribution'], title='Detection Class Distribution')
            generated_files.append(file3)

        # 4. 신뢰도 분포 (detector_summary에서 추출)
        if detector_summary and 'all_confidences' in detector_summary:
            file4 = self.plot_confidence_distribution(detector_summary['all_confidences'])
            generated_files.append(file4)

        # 5. 파일 종류 분포
        if detector_summary and 'file_type_distribution' in detector_summary:
            file5 = self.plot_file_type_analysis(detector_summary['file_type_distribution'])
            generated_files.append(file5)

        # 6. 불량 유형 분포 (클래스 분포와 동일)
        if detector_summary and 'class_distribution' in detector_summary:
            file6 = self.plot_defect_type_analysis(detector_summary['class_distribution'])
            generated_files.append(file6)

        # 7. 파일명 분류 분석
        if detector_summary and 'file_classification_stats' in detector_summary:
            file7 = self.plot_file_classification_analysis(
                detector_summary['file_classification_stats'],
                detector_summary.get('file_classification_distribution', {})
            )
            if file7:
                generated_files.append(file7)

        return generated_files


def main():
    """테스트 코드"""
    visualizer = ResultVisualizer()

    # 샘플 데이터
    sample_results = {
        'metrics': {
            'overall': {
                'precision': 0.85,
                'recall': 0.92,
                'f1_score': 0.88,
                'tp': 46,
                'fp': 8,
                'fn': 4,
            },
            'per_class': {
                'dog': {'precision': 0.90, 'recall': 0.95, 'f1_score': 0.92},
                'cat': {'precision': 0.80, 'recall': 0.90, 'f1_score': 0.85},
                'bird': {'precision': 0.85, 'recall': 0.85, 'f1_score': 0.85},
            },
        },
        'ap_scores': {
            'dog': 0.92,
            'cat': 0.85,
            'bird': 0.87,
        },
        'detection_rate': 92.5,
    }

    sample_detector_summary = {
        'class_distribution': {'dog': 25, 'cat': 15, 'bird': 10},
        'all_confidences': np.random.uniform(0.5, 0.99, 50).tolist(),
        'file_type_distribution': {'jpg': 30, 'png': 15, 'bmp': 5},
    }

    # 전체 리포트 생성
    files = visualizer.create_full_report(sample_results, sample_detector_summary)
    print(f"\n[+] Generated {len(files)} visualization files")


if __name__ == "__main__":
    main()
