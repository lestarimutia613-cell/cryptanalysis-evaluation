"""
Experiments Module
Script untuk menjalankan eksperimen komprehensif evaluasi cryptanalysis
"""

import random
import string
import pandas as pd
import json
import os
from datetime import datetime
from typing import Dict, List

from src.caesar_cipher import CaesarCipher
from src.vigenere_cipher import Vigenèrecipher
from src.brute_force import BruteForceAnalysis
from src.metrics import MetricsCalculator
from src.heuristics import Heuristics


class CryptoanalysisExperiment:
    """
    Kelas untuk menjalankan eksperimen cryptanalysis komprehensif
    """
    
    def __init__(self, output_dir='results'):
        """
        Initialize experiment
        
        Args:
            output_dir (str): Direktori untuk menyimpan hasil
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.results = []
        self.summary = {}
    
    @staticmethod
    def generate_plaintext(length: int) -> str:
        """
        Generate random plaintext dari sample teks
        
        Args:
            length (int): Panjang plaintext
            
        Returns:
            str: Random plaintext
        """
        sample_texts = [
            "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",
            "CRYPTOGRAPHY IS THE PRACTICE AND STUDY OF TECHNIQUES",
            "SECURITY THROUGH OBSCURITY IS NOT A GOOD IDEA",
            "HEURISTIC GUIDED SEARCH IMPROVES BRUTE FORCE ATTACK",
            "INFORMATION SECURITY IS THE PRACTICE OF PROTECTING",
            "THE ONLY SECURE COMPUTER IS ONE THAT IS OFF",
            "ENCRYPTION IS CRITICAL TO DIGITAL SECURITY",
            "FREQUENCY ANALYSIS IS FUNDAMENTAL TO CRYPTANALYSIS",
            "SUBSTITUTION CIPHER WAS USED BY JULIUS CAESAR",
            "POLYALPHABETIC CIPHER IS MORE SECURE THAN MONOALPHABETIC"
        ]
        
        selected = random.choice(sample_texts)
        while len(selected) < length:
            selected += " " + random.choice(sample_texts)
        
        return selected[:length].upper()
    
    def experiment_caesar_cipher(self, text_sizes: List[int] = None, 
                                 num_trials: int = 5) -> pd.DataFrame:
        """
        Experiment untuk Caesar cipher
        
        Args:
            text_sizes (list): Daftar ukuran teks untuk ditest
            num_trials (int): Jumlah trial per ukuran teks
            
        Returns:
            pd.DataFrame: Hasil eksperimen
        """
        if text_sizes is None:
            text_sizes = [50, 100, 200, 500]
        
        results = []
        
        print("\n" + "="*70)
        print("EXPERIMENT 1: CAESAR CIPHER")
        print("="*70)
        
        for text_size in text_sizes:
            print(f"\nTesting text size: {text_size} characters")
            
            for trial in range(num_trials):
                # Generate plaintext dan key
                plaintext = self.generate_plaintext(text_size)
                key = random.randint(1, 25)
                ciphertext = CaesarCipher.encrypt(plaintext, key)
                
                # Brute force tanpa heuristik
                analyzer_no_h = BruteForceAnalysis(use_heuristics=False)
                result_no_h = analyzer_no_h.caesar_brute_force(ciphertext, threshold=0)
                
                # Brute force dengan heuristik
                analyzer_with_h = BruteForceAnalysis(use_heuristics=True)
                result_with_h = analyzer_with_h.caesar_brute_force(ciphertext, threshold=50.0)
                
                # Hitung metrik
                ssrr = MetricsCalculator.calculate_search_space_reduction_rate(
                    result_no_h['total_keyspace'],
                    result_with_h['candidates_above_threshold']
                )
                
                trr = MetricsCalculator.calculate_time_reduction_rate(
                    result_no_h['execution_time'],
                    result_with_h['execution_time']
                )
                
                ei = MetricsCalculator.calculate_efficiency_index(trr, ssrr)
                
                # Cek apakah plaintext benar ditemukan
                top_candidate = result_with_h['top_candidates'][0] if result_with_h['top_candidates'] else None
                correct = top_candidate and top_candidate[0] == key if top_candidate else False
                
                results.append({
                    'cipher_type': 'Caesar',
                    'text_size': text_size,
                    'trial': trial + 1,
                    'actual_key': key,
                    'total_keyspace': result_no_h['total_keyspace'],
                    'search_space_reduction_rate': ssrr,
                    'time_reduction_rate': trr,
                    'efficiency_index': ei,
                    'time_without_heuristics': result_no_h['execution_time'],
                    'time_with_heuristics': result_with_h['execution_time'],
                    'candidates_above_threshold': result_with_h['candidates_above_threshold'],
                    'correct_found': correct
                })
                
                print(f"  Trial {trial+1}: SSRR={ssrr:.2f}%, TRR={trr:.2f}%, EI={ei:.4f}, Correct={correct}")
        
        df = pd.DataFrame(results)
        return df
    
    def experiment_vigenere_cipher(self, text_sizes: List[int] = None,
                                   key_lengths: List[int] = None,
                                   num_trials: int = 3) -> pd.DataFrame:
        """
        Experiment untuk Vigenère cipher
        
        Args:
            text_sizes (list): Daftar ukuran teks
            key_lengths (list): Daftar panjang kunci
            num_trials (int): Jumlah trial per kombinasi
            
        Returns:
            pd.DataFrame: Hasil eksperimen
        """
        if text_sizes is None:
            text_sizes = [100, 200, 500]
        if key_lengths is None:
            key_lengths = [3, 4, 5]
        
        results = []
        
        print("\n" + "="*70)
        print("EXPERIMENT 2: VIGENÈRE CIPHER")
        print("="*70)
        
        for text_size in text_sizes:
            for key_length in key_lengths:
                print(f"\nTesting text size: {text_size}, key length: {key_length}")
                
                for trial in range(num_trials):
                    # Generate plaintext dan key
                    plaintext = self.generate_plaintext(text_size)
                    key = ''.join(random.choice(string.ascii_uppercase) for _ in range(key_length))
                    ciphertext = Vigenèrecipher.encrypt(plaintext, key)
                    
                    # Brute force tanpa heuristik (dengan keyspace terbatas)
                    analyzer_no_h = BruteForceAnalysis(use_heuristics=False)
                    result_no_h = analyzer_no_h.vigenere_brute_force(
                        ciphertext, max_key_length=key_length, threshold=0
                    )
                    
                    # Brute force dengan heuristik
                    analyzer_with_h = BruteForceAnalysis(use_heuristics=True)
                    result_with_h = analyzer_with_h.vigenere_brute_force(
                        ciphertext, max_key_length=key_length, threshold=50.0
                    )
                    
                    # Hitung metrik
                    ssrr = MetricsCalculator.calculate_search_space_reduction_rate(
                        result_no_h['total_keyspace'],
                        result_with_h['candidates_above_threshold']
                    )
                    
                    trr = MetricsCalculator.calculate_time_reduction_rate(
                        result_no_h['execution_time'],
                        result_with_h['execution_time']
                    )
                    
                    ei = MetricsCalculator.calculate_efficiency_index(trr, ssrr)
                    
                    # Cek apakah key benar ditemukan
                    top_candidate = result_with_h['top_candidates'][0] if result_with_h['top_candidates'] else None
                    correct = top_candidate and top_candidate[0].upper() == key.upper() if top_candidate else False
                    
                    results.append({
                        'cipher_type': 'Vigenère',
                        'text_size': text_size,
                        'key_length': key_length,
                        'trial': trial + 1,
                        'actual_key': key,
                        'total_keyspace': result_no_h['total_keyspace'],
                        'search_space_reduction_rate': ssrr,
                        'time_reduction_rate': trr,
                        'efficiency_index': ei,
                        'time_without_heuristics': result_no_h['execution_time'],
                        'time_with_heuristics': result_with_h['execution_time'],
                        'candidates_above_threshold': result_with_h['candidates_above_threshold'],
                        'correct_found': correct
                    })
                    
                    print(f"  Trial {trial+1}: SSRR={ssrr:.2f}%, TRR={trr:.2f}%, EI={ei:.4f}, Correct={correct}")
        
        df = pd.DataFrame(results)
        return df
    
    def run_all_experiments(self):
        """
        Jalankan semua eksperimen
        
        Returns:
            dict: Hasil semua eksperimen
        """
        print("\n" + "="*70)
        print("CRYPTANALYSIS EVALUATION EXPERIMENTS")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        # Caesar cipher experiments
        caesar_df = self.experiment_caesar_cipher(
            text_sizes=[50, 100, 200],
            num_trials=3
        )
        
        # Vigenère cipher experiments
        vigenere_df = self.experiment_vigenere_cipher(
            text_sizes=[100, 200],
            key_lengths=[3, 4, 5],
            num_trials=2
        )
        
        # Save results
        self._save_results(caesar_df, vigenere_df)
        
        # Print summary
        self._print_summary(caesar_df, vigenere_df)
        
        return {
            'caesar': caesar_df,
            'vigenere': vigenere_df
        }
    
    def _save_results(self, caesar_df: pd.DataFrame, vigenere_df: pd.DataFrame):
        """Simpan hasil eksperimen"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save CSV
        caesar_file = os.path.join(self.output_dir, f'caesar_results_{timestamp}.csv')
        vigenere_file = os.path.join(self.output_dir, f'vigenere_results_{timestamp}.csv')
        
        caesar_df.to_csv(caesar_file, index=False)
        vigenere_df.to_csv(vigenere_file, index=False)
        
        print(f"\nResults saved:")
        print(f"  - {caesar_file}")
        print(f"  - {vigenere_file}")
        
        # Save summary JSON
        summary = {
            'caesar_stats': {
                'avg_ssrr': float(caesar_df['search_space_reduction_rate'].mean()),
                'avg_trr': float(caesar_df['time_reduction_rate'].mean()),
                'avg_ei': float(caesar_df['efficiency_index'].mean()),
                'accuracy': float(caesar_df['correct_found'].sum() / len(caesar_df) * 100)
            },
            'vigenere_stats': {
                'avg_ssrr': float(vigenere_df['search_space_reduction_rate'].mean()),
                'avg_trr': float(vigenere_df['time_reduction_rate'].mean()),
                'avg_ei': float(vigenere_df['efficiency_index'].mean()),
                'accuracy': float(vigenere_df['correct_found'].sum() / len(vigenere_df) * 100)
            },
            'timestamp': timestamp
        }
        
        summary_file = os.path.join(self.output_dir, f'summary_{timestamp}.json')
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"  - {summary_file}")
    
    def _print_summary(self, caesar_df: pd.DataFrame, vigenere_df: pd.DataFrame):
        """Print summary hasil eksperimen"""
        print("\n" + "="*70)
        print("EXPERIMENT SUMMARY")
        print("="*70)
        
        print("\n### CAESAR CIPHER ###")
        print(f"Average SSRR: {caesar_df['search_space_reduction_rate'].mean():.2f}%")
        print(f"Average TRR: {caesar_df['time_reduction_rate'].mean():.2f}%")
        print(f"Average EI: {caesar_df['efficiency_index'].mean():.4f}")
        print(f"Accuracy (correct key found): {caesar_df['correct_found'].sum() / len(caesar_df) * 100:.2f}%")
        
        print("\n### VIGENÈRE CIPHER ###")
        print(f"Average SSRR: {vigenere_df['search_space_reduction_rate'].mean():.2f}%")
        print(f"Average TRR: {vigenere_df['time_reduction_rate'].mean():.2f}%")
        print(f"Average EI: {vigenere_df['efficiency_index'].mean():.4f}")
        print(f"Accuracy (correct key found): {vigenere_df['correct_found'].sum() / len(vigenere_df) * 100:.2f}%")
        
        print("\n" + "="*70)


if __name__ == "__main__":
    experiment = CryptoanalysisExperiment()
    results = experiment.run_all_experiments()
