import re
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.controllers.until import generate_otp, save_otp_to_db, send_email, generate_reset_token, send_reset_email, verify_reset_token
from app.extensions import db, bcrypt
from app.models import User, OTP
from datetime import datetime

# Blueprint untuk controller_user
user_bp = Blueprint('user', __name__)

# Halaman Profile
@user_bp.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    # Validasi user ID dari session (opsional)
    if session.get('user_id') != user_id:
        flash("Anda tidak memiliki akses ke profil ini.", "danger")
        return redirect(url_for('pg.home'))

    user = User.query.get(user_id)
    if not user:
        flash("User tidak ditemukan.", "danger")
        return redirect(url_for('pg.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        alamat = request.form.get('alamat')
        waktu_buka = request.form.get('waktu_buka')
        waktu_tutup = request.form.get('waktu_tutup')
        rentang_harga_murah = request.form.get('rentang_harga_murah')
        rentang_harga_mahal = request.form.get('rentang_harga_mahal')
        kontak_nomor = request.form.get('kontak_nomor')

        # Validasi input
        if not username or not alamat or not waktu_buka or not waktu_tutup:
            flash("Semua field wajib diisi kecuali password!", "danger")
            return redirect(url_for('user.profile', user_id=user_id))

        try:
            user.waktu_buka = datetime.strptime(waktu_buka, '%H:%M').time()
            user.waktu_tutup = datetime.strptime(waktu_tutup, '%H:%M').time()
            user.rentang_harga_murah = int(rentang_harga_murah) if rentang_harga_murah else None
            user.rentang_harga_mahal = int(rentang_harga_mahal) if rentang_harga_mahal else None
            if user.rentang_harga_murah and user.rentang_harga_mahal:
                if user.rentang_harga_murah > user.rentang_harga_mahal:
                    flash("Harga minimum tidak boleh lebih besar dari harga maksimum.", "danger")
                    return redirect(url_for('user.profile', user_id=user_id))
        except ValueError:
            flash("Format waktu atau angka tidak valid!", "danger")
            return redirect(url_for('user.profile', user_id=user_id))

        if kontak_nomor and (not kontak_nomor.isdigit() or len(kontak_nomor) < 10 or len(kontak_nomor) > 15):
            flash("Nomor kontak hanya boleh berupa angka dan panjangnya 10-15 karakter!", "danger")
            return redirect(url_for('user.profile', user_id=user_id))

        # Update data user
        user.username = username
        user.alamat = alamat
        user.kontak_nomor = kontak_nomor

        if password:
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')

        db.session.commit()
        flash("Profil berhasil diperbarui!", "success")
        return redirect(url_for('user.profile', user_id=user_id))

    return render_template('profile.html', user=user, user_id=user_id)

# Login
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Ambil user berdasarkan email
        user = User.query.filter_by(email=email).first()

        # Debugging Output
        print(f"Email: {email}, Password Input: {password}")
        if user:
            print(f"User Found: {user.username}, Hashed Password: {user.password}")
        else:
            print("User not found.")

        # Validasi user dan password
        if user and bcrypt.check_password_hash(user.password, password):
            print("Password match!")  # Debug log
            session['user_id'] = user.id
            session['username'] = user.username
            flash("Login berhasil!", "success")
            return redirect(url_for('pg.home'))
        else:
            print("Password mismatch!")  # Debug log
            flash("Email atau password salah.", "danger")
        return redirect(url_for('user.login'))


    return render_template('login.html')

# Forget password
@user_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash("Email tidak ditemukan.", "danger")
            return redirect(url_for('user.forgot_password'))

        # Generate token (contoh menggunakan serializer)
        token = generate_reset_token(user.email)

        # Kirim email (implementasi send_email ada di langkah 3)
        send_reset_email(user.email, token)

        flash("Email reset password telah dikirim. Silakan cek email Anda.", "success")
        return redirect(url_for('user.login'))

    return render_template('forgot_password.html')

# Reset password
@user_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = verify_reset_token(token)  # Verifikasi token
    except:
        flash("Token reset password tidak valid atau telah kedaluwarsa.", "danger")
        return redirect(url_for('user.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Terjadi kesalahan. Silakan ulangi proses reset password.", "danger")
            return redirect(url_for('user.forgot_password'))

        # Update password
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        db.session.commit()

        flash("Password berhasil diubah. Silakan login dengan password baru.", "success")
        return redirect(url_for('user.login'))

    return render_template('reset_password.html', email=email)

# Register
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validasi input
        if not username or not email or not password:
            flash("Semua field wajib diisi!", "danger")
            return redirect(url_for('user.register'))

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            flash("Format email tidak valid!", "danger")
            return redirect(url_for('user.register'))

        if User.query.filter_by(email=email).first():
            flash("Email sudah terdaftar.", "danger")
            return redirect(url_for('user.register'))

        # Kirim OTP ke email
        otp = generate_otp()  # Fungsi untuk membuat OTP
        save_otp_to_db(email, otp)  # Simpan OTP ke database
        send_email(email, otp)  # Fungsi eksternal untuk mengirim OTP via email
        session['register_data'] = {'username': username, 'email': email, 'password': password}

        flash("Kode OTP telah dikirim ke email Anda. Masukkan kode untuk verifikasi.", "info")
        return redirect(url_for('user.verify_otp', email=email))

    return render_template('register.html')

# Otp
@user_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    # Ambil email dari parameter URL
    email = request.args.get('email')
    if not email:
        flash("Email tidak ditemukan. Silakan ulangi proses verifikasi.", "danger")
        return redirect(url_for('user.register'))

    if request.method == 'POST':
        otp_input = request.form.get('otp')  # Ambil OTP dari form

        # Validasi input OTP
        if not otp_input:
            flash("Kode OTP tidak boleh kosong.", "danger")
            return redirect(url_for('user.verify_otp', email=email))

        # Cari entri OTP berdasarkan email
        otp_entry = OTP.query.filter_by(email=email).first()
        if not otp_entry:
            flash("Kode OTP tidak ditemukan.", "danger")
            return redirect(url_for('user.verify_otp', email=email))

        # Validasi apakah OTP masih valid
        if not otp_entry.is_valid():
            flash("Kode OTP telah kedaluwarsa. Silakan minta kode OTP baru.", "danger")
            db.session.delete(otp_entry)  # Hapus OTP kedaluwarsa
            db.session.commit()
            return redirect(url_for('user.request_otp'))

        # Periksa kecocokan OTP
        if otp_entry.otp_code != otp_input:  # Pastikan kolom di model adalah `otp_code`
            flash("Kode OTP salah.", "danger")
            return redirect(url_for('user.verify_otp', email=email))

        # Ambil data registrasi dari sesi
        register_data = session.pop('register_data', None)
        if not register_data:
            flash("Data registrasi tidak ditemukan. Silakan ulangi proses pendaftaran.", "danger")
            return redirect(url_for('user.register'))

        # Tambahkan user ke database
        try:
            user = User(
                username=register_data['username'],
                email=register_data['email'],
                password=bcrypt.generate_password_hash(register_data['password']).decode('utf-8')
            )
            db.session.add(user)
            db.session.delete(otp_entry)  # Hapus OTP setelah berhasil diverifikasi
            db.session.commit()

            flash("Verifikasi berhasil! Akun Anda telah terdaftar.", "success")
            return redirect(url_for('user.login'))
        except Exception as e:
            db.session.rollback()
            flash("Terjadi kesalahan saat menyimpan data pengguna. Silakan coba lagi.", "danger")
            print(f"Error: {e}")  # Debugging
            return redirect(url_for('user.verify_otp', email=email))

    # Jika metode GET, tampilkan halaman verifikasi OTP
    return render_template('verify_otp.html', email=email)

# Logout
@user_bp.route('/logout')
def logout():
    session.clear()
    # flash("Logout berhasil!", "success")
    return redirect(url_for('pg.home'))

# Delete akun
@user_bp.route('/delete-account', methods=['POST'])
def delete_account():
    user_id = session.get('user_id')
    if not user_id:
        flash("Anda harus login untuk menghapus akun.", "danger")
        return redirect(url_for('user.login'))

    user = User.query.get(user_id)
    if not user:
        flash("Pengguna tidak ditemukan.", "danger")
        return redirect(url_for('pg.home'))

    # Hapus pengguna dari database
    db.session.delete(user)
    db.session.commit()

    # Hapus sesi setelah akun dihapus
    session.clear()

    flash("Akun Anda berhasil dihapus.", "success")
    return redirect(url_for('pg.home'))
