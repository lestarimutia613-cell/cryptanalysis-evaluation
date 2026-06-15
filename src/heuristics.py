"""
Heuristics for Cryptanalysis
Implementasi 5 heuristik untuk membimbing pencarian brute-force
"""

import math
from collections import Counter

class Heuristics:
    """
    Kumpulan heuristik untuk evaluasi kualitas plaintext
    """
    
    ENGLISH_FREQ = {
        'A': 8.2, 'B': 1.5, 'C': 2.8, 'D': 4.3, 'E': 12.7,
        'F': 2.2, 'G': 2.0, 'H': 6.1, 'I': 7.0, 'J': 0.15,
        'K': 0.77, 'L': 4.0, 'M': 2.4, 'N': 6.7, 'O': 7.5,
        'P': 1.9, 'Q': 0.10, 'R': 6.0, 'S': 6.3, 'T': 9.1,
        'U': 2.8, 'V': 0.98, 'W': 2.4, 'X': 0.15, 'Y': 2.0,
        'Z': 0.07
    }
    
    COMMON_BIGRAMS = [
        'TH', 'HE', 'IN', 'ER', 'AN', 'ED', 'ND', 'TO', 'EN', 'TI',
        'ES', 'OR', 'TE', 'AR', 'YOU', 'IT', 'HA', 'ET', 'NG', 'ON'
    ]
    
    def __init__(self, common_words_file=None):
        self.common_words = self._load_common_words(common_words_file)
    
    @staticmethod
    def _load_common_words(filepath=None):
        return {
            'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'CAN',
            'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'HAD', 'HAS', 'HIS',
            'HOW', 'MAN', 'OLD', 'SEE', 'NOW', 'WAY', 'WHO', 'OIL',
            'USE', 'HIM', 'TWO', 'MAY', 'SAY', 'SHE', 'ITS', 'LET'
        }
    
    @staticmethod
    def text_to_alpha_only(text):
        return ''.join(c for c in text if c.isalpha()).upper()
    
    @staticmethod
    def frequency_analysis_heuristic(plaintext):
        """
        1. English Frequency Analysis Heuristic (EFAH)
        Score tinggi = plaintext lebih mungkin Inggris yang valid
        """
        text = Heuristics.text_to_alpha_only(plaintext)
        if len(text) < 10:
            return 0
        
        freq = Counter(text)
        total = len(text)
        
        chi_square = 0
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            observed = freq.get(letter, 0) / total * 100
            expected = Heuristics.ENGLISH_FREQ.get(letter, 0)
            if expected > 0:
                chi_square += (observed - expected) ** 2 / expected
        
        score = max(0, 100 - chi_square * 2)
        return min(100, score)
    
    @staticmethod
    def chi_square_statistical_heuristic(plaintext):
        """
        2. Chi-Square Statistical Test Heuristic (CSTTH)
        """
        text = Heuristics.text_to_alpha_only(plaintext)
        if len(text) < 10:
            return float('inf')
        
        freq = Counter(text)
        total = len(text)
        
        chi_square = 0
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            observed = freq.get(letter, 0)
            expected = (Heuristics.ENGLISH_FREQ.get(letter, 0) / 100) * total
            if expected > 0:
                chi_square += (observed - expected) ** 2 / expected
        
        return chi_square
    
    @staticmethod
    def entropy_based_heuristic(plaintext):
        """
        3. Entropy-Based Heuristic (EBH)
        """
        text = Heuristics.text_to_alpha_only(plaintext)
        if len(text) == 0:
            return 0
        
        freq = Counter(text)
        total = len(text)
        
        entropy = 0
        for count in freq.values():
            probability = count / total
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def dictionary_based_heuristic(self, plaintext):
        """
        4. Dictionary-Based Heuristic (DBH)
        """
        words = plaintext.upper().split()
        if len(words) == 0:
            return 0
        
        found = sum(1 for word in words if word in self.common_words)
        return (found / len(words)) * 100
    
    @staticmethod
    def ngram_analysis_heuristic(plaintext, n=2):
        """
        5. N-gram Analysis Heuristic (NAH)
        """
        text = Heuristics.text_to_alpha_only(plaintext)
        if len(text) < n:
            return 0
        
        ngrams = [text[i:i+n] for i in range(len(text) - n + 1)]
        common_ngrams = Heuristics.COMMON_BIGRAMS
        
        match_count = sum(1 for ng in ngrams if ng in common_ngrams)
        return (match_count / len(ngrams)) * 100 if ngrams else 0
    
    def combined_heuristic_score(self, plaintext, weights=None):
        """
        Kombinasi semua 5 heuristik dengan bobot tertentu
        """
        if weights is None:
            weights = {
                'frequency': 0.25,
                'entropy': 0.15,
                'dictionary': 0.35,
                'ngram': 0.25
            }
        
        scores = {
            'frequency': self.frequency_analysis_heuristic(plaintext),
            'entropy': max(0, 100 - self.entropy_based_heuristic(plaintext) * 10),
            'dictionary': self.dictionary_based_heuristic(plaintext),
            'ngram': self.ngram_analysis_heuristic(plaintext)
        }
        
        combined = sum(scores[key] * weights[key] for key in weights)
        return min(100, max(0, combined))


if __name__ == "__main__":
    h = Heuristics()
    valid_text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    random_text = "XYZABC DEFGH IJKLM NOPQR STUVW"
    
    print("=== Heuristic Scores ===")
    print(f"\nValid English: '{valid_text}'")
    print(f"  Frequency: {h.frequency_analysis_heuristic(valid_text):.2f}")
    print(f"  Combined: {h.combined_heuristic_score(valid_text):.2f}")
    print(f"\nRandom: '{random_text}'")
    print(f"  Frequency: {h.frequency_analysis_heuristic(random_text):.2f}")
    print(f"  Combined: {h.combined_heuristic_score(random_text):.2f}")
