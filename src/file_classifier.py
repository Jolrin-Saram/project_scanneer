"""
File Classifier - 파일명 기반 지능형 분류 모듈
파일명에 포함된 알파벳과 숫자를 기준으로 자동 분류
"""

import os
import re
from typing import Dict, List, Tuple, Any
from collections import defaultdict


class FileClassifier:
    """파일명 패턴을 기반으로 파일을 분류하는 클래스"""

    def __init__(self):
        """초기화"""
        self.classifications = {}  # {original_filename: classified_type}
        self.classification_groups = {}  # {classification_type: [files]}
        self.classification_stats = {}  # {classification_type: count}

    def extract_classification(self, filename: str) -> str:
        """
        파일명에서 분류 타입 추출

        규칙:
        1. 파일명에서 '('를 기준으로 앞부분만 사용
        2. '_'가 있는 경우:
           - '_' 이전의 모든 문자 + '_' + '_' 이후의 알파벳들
           - 예: A_H8(1)8888 → A_H
           - 예: AB_CD123(2) → AB_CD
        3. '_'가 없는 경우:
           - 알파벳이 있으면 알파벳만
           - 알파벳이 없으면 전체 (숫자만)
           - 예: AB7(1) → AB
           - 예: 2211(1)8888 → 2211

        Args:
            filename: 파일명 (확장자 포함)

        Returns:
            분류 타입 (문자열)
        """
        # 확장자 제거
        name_without_ext = os.path.splitext(filename)[0]

        # '('를 기준으로 앞부분만 사용
        before_paren = name_without_ext.split('(')[0].strip()

        # '_'가 있는지 확인
        if '_' in before_paren:
            # '_' 이전과 이후로 분리
            parts = before_paren.split('_', 1)  # 첫 번째 '_'만 분리
            before_underscore = parts[0]
            after_underscore = parts[1] if len(parts) > 1 else ''

            # '_' 이후의 알파벳만 추출
            after_underscore_letters = re.match(r'[A-Za-z]+', after_underscore)

            if after_underscore_letters:
                # '_' 이전 + '_' + '_' 이후 알파벳
                classification = before_underscore + '_' + after_underscore_letters.group()
            else:
                # '_' 이후에 알파벳이 없으면 '_' 앞까지만
                classification = before_underscore

        else:
            # '_'가 없는 경우
            # 알파벳만 추출
            letters_only = re.findall(r'[A-Za-z]+', before_paren)

            if letters_only:
                # 알파벳이 있으면 알파벳만 (전체 알파벳 부분)
                classification = ''.join(letters_only)
            else:
                # 알파벳이 없으면 전체 (숫자만)
                classification = before_paren

        return classification

    def classify_files(self, filenames: List[str]) -> Dict[str, str]:
        """
        여러 파일을 분류

        Args:
            filenames: 파일명 리스트

        Returns:
            {filename: classification_type} 딕셔너리
        """
        for filename in filenames:
            classification = self.extract_classification(filename)
            self.classifications[filename] = classification

        return self.classifications

    def get_classification_groups(self) -> Dict[str, List[str]]:
        """
        분류 타입별로 파일을 그룹화

        Returns:
            {classification_type: [files]} 딕셔너리
        """
        groups = defaultdict(list)

        for filename, classification in self.classifications.items():
            groups[classification].append(filename)

        self.classification_groups = dict(groups)
        return self.classification_groups

    def get_classification_stats(self) -> Dict[str, int]:
        """
        분류 타입별 파일 수 통계

        Returns:
            {classification_type: count} 딕셔너리
        """
        stats = {}

        for classification, files in self.classification_groups.items():
            stats[classification] = len(files)

        # 개수 기준으로 정렬
        self.classification_stats = dict(
            sorted(stats.items(), key=lambda x: x[1], reverse=True)
        )

        return self.classification_stats

    def print_classification_report(self):
        """분류 결과 리포트 출력"""
        if not self.classifications:
            print("[!] No files classified yet")
            return

        # 그룹화
        self.get_classification_groups()

        # 통계 계산
        self.get_classification_stats()

        print("\n" + "="*70)
        print("FILE CLASSIFICATION REPORT")
        print("="*70)

        print(f"\nTotal files: {len(self.classifications)}")
        print(f"Total classification types: {len(self.classification_groups)}")

        print("\nClassification Summary:")
        print("-" * 70)
        print(f"{'Classification Type':<30} {'Count':<10} {'Percentage':<10}")
        print("-" * 70)

        for classification, count in self.classification_stats.items():
            percentage = (count / len(self.classifications)) * 100
            print(f"{classification:<30} {count:<10} {percentage:>6.1f}%")

        print("-" * 70)

        print("\nDetailed Classification:")
        print("-" * 70)

        for classification in sorted(self.classification_groups.keys()):
            files = self.classification_groups[classification]
            print(f"\n{classification} ({len(files)} files):")
            for filename in sorted(files):
                print(f"  - {filename}")

        print("\n" + "="*70 + "\n")

    def export_classification(self, output_path: str = None) -> str:
        """
        분류 결과를 JSON으로 내보내기

        Args:
            output_path: 저장 경로

        Returns:
            저장된 파일 경로
        """
        import json
        import os

        if output_path is None:
            output_path = "D:/project/data-tools/config/file_classification.json"

        # 그룹화
        self.get_classification_groups()
        self.get_classification_stats()

        export_data = {
            'total_files': len(self.classifications),
            'total_classifications': len(self.classification_groups),
            'classifications': {
                filename: classification
                for filename, classification in self.classifications.items()
            },
            'groups': self.classification_groups,
            'statistics': self.classification_stats,
        }

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        print(f"[+] Classification exported to {output_path}")
        return output_path


def test_classification():
    """분류 규칙 테스트"""
    test_cases = [
        ('A_H8(1)8888.jpg', 'A_H'),
        ('AB7(1).jpg', 'AB'),
        ('2211(1)8888.jpg', '2211'),
        ('AB_CD123(2).jpg', 'AB_CD'),
        ('XYZ_ABC456(3)999.jpg', 'XYZ_ABC'),
        ('123_456(1).jpg', '123'),
        ('SAMPLE.jpg', 'SAMPLE'),
        ('2211.jpg', '2211'),
        ('AB_123(1).jpg', 'AB'),
        ('IMG_001_02.jpg', 'IMG_001'),
    ]

    classifier = FileClassifier()

    print("\n" + "="*70)
    print("FILE CLASSIFICATION TEST")
    print("="*70)
    print(f"{'Filename':<35} {'Classification':<20} {'Status':<10}")
    print("-" * 70)

    all_pass = True
    for filename, expected in test_cases:
        result = classifier.extract_classification(filename)
        status = "[PASS]" if result == expected else "[FAIL]"

        if result != expected:
            all_pass = False
            print(f"{filename:<35} {result:<20} {status:<10} (expected: {expected})")
        else:
            print(f"{filename:<35} {result:<20} {status:<10}")

    print("-" * 70)
    if all_pass:
        print("[+] All tests passed!")
    else:
        print("[!] Some tests failed!")

    print("="*70 + "\n")


def main():
    """테스트 코드"""
    # 테스트 케이스 검증
    test_classification()

    # 샘플 분류
    sample_files = [
        'A_H8(1)8888.jpg',
        'A_H8(2)0000.jpg',
        'A_H8(3)2222.jpg',
        'AB7(1).jpg',
        'AB7(2).jpg',
        '2211(1)8888.jpg',
        '2211(2)0000.jpg',
        'XYZ_ABC456(1).jpg',
    ]

    classifier = FileClassifier()
    classifier.classify_files(sample_files)
    classifier.print_classification_report()
    classifier.export_classification()


if __name__ == "__main__":
    main()
