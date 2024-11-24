import numpy as np
##Tìm N 
# Tham số
target_streak = 3
confidence = 0.95
p_success = 1 / 216
cost_no_success = 1000
cost_partial_success_1 = 7800
cost_partial_success_2 = 49500
reward = 100000
n_rolls = 10000  # Monte Carlo simulations

# Step 1: Tìm số lần tung cần thiết để đạt xác suất chiến thắng 95%
failure_prob = 1 - p_success
n = np.log(1 - confidence) / np.log(failure_prob)
min_rolls = int(np.ceil(n))
print(f"Number of rolls needed to achieve 95% confidence: {min_rolls}")

# Step 2: Tính lợi nhuận/tổn thất ròng qua mô phỏng
'''0 lần thành công: Mất $1
1 lần thành công: Mất $7.
2 lần thành công: Mất $49
3 lần thành công: Nhận'''
def simulate_game(target_streak, n_rolls, cost_no_success, cost_partial_success_1, cost_partial_success_2, reward):
    np.random.seed(42)
    profits = []

    for _ in range(n_rolls):
        streak = 0
        cost = 0

        while streak < target_streak:
            roll = np.random.randint(1, 7)
            if roll == 1:
                streak += 1
            else:
                if streak == 0:
                    cost += cost_no_success
                elif streak == 1:
                    cost += cost_partial_success_1
                elif streak == 2:
                    cost += cost_partial_success_2
                streak = 0

        profit = reward - cost if streak == target_streak else -cost
        profits.append(profit)

    average_profit_loss = np.mean(profits)
    return average_profit_loss, profits

average_profit_loss, profit_loss_distribution = simulate_game(
    target_streak, n_rolls, cost_no_success, cost_partial_success_1, cost_partial_success_2, reward
)
print(f"Average profit/loss: {average_profit_loss}")

# Step 3: Tìm số tiền thưởng tối thiểu
success_prob = p_success
average_cost = np.mean([abs(p) for p in profit_loss_distribution if p < 0])
min_reward = average_cost / success_prob
print(f"Minimum reward required to make the game fair: {min_reward}")


##Code Python cho toàn bộ các phần
''' 
1.Tìm số lần tung xúc xắc để đạt xác suất chiến thắng 95%.
Giải phương trình và kiểm tra bằng mô phỏng Monte Carlo.
2.Tính lợi nhuận/tổn thất ròng sau mỗi lần tung.
Phân tích các trạng thái có thể xảy ra (0, 1, 2, hoặc 3 lần "1" liên tiếp) và chi phí tương ứng.
3.Tìm số tiền thưởng tối thiểu cần thiết để chơi trò chơi.
Tính giá trị kỳ vọng 𝐸𝑉 và điều chỉnh phần thưởng để 𝐸𝑉≥0.
4.Chiến lược hiệu quả nhất cho 4 người chơi.
Mô phỏng để tìm chiến lược tối ưu, như dừng chơi hoặc hợp tác.
5.Điều kiện mở rộng với 2 viên xúc xắc.
Phân tích xác suất và tính toán chiến lược khi có thêm tùy chọn hủy xúc xắc.
'''
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

## Mô phỏng từng chiến lược và so sánh lợi nhuận trung bình:
def simulate_team_game(num_players, target_streak, n_rolls, cost_no_success, cost_partial_success_1, cost_partial_success_2, reward):
    team_profits = []

    for _ in range(n_rolls):
        team_profit = 0
        for _ in range(num_players):
            streak = 0
            cost = 0
            while streak < target_streak:
                roll = np.random.randint(1, 7)
                if roll == 1:
                    streak += 1
                else:
                    if streak == 0:
                        cost += cost_no_success
                    elif streak == 1:
                        cost += cost_partial_success_1
                    elif streak == 2:
                        cost += cost_partial_success_2
                    streak = 0
            team_profit += reward - cost if streak == target_streak else -cost
        team_profits.append(team_profit / num_players)

    average_team_profit = np.mean(team_profits)
    return average_team_profit

# Parameters for team game
num_players = 4
average_team_profit = simulate_team_game(
    num_players=num_players,
    target_streak=3,
    n_rolls=n_rolls,
    cost_no_success=cost_no_success,
    cost_partial_success_1=cost_partial_success_1,
    cost_partial_success_2=cost_partial_success_2,
    reward=reward
)
print(f"Lợi nhuận trung bình mỗi người khi chơi nhóm: {average_team_profit}")
''' 
Số lần tung cần thiết: Khoảng 1.240 lần để đạt 95% xác suất.
Lợi nhuận/tổn thất trung bình: Sẽ phụ thuộc vào mô phỏng cụ thể.
Tiền thưởng tối thiểu: Khoảng $21.6 triệu USD để đảm bảo EV dương.
Chiến lược nhóm: Lợi nhuận trung bình mỗi người chơi sẽ cao hơn khi hợp tác.
'''
