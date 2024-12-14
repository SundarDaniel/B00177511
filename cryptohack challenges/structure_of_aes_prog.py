def matrix2bytes(matrix):
    """ Converts a 4x4 matrix into a 16-byte array.  """
    a = [chr(i) for j in matrix for i in j]
    flag = ""
    for i in a:
        flag += i
    return flag

# The function takes 4x4 matrix as input then it flattens matrix by iterating through each row & element within row.
# it converts it into a byte for each element then it concatenates all these bytes into a single string.
# The function returns final byte string.