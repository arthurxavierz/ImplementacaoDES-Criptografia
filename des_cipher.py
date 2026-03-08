import os
import sys

# Permutação Inicial (IP)
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17,  9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7,
]

# Permutação Inicial Inversa (IP^-1)
IP_INV = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41,  9, 49, 17, 57, 25,
]

# Permutação de Expansão E (32 → 48 bits)
E = [
    32,  1,  2,  3,  4,  5,
     4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1,
]

# Permutação P
P = [
    16,  7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26,  5, 18, 31, 10,
     2,  8, 24, 14, 32, 27,  3,  9,
    19, 13, 30,  6, 22, 11,  4, 25,
]

# Permutação de Paridade PC-1
PC1 = [
    57, 49, 41, 33, 25, 17,  9,
     1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4,
]

# Permutação de Compressão PC-2
PC2 = [
    14, 17, 11, 24,  1,  5,
     3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8,
    16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32,
]

# Número de rotações por rodada
SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# S-Boxes (8 caixas de substituição)
S_BOXES = [
    # S1
    [
        [14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
        [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
        [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
        [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13],
    ],
    # S2
    [
        [15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
        [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
        [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
        [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9],
    ],
    # S3
    [
        [10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
        [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
        [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
        [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12],
    ],
    # S4
    [
        [ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
        [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
        [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
        [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14],
    ],
    # S5
    [
        [ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
        [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
        [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
        [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3],
    ],
    # S6
    [
        [12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
        [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
        [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
        [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13],
    ],
    # S7
    [
        [ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
        [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
        [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
        [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12],
    ],
    # S8
    [
        [13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
        [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
        [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
        [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11],
    ],
]

# ─────────────────────────────────────────────
# FUNÇÕES UTILITÁRIAS
# ─────────────────────────────────────────────

def bytes_to_bits(data: bytes) -> list:
    """Converte bytes para lista de bits."""
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

def bits_to_bytes(bits: list) -> bytes:
    """Converte lista de bits para bytes."""
    result = []
    for i in range(0, len(bits), 8):
        byte = 0
        for bit in bits[i:i+8]:
            byte = (byte << 1) | bit
        result.append(byte)
    return bytes(result)

def permute(block: list, table: list) -> list:
    """Aplica uma permutação usando a tabela fornecida."""
    return [block[t - 1] for t in table]

def xor(a: list, b: list) -> list:
    """XOR bit a bit entre duas listas."""
    return [x ^ y for x, y in zip(a, b)]

def left_shift(bits: list, n: int) -> list:
    """Rotação circular para a esquerda."""
    return bits[n:] + bits[:n]

# ─────────────────────────────────────────────
# GERAÇÃO DAS SUBCHAVES (Key Schedule)
# ─────────────────────────────────────────────

def generate_subkeys(key: bytes) -> list:
    """Gera as 16 subchaves de 48 bits a partir da chave de 64 bits."""
    key_bits = bytes_to_bits(key)
    key_56 = permute(key_bits, PC1)          # 64 → 56 bits
    C, D = key_56[:28], key_56[28:]          # Divide em duas metades
    subkeys = []
    for shift in SHIFTS:
        C = left_shift(C, shift)
        D = left_shift(D, shift)
        subkey = permute(C + D, PC2)         # 56 → 48 bits
        subkeys.append(subkey)
    return subkeys

# ─────────────────────────────────────────────
# FUNÇÃO F (núcleo do DES)
# ─────────────────────────────────────────────

def f_function(R: list, subkey: list) -> list:
    """Função F: expansão → XOR com subchave → S-Boxes → permutação P."""
    R_expanded = permute(R, E)               # 32 → 48 bits
    xored = xor(R_expanded, subkey)          # XOR com subchave

    # S-Boxes: 48 → 32 bits
    output = []
    for i in range(8):
        chunk = xored[i*6:(i+1)*6]
        row = (chunk[0] << 1) | chunk[5]    # Bits 1 e 6 = linha
        col = (chunk[1] << 3) | (chunk[2] << 2) | (chunk[3] << 1) | chunk[4]  # Bits 2-5 = coluna
        val = S_BOXES[i][row][col]
        for j in range(3, -1, -1):
            output.append((val >> j) & 1)

    return permute(output, P)

# ─────────────────────────────────────────────
# CIFRAGEM / DECIFRAGEM DE UM BLOCO (64 bits)
# ─────────────────────────────────────────────

def des_block(block: bytes, subkeys: list) -> bytes:
    """Cifra ou decifra um bloco de 8 bytes com as subchaves fornecidas."""
    bits = bytes_to_bits(block)
    bits = permute(bits, IP)                 # Permutação inicial
    L, R = bits[:32], bits[32:]

    for i in range(16):                      # 16 rodadas de Feistel
        L, R = R, xor(L, f_function(R, subkeys[i]))

    combined = permute(R + L, IP_INV)        # Permutação final (note R+L)
    return bits_to_bytes(combined)

# ─────────────────────────────────────────────
# PADDING PKCS#7
# ─────────────────────────────────────────────

def pkcs7_pad(data: bytes, block_size: int = 8) -> bytes:
    """Adiciona padding PKCS#7 para completar o último bloco."""
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)

def pkcs7_unpad(data: bytes) -> bytes:
    """Remove o padding PKCS#7 após a decifragem."""
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 8:
        raise ValueError("Padding inválido — chave incorreta ou arquivo corrompido.")
    return data[:-pad_len]

# ─────────────────────────────────────────────
# CIFRAGEM / DECIFRAGEM DE ARQUIVO COMPLETO
# ─────────────────────────────────────────────

def prepare_key(key_str: str) -> bytes:
    """Prepara a chave: converte string para 8 bytes (64 bits)."""
    key_bytes = key_str.encode('utf-8')
    if len(key_bytes) < 8:
        key_bytes = key_bytes.ljust(8, b'\x00')   # Preenche com zeros se curta
    return key_bytes[:8]                            # Trunca para 8 bytes

def encrypt_file(input_path: str, output_path: str, key_str: str):
    """Cifra um arquivo binário usando DES."""
    key = prepare_key(key_str)
    subkeys = generate_subkeys(key)

    with open(input_path, 'rb') as f:
        data = f.read()

    padded = pkcs7_pad(data)

    encrypted = bytearray()
    total = len(padded) // 8
    for i, block_idx in enumerate(range(0, len(padded), 8)):
        block = padded[block_idx:block_idx + 8]
        encrypted += des_block(block, subkeys)
        print(f"\r  Cifrando... {i+1}/{total} blocos", end='')

    print()
    with open(output_path, 'wb') as f:
        f.write(bytes(encrypted))

    print(f"  ✅ Arquivo cifrado salvo em: {output_path}")

def decrypt_file(input_path: str, output_path: str, key_str: str):
    """Decifra um arquivo binário usando DES."""
    key = prepare_key(key_str)
    subkeys = generate_subkeys(key)
    subkeys_reversed = subkeys[::-1]         # Inverte a ordem das subchaves

    with open(input_path, 'rb') as f:
        data = f.read()

    if len(data) % 8 != 0:
        raise ValueError("Arquivo cifrado corrompido (tamanho inválido).")

    decrypted = bytearray()
    total = len(data) // 8
    for i, block_idx in enumerate(range(0, len(data), 8)):
        block = data[block_idx:block_idx + 8]
        decrypted += des_block(block, subkeys_reversed)
        print(f"\r  Decifrando... {i+1}/{total} blocos", end='')

    print()
    unpadded = pkcs7_unpad(bytes(decrypted))

    with open(output_path, 'wb') as f:
        f.write(unpadded)

    print(f"  ✅ Arquivo decifrado salvo em: {output_path}")

# ─────────────────────────────────────────────
# INTERFACE DE LINHA DE COMANDO
# ─────────────────────────────────────────────

def menu():
    print("=" * 50)
    print("   🔐 DES - Cifragem de Arquivos Binários")
    print("=" * 50)
    print("  [1] Cifrar arquivo")
    print("  [2] Decifrar arquivo")
    print("  [0] Sair")
    print("=" * 50)
    return input("  Escolha uma opção: ").strip()

def main():
    while True:
        opcao = menu()

        if opcao == "1":
            entrada = input("\n  Caminho do arquivo de entrada: ").strip().strip('"')
            if not os.path.exists(entrada):
                print("  ❌ Arquivo não encontrado!")
                continue
            saida = input("  Caminho do arquivo cifrado (saída): ").strip().strip('"')
            chave = input("  Chave (qualquer texto, até 8 chars): ").strip()
            print()
            encrypt_file(entrada, saida, chave)

        elif opcao == "2":
            entrada = input("\n  Caminho do arquivo cifrado: ").strip().strip('"')
            if not os.path.exists(entrada):
                print("  ❌ Arquivo não encontrado!")
                continue
            saida = input("  Caminho do arquivo decifrado (saída): ").strip().strip('"')
            chave = input("  Chave usada na cifragem: ").strip()
            print()
            try:
                decrypt_file(entrada, saida, chave)
            except ValueError as e:
                print(f"  ❌ Erro: {e}")

        elif opcao == "0":
            print("\n  Até logo! 👋\n")
            break
        else:
            print("  ❌ Opção inválida.")

        print()

if __name__ == "__main__":
    main()