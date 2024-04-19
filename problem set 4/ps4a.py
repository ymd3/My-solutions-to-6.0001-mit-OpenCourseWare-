# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    if len(sequence) == 1:
        return [sequence]
    if len(sequence) > 1:
        b = sequence[1:]
        b = list(b)
        for perms in get_permutations(''.join(b)):
            x = list(perms)   #['a']

            for num in range(len(x) + 1):          #len(x) = 1      0,1
                y = x[:]                    #['a']
                y.insert(num,sequence[0])
                b.append(''.join(y))
                for perm in b:
                    if len(perm) < len(sequence):
                        b.remove(perm)
                    if b.count(perm) > 1:
                        b.remove(perm)
        return b




if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a
#    sequence of length n)

    print(get_permutations('aeiou'))

