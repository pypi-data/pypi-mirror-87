REVERSETRANS = str.maketrans("ACTGNactgn-", "TGACNtgacn-")


def revcomp(s):
    """
    return reverse complement of a sequence.
    """
    # define the dic out side is much faster.    
    # comp = map(lambda x: REVSECOMPDICT[x], s[::-1]) # slightly slower
    return s.translate(REVERSETRANS)[::-1]


# def lev_distance(s1, s2, threshold=1000):
#     """
#     calculate lev_distance of s1 and s2.
#     use threshold to calculate diagonally.stop at threshold. fastest.
#     """
#     if len(s1) > len(s2):
#         s1, s2 = s2, s1
#     l1 = len(s1)
#     vertical = [0]
#     horizontal = [0]
#     for i in range(l1):
#         char1 = s1[i]
#         char2 = s2[i]
#         newvertical = [i+1]
#         newhorizontal = [i+1]
#         for k in range(i):
#             if char1 == s2[k]:
#                 newvertical.append(vertical[k])
#             else:
#                 newvertical.append(
#                     1+min(newvertical[-1], vertical[k], vertical[k+1]))
#             if char2 == s1[k]:
#                 newhorizontal.append(horizontal[k])
#             else:
#                 newhorizontal.append(
#                     1+min(newhorizontal[-1], horizontal[k], horizontal[k+1]))
#         last = vertical[-1] if char1 == char2 else (
#             1+min(newvertical[-1], newhorizontal[-1], vertical[-1]))
#         newhorizontal.append(last)
#         newvertical.append(last)
#         currentmin = min(min(newhorizontal), min(newvertical))
#         if currentmin > threshold:
#             return currentmin
#         vertical, horizontal = newvertical, newhorizontal
#     horizontal.append(last)
#     for index2, char2 in enumerate(s2[l1:]):
#         newhorizontal = [index2+l1+1]
#         for index1, char1 in enumerate(s1):
#             if char1 == char2:
#                 newhorizontal.append(horizontal[index1])
#             else:
#                 newhorizontal.append(1 + min((horizontal[index1],
#                                               horizontal[index1 + 1],
#                                               newhorizontal[-1])))
#         currentmin = min(newhorizontal)
#         if currentmin > threshold:
#             return currentmin
#         horizontal = newhorizontal
#     return horizontal[-1]
