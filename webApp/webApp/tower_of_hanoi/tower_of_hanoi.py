LINEBREAK = '\n'
ansList = ['']
tower1 = ([], 'Tower 1')
tower2 = ([], 'Tower 2')
tower3 = ([], 'Tower 3')


def init_towers(n: int) -> None:
    """
    Given number of disks <n>, initialize the 3 towers as lists.
    """
    global tower1
    global tower2
    global tower3
    for i in range(n, 0, -1):
        tower1[0].append(i)
    tower2 = ([], 'Tower 2')
    tower3 = ([], 'Tower 3')


def move(n: int, origin: tuple[list[int], str],
         destination: tuple[list[int], str], temp: tuple[list[int], str],
         original_n) -> None:
    if n == 1:
        destination[0].append(origin[0].pop())
        ansList[0] += f'Move disk from {origin[1]} to {destination[1]}{LINEBREAK}'
        ansList[0] += format_towers(original_n) + 2 * LINEBREAK
        return
    move(n - 1, origin, temp, destination, original_n)
    move(1, origin, destination, origin, original_n)
    move(n - 1, temp, destination, origin, original_n)


def hanoi(n: int) -> str:
    global tower1
    global tower2
    global tower3
    global ansList
    ansList[0] = ''
    init_towers(n)
    ansList[0] += 'Starting Position: ' + LINEBREAK + format_towers(n) + LINEBREAK
    move(n, tower1, tower3, tower2, n)
    return ansList[0]


def format_towers(n) -> str:
    global tower1
    global tower2
    global tower3
    ans = ''
    for i in range(n - 1, -1, -1):
        if i < len(tower1[0]):
            ans += ' ' * (n - tower1[0][i]) + str(tower1[0][i]) * tower1[0][i] + '|' + str(tower1[0][i]) * tower1[0][i] + ' ' * (n - tower1[0][i]) + ' ' * 2
        else:
            ans += ' ' * n + '|' + ' ' * n + ' ' * 2

        if i < len(tower2[0]):
            ans += ' ' * (n - tower2[0][i]) + str(tower2[0][i]) * tower2[0][i] + '|' + str(tower2[0][i]) * tower2[0][i] + ' ' * (n - tower2[0][i]) + ' ' * 2
        else:
            ans += ' ' * n + '|' + ' ' * n + ' ' * 2

        if i < len(tower3[0]):
            ans += ' ' * (n - tower3[0][i]) + str(tower3[0][i]) * tower3[0][i] + '|' + str(tower3[0][i]) * tower3[0][i] + ' ' * (n - tower3[0][i])
        else:
            ans += ' ' * n + '|' + ' ' * n

        ans += LINEBREAK
    return ans
