import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Tham số
confidence = 0.95
p_success = 1 / 12  # Probability of getting 11, 16 or 66

# Tìm n
failure_prob = 1 - p_success
n = np.log(1 - confidence) / np.log(failure_prob)
min_rolls = int(np.ceil(n))
print(f"So lan tung can thiet de dat xac suat chien thang 95%: {min_rolls}")

# Tính lợi nhuận / tổn thất qau mô phỏng 
''' 
Không thành công: Mất $1.000.
1 lần thành công và thất bại: Mất $7.800.
2 lần thành công và thất bại: Mất $49.500.
3 lần thành công: Nhận thưởng 3 triệu USD
'''
def simulate_game_2_dice(target_streak, n_rolls, cost_no_success, cost_partial_success_1, cost_partial_success_2, reward):
    np.random.seed(42)
    profits = []

    for _ in range(n_rolls):
        streak = 0
        cost = 0

        while streak < target_streak:
            roll = np.random.randint(1, 7), np.random.randint(1, 7)  # Simulate rolling two dice
            if roll == (1, 1) or roll == (1, 6) or roll == (6, 1) or roll == (6, 6):
                streak += 1
            else:
                if streak == 0:
                    cost += cost_no_success
                elif streak == 1:
                    cost += cost_partial_success_1
                elif streak == 2:
                    cost += cost_partial_success_2
                streak = 0  # Reset streak after failure

        profit = reward - cost if streak == target_streak else -cost
        profits.append(profit)

    average_profit_loss = np.mean(profits)
    return average_profit_loss, profits

# Parameters
n_rolls = 10000
cost_no_success = 1000
cost_partial_success_1 = 7800
cost_partial_success_2 = 49500
reward = 3000000

average_profit_loss, profit_loss_distribution = simulate_game_2_dice(
    target_streak=3,
    n_rolls=n_rolls,
    cost_no_success=cost_no_success,
    cost_partial_success_1=cost_partial_success_1,
    cost_partial_success_2=cost_partial_success_2,
    reward=reward
)

print(f"Lợi nhuận trung bình: {average_profit_loss}")


## Tính số tiền thưởng tối thiểu
# Calculate minimum reward
success_prob = p_success
average_cost = np.mean([abs(p) for p in profit_loss_distribution if p < 0])
min_reward = average_cost / success_prob

print(f"Số tiền thưởng tối thiểu để chơi: {min_reward}")

##Chiến lược hiệu quả nhất khi có 4 người chơi cùng lúc
def simulate_team_game_2_dice(num_players, target_streak, n_rolls, cost_no_success, cost_partial_success_1, cost_partial_success_2, reward):
    team_profits = []

    for _ in range(n_rolls):
        team_profit = 0
        for _ in range(num_players):
            streak = 0
            cost = 0
            while streak < target_streak:
                roll = np.random.randint(1, 7), np.random.randint(1, 7)
                if roll == (1, 1) or roll == (1, 6) or roll == (6, 1) or roll == (6, 6):
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
average_team_profit = simulate_team_game_2_dice(
    num_players=num_players,
    target_streak=3,
    n_rolls=n_rolls,
    cost_no_success=cost_no_success,s
    cost_partial_success_1=cost_partial_success_1,
    cost_partial_success_2=cost_partial_success_2,
    reward=reward
)

print(f"Lợi nhuận trung bình mỗi người khi chơi nhóm: {average_team_profit}")

