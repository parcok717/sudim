import subprocess
import random
import time
import os

def generate_start_key():
    """
    Membuat key hex 64 karakter (256 bit) dengan:
    - 214 bit pertama random (53.5 karakter hex)
    - 42 bit terakhir 0 (10.5 karakter hex)
    """
    # 214 bit = 53.5 karakter hex, kita ambil 54 karakter dan atur bit terakhir
    random_bits = random.getrandbits(214)
    
    # Konversi ke hex dan pastikan panjang 54 karakter (216 bit)
    hex_str = format(random_bits, '054x')  # 54 karakter hex = 216 bit
    
    # Hapus 2 bit terakhir untuk mendapatkan 214 bit tepat
    hex_str = hex_str[:-1] + '0'  # Set karakter terakhir ke 0 (2 LSB)
    
    # Tambahkan 10 karakter '0' untuk 42 bit sisanya
    start_key = hex_str + '0' * 10  # Total 64 karakter
    
    return start_key

def run_vanitysearch(start_key):
    """Menjalankan perintah vanitysearch dengan start key tertentu"""
    command = [
        "./log",
        "-gpuId", "0",
        "-i", "rich.txt",
        "-o", "output.txt",
        "-start", start_key,
        "-range", "42",
        "-random"
    ]
    
    print(f"\n{'='*60}")
    print(f"Menjalankan dengan start key:")
    print(f"{start_key}")
    print(f"{'='*60}\n")
    
    try:
        # Jalankan proses
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # Tampilkan output real-time
        for line in process.stdout:
            print(line.strip())
            time.sleep(0.1)  # Delay kecil untuk mencegah buffer penuh
            
        process.wait()
        return process.returncode
        
    except KeyboardInterrupt:
        print("\n\nProses dihentikan oleh user")
        process.terminate()
        return -1
    except Exception as e:
        print(f"Error: {e}")
        return -1

def main():
    """Program utama"""
    print("VanitySearch Automation Script")
    print("="*60)
    
    # Cek apakah file executable exists
    if not os.path.exists("./log"):
        print("Error: File ./log tidak ditemukan!")
        print("Pastikan log berada di direktori yang sama")
        return
    
    # Cek apakah file input exists
    if not os.path.exists("rich.txt"):
        print("Warning: File rich.txt tidak ditemukan!")
        print("Membuat file rich.txt kosong...")
        open("rich.txt", "w").close()
    
    iteration = 1
    
    try:
        while True:
            print(f"\n{'='*60}")
            print(f"Iterasi ke-{iteration}")
            print(f"{'='*60}")
            
            # Generate start key baru
            start_key = generate_start_key()
            
            # Jalankan vanitysearch
            return_code = run_vanitysearch(start_key)
            
            if return_code == 0:
                print(f"\nIterasi {iteration} selesai dengan sukses")
            elif return_code == -1:
                print(f"\nIterasi {iteration} dihentikan")
                break
            else:
                print(f"\nIterasi {iteration} selesai dengan kode: {return_code}")
            
            iteration += 1
            
            # Tunggu sebentar sebelum iterasi berikutnya
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh user")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
