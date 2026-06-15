"""
Main Demo Script
Script utama untuk demonstrasi semua fitur
"""

from src.caesar_cipher import CaesarCipher
from src.vigenere_cipher import VigenèreCipher
from src.heuristics import Heuristics
from src.brute_force import BruteForceAnalysis
from src.metrics import MetricsCalculator


def demo_caesar():
    """Demo Caesar Cipher"""
    print("\n" + "="*70)
    print("DEMO 1: CAESAR CIPHER")
    print("="*70)
    
    plaintext = "HELLO WORLD THIS IS A SECRET MESSAGE"
    shift = 3
    
    ciphertext = CaesarCipher.encrypt(plaintext, shift)
    print(f"\nPlaintext: {plaintext}")
    print(f"Shift: {shift}")
    print(f"Ciphertext: {ciphertext}")
    print(f"Decrypted: {CaesarCipher.decrypt(ciphertext, shift)}")
    
    print("\n--- Brute Force Comparison ---")
    analyzer_no_h = BruteForceAnalysis(use_heuristics=False)
    result_no_h = analyzer_no_h.caesar_brute_force(ciphertext, threshold=0)
    print(f"\nWithout Heuristics:")
    print(f"  Time: {result_no_h['execution_time']:.6f}s")
    
    analyzer_with_h = BruteForceAnalysis(use_heuristics=True)
    result_with_h = analyzer_with_h.caesar_brute_force(ciphertext, threshold=50.0)
    print(f"\nWith Heuristics (threshold=50):")
    print(f"  Time: {result_with_h['execution_time']:.6f}s")
    print(f"  Candidates: {result_with_h['candidates_above_threshold']}")
    
    ssrr = MetricsCalculator.calculate_search_space_reduction_rate(
        result_no_h['total_keyspace'],
        result_with_h['candidates_above_threshold']
    )
    trr = MetricsCalculator.calculate_time_reduction_rate(
        result_no_h['execution_time'],
        result_with_h['execution_time']
    )
    ei = MetricsCalculator.calculate_efficiency_index(trr, ssrr)
    
    print(f"\nMetrics:")
    print(f"  SSRR: {ssrr:.2f}%")
    print(f"  TRR: {trr:.2f}%")
    print(f"  EI: {ei:.4f}")


def demo_vigenere():
    """Demo Vigenère Cipher"""
    print("\n" + "="*70)
    print("DEMO 2: VIGENÈRE CIPHER")
    print("="*70)
    
    plaintext = "HELLO WORLD THIS IS A SECRET MESSAGE"
    key = "SECRET"
    
    ciphertext = VigenèreCipher.encrypt(plaintext, key)
    print(f"\nPlaintext: {plaintext}")
    print(f"Key: {key}")
    print(f"Ciphertext: {ciphertext}")
    print(f"Decrypted: {VigenèreCipher.decrypt(ciphertext, key)}")
    
    print("\n--- Kasiski Examination ---")
    analysis = VigenèreCipher.kasiski_examination(ciphertext)
    print(f"Possible key lengths: {analysis}")


def demo_heuristics():
    """Demo Heuristics"""
    print("\n" + "="*70)
    print("DEMO 3: HEURISTICS EVALUATION")
    print("="*70)
    
    h = Heuristics()
    valid_text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    random_text = "XYZABC DEFGH IJKLM NOPQR STUVW"
    
    print(f"\n--- Valid English Text ---")
    print(f"Text: {valid_text}")
    print(f"  Frequency: {h.frequency_analysis_heuristic(valid_text):.2f}")
    print(f"  Chi-Square: {h.chi_square_statistical_heuristic(valid_text):.2f}")
    print(f"  Entropy: {h.entropy_based_heuristic(valid_text):.2f}")
    print(f"  Dictionary: {h.dictionary_based_heuristic(valid_text):.2f}%")
    print(f"  N-gram: {h.ngram_analysis_heuristic(valid_text):.2f}%")
    print(f"  Combined: {h.combined_heuristic_score(valid_text):.2f}")
    
    print(f"\n--- Random Text ---")
    print(f"Text: {random_text}")
    print(f"  Frequency: {h.frequency_analysis_heuristic(random_text):.2f}")
    print(f"  Chi-Square: {h.chi_square_statistical_heuristic(random_text):.2f}")
    print(f"  Entropy: {h.entropy_based_heuristic(random_text):.2f}")
    print(f"  Dictionary: {h.dictionary_based_heuristic(random_text):.2f}%")
    print(f"  N-gram: {h.ngram_analysis_heuristic(random_text):.2f}%")
    print(f"  Combined: {h.combined_heuristic_score(random_text):.2f}")


def main():
    """Main function"""
    print("\n" + "="*70)
    print("CRYPTANALYSIS EVALUATION PROJECT")
    print("Heuristic-Guided Brute-Force Cryptanalysis")
    print("="*70)
    
    demo_caesar()
    demo_vigenere()
    demo_heuristics()
    
    print("\n" + "="*70)
    print("DEMO COMPLETE!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
