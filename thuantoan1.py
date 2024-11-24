import numpy as np

def calculate_rolls_to_confidence(target_streak=3, confidence=0.95, p_success=1/216):
    """
    Calculate the number of rolls needed to reach the desired confidence level of winning.

    Parameters:
    - target_streak: Number of consecutive successes needed.
    - confidence: Desired confidence level (e.g., 0.95).
    - p_success: Probability of success in a single roll.

    Returns:
    - n: Minimum number of rolls needed.
    """
    # Solve for n in: 1 - (1 - p_success)^n >= confidence
    failure_prob = 1 - p_success
    n = np.log(1 - confidence) / np.log(failure_prob)
    return int(np.ceil(n))


def calculate_profit_loss_distribution(target_streak=3, n_rolls=1000, 
                                       cost_no_success=1000, 
                                       cost_partial_success_1=7800, 
                                       cost_partial_success_2=49500, reward=100000):
    """
    Simulate profit/loss for each roll distribution in the game.

    Parameters:
    - target_streak: Number of consecutive successes needed to win.
    - n_rolls: Number of simulations to perform.
    - cost_no_success: Cost per roll with no success.
    - cost_partial_success_1: Cost for achieving 1 success and failing.
    - cost_partial_success_2: Cost for achieving 2 successes and failing.
    - reward: Reward for achieving the target streak.

    Returns:
    - average_profit_loss: Average profit/loss over all simulations.
    - detailed_results: List of individual profits/losses.
    """
    np.random.seed(42)  # For reproducibility
    profits = []

    for _ in range(n_rolls):
        streak = 0
        cost = 0

        while streak < target_streak:
            roll = np.random.randint(1, 7)  # Simulate dice roll (1 to 6)
            if roll == 1:
                streak += 1
            else:
                if streak == 0:
                    cost += cost_no_success
                elif streak == 1:
                    cost += cost_partial_success_1
                elif streak == 2:
                    cost += cost_partial_success_2
                streak = 0  # Reset streak after failure

        # Calculate profit or loss for this game
        profit = reward - cost if streak == target_streak else -cost
        profits.append(profit)

    # Average profit/loss across all simulations
    average_profit_loss = np.mean(profits)
    return average_profit_loss, profits


# Part 1: Calculate number of rolls for 95% confidence
target_streak = 3
confidence = 0.95
p_success = 1 / 216
min_rolls = calculate_rolls_to_confidence(target_streak, confidence, p_success)

# Part 2: Calculate profit/loss distribution
average_profit_loss, profit_loss_distribution = calculate_profit_loss_distribution(
    target_streak=target_streak,
    n_rolls=10000,  # Number of Monte Carlo simulations
    cost_no_success=1000,
    cost_partial_success_1=7800,
    cost_partial_success_2=49500,
    reward=100000
)

min_rolls, average_profit_loss
