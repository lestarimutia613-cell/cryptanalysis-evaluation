# Metodologi Penelitian

## 1. Desain Eksperimen

### Variabel Independen
1. **Tipe Cipher**
   - Caesar cipher
   - Vigenère cipher

2. **Ukuran Plaintext**
   - 50 karakter
   - 100 karakter
   - 200 karakter
   - 500 karakter

3. **Kompleksitas Kunci**
   - Caesar: shift 1-25
   - Vigenère: panjang 3-8 karakter

4. **Penggunaan Heuristik**
   - Dengan heuristik (5 jenis)
   - Tanpa heuristik (brute-force murni)

### Variabel Dependen
1. Search Space Reduction Rate (SSRR)
2. Time Reduction Rate (TRR)
3. Efficiency Index (EI)
4. Accuracy Rate
5. False Positive Rate (FPR)

## 2. Dataset

### Plaintext Source
- Teks bahasa Inggris umum
- Berbagai panjang (50-500 karakter)
- Distribusi frekuensi normal

### Key Generation
- Caesar: random shift 1-25
- Vigenère: random string dengan panjang 3-8
- Jumlah trial per kondisi: 3-5

## 3. Prosedur Eksperimen

### Fase 1: Persiapan
1. Load plaintext samples
2. Load English frequency table
3. Initialize heuristics module

### Fase 2: Encryption
1. Random select plaintext
2. Random generate key
3. Encrypt plaintext

### Fase 3: Brute-Force Tanpa Heuristik
1. Jalankan brute-force penuh
2. Rekam waktu eksekusi
3. Hitung jumlah evaluasi

### Fase 4: Brute-Force Dengan Heuristik
1. Jalankan brute-force dengan threshold
2. Evaluasi dengan 5 heuristik
3. Filter candidate dengan score ≥ threshold
4. Rekam metrik

### Fase 5: Perhitungan Metrik
```
SSRR = (Total Keyspace - Filtered) / Total Keyspace × 100%
TRR = (Time Without H - Time With H) / Time Without H × 100%
EI = TRR / SSRR
```

## 4. Threshold Heuristik

### Penentuan Threshold
- Threshold optimal: 50.0 untuk combined score
- Plaintext valid: typically score 60-100
- Random/cipher: typically score 20-50

## 5. Parameter Eksperimen

| Parameter | Value | Justifikasi |
|-----------|-------|-------------|
| Caesar shift | 1-25 | Full keyspace |
| Vigenère max key length | 6 | Practical range |
| Plaintext sizes | 50, 100, 200, 500 | Varying complexity |
| Number of trials | 3-5 | Statistical reliability |
| Heuristic threshold | 50.0 | Optimal balance |

## Referensi Metodologi

1. Stallings, W. (2017). Cryptography and Network Security
2. Friedman, W. F., & Mendelsohn, C. J. (1938). The Index of Coincidence
