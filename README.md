## Data Preprocessing

Notebook ini berisi tahapan preprocessing data yang dilakukan untuk mempersiapkan dataset sebelum digunakan pada proses pelatihan model machine learning.

### Tahapan Preprocessing

1. **Load Dataset**

   * Mengimpor library yang diperlukan.
   * Memuat dataset ke dalam DataFrame untuk proses analisis dan transformasi.

2. **Data Cleaning**

   * Memeriksa struktur dan tipe data setiap kolom.
   * Mengonversi fitur ke tipe data yang sesuai.
   * Menangani missing values menggunakan nilai median.
   * Menghapus data duplikat untuk menjaga kualitas dataset.

3. **Exploratory Check**

   * Melakukan pemeriksaan distribusi data dan variabel target.
   * Mengidentifikasi potensi ketidakseimbangan kelas (*class imbalance*).

4. **Feature-Target Separation**

   * Memisahkan fitur (X) dan target (y) sebagai persiapan untuk proses balancing dan pemodelan.

5. **Data Balancing**

   * Menerapkan **SMOTE (Synthetic Minority Oversampling Technique)** untuk menyeimbangkan distribusi kelas pada variabel target.
   * Memverifikasi hasil balancing melalui visualisasi distribusi kelas.

6. **Feature Scaling**

   * Melakukan standarisasi fitur menggunakan **StandardScaler** agar seluruh fitur berada pada skala yang seragam.

7. **Export Processed Data**

   * Menyimpan dataset hasil preprocessing ke dalam file CSV yang siap digunakan pada tahap training dan evaluasi model.

### Output

Dataset hasil preprocessing telah:

* Bebas dari data duplikat.
* Tidak memiliki missing values pada fitur numerik.
* Memiliki distribusi kelas yang lebih seimbang.
* Telah distandarisasi untuk mendukung performa model machine learning.
