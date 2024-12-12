from flask import Blueprint, render_template, redirect, jsonify, flash
from app.extensions import db
from app.models import User

# Blueprint untuk controller_pg
pg_bp = Blueprint('pg', __name__)

# Home Page
@pg_bp.route('/')
def home():
    return render_template('home.html')

# Route untuk mengunduh aplikasi
@pg_bp.route('/unduh')
def unduh():
    apk_url = "https://yourserver.com/path/to/mypg_bp.apk"

    # Simulasi ketersediaan file
    file_available = False  # Ubah ke True jika file tersedia

    if file_available:
        return redirect(apk_url)
    else:
        flash("File belum tersedia. Silakan coba lagi nanti.", "info")
        return render_template("home.html")

# Route untuk halaman afiliasi
@pg_bp.route('/afiliasi')
def afiliasi():
    users = User.query.all()  # Ambil objek User langsung
    return render_template('afi_page.html', users=users)
