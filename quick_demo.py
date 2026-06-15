"""
Quick Demo Script
Script untuk demo cepat semua fitur
"""

from src.caesar_cipher import CaesarCipher
from src.vigenere_cipher import Vigenèrecipher
from src.heuristics import Heuristics
from src.brute_force import BruteForceAnalysis
from src.metrics import MetricsCalculator


def quick_demo():
    """
    Quick demo dari semua fitur
    """
    print("\n" + "="*70)
    print("QUICK DEMO - CRYPTANALYSIS EVALUATION PROJECT")
    print("="*70)
    
    # ========== DEMO 1: Caesar Cipher ==========
    print("\n" + "-"*70)
    print("DEMO 1: Caesar Cipher Encryption & Decryption")
    print("-"*70)
    
    plaintext_caesar = "HELLO WORLD THIS IS A SECRET MESSAGE"
    key_caesar = 5
    
    print(f"\nOriginal Text: {plaintext_caesar}")
    print(f"Key (Shift): {key_caesar}")
    
    ciphertext_caesar = CaesarCipher.encrypt(plaintext_caesar, key_caesar)
    print(f"Encrypted: {ciphertext_caesar}")
    
    decrypted_caesar = CaesarCipher.decrypt(ciphertext_caesar, key_caesar)
    print(f"Decrypted: {decrypted_caesar}")
    
    # ========== DEMO 2: Vigenère Cipher ==========
    print("\n" + "-"*70)
    print("DEMO 2: Vigenère Cipher Encryption & Decryption")
    print("-"*70)
    
    plaintext_vigenere = "HELLO WORLD THIS IS A SECRET MESSAGE"
    key_vigenere = "SECRETKEY"
    
    print(f"\nOriginal Text: {plaintext_vigenere}")
    print(f"Key: {key_vigenere}")
    
    ciphertext_vigenere = Vigenèrecipher.encrypt(plaintext_vigenere, key_vigenere)
    print(f"Encrypted: {ciphertext_vigenere}")
    
    decrypted_vigenere = Vigenèrecipher.decrypt(ciphertext_vigenere, key_vigenere)
    print(f"Decrypted: {decrypted_vigenere}")
    
    # ========== DEMO 3: Heuristics ==========
    print("\n" + "-"*70)
    print("DEMO 3: Heuristics Evaluation")
    print("-"*70)
    
    h = Heuristics()
    
    valid_text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    random_text = "XYZABC DEFGH IJKLM NOPQR STUVW XYZAB"
    
    print(f"\nValid English Text: {valid_text}")
    print(f"  Frequency Score: {h.frequency_analysis_heuristic(valid_text):.2f}")
    print(f"  Chi-Square Score: {h.chi_square_statistical_heuristic(valid_text):.2f}")
    print(f"  Entropy Score: {h.entropy_based_heuristic(valid_text):.2f}")
    print(f"  Dictionary Score: {h.dictionary_based_heuristic(valid_text):.2f}%")
    print(f"  N-gram Score: {h.ngram_analysis_heuristic(valid_text):.2f}%")
    print(f"  Combined Score: {h.combined_heuristic_score(valid_text):.2f}")
    
    print(f"\nRandom Text: {random_text}")
    print(f"  Frequency Score: {h.frequency_analysis_heuristic(random_text):.2f}")
    print(f"  Chi-Square Score: {h.chi_square_statistical_heuristic(random_text):.2f}")
    print(f"  Entropy Score: {h.entropy_based_heuristic(random_text):.2f}")
    print(f"  Dictionary Score: {h.dictionary_based_heuristic(random_text):.2f}%")
    print(f"  N-gram Score: {h.ngram_analysis_heuristic(random_text):.2f}%")
    print(f"  Combined Score: {h.combined_heuristic_score(random_text):.2f}")
    
    # ========== DEMO 4: Brute-Force Comparison ==========
    print("\n" + "-"*70)
    print("DEMO 4: Brute-Force with/without Heuristics (Caesar)")
    print("-"*70)
    
    test_plaintext = "THE ANSWER IS FORTY TWO"
    test_key = 7
    test_ciphertext = CaesarCipher.encrypt(test_plaintext, test_key)
    
    print(f"\nPlaintext: {test_plaintext}")
    print(f"Key: {test_key}")
    print(f"Ciphertext: {test_ciphertext}")
    
    # Without heuristics
    analyzer_no_h = BruteForceAnalysis(use_heuristics=False)
    result_no_h = analyzer_no_h.caesar_brute_force(test_ciphertext, threshold=0)
    
    print(f"\nBrute-Force WITHOUT Heuristics:")
    print(f"  Total Keyspace: {result_no_h['total_keyspace']}")
    print(f"  Time: {result_no_h['execution_time']:.6f}s")
    print(f"  Candidates Evaluated: {result_no_h['evaluated_count']}")
    
    # With heuristics
    analyzer_with_h = BruteForceAnalysis(use_heuristics=True)
    result_with_h = analyzer_with_h.caesar_brute_force(test_ciphertext, threshold=50.0)
    
    print(f"\nBrute-Force WITH Heuristics (threshold=50):")
    print(f"  Total Keyspace: {result_with_h['total_keyspace']}")
    print(f"  Time: {result_with_h['execution_time']:.6f}s")
    print(f"  Candidates Above Threshold: {result_with_h['candidates_above_threshold']}")
    
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
    
    print(f"\nPerformance Metrics:")
    print(f"  SSRR (Search Space Reduction Rate): {ssrr:.2f}%")
    print(f"  TRR (Time Reduction Rate): {trr:.2f}%")
    print(f"  EI (Efficiency Index): {ei:.4f}")
    
    if result_with_h['top_candidates']:
        best_shift, best_text, best_score = result_with_h['top_candidates'][0]
        print(f"\nTop Candidate:")
        print(f"  Shift: {best_shift}")
        print(f"  Text: {best_text}")
        print(f"  Score: {best_score:.2f}")
        print(f"  Correct: {best_shift == test_key}")
    
    print("\n" + "="*70)
    print("DEMO COMPLETE!")
    print("="*70 + "\n")


if __name__ == "__main__":
    quick_demo()
