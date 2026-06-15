"""
Caesar Cipher Implementation
Implementasi Caesar cipher dengan fungsi enkripsi dan dekripsi
"""

class CaesarCipher:
    """
    Caesar cipher adalah cipher substitusi monoalfabetik sederhana
    yang menggeser setiap huruf dalam plaintext sebesar n posisi.
    """
    
    def __init__(self, shift=3):
        """
        Initialize Caesar cipher dengan shift tertentu
        
        Args:
            shift (int): Jumlah posisi pergeseran (0-25)
        """
        self.shift = shift % 26
    
    @staticmethod
    def encrypt(plaintext, shift):
        """
        Enkripsi plaintext menggunakan Caesar cipher
        
        Args:
            plaintext (str): Teks yang akan dienkripsi
            shift (int): Jumlah posisi pergeseran
            
        Returns:
            str: Ciphertext yang terenkripsi
        """
        ciphertext = ""
        shift = shift % 26
        
        for char in plaintext:
            if char.isalpha():
                is_upper = char.isupper()
                char = char.upper()
                shifted = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                ciphertext += shifted if is_upper else shifted.lower()
            else:
                ciphertext += char
        
        return ciphertext
    
    @staticmethod
    def decrypt(ciphertext, shift):
        """
        Dekripsi ciphertext menggunakan Caesar cipher
        
        Args:
            ciphertext (str): Teks yang akan didekripsi
            shift (int): Jumlah posisi pergeseran
            
        Returns:
            str: Plaintext yang terdekripsi
        """
        return CaesarCipher.encrypt(ciphertext, -shift)
    
    @staticmethod
    def brute_force_all_shifts(ciphertext):
        """
        Coba semua kemungkinan shift (1-25)
        
        Args:
            ciphertext (str): Teks yang akan di-brute-force
            
        Returns:
            list: List tuple (shift, plaintext)
        """
        results = []
        for shift in range(26):
            plaintext = CaesarCipher.decrypt(ciphertext, shift)
            results.append((shift, plaintext))
        return results


if __name__ == "__main__":
    plaintext = "HELLO WORLD"
    shift = 3
    ciphertext = CaesarCipher.encrypt(plaintext, shift)
    print(f"Plaintext: {plaintext}")
    print(f"Ciphertext: {ciphertext}")
    print(f"Decrypted: {CaesarCipher.decrypt(ciphertext, shift)}")
