# Proyek Tengah Semester C06 - PBP Gasal 2024/2025
- [Nama Aplikasi](#nama-aplikasi-dinepasar)
- [Anggota Kelompok C06](#anggota-kelompok-c06)
- [Deskripsi Aplikasi](#deskripsi-aplikasi)
- [Modul Aplikasi](#modul-aplikasi)
- [Sumber Initial Dataset](#sumber-initial-dataset)
- [Role Pengguna](#role-pengguna)
- [Tautan Deployment Aplikasi](#tautan-deployment-aplikasi)

# Nama Aplikasi: Dinepasar


### Anggota Kelompok C06
| Nama | NPM |
| :--------------: | :--------: |
| Wirya Dharma Kurnia | 2306152115 |
| Calvin Joy Tarigan | 2306244974 |
| Namira Aulia | 2306165931 |
| Joanne Kenisa Adelina | 2306275626 |
| Anindya Nabila Syifa | 2306165805 |


## Deskripsi Aplikasi
Denpasar, Bali terkenal sebagai statusnya sebagai destinasi pariwisata yang terkenal dengan keindahan budaya dan ragam kulinernya. Sebagai salah satu destinasi favorit turis, Denpasar tidak hanya menyajikan pantai yang eksotis dan keunikan budaya, namun juga variasi hidangan lezat yang mampu memanjakan lidah.

Di tengah keberagaman kuliner tersebut, turis seringkali menemui kesulitan dalam menentukan tempat makan yang sesuai dengan selera pribadi. Untuk mengatasi masalah tersebut, Dinepasar hadir sebagai platform digital yang dirancang khusus untuk menemukan restoran yang sesuai dengan permintaan pengguna. Situs ini menyediakan informasi yang lengkap dan terpercaya mengenai restoran-restoran yang ada di kota Denpasar, termasuk menu, harga, lokasi, rating, hingga dari review pengunjung lain. 

Lebih dari itu, Dinepasar dapat menjadi teman setia dalam mengeksplorasi cita rasa khas kuliner Denpasar. Hadirnya situs ini diharapkan dapat memberikan pengalaman liburan yang lebih mudah, praktis, dan berkesan dalam memenuhi kebutuhan kuliner para turis.


## Modul Aplikasi
- Autentikasi, Role Pengguna, dan Halaman Utama

Dinepasar menyediakan fitur autentikasi dengan halaman registrasi dan login. Setelah login, pengguna akan diarahkan ke landing page yang menampilkan pesan pembuka. Sejak memasuki halaman utama dan seterusnya, fitur yang dapat digunakan pengguna akan ditentukan oleh rolenya, sebagai user biasa atau sebagai admin.
- Pencarian dan Daftar Restoran

Pengguna dapat mencari restoran melalui search bar di bagian atas halaman. Daftar restoran ditampilkan dari A-Z sesuai dataset, dan setiap restoran menampilkan preview saat diklik.
- Preview Restoran dan Ulasan

Halaman preview restoran menampilkan informasi lengkap tentang satu restoran, termasuk ulasan dari pengguna lain. Di halaman ini, pengguna juga dapat menambahkan restoran tersebut ke daftar favorit atau wishlist melalui tombol yang disediakan.
- Tambahkan ke Favorit

Halaman favorit memungkinkan pengguna menyimpan restoran favorit. Di bagian bawah halaman, pengguna juga akan diberikan rekomendasi restoran lain berdasarkan preferensi mereka.
- Informasi tentang Denpasar

Dinepasar menyediakan halaman khusus yang berisi informasi tentang berbagai hal terkait Denpasar. Halaman ini juga dilengkapi dengan penambahan artikel sebagai cara untuk setiap pengguna berbagi informasi spesifik mengenai Denpasar.

Berikut link menuju detail penjelasan modul dan pembagiannya:
https://docs.google.com/spreadsheets/d/1D2Tk0wCMrCWT3HMLjPZVTOpfQ64sDqC_8w8SRwu9P0g/edit?usp=sharing


## Sumber Initial Dataset
- Dataset:

https://docs.google.com/spreadsheets/d/148R7MeizpXdl2PQJxHuYX6YQg4IeXM9quS3PN8Lgwts/edit?gid=0#gid=0 

- Sumber dataset:

https://www.google.com/maps

https://gofood.co.id/


## Role Pengguna
- User

User setelah login bisa mengakses berbagai fitur seperti autentikasi, halaman profil pengguna untuk melihat dan mengedit profil, serta halaman utama yang mengintegrasikan seluruh data. User dapat mencari restoran menggunakan search bar, melihat daftar restoran dari A-Z, melihat detail restoran beserta ulasan, dan menyimpan restoran ke dalam favorit. Ada juga halaman khusus untuk informasi tentang Denpasar. 

- Admin

Selain memiliki akses seperti user, juga dapat menambahkan dan menghapus card restoran pada halaman pencarian.


## Tautan Deployment Aplikasi
https://pbp.cs.ui.ac.id/namira.aulia31/dinepasar