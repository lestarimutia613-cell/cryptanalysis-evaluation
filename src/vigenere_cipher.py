"""
Vigenère Cipher Implementation
Implementasi Vigenère cipher dengan fungsi enkripsi dan dekripsi
"""

class VigenèreCipher:
    """
    Vigenère cipher adalah cipher substitusi polialfabetik
    yang menggunakan kunci berulang untuk enkripsi.
    """
    
    def __init__(self, key):
        """
        Initialize Vigenère cipher dengan kunci
        
        Args:
            key (str): Kunci untuk enkripsi/dekripsi
        """
        self.key = key.upper()
    
    @staticmethod
    def _prepare_key(plaintext, key):
        """
        Siapkan kunci dengan panjang sesuai plaintext
        
        Args:
            plaintext (str): Plaintext yang akan dienkripsi
            key (str): Kunci asli
            
        Returns:
            str: Kunci yang diperpanjang
        """
        key = key.upper()
        key_index = 0
        prepared_key = ""
        
        for char in plaintext:
            if char.isalpha():
                prepared_key += key[key_index % len(key)]
                key_index += 1
            else:
                prepared_key += char
        
        return prepared_key
    
    @staticmethod
    def encrypt(plaintext, key):
        """
        Enkripsi plaintext menggunakan Vigenère cipher
        
        Args:
            plaintext (str): Teks yang akan dienkripsi
            key (str): Kunci untuk enkripsi
            
        Returns:
            str: Ciphertext yang terenkripsi
        """
        ciphertext = ""
        prepared_key = VigenèreCipher._prepare_key(plaintext, key)
        
        for i, char in enumerate(plaintext):
            if char.isalpha():
                is_upper = char.isupper()
                char = char.upper()
                key_char = prepared_key[i].upper()
                shift = ord(key_char) - ord('A')
                shifted = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                ciphertext += shifted if is_upper else shifted.lower()
            else:
                ciphertext += char
        
        return ciphertext
    
    @staticmethod
    def decrypt(ciphertext, key):
        """
        Dekripsi ciphertext menggunakan Vigenère cipher
        
        Args:
            ciphertext (str): Teks yang akan didekripsi
            key (str): Kunci untuk dekripsi
            
        Returns:
            str: Plaintext yang terdekripsi
        """
        plaintext = ""
        prepared_key = VigenèreCipher._prepare_key(ciphertext, key)
        
        for i, char in enumerate(ciphertext):
            if char.isalpha():
                is_upper = char.isupper()
                char = char.upper()
                key_char = prepared_key[i].upper()
                shift = ord(key_char) - ord('A')
                shifted = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                plaintext += shifted if is_upper else shifted.lower()
            else:
                plaintext += char
        
        return plaintext
    
    @staticmethod
    def kasiski_examination(ciphertext, max_distance=20):
        """
        Kasiski examination untuk memperkirakan panjang kunci
        
        Args:
            ciphertext (str): Ciphertext yang akan dianalisis
            max_distance (int): Jarak maksimal untuk mencari repetisi
            
        Returns:
            dict: Statistik kemungkinan panjang kunci
        """
        text_only = ''.join(c for c in ciphertext if c.isalpha()).upper()
        distances = []
        
        for i in range(len(text_only) - 2):
            bigram = text_only[i:i+2]
            for j in range(i + 2, min(i + max_distance, len(text_only) - 1)):
                if text_only[j:j+2] == bigram:
                    distances.append(j - i)
        
        from collections import Counter
        factors = Counter()
        for distance in distances:
            for i in range(1, distance + 1):
                if distance % i == 0:
                    factors[i] += 1
        
        return dict(sorted(factors.items(), key=lambda x: x[1], reverse=True)[:10])


if __name__ == "__main__":
    plaintext = "HELLO WORLD"
    key = "SECRET"
    ciphertext = VigenèreCipher.encrypt(plaintext, key)
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print(f"Ciphertext: {ciphertext}")
    print(f"Decrypted: {VigenèreCipher.decrypt(ciphertext, key)}")
