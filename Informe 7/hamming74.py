# Hamming (7,4) — Paridad PAR
# Posiciones (1-indexado): [1=P1, 2=P2, 3=d0, 4=P4, 5=d1, 6=d2, 7=d3]

def hamming74_encode(bits4):
    """
    bits4: lista [d3, d2, d1, d0] (MSB->LSB), enteros 0/1
    return: lista de 7 bits [P1, P2, d3, P4, d2, d1, d0]
    """
    assert len(bits4) == 4 and all(b in (0,1) for b in bits4)
    d3, d2, d1, d0 = bits4

    # Paridades (paridad par)
    P1 = d3 ^ d2 ^ d0              # cubre pos 1,3,5,7
    P2 = d3 ^ d1 ^ d0              # cubre pos 2,3,6,7
    P4 = d2 ^ d1 ^ d0              # cubre pos 4,5,6,7

    # Codeword: [P1, P2, d3, P4, d2, d1, d0]
    return [P1, P2, d3, P4, d2, d1, d0]

def hamming74_decode(code7):
    """
    code7: lista de 7 bits [P1, P2, d3, P4, d2, d1, d0]
    return: (data4_corr, syndrome, hubo_correccion, code7_corr)
      - data4_corr: [d3,d2,d1,d0] corregidos (MSB->LSB)
      - syndrome: 0 si sin error; 1..7 = posición (1-indexada) del bit errado
      - hubo_correccion: bool
      - code7_corr: código corregido (lista de 7 bits)
    """
    assert len(code7) == 7 and all(b in (0,1) for b in code7)
    c = code7[:]  # copia para poder corregir

    # Síndrome con paridad par (mismas coberturas que en la codificación)
    s1 = c[0] ^ c[2] ^ c[4] ^ c[6]   # chequeo P1: pos 1,3,5,7
    s2 = c[1] ^ c[2] ^ c[5] ^ c[6]   # chequeo P2: pos 2,3,6,7
    s4 = c[3] ^ c[4] ^ c[5] ^ c[6]   # chequeo P4: pos 4,5,6,7

    syndrome = s1 + (s2 << 1) + (s4 << 2)   # 0..7 (1-indexado)
    corrected = False
    if syndrome != 0:
        pos = syndrome - 1                  # a índice 0
        c[pos] ^= 1                         # corregir bit
        corrected = True

    # Extraer datos en el orden  [d3,d2,d1,d0]
    data4 = [c[2], c[4], c[5], c[6]]
    return data4, syndrome, corrected, c

