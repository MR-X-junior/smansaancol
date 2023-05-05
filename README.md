# smansaancol
smansaancol adalah library sederhana yang di gunakan untuk scraping web [elearning SMA N1 MUARA ANCALONG](https://elearning.sman1muaraancalong.sch.id)

# Informasi Library
*Author :* [**Rahmat adha**](https://facebook.com/Anjay.pro098)\
*Library :* [**smansaancol**](https://github.com/MR-X-Junior/smansaancol)\
*License:* [**MIT License**](https://github.com/MR-X-junior/smansaancol/blob/main/LICENSE)\
*Release:* **05**/05/20**23**\
*Version :* **0.0.1**

**NOTE: LIBRARY INI BUKAN LIBRARY RESMI DARI SMA N1 MUARA ANCALONG**

## Contoh cara penggunaan

### Pertama-tama login ke akun terlebih dahalu.
Kamu bisa menggunakan class `Elearning` untuk login ke akun E-learning 

#### Contoh:

```python
from smansaancol import Elearning

elearning = Elearning(username = "10xxxxxxxx", password = "password akun elearning")
```

### Mendapatkan informasi pengguna
Kamu bisa menggunakan method `get_user_info` untuk mendapatkan informasi pengguna.\
method `get_user_info` akan mengembalikan informasi akun dalam bentuk `dict`

#### Contoh:

```python
>>> elearning.get_user_info()
{'nama': 'Rahmat Adha', 'username': 'xxxxxxxxxx', 'password': 'xxxxxxxxxx', 'kelas': 'XC', 'user': 'Oxxxxx', 'api_key': '76310EEFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'status': 'Anda belum absen hari ini.'}
```

### Absen
Kamu bisa menggunakan method `absen` untuk melakukan absen ke web E-learning\
Method `absen` akan mengembalikan status absen dalam format `json`

#### Contoh (1):

```python
>>> elearning.absen()
{'status': 'success', 'data': [], 'message': 'Berhasil absen.'}
```

#### Contoh (2):

```python
>>> elearning.absen(json = False)
>>> True
```

### Get Materi
Kamu bisa menggunakan method `get_materi` untuk mendapatkan list materi siswa yang di berikan oleh guru.

Method ini akan mengembalikan `list` yang di dalam nya terdapat sekumpulan object `Materi` jika argumen `return_dict` nya adalah `False`, sebaliknya jika argumen `return_dict` nya adalah `True` maka method ini akan mengembalikan `list` yang di dalamnya terdapat sekumpulan `dict`.

Default dari argument `return_dict` adalah `False`

#### Contoh(1):

```python
>>> elearning.get_materi(limit = 3)
[Smansa Materi : mapel='MTKW' title='Barisan dan Deret' tanggal_publish='2022-10-27 11:15:00' deskripsi=''Asalamualaikum wr wb, selamat pagi anak-anak semua, mudah-mudahan selalu dalam lindungan Allah SWT,\nhari ini ada jam pelajaran ibu di kelas kalian dan jangan lupa absen terlebih dahulu.\nMengingatkan kembali tentang barisan dan deret, Silahkan kalian rangkum di buku catatan kalian,\napa yang anda dapatkan dalam video yang ibu bagikan. Terima kasih wasalamualaikum wr wb\n'', Smansa Materi : mapel='SJRW' title='awal kehidupan masyarakat indonesia' tanggal_publish='2022-10-31 08:05:00' deskripsi=''selamat pagi dan salam sehat selalu\nsimaklah vidio berukut'', Smansa Materi : mapel='BIO' title='Monera' tanggal_publish='2022-10-31 10:45:00' deskripsi=''Siswa sekalian mohon ditonton dan lihat vidio dengan seksama setelah itu buatlah resume untuk tiap-tiap siswa\n'']
```

#### Contoh(2):

```python
>>> elearning.get_materi(limit = 3, return_dict = True)
[{'guru': 'Eni Karnawati, S.Pd', 'mapel': 'MTKW', 'title': 'Barisan dan Deret', 'materi_url': 'https://elearning.sman1muaraancalong.sch.id/lihatmateri/N2xPMHQxM2ZEZGNiTGJyL1FFaEdkdz09'}, {'guru': 'Herlinda, S.Pd', 'mapel': 'SJRW', 'title': 'awal kehidupan masyarakat indonesia', 'materi_url': 'https://elearning.sman1muaraancalong.sch.id/lihatmateri/RFZWLy9KRUxGaXp2R3pHa0Z5akluUT09'}, {'guru': 'Sakbani, SP', 'mapel': 'BIO', 'title': 'Monera', 'materi_url': 'https://elearning.sman1muaraancalong.sch.id/lihatmateri/aUQyWC9xdlZhbE1xaGtCRzh3S21DUT09'}]
```

### View Materi
Kamu bisa menggunakan method `view_materi` untuk parsing materi yang ada di E-learning, method ini akan mengembalikan object `Materi`

#### Contoh:

```python
>>> elearning.view_materi('https://elearning.sman1muaraancalong.sch.id/lihatmateri/N2xPMHQxM2ZEZGNiTGJyL1FFaEdkdz09')
Smansa Materi : mapel='MTKW' title='Barisan dan Deret' tanggal_publish='2022-10-27 11:15:00' deskripsi=''Asalamualaikum wr wb, selamat pagi anak-anak semua, mudah-mudahan selalu dalam lindungan Allah SWT,\nhari ini ada jam pelajaran ibu di kelas kalian dan jangan lupa absen terlebih dahulu.\nMengingatkan kembali tentang barisan dan deret, Silahkan kalian rangkum di buku catatan kalian,\napa yang anda dapatkan dalam video yang ibu bagikan. Terima kasih wasalamualaikum wr wb\n''
```

### Mendapatkan komentar pada materi
Kamu bisa menggunakan method `get_comment` untuk mendapatkan komentar pada materi.

#### Contoh:

```python
>>> materi = elearning.view_materi('https://elearning.sman1muaraancalong.sch.id/lihatmateri/N2xPMHQxM2ZEZGNiTGJyL1FFaEdkdz09')
>>> materi.get_comment(limit = 2)
[{'name': 'Tiara Safitri', 'kelas': ' XC', 'message': 'Baik buk', 'time': '27 Oct 2022 11:19:54'}, {'name': 'Rahima Kuraini', 'kelas': ' XC', 'message': 'Iya buk', 'time': '27 Oct 2022 11:31:42'}]
```

### Mengirim komentar pada materi
Kamu bisa menggunakan method `send_comment` untuk mengirim komentar ke materi

#### Contoh:

```python
>>> materi = elearning.view_materi('https://elearning.sman1muaraancalong.sch.id/lihatmateri/N2xPMHQxM2ZEZGNiTGJyL1FFaEdkdz09')
>>> materi.send_comment("Siap buk :)")
True
```

##### Hasilnya:
![Contoh cara mengirim komentar](https://i.ibb.co/tPH8yVp/IMG-20230502-203327.jpg)


#### Attribute Materi
*(Untuk `Materi` Object)*
- **sessions**: Requests sessions object
- **materi_url**: Materi url
- **req**: Response object from Requests
- **res**: Beautiful Soup Object
- **mapel**: Nama Mata Pelajaran
- **title**: Judul Materi
- **tanggal_publish**: Tanggal Materi Di Publish
- **deskripsi**: Deskripsi Materi
- **youtube_embed**: Url embed video YouTube
- **youtube_video**: Url video YouTube
- **file**: Link download file pendukung materi

# Cara install
**smansaancol** sudah tersedia di PyPi sehingga kamu bisa memasangnya menggunakan pip

```console
$ python -m pip install smansaancol
```

# Donate
[![Donate for Rahmat adha](https://i.ibb.co/PwYMWsK/Saweria-Logo.png)](https://saweria.co/rahmatadha)
