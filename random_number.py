from matplotlib import pyplot as plt
def main():
    init_number = 131
    a = 7 ** 5
    c = 0
    m1 = 2 ** 31
    m2 = 2 ** 31 - 1
    result1 = init_number
    result2 = init_number
    list1 = []
    list2 = []
    for _ in range(100000):
        result1 = (a * result1 + c) % m1
        result2 = (a * result2 + c) % m2
        list1.append(result1)
        list2.append(result2)
        print(result1, result2)
    plt.figure()
    ax1 = plt.subplot(121)
    ax2 = plt.subplot(122)
    ax1.hist(list1,bins=1000, density=1)
    ax2.hist(list2,bins=1000, density=1)
    plt.show()
if __name__ == '__main__':
    main()
