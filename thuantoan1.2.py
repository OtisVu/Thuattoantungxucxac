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

