@echo off
title ML Prediction - Auto Run
color 0D

echo ============================================================
echo    MACHINE LEARNING - PREDIKSI HARGA SAHAM
echo    Linear Regression - Auto Run
echo ============================================================
echo.

cd /d C:\Users\jacin\Documents\Streaming_AnalyticsSahamTL
call venv\Scripts\activate
cd 7_machine_learning

echo [1/2] Menjalankan prediksi...
python predict.py

echo.
echo [2/2] Selesai. Prediksi tersimpan di PostgreSQL.
echo.
echo ============================================================
echo    PREDIKSI BERHASIL DIPERBARUI
echo ============================================================
echo.
echo   Target waktu: 1 jam ke depan
echo   Model: Linear Regression
echo   Data: 5 saham Timor-Leste
echo.
echo   Untuk lihat hasil:
echo     - Buka dashboard: http://localhost:8501
echo     - Pilih tab: "Prediction (ML)"
echo.
echo ============================================================