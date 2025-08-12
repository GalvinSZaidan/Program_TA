# Ekstraksi Fitur Sinyal EKG 3-Channel 📈❤

Skrip Python ini dirancang untuk membaca, memproses, dan menganalisis data sinyal Elektrokardiogram (EKG) dari 3 lead (I-mV, II-mV, V1-mV). Program akan secara otomatis membersihkan sinyal dari noise, mendeteksi gelombang P, Q, R, S, T, dan mengekstrak fitur-fitur klinis penting.

Hasil analisis berupa nilai-nilai interval, rasio, dan detak jantung per menit (BPM), serta visualisasi grafis dari setiap tahapan proses.



---

## ✨ Fitur Utama

-   *Membaca Data EKG*: Mengimpor data dari file .csv dengan 3 kolom.
-   *Pra-pemrosesan Sinyal*:
    -   Menghilangkan baseline wander (noise frekuensi rendah).
    -   Menerapkan filter Butterworth dan FIR untuk membersihkan sinyal.
-   *Deteksi Puncak PQRST*: Secara otomatis mendeteksi semua puncak dan gelombang penting (P, Q, R, S, T) pada sinyal EKG.
-   *Ekstraksi Fitur Klinis*: Menghitung metrik-metrik penting, seperti:
    -   Interval RR, PR, ST, dan QS
    -   Interval QTc (Interval QT yang terkoreksi)
    -   Rasio R/S dari lead V1
    -   Heart Rate (BPM)
-   *Visualisasi Data*: Menampilkan grafik sinyal mentah, sinyal setelah difilter, dan sinyal akhir dengan penanda puncak PQRST untuk setiap lead.

---

## 🚀 Cara Menggunakan

Ikuti langkah-langkah berikut untuk menjalankan program ini.

### 1. Persiapan (Instalasi Library)

Pastikan Anda sudah menginstal Python di komputer Anda. Kemudian, buka terminal atau command prompt dan instal semua library yang dibutuhkan dengan perintah berikut:

```bash
pip install pandas numpy matplotlib scipy neurokit2

### 2. Siapkan Data Anda
 * Siapkan data EKG Anda dalam format file CSV (.csv).
 * Pastikan file CSV Anda memiliki 3 kolom dengan nama header: I-mV, II-mV, dan V1-mV.
 * Program ini dirancang untuk melewati baris header pertama (skiprows=1), jadi pastikan data sinyal dimulai dari baris kedua.
Contoh struktur file data_ekg.csv:
I-mV,II-mV,V1-mV
0.12,0.34,-0.05
0.15,0.36,-0.04
...

### 3. Konfigurasi Skrip
 * Buka file .py dengan editor kode Anda.
 * Cari baris kode untuk membaca file CSV:
   # Ganti 'path/ke/file/anda.csv' dengan lokasi file CSV Anda
file_path = 'path/ke/file/anda.csv'
dataset = pd.read_csv(file_path, names=['I-mV', 'II-mV', 'V1-mV'], sep=',', skiprows=1)

 * Ubah path file di dalam tanda kutip ('...') menjadi lokasi file CSV Anda yang sudah disiapkan.

---

### 4. Jalankan Program
Buka terminal, navigasikan ke direktori tempat Anda menyimpan file skrip, lalu jalankan dengan perintah:
python nama_file_skrip_anda.py