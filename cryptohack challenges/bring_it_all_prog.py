def decrypt(k, ct):

    rk = expand_key(k)
    
    s = bytes2matrix(ct)
    
    add_round_key(s, rk[N_ROUNDS])
    for i in range(N_ROUNDS - 1, 0, -1):
        inv_shift_rows(s)
        sub_bytes(s, inv_s_box)
        add_round_key(s, rk[i])
        inv_mix_columns(s)

    
    inv_shift_rows(s)
    sub_bytes(s, inv_s_box)
    add_round_key(s, rk[0])
    
    pt = matrix2bytes(s)
    return pt

print(decrypt(k, ct))

# It expands the key into round key and converts the cipher-text into a matrix. It goes through number of rounds and after processing all the rounds, then it generates
# the plain text