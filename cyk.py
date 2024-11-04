# Definisikan aturan produksi grammar dalam bentuk CNF
grammar = {
    'S': [('A', 'B'), ('B', 'C')],
    'A': [('B', 'A'), ('a',)],
    'B': [('C', 'C'), ('b',)],
    'C': [('A', 'B'), ('a',)]
}

# Fungsi untuk mengecek apakah simbol terminal dihasilkan oleh produksi grammar
def is_terminal(symbol, terminal):
    return (terminal,) in grammar.get(symbol, [])

# Fungsi untuk mencetak tabel parsing dengan header string input, header kolom, dan border
def print_table(table, n, string):
    print("\nTabel Parsing CYK:")
    # Mencetak header kolom (Posisi Awal Substring)
    header = "Length \\ Pos"
    for j in range(n):
        header += f"|{j+1:^10}"
    print(header)
    print("-" * (12 + (n * 11)))
    # Mencetak setiap baris dengan header panjang substring
    for length in range(1, n + 1):
        row = f"{length:^12}"
        for start in range(n):
            if start <= n - length:
                cell = "{" + ",".join(sorted(table[length - 1][start])) + "}"
                row += f"|{cell:^10}"
            else:
                row += "|          "
        print(row)
        print("-" * (12 + (n * 11)))
    # Mencetak string input di bawah tabel
    input_str = "Input Str   "
    for char in string:
        input_str += f"|{char:^10}"
    print(input_str)

# Fungsi utama CYK untuk mengecek apakah string dihasilkan oleh grammar
def cyk_parse(string):
    n = len(string)
    
    # Inisialisasi tabel untuk menyimpan hasil parsing
    table = [[set() for _ in range(n)] for _ in range(n)]
    
    # Isi tabel untuk simbol terminal (panjang substring = 1)
    print("Mengisi tabel untuk panjang substring 1 (simbol terminal):")
    for i in range(n):
        for head, productions in grammar.items():
            if is_terminal(head, string[i]):
                table[0][i].add(head)
        print(f"Isi tabel pada posisi [length=1, start={i+1}] untuk simbol '{string[i]}': {table[0][i]}")
    print_table(table, n, string)
    
    # Mengisi tabel untuk substring dengan panjang > 1
    for length in range(2, n + 1):       # Panjang substring
        print(f"\nMengisi tabel untuk panjang substring {length}:")
        for start in range(n - length + 1):  # Posisi awal substring
            for split in range(1, length):   # Posisi pembagian substring
                left_cell = table[split - 1][start]
                right_cell = table[length - split - 1][start + split]
                for head, productions in grammar.items():
                    for production in productions:
                        if len(production) == 2:
                            B, C = production
                            if B in left_cell and C in right_cell:
                                if head not in table[length - 1][start]:
                                    print(f"Menemukan {head} -> {B} {C} untuk posisi [length={length}, start={start+1}] (menggabungkan [length={split}, start={start+1}] dan [length={length - split}, start={start + split +1}])")
                                table[length - 1][start].add(head)
        print_table(table, n, string)
    
    # Cek apakah simbol awal (S) ada di posisi [n-1][0] (panjang substring n, start posisi 0)
    return 'S' in table[n - 1][0]

# Ambil input string dari pengguna
string = input("Masukkan string yang akan diuji: ")

# Panggil fungsi CYK dan tampilkan hasilnya
if cyk_parse(string):
    print(f"\nString '{string}' dapat dihasilkan oleh grammar.")
else:
    print(f"\nString '{string}' TIDAK dapat dihasilkan oleh grammar.")
