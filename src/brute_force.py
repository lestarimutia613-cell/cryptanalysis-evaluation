"""
Advanced Brute Force with Extended Features
Brute-force dengan fitur tambahan dan optimization
"""

import time
from src.caesar_cipher import CaesarCipher
from src.vigenere_cipher import Vigenèrecipher
from src.heuristics import Heuristics
from src.metrics import MetricsCalculator


class BruteForceAnalysis:
    """
    Implementasi brute-force attack dengan tracking metrik (Extended Version)
    """
    
    def __init__(self, use_heuristics=False):
        self.use_heuristics = use_heuristics
        self.heuristics = Heuristics() if use_heuristics else None
        self.metrics = {}
    
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
            'evaluated_count': 26,
            'candidates_above_threshold': len(candidates),
            'top_candidates': candidates[:5],
            'execution_time': end_time - start_time,
            'search_space_reduction': ((26 - len(candidates)) / 26 * 100) if self.use_heuristics else 0
        }
    
    def vigenere_brute_force(self, ciphertext, max_key_length=6, threshold=50.0):
        """
        Brute-force Vigenère cipher dengan panjang kunci terbatas
        """
        start_time = time.time()
        candidates = []
        
        # Generate semua kemungkinan kunci (limited)
        keys = self._generate_vigenere_keys(max_key_length)[:10000]
        total_keyspace = len(keys)
        
        for key in keys:
            plaintext = Vigenèrecipher.decrypt(ciphertext, key)
            
            if self.use_heuristics:
                score = self.heuristics.combined_heuristic_score(plaintext)
                if score >= threshold:
                    candidates.append((key, plaintext, score))
            else:
                candidates.append((key, plaintext, 0))
        
        end_time = time.time()
        
        if self.use_heuristics:
            candidates.sort(key=lambda x: x[2], reverse=True)
        
        return {
            'method': 'Vigenère Brute-Force',
            'use_heuristics': self.use_heuristics,
            'max_key_length': max_key_length,
            'total_keyspace': total_keyspace,
            'evaluated_count': len(keys),
            'candidates_above_threshold': len(candidates),
            'top_candidates': candidates[:5],
            'execution_time': end_time - start_time,
            'search_space_reduction': ((total_keyspace - len(candidates)) / total_keyspace * 100) if self.use_heuristics else 0
        }
    
    @staticmethod
    def _generate_vigenere_keys(max_length, alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        """Generate semua kemungkinan kunci Vigenère hingga panjang tertentu"""
        keys = []
        
        for length in range(1, max_length + 1):
            if length == 1:
                keys.extend(list(alphabet))
            elif length == 2:
                for a in alphabet:
                    for b in alphabet:
                        keys.append(a + b)
                        if len(keys) > 10000:
                            return keys
            elif length == 3:
                for a in alphabet[:5]:
                    for b in alphabet[:5]:
                        for c in alphabet[:5]:
                            keys.append(a + b + c)
                            if len(keys) > 10000:
                                return keys
        
        return keys
    
    def compare_with_without_heuristics(self, ciphertext, cipher_type='caesar'):
        """
        Bandingkan brute-force dengan dan tanpa heuristik
        """
        # Tanpa heuristik
        analyzer_no_h = BruteForceAnalysis(use_heuristics=False)
        if cipher_type == 'caesar':
            result_no_h = analyzer_no_h.caesar_brute_force(ciphertext, threshold=0)
        else:
            result_no_h = analyzer_no_h.vigenere_brute_force(ciphertext)
        
        # Dengan heuristik
        analyzer_with_h = BruteForceAnalysis(use_heuristics=True)
        if cipher_type == 'caesar':
            result_with_h = analyzer_with_h.caesar_brute_force(ciphertext, threshold=50.0)
        else:
            result_with_h = analyzer_with_h.vigenere_brute_force(ciphertext)
        
        # Calculate metrics
        ssrr = MetricsCalculator.calculate_search_space_reduction_rate(
            result_no_h['total_keyspace'],
            result_with_h['candidates_above_threshold']
        )
        
        trr = MetricsCalculator.calculate_time_reduction_rate(
            result_no_h['execution_time'],
            result_with_h['execution_time']
        )
        
        ei = MetricsCalculator.calculate_efficiency_index(trr, ssrr)
        
        comparison = {
            'cipher_type': cipher_type,
            'without_heuristics': result_no_h,
            'with_heuristics': result_with_h,
            'ssrr': ssrr,
            'trr': trr,
            'efficiency_index': ei,
            'time_reduction_rate': trr,
            'search_space_reduction_rate': ssrr
        }
        
        return comparison
