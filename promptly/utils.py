def numeric_options(options):

    max = len(options) + 1
    numbers = range(1, max)
    # call to list if for python 3
    return list(zip(numbers, options))

