"""
Metrics Calculation
Perhitungan metrik evaluasi untuk cryptanalysis
"""

class MetricsCalculator:
    """
    Calculator untuk metrik evaluasi cryptanalysis
    """
    
    @staticmethod
    def calculate_search_space_reduction_rate(total_keyspace, search_space_reduced):
        """
        SSRR = (Total Keyspace - Reduced) / Total Keyspace × 100%
        """
        if total_keyspace == 0:
            return 0
        ssrr = (total_keyspace - search_space_reduced) / total_keyspace * 100
        return min(100, max(0, ssrr))
    
    @staticmethod
    def calculate_time_reduction_rate(time_without_heuristics, time_with_heuristics):
        """
        TRR = (Time Without H - Time With H) / Time Without H × 100%
        """
        if time_without_heuristics == 0:
            return 0
        trr = (time_without_heuristics - time_with_heuristics) / time_without_heuristics * 100
        return min(100, max(0, trr))
    
    @staticmethod
    def calculate_accuracy_rate(correct_predictions, total_predictions):
        """
        Accuracy = Correct / Total × 100%
        """
        if total_predictions == 0:
            return 0
        return (correct_predictions / total_predictions) * 100
    
    @staticmethod
    def calculate_efficiency_index(time_reduction_rate, search_space_reduction_rate):
        """
        EI = TRR / SSRR
        """
        if search_space_reduction_rate == 0:
            return 0
        return time_reduction_rate / search_space_reduction_rate
    
    @staticmethod
    def calculate_false_positive_rate(false_positives, total_negatives):
        """
        FPR = False Positives / Total Negatives × 100%
        """
        if total_negatives == 0:
            return 0
        return (false_positives / total_negatives) * 100


if __name__ == "__main__":
    ssrr = MetricsCalculator.calculate_search_space_reduction_rate(26, 5)
    trr = MetricsCalculator.calculate_time_reduction_rate(2.0, 0.5)
    ei = MetricsCalculator.calculate_efficiency_index(trr, ssrr)
    print(f"SSRR: {ssrr:.2f}%")
    print(f"TRR: {trr:.2f}%")
    print(f"EI: {ei:.4f}")
