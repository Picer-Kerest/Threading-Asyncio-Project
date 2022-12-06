
def read_ints(path):
    lst = []
    with open(path, 'r') as f:
        while line := f.readline():
            lst.append(int(line))
    return lst


def count_three_sum(ints):
    print(f'started count_three_sum in')

    n = len(ints)
    counter = 0

    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                if ints[i] + ints[j] + ints[k] == 0:
                    counter += 1
                    print(f'Triple found in: {ints[i]}, {ints[j]}, {ints[k]}', end='\n')

    print(f'ended count_three_sum in. Triplets counter= {counter}')
    return counter


if __name__ == '__main__':
    print('started main')

    ints = read_ints('../data/1Kints.txt')
    count_three_sum(ints)

    print('What are you waiting for?')
    print('ended main')
