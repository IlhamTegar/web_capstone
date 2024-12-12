import os
from app import create_app

def main():
    # Tentukan mode debug dari environment variable
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    # Buat aplikasi dari factory function
    app = create_app()

    # Logging untuk mode debug
    if debug_mode:
        app.logger.info("Aplikasi berjalan dalam mode debug.")

    # Jalankan aplikasi
    app.run(debug=debug_mode)

if __name__ == "__main__":
    main()
