# Dokumentasi Teori - Cryptanalysis

## 1. Caesar Cipher

### Definisi
Caesar cipher adalah cipher substitusi monoalfabetik paling sederhana yang menggeser setiap huruf dalam plaintext sebesar n posisi tetap dalam alfabet.

### Formula Enkripsi
```
C = (P + K) mod 26
```
Dimana:
- C = Ciphertext
- P = Plaintext (0-25 untuk A-Z)
- K = Key (shift)

### Ruang Kunci
- Total: 26 kemungkinan
- Praktis: 25 kemungkinan (shift 1-25)

### Kelemahan
1. Ruang kunci sangat kecil → rentan brute-force
2. Pola frekuensi huruf sama dengan plaintext
3. Tidak ada diffusion atau confusion
4. Mudah dipecahkan dengan frequency analysis

## 2. Vigenère Cipher

### Definisi
Vigenère cipher adalah cipher substitusi polialfabetik yang menggunakan kunci berulang untuk mengenkripsi plaintext.

### Formula Enkripsi
```
C_i = (P_i + K_i) mod 26
```
Dimana:
- C_i = Ciphertext character ke-i
- P_i = Plaintext character ke-i
- K_i = Key character ke-i (diulang)

### Ruang Kunci
```
Total Keys = 26^n
```
Dimana n = panjang kunci

## 3. Heuristik dalam Cryptanalysis

### 1. Frequency Analysis Heuristic (EFAH)
```
Score = 100 - (Chi-Square × 2)
```
Menggunakan distribusi frekuensi huruf bahasa Inggris.

### 2. Chi-Square Statistical Heuristic (CSTTH)
```
χ² = Σ[(Observed - Expected)² / Expected]
```

### 3. Entropy-Based Heuristic (EBH)
```
H = -Σ(p_i × log₂(p_i))
Score = 100 - (H × 10)
```

### 4. Dictionary-Based Heuristic (DBH)
```
Score = (Matching Words / Total Words) × 100%
```

### 5. N-gram Analysis Heuristic (NAH)
```
Score = (Matching N-grams / Total N-grams) × 100%
```

## Metrik Evaluasi

### SSRR (Search Space Reduction Rate)
```
SSRR = (Total Keyspace - Reduced) / Total Keyspace × 100%
```

### TRR (Time Reduction Rate)
```
TRR = (Time Without H - Time With H) / Time Without H × 100%
```

### EI (Efficiency Index)
```
EI = TRR / SSRR
```

### Referensi
1. Singh, S. (2000). The Code Breaker
2. Stallings, W. (2017). Cryptography and Network Security
3. Shannon, C. E. (1949). Communication Theory of Secrecy Systems
