from pymongo import MongoClient

# Konfigurasi koneksi MongoDB
client = MongoClient('localhost', 27017)
db = client['db_puspamukti']

# Data untuk koleksi ekstrakulikuler
ekstrakulikuler_data = [
    {
        "id": 1,
        "title": "Klub Seni",
        "description": "Klub seni yang memfasilitasi siswa untuk mengembangkan bakat dan minat dalam seni rupa.",
        "img_url": "https://placehold.co/600x400",
        "action_link": "#"
    },
    {
        "id": 2,
        "title": "Tim Basket",
        "description": "Tim basket sekolah yang telah memenangkan berbagai kejuaraan.",
        "img_url": "https://placehold.co/600x400",
        "action_link": "#"
    },
    {
        "id": 3,
        "title": "Paduan Suara",
        "description": "Paduan suara yang tampil di berbagai acara sekolah dan lomba.",
        "img_url": "https://placehold.co/600x400",
        "action_link": "#"
    }
]

# Data untuk koleksi galeri
galeri_data = [
    {
        "id": 1,
        "title": "Pameran Seni Rupa",
        "description": "Pameran seni rupa kontemporer menampilkan karya seniman lokal.",
        "img_url": "https://placehold.co/600x400",
        "action_link": "#"
    },
    {
        "id": 2,
        "title": "Konser Musik Jazz",
        "description": "Nikmati malam penuh jazz dengan musisi terkenal.",
        "img_url": "https://placehold.co/600x400",
        "action_link": "#"
    },
    {
        "id": 3,
        "title": "Festival Kuliner",
        "description": "Festival kuliner menghadirkan makanan dari berbagai daerah.",
        "img_url": "https://placehold.co/600x400",
        "action_link": "#"
    }
]

# Data untuk koleksi sarpras
sarpras_data = [
    {
        "id": 1,
        "title": "Laboratorium Komputer",
        "description": "Laboratorium komputer dilengkapi dengan perangkat keras dan lunak terbaru untuk mendukung kegiatan belajar mengajar.",
        "img_url": "https://placehold.co/600x400",
        "action_link": "#"
    },
    {
        "id": 2,
        "title": "Perpustakaan",
        "description": "Perpustakaan sekolah menyediakan koleksi buku yang lengkap dan nyaman untuk belajar.",
        "img_url": "https://placehold.co/600x400",
        "action_link": "#"
    },
    {
        "id": 3,
        "title": "Lapangan Olahraga",
        "description": "Lapangan olahraga multifungsi yang dapat digunakan untuk berbagai jenis olahraga.",
        "img_url": "https://placehold.co/600x400",
        "action_link": "#"
    }
]

# Menyisipkan data ke dalam koleksi
db.ekstrakulikuler.insert_many(ekstrakulikuler_data)
db.galeri.insert_many(galeri_data)
db.sarpras.insert_many(sarpras_data)

print("Data berhasil dimasukkan ke dalam database MongoDB")
