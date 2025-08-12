# Ekstraksi Fitur Sinyal EKG 5-Lead 📈❤

Skrip Python ini dirancang untuk membaca, memproses, dan menganalisis data sinyal Elektrokardiogram (EKG) dari 5 lead yang menghasilkan 3 channel ```(I-mV, II-mV, V1-mV)```. Program akan secara otomatis membersihkan sinyal dari noise, mendeteksi gelombang P, Q, R, S, T, dan mengekstrak fitur-fitur klinis penting.

Hasil analisis berupa nilai-nilai interval, rasio, dan detak jantung per menit (BPM), serta visualisasi grafis dari setiap tahapan proses.





## ✨ Fitur Utama

-   *Membaca Data EKG*: Mengimpor data dari file ```.csv``` dengan 3 kolom.
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


## 🚀 Cara Menggunakan

Ikuti langkah-langkah berikut untuk menjalankan program ini.

#### 1. Persiapan (Instalasi Library)

Pastikan Anda sudah menginstal Python di komputer Anda. Kemudian, buka terminal atau command prompt dan instal semua library yang dibutuhkan dengan perintah berikut:

```bash
pip install pandas numpy matplotlib scipy neurokit2
```

#### 2. Siapkan Data Anda
 * Siapkan data EKG Anda dalam format file CSV (```.csv```).
 * Pastikan file CSV Anda memiliki 3 kolom dengan nama header: I-mV, II-mV, dan V1-mV.
 * Program ini dirancang untuk melewati baris header pertama (skiprows=1), jadi pastikan data sinyal dimulai dari baris kedua.
Contoh struktur file ```data_ekg.csv```:

```bash
I-mV,II-mV,V1-mV
0.12,0.34,-0.05
0.15,0.36,-0.04
...
```

#### 3. Konfigurasi Skrip
 * Buka file .py dengan editor kode Anda.
 * Cari baris kode untuk membaca file CSV:
   #### Ganti '```path/ke/file/anda.csv```' dengan lokasi file CSV Anda

```bash
file_path = 'path/ke/file/anda.csv'
dataset = pd.read_csv(file_path, names=['I-mV', 'II-mV', 'V1-mV'], sep=',', skiprows=1)

 * Ubah path file di dalam tanda kutip ('...') menjadi lokasi file CSV Anda yang sudah disiapkan.
```
#### 4. Jalankan Program
Buka terminal, navigasikan ke direktori tempat Anda menyimpan file skrip, lalu jalankan dengan perintah:
```bash 
python nama_file_skrip_anda.py
```

## 📊 Memahami Hasil

Setelah program dijalankan, Anda akan melihat beberapa output:

#### 1\. Jendela Grafik (Plots)

Akan muncul beberapa jendela grafik yang menampilkan:

  - Grafik sinyal mentah untuk setiap lead.
  - Grafik perbandingan sinyal setelah baseline correction, filter Butterworth, dan filter FIR.
  - Grafik akhir yang menampilkan sinyal EKG bersih lengkap dengan *penanda (marker 'x') dan label (P, Q, R, S, T)* pada setiap puncak yang terdeteksi.

#### 2\. Output di Terminal

Di terminal tempat Anda menjalankan skrip, akan tercetak hasil ekstraksi fitur seperti ini:

```bash 
I_mV - ST Interval (ms) - Mean: 123.45 , Standard Deviation: 6.78
II_mV - RR Interval (ms) - Mean: 800.12 , Standard Deviation: 15.34
II_mV - PR Interval (ms) - Mean: 160.56 , Standard Deviation: 5.12
II_mV - QS Interval (ms) - Mean: 95.89 , Standard Deviation: 4.01
II_mV - QT Interval (ms) - Mean: 400.78 , Standard Deviation: 10.22
II_mV - QTc Interval (ms) - Mean: 447.89
II_mV - BPM: 75.0
V1_mV - R/S Ratio: 0.85
```

#### 3\. (Opsional) Menyimpan Hasil ke Excel

Di bagian akhir skrip, terdapat kode yang dinonaktifkan dengan tanda komentar (#) untuk menyimpan hasil ke file Excel. Untuk mengaktifkannya:

  - Hapus tanda # pada blok kode di bagian akhir.
  - Sesuaikan path dan nama file Excel (```.xlsx```) sesuai keinginan Anda.
  - Jika Anda menjalankan program untuk banyak data, kode tersebut sudah dirancang untuk *menambahkan hasil baru ke baris berikutnya* tanpa menimpa data lama.

---
 <br />
 <br />
 <br />

# ❤️‍🩹 Klasifikasi Sinyal EKG Menggunakan Model ANN 🤖

Proyek ini menggunakan model *Artificial Neural Network* (ANN) yang telah dilatih untuk mengklasifikasikan data sinyal EKG ke dalam empat kategori: **Normal**, **Abnormal**, **Berpotensi Aritmia**, dan **Sangat Berpotensi Aritmia**.

Skrip `inference_code_h5.py` akan memuat data baru, melakukan pra-pemrosesan, menjalankan inferensi menggunakan model yang tersimpan, dan menyimpan hasilnya ke dalam sebuah *file* Excel.

## 📋 Prasyarat

Sebelum menjalankan program, pastikan Anda sudah menginstal semua *library* yang dibutuhkan.

```bash
pip install numpy pandas tensorflow scikit-learn joblib openpyxl
```

## 📁 Struktur Proyek
Pastikan Anda menyusun file dan direktori seperti contoh di bawah ini agar skrip dapat berjalan tanpa masalah. Anda bisa mengubah path di dalam file .py jika struktur direktori Anda berbeda.

```bash
/proyek-klasifikasi-ekg/
|
├── model/
|   ├── modelann91.h5         # File model terlatih
|   └── scaler91.pkl          # File scaler
|
├── data_input/
|   └── DataUntukPrediksi.xlsx # File data yang akan diprediksi
|
└── inference_code_h5.py      # Skrip utama untuk inferensi
```

## 🚀 Cara Penggunaan
Ikuti langkah-langkah berikut untuk menjalankan program:

#### 1\. 🧠 Siapkan Model dan Scaler
Letakkan file model ```.h5``` (misalnya ```modelann91.h5```) dan file scaler ```.pkl``` (misalnya ```scaler91.pkl```) di dalam direktori yang sesuai (contoh: ```/model/```).

#### 2\.📊 Siapkan Data Input
- Siapkan data EKG yang ingin Anda klasifikasikan dalam format Excel (```.xlsx```).
- Pastikan file Excel tersebut memiliki header kolom yang sesuai dengan data yang digunakan saat melatih model, termasuk kolom aktual jika ingin ada perbandingan.
- Letakkan file ini di direktori ``` data_input/```.

#### 3\. ✏️ Konfigurasi Path dalam Skrip
Buka file ```inference_code_h5.py``` dan sesuaikan path berikut sesuai dengan struktur direktori Anda:
```bash
# Path ke model yang telah dilatih
save_model_path = 'model/modelann91.h5'

# Path ke scaler yang telah disimpan
scaler_path = 'model/scaler91.pkl'

# Path ke data baru yang akan diinferensi
url_new_data = 'data_input/DataUntukPrediksi.xlsx'

# Path untuk menyimpan hasil prediksi
output_file = 'hasil/hasil_prediksi.xlsx'
```

#### 4\. ▶️ Jalankan Skrip
Buka terminal atau command prompt, arahkan ke direktori utama proyek, dan jalankan perintah berikut
```bash
python inference_code_h5.py
```

#### 5\. 💻 Contoh Output Terminal
Setelah skrip berhasil dijalankan, Anda akan melihat output di terminal yang mirip seperti ini. Output ini menunjukkan hasil prediksi dalam bentuk array dan konfirmasi bahwa file hasil telah disimpan.

```bash
Prediksi kelas untuk data baru:
['Normal' 'Abnormal' 'Berpotensi Aritmia' 'Normal' 'Sangat Berpotensi Aritmia']
Hasil prediksi telah disimpan ke hasil/hasil_prediksi.xlsx
```

#### 6\. 🔍 Lihat Hasilnya
- Periksa direktori output yang Anda tentukan (misalnya ```hasil/```).
- Di dalamnya akan ada file Excel baru (misalnya ```hasil_prediksi.xlsx```) yang berisi data asli ditambah dengan kolom **"Klasifikasi Model"** yang menunjukkan hasil prediksi untuk setiap baris data.
