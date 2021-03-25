# This is an implementation of a "monobound binary search" from
# https://github.com/scandum/binary_search/blob/master/binary_search.c#L195-L226
def binsearch(arr: list, key: int):
    bot = 0
    top = len(arr)

    while top > 1:
        mid = top // 2
        if key >= arr[bot + mid]:
            bot += mid
        top -= mid

    return bot
