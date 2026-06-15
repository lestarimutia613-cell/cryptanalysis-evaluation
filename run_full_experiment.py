"""
Run Experiments and Visualize Results
Script untuk menjalankan eksperimen lengkap dan membuat visualisasi
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.experiments import CryptoanalysisExperiment
from src.visualization import CryptoanalysisVisualizer


def main():
    """
    Main function untuk menjalankan eksperimen dan visualisasi lengkap
    """
    print("\n" + "="*70)
    print("CRYPTANALYSIS EVALUATION PROJECT")
    print("Full Experiment & Visualization Pipeline")
    print("="*70 + "\n")
    
    # Step 1: Run experiments
    print("STEP 1: Running Experiments...")
    print("-" * 70)
    
    experiment = CryptoanalysisExperiment(output_dir='results')
    results = experiment.run_all_experiments()
    
    caesar_df = results['caesar']
    vigenere_df = results['vigenere']
    
    # Step 2: Create visualizations
    print("\n\nSTEP 2: Creating Visualizations...")
    print("-" * 70)
    
    visualizer = CryptoanalysisVisualizer(output_dir='results/graphs')
    visualizer.create_comprehensive_report(caesar_df, vigenere_df)
    
    print("\n" + "="*70)
    print("EXPERIMENT & VISUALIZATION COMPLETE!")
    print("="*70)
    print("\nResults saved in 'results/' directory")
    print("Graphs saved in 'results/graphs/' directory")
    print("\nNext steps:")
    print("1. Open results/graphs/ to view visualizations")
    print("2. Check results/caesar_results_*.csv for detailed data")
    print("3. Check results/vigenere_results_*.csv for detailed data")
    print("4. Review results/summary_*.json for summary statistics")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
