from scipy.special import comb
import numpy as np


def prob():
    return np.sum(np.array([comb(35, i) * (0.1 ** i) * (0.9 ** (35 - i)) for i in np.arange(11, 36)]))


def test_conflict():
    random_array = np.random.random(size=(35,))
    for i in range(35):
        random_num = random_array[i]
        flag = False
        bound = random_num + 0.1
        total_sum = 0
        if bound > 1:
            bound -= 1
            flag = True
        for j in range(35):
            if j == i:
                continue
            if flag:
                total_sum += 1 if random_array[j] < bound or random_array[j] > random_num else 0
            else:
                total_sum += 1 if random_array[j] > random_num and random_array[j] < bound else 0
        if total_sum > 8:
            return True

    return False


def main():
    total_sum = 0
    for i in range(1000000):
        total_sum += 1 if test_conflict() else 0
        print(total_sum / (i + 1))


if __name__ == "__main__":
    print(prob())