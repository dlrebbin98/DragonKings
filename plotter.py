import matplotlib.pyplot as plt

with open('size_1000.txt', 'r') as f:
    data = f.readlines()
    for i in range(len(data)):
        data[i] = data[i].split(',')
        data[i][1] = float(data[i][1].strip('\n'))
    # plt.xlim(0, 1)
    plt.plot([float(row[0]) for row in data], [row[1] for row in data])
    plt.xlabel('epsilon')
    plt.ylabel('failure size')
    plt.title('Failure size vs epsilon')
    plt.xscale('log')
    plt.savefig('results.png')
    # plot on log scale
