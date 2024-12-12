import random
from flask_mail import Message
from app.extensions import mail, db
from datetime import datetime, timedelta
from app.models import OTP
from itsdangerous import URLSafeTimedSerializer
from flask import current_app, url_for
from flask_mail import Message
from app import mail

def generate_otp(length=6):
    """Membuat kode OTP acak dengan panjang tertentu."""
    return ''.join(random.choices('0123456789', k=length))

def send_email(recipient, otp):
    """Kirim email dengan subjek dan isi untuk OTP."""
    subject = "Kode Verifikasi Akun Anda"
    body = f"Kode OTP Anda adalah: {otp}. Kode ini berlaku selama 5 menit."
    msg = Message(subject=subject, recipients=[recipient], body=body)
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error saat mengirim email: {e}")
        return False

def is_email_valid(email):
    """Validasi sederhana untuk email."""
    import re
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def clean_expired_otp():
    """Hapus OTP yang sudah kedaluwarsa."""
    expiry_time = datetime.utcnow() - timedelta(minutes=10)  # Contoh: OTP kedaluwarsa setelah 10 menit
    OTP.query.filter(OTP.timestamp < expiry_time).delete()  # Hapus OTP yang kedaluwarsa
    db.session.commit()

def save_otp_to_db(email, otp_code):
    """Simpan OTP ke database."""
    from app.models import OTP  # Import model OTP

    # Hapus OTP yang sudah kedaluwarsa
    clean_expired_otp()

    # Simpan OTP baru ke database
    new_otp = OTP(email=email, otp_code=otp_code)
    db.session.add(new_otp)
    db.session.commit()

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
    except:
        return None
    return email

def send_reset_email(email, token):
    reset_url = url_for('user.reset_password', token=token, _external=True)
    msg = Message("Reset Password", sender="noreply@yourapp.com", recipients=[email])
    msg.body = f"Klik link berikut untuk mereset password Anda: {reset_url}"
    mail.send(msg)

# def save_otp_to_db(email, otp):
#     clean_expired_otp()
#     otp_entry = OTP.query.filter_by(email=email).first()
#     if otp_entry:
#         otp_entry.otp = otp
#         otp_entry.timestamp = datetime.utcnow()
#     else:
#         otp_entry = OTP(email=email, otp=otp, timestamp=datetime.utcnow())
#         db.session.add(otp_entry)
#     db.session.commit()
