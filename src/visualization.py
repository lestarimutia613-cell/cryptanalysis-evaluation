"""
Visualization Module
Visualisasi hasil eksperimen cryptanalysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List
import os


class CryptoanalysisVisualizer:
    """
    Visualisasi hasil eksperimen
    """
    
    def __init__(self, output_dir='results/graphs'):
        """
        Initialize visualizer
        
        Args:
            output_dir (str): Direktori untuk menyimpan grafik
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style
        sns.set_style("whitegrid")
        sns.set_palette("husl")
        plt.rcParams['figure.figsize'] = (12, 6)
        plt.rcParams['font.size'] = 10
    
    def plot_ssrr_vs_text_size(self, caesar_df: pd.DataFrame, 
                               save=True, filename='ssrr_vs_text_size.png'):
        """
        Plot SSRR vs ukuran teks untuk Caesar cipher
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Aggregate by text size
        avg_data = caesar_df.groupby('text_size')['search_space_reduction_rate'].agg(['mean', 'std'])
        
        ax.errorbar(avg_data.index, avg_data['mean'], yerr=avg_data['std'],
                   marker='o', markersize=10, capsize=5, capthick=2, linewidth=2.5, 
                   color='steelblue', ecolor='lightblue')
        
        ax.set_xlabel('Text Size (characters)', fontsize=12, fontweight='bold')
        ax.set_ylabel('SSRR (%)', fontsize=12, fontweight='bold')
        ax.set_title('Search Space Reduction Rate vs Text Size (Caesar Cipher)', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 105)
        
        if save:
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved: {filepath}")
        
        plt.close()
    
    def plot_trr_vs_text_size(self, caesar_df: pd.DataFrame,
                             save=True, filename='trr_vs_text_size.png'):
        """
        Plot TRR vs ukuran teks
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        avg_data = caesar_df.groupby('text_size')['time_reduction_rate'].agg(['mean', 'std'])
        
        ax.errorbar(avg_data.index, avg_data['mean'], yerr=avg_data['std'],
                   marker='s', markersize=10, capsize=5, capthick=2, linewidth=2.5, 
                   color='coral', ecolor='lightsalmon')
        
        ax.set_xlabel('Text Size (characters)', fontsize=12, fontweight='bold')
        ax.set_ylabel('TRR (%)', fontsize=12, fontweight='bold')
        ax.set_title('Time Reduction Rate vs Text Size (Caesar Cipher)',
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 105)
        
        if save:
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved: {filepath}")
        
        plt.close()
    
    def plot_efficiency_index(self, caesar_df: pd.DataFrame, vigenere_df: pd.DataFrame,
                             save=True, filename='efficiency_index.png'):
        """
        Plot Efficiency Index untuk kedua cipher
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Caesar
        caesar_ei = caesar_df.groupby('text_size')['efficiency_index'].mean()
        ax1.bar(caesar_ei.index, caesar_ei.values, color='steelblue', alpha=0.7, 
                edgecolor='black', linewidth=1.5)
        ax1.set_xlabel('Text Size (characters)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Efficiency Index (EI)', fontsize=11, fontweight='bold')
        ax1.set_title('Caesar Cipher - Efficiency Index', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for i, v in enumerate(caesar_ei.values):
            ax1.text(caesar_ei.index[i], v + 0.01, f'{v:.3f}', ha='center', fontsize=9)
        
        # Vigenère
        vigenere_ei = vigenere_df.groupby('key_length')['efficiency_index'].mean()
        ax2.bar(vigenere_ei.index, vigenere_ei.values, color='coral', alpha=0.7, 
                edgecolor='black', linewidth=1.5)
        ax2.set_xlabel('Key Length', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Efficiency Index (EI)', fontsize=11, fontweight='bold')
        ax2.set_title('Vigenère Cipher - Efficiency Index', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for i, v in enumerate(vigenere_ei.values):
            ax2.text(vigenere_ei.index[i], v + 0.01, f'{v:.3f}', ha='center', fontsize=9)
        
        plt.tight_layout()
        
        if save:
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved: {filepath}")
        
        plt.close()
    
    def plot_execution_time_comparison(self, caesar_df: pd.DataFrame,
                                      save=True, filename='execution_time_comparison.png'):
        """
        Plot perbandingan waktu eksekusi dengan/tanpa heuristik
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        text_sizes = sorted(caesar_df['text_size'].unique())
        x = np.arange(len(text_sizes))
        width = 0.35
        
        without_h = [caesar_df[caesar_df['text_size'] == ts]['time_without_heuristics'].mean() 
                    for ts in text_sizes]
        with_h = [caesar_df[caesar_df['text_size'] == ts]['time_with_heuristics'].mean()
                 for ts in text_sizes]
        
        bars1 = ax.bar(x - width/2, without_h, width, label='Without Heuristics', 
                      alpha=0.8, color='steelblue', edgecolor='black')
        bars2 = ax.bar(x + width/2, with_h, width, label='With Heuristics', 
                      alpha=0.8, color='coral', edgecolor='black')
        
        ax.set_xlabel('Text Size (characters)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Execution Time (seconds)', fontsize=12, fontweight='bold')
        ax.set_title('Execution Time Comparison (Caesar Cipher)',
                    fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(text_sizes)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3, axis='y')
        
        if save:
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved: {filepath}")
        
        plt.close()
    
    def plot_vigenere_key_length_analysis(self, vigenere_df: pd.DataFrame,
                                         save=True, filename='vigenere_key_length.png'):
        """
        Plot analisis Vigenère berdasarkan panjang kunci
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # SSRR vs Key Length
        ssrr_data = vigenere_df.groupby('key_length')['search_space_reduction_rate'].mean()
        ax1.plot(ssrr_data.index, ssrr_data.values, marker='o', markersize=12, 
                linewidth=2.5, color='green', markerfacecolor='lightgreen', 
                markeredgecolor='darkgreen', markeredgewidth=2)
        ax1.set_xlabel('Key Length', fontsize=11, fontweight='bold')
        ax1.set_ylabel('SSRR (%)', fontsize=11, fontweight='bold')
        ax1.set_title('Vigenère: SSRR vs Key Length', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, 105)
        
        # Add value labels
        for i, v in enumerate(ssrr_data.values):
            ax1.text(ssrr_data.index[i], v + 2, f'{v:.1f}%', ha='center', fontsize=9)
        
        # TRR vs Key Length
        trr_data = vigenere_df.groupby('key_length')['time_reduction_rate'].mean()
        ax2.plot(trr_data.index, trr_data.values, marker='s', markersize=12,
                linewidth=2.5, color='red', markerfacecolor='lightcoral', 
                markeredgecolor='darkred', markeredgewidth=2)
        ax2.set_xlabel('Key Length', fontsize=11, fontweight='bold')
        ax2.set_ylabel('TRR (%)', fontsize=11, fontweight='bold')
        ax2.set_title('Vigenère: TRR vs Key Length', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 105)
        
        # Add value labels
        for i, v in enumerate(trr_data.values):
            ax2.text(trr_data.index[i], v + 2, f'{v:.1f}%', ha='center', fontsize=9)
        
        plt.tight_layout()
        
        if save:
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved: {filepath}")
        
        plt.close()
    
    def plot_accuracy_comparison(self, caesar_df: pd.DataFrame, 
                                vigenere_df: pd.DataFrame,
                                save=True, filename='accuracy_comparison.png'):
        """
        Plot perbandingan akurasi (correct key found)
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Hitung akurasi per cipher
        ciphers = ['Caesar', 'Vigenère']
        accuracies = [
            caesar_df['correct_found'].sum() / len(caesar_df) * 100,
            vigenere_df['correct_found'].sum() / len(vigenere_df) * 100
        ]
        
        colors = ['steelblue', 'coral']
        bars = ax.bar(ciphers, accuracies, color=colors, alpha=0.8, 
                     edgecolor='black', width=0.6, linewidth=2)
        
        # Add value labels on bars
        for bar, acc in zip(bars, accuracies):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{acc:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
        ax.set_title('Heuristic-Guided Brute-Force: Accuracy Comparison',
                    fontsize=14, fontweight='bold')
        ax.set_ylim(0, 115)
        ax.grid(True, alpha=0.3, axis='y')
        
        if save:
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved: {filepath}")
        
        plt.close()
    
    def plot_heatmap_metrics(self, vigenere_df: pd.DataFrame,
                            save=True, filename='vigenere_metrics_heatmap.png'):
        """
        Plot heatmap metrik untuk Vigenère
        """
        # Pivot data
        pivot_ssrr = vigenere_df.pivot_table(
            values='search_space_reduction_rate',
            index='text_size',
            columns='key_length',
            aggfunc='mean'
        )
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(pivot_ssrr, annot=True, fmt='.1f', cmap='YlGnBu', ax=ax, 
                   cbar_kws={'label': 'SSRR (%)'}, linewidths=1, linecolor='gray')
        
        ax.set_title('Vigenère Cipher: SSRR Heatmap (Text Size vs Key Length)',
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('Key Length', fontsize=12, fontweight='bold')
        ax.set_ylabel('Text Size (characters)', fontsize=12, fontweight='bold')
        
        if save:
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved: {filepath}")
        
        plt.close()
    
    def plot_metrics_summary_table(self, caesar_df: pd.DataFrame,
                                   vigenere_df: pd.DataFrame,
                                   save=True, filename='metrics_summary.png'):
        """
        Plot tabel summary metrik
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        fig.suptitle('Cryptanalysis Metrics Summary', fontsize=16, fontweight='bold', y=0.98)
        
        # Caesar summary
        caesar_summary = caesar_df.groupby('text_size').agg({
            'search_space_reduction_rate': 'mean',
            'time_reduction_rate': 'mean',
            'efficiency_index': 'mean',
            'correct_found': lambda x: (x.sum() / len(x) * 100)
        }).round(2)
        caesar_summary.columns = ['SSRR (%)', 'TRR (%)', 'EI', 'Accuracy (%)']
        
        ax1.axis('tight')
        ax1.axis('off')
        table1 = ax1.table(cellText=caesar_summary.values,
                          colLabels=caesar_summary.columns,
                          rowLabels=[f'{size} chars' for size in caesar_summary.index],
                          cellLoc='center',
                          loc='center',
                          colWidths=[0.15, 0.15, 0.15, 0.15])
        table1.auto_set_font_size(False)
        table1.set_fontsize(10)
        table1.scale(1, 2)
        ax1.set_title('Caesar Cipher Metrics', fontsize=12, fontweight='bold', pad=20)
        
        # Vigenère summary
        vigenere_summary = vigenere_df.groupby('key_length').agg({
            'search_space_reduction_rate': 'mean',
            'time_reduction_rate': 'mean',
            'efficiency_index': 'mean',
            'correct_found': lambda x: (x.sum() / len(x) * 100)
        }).round(2)
        vigenere_summary.columns = ['SSRR (%)', 'TRR (%)', 'EI', 'Accuracy (%)']
        
        ax2.axis('tight')
        ax2.axis('off')
        table2 = ax2.table(cellText=vigenere_summary.values,
                          colLabels=vigenere_summary.columns,
                          rowLabels=[f'Length {key}' for key in vigenere_summary.index],
                          cellLoc='center',
                          loc='center',
                          colWidths=[0.15, 0.15, 0.15, 0.15])
        table2.auto_set_font_size(False)
        table2.set_fontsize(10)
        table2.scale(1, 2)
        ax2.set_title('Vigenère Cipher Metrics', fontsize=12, fontweight='bold', pad=20)
        
        if save:
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved: {filepath}")
        
        plt.close()
    
    def create_comprehensive_report(self, caesar_df: pd.DataFrame, 
                                   vigenere_df: pd.DataFrame):
        """
        Buat comprehensive visualization report
        """
        print("\nCreating comprehensive visualization report...")
        print("-" * 70)
        
        self.plot_ssrr_vs_text_size(caesar_df)
        self.plot_trr_vs_text_size(caesar_df)
        self.plot_efficiency_index(caesar_df, vigenere_df)
        self.plot_execution_time_comparison(caesar_df)
        self.plot_vigenere_key_length_analysis(vigenere_df)
        self.plot_accuracy_comparison(caesar_df, vigenere_df)
        self.plot_heatmap_metrics(vigenere_df)
        self.plot_metrics_summary_table(caesar_df, vigenere_df)
        
        print("-" * 70)
        print("Visualization report complete!")
        print(f"All graphs saved to: {self.output_dir}")


if __name__ == "__main__":
    # Sample data untuk testing
    sample_caesar = pd.DataFrame({
        'text_size': [50, 50, 100, 100, 200, 200],
        'search_space_reduction_rate': [80, 85, 78, 82, 76, 81],
        'time_reduction_rate': [75, 80, 70, 78, 65, 75],
        'efficiency_index': [0.94, 0.94, 0.90, 0.95, 0.86, 0.93],
        'time_without_heuristics': [1.5, 1.4, 2.2, 2.1, 4.5, 4.6],
        'time_with_heuristics': [0.38, 0.28, 0.66, 0.46, 1.58, 1.15],
        'correct_found': [True, True, True, True, True, True]
    })
    
    sample_vigenere = pd.DataFrame({
        'key_length': [3, 3, 4, 4, 5, 5],
        'text_size': [100, 100, 200, 200, 200, 200],
        'search_space_reduction_rate': [60, 65, 55, 60, 50, 55],
        'time_reduction_rate': [55, 60, 50, 55, 45, 50],
        'efficiency_index': [0.92, 0.92, 0.91, 0.92, 0.90, 0.91],
        'correct_found': [True, True, True, True, False, True]
    })
    
    visualizer = CryptoanalysisVisualizer()
    visualizer.create_comprehensive_report(sample_caesar, sample_vigenere)
