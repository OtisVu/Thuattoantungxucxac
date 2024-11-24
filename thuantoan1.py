#Tung xúc xắc với 1 viên để đạt xác suất 95%
import numpy as np
def simulate_single_dice_optimized(target_streak=3, confidence=0.95, simulations=10000):
    """
    Optimized simulation to determine the minimum number of rolls needed
    to achieve the target streak with a given confidence level.
    
    Parameters:
    - target_streak: Number of consecutive "1" rolls needed.
    - confidence: Desired confidence level (e.g., 0.95).
    - simulations: Number of Monte Carlo simulations.
    
    Returns:
    - min_rolls: Minimum number of rolls needed to achieve the confidence level.
    """
    np.random.seed(42)  # For reproducibility
    results = []

    for _ in range(simulations):
        streak = 0
        rolls = 0

        while streak < target_streak:
            rolls += 1
            roll = np.random.randint(1, 7)  # Simulate a dice roll (1 to 6)
            if roll == 1:
                streak += 1
            else:
                streak = 0

        results.append(rolls)

    # Convert results to a sorted array for fast percentile calculation
    results = np.sort(results)
    # Determine the minimum number of rolls needed to achieve the desired confidence level
    threshold_index = int(confidence * len(results)) - 1
    min_rolls = results[threshold_index]

    return int(min_rolls), results

# Run the optimized simulation
min_rolls_optimized, roll_distribution_optimized = simulate_single_dice_optimized()

min_rolls_optimized

'''
=>Theo mô phỏng tối ưu hóa, bạn cần tối thiểu 771 lần tung xúc xắc để đạt được xác suất chiến thắng 95% khi yêu cầu chuỗi 3 lần tung "1" liên tiếp với 1 viên xúc xắc.
'''