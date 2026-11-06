@echo off
title Capstone - Stop All Services (GRACEFUL)
color 0E

echo ============================================================
echo    STOPPING ALL SERVICES - GRACEFUL SHUTDOWN
echo ============================================================
echo.
echo   SCRIPT INI TIDAK MEMATIKAN PAKSA JAVA (SPARK/KAFKA)
echo   Hanya PostgreSQL yang di-stop otomatis.
echo.
echo   Untuk Spark, Kafka, Producer, Streamlit:
echo   Anda harus Ctrl+C secara MANUAL di CMD masing-masing.
echo.
echo ============================================================
echo.
echo   URUTAN SHUTDOWN YANG BENAR:
echo.
echo   [1] Streamlit Dashboard
echo       - Buka CMD Streamlit, tekan Ctrl+C sekali
echo.
echo   [2] Spark Streaming
echo       - Buka CMD Spark, tekan Ctrl+C sekali
echo       - TUNGGU 15 detik sampai muncul:
echo           [STOP] Dihentikan oleh user
echo           [OK] Spark Streaming dihentikan
echo       - JANGAN pakai taskkill /F untuk Spark!
echo.
echo   [3] Kafka Producer
echo       - Buka CMD Producer, tekan Ctrl+C sekali
echo.
echo   [4] Kafka Server
echo       - Buka CMD Kafka, tekan Ctrl+C sekali
echo       - TUNGGU 15 detik
echo.
echo   [5] PostgreSQL
echo       - Akan di-stop otomatis oleh script ini
echo.
echo ============================================================
echo.
echo   Tekan tombol apa saja untuk STOP PostgreSQL...
echo.
pause >nul

echo.
echo [5/5] Stopping PostgreSQL...
C:\PostgreSQL\17\bin\pg_ctl -D C:\PostgreSQL\17\data stop

echo.
echo ============================================================
echo    POSTGRESQL STOPPED
echo ============================================================
echo.
echo   Pastikan Anda sudah Ctrl+C di CMD berikut:
echo     - Streamlit Dashboard
echo     - Spark Streaming
echo     - Kafka Producer
echo     - Kafka Server
echo.
echo   Jika belum, lakukan sekarang sebelum tutup laptop.
echo.
echo ============================================================
pause