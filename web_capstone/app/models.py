from datetime import datetime, timedelta
from .extensions import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Tambahan kolom untuk profil
    alamat = db.Column(db.String(255), nullable=True)  # Alamat pengguna
    waktu_buka = db.Column(db.Time, nullable=True)     # Jam buka
    waktu_tutup = db.Column(db.Time, nullable=True)    # Jam tutup
    rentang_harga_murah = db.Column(db.Integer, nullable=True)  # Rentang harga minimum
    rentang_harga_mahal = db.Column(db.Integer, nullable=True)  # Rentang harga maksimum
    kontak_nomor = db.Column(db.String(15), nullable=True)  # Nomor kontak

    def __init__(self, username, email, password, alamat=None, waktu_buka=None, waktu_tutup=None, rentang_harga_murah=None, rentang_harga_mahal=None, kontak_nomor=None):
        self.username = username
        self.email = email
        self.password = password
        self.alamat = alamat
        self.waktu_buka = waktu_buka
        self.waktu_tutup = waktu_tutup
        self.rentang_harga_murah = rentang_harga_murah
        self.rentang_harga_mahal = rentang_harga_mahal
        self.kontak_nomor = kontak_nomor

    def check_password(self, password):
        """Memeriksa kecocokan password."""
        return bcrypt.check_password_hash(self.password, password)

    @classmethod
    def find_by_email(cls, email):
        """Mencari user berdasarkan email."""
        return cls.query.filter_by(email=email).first()

    def __repr__(self):
        return f"<User {self.username} - {self.email}>"

class OTP(db.Model):
    __tablename__ = 'otp'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def is_valid(self):
        """Periksa apakah OTP masih valid (belum kedaluwarsa)."""
        expiry_time = self.timestamp + timedelta(minutes=5)  # Misalnya, berlaku 5 menit
        return datetime.utcnow() <= expiry_time