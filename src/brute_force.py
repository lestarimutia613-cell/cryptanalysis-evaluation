"""
Brute Force Cryptanalysis
Implementasi brute-force dengan dan tanpa heuristik
"""

import time
from src.caesar_cipher import CaesarCipher
from src.vigenere_cipher import VigenèreCipher
from src.heuristics import Heuristics


class BruteForceAnalysis:
    """
    Implementasi brute-force attack dengan tracking metrik
    """
    
    def __init__(self, use_heuristics=False):
        self.use_heuristics = use_heuristics
        self.heuristics = Heuristics() if use_heuristics else None
    
    def caesar_brute_force(self, ciphertext, threshold=50.0):
        """
        Brute-force Caesar cipher
        """
        start_time = time.time()
        candidates = []
        
        for shift in range(26):
            plaintext = CaesarCipher.decrypt(ciphertext, shift)
            
            if self.use_heuristics:
                score = self.heuristics.combined_heuristic_score(plaintext)
                if score >= threshold:
                    candidates.append((shift, plaintext, score))
            else:
                candidates.append((shift, plaintext, 0))
        
        end_time = time.time()
        
        if self.use_heuristics:
            candidates.sort(key=lambda x: x[2], reverse=True)
        
        return {
            'total_keyspace': 26,
            'candidates_above_threshold': len(candidates),
            'top_candidates': candidates[:5],
            'execution_time': end_time - start_time,
            'search_space_reduction': ((26 - len(candidates)) / 26 * 100) if self.use_heuristics else 0
        }


if __name__ == "__main__":
    plaintext = "THE QUICK BROWN FOX"
    ciphertext = CaesarCipher.encrypt(plaintext, 3)
    print(f"Original: {plaintext}")
    print(f"Encrypted: {ciphertext}")
    
    print("\n=== WITHOUT HEURISTICS ===")
    analyzer_no_h = BruteForceAnalysis(use_heuristics=False)
    result_no_h = analyzer_no_h.caesar_brute_force(ciphertext, threshold=0)
    print(f"Time: {result_no_h['execution_time']:.6f}s")
    
    print("\n=== WITH HEURISTICS ===")
    analyzer_with_h = BruteForceAnalysis(use_heuristics=True)
    result_with_h = analyzer_with_h.caesar_brute_force(ciphertext, threshold=50.0)
    print(f"Time: {result_with_h['execution_time']:.6f}s")
    print(f"SSRR: {result_with_h['search_space_reduction']:.2f}%")
