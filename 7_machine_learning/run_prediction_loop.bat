@echo off
title ML Prediction - Auto Loop (5 menit)
color 0D

echo ============================================================
echo    MACHINE LEARNING - AUTO PREDICTION LOOP
echo    Interval: 5 menit
echo ============================================================
echo.
echo   Tekan Ctrl+C untuk berhenti.
echo.

:loop
echo.
echo ============================================================
echo [%date% %time%] Menjalankan prediksi...
echo ============================================================

cd /d C:\Users\jacin\Documents\Streaming_AnalyticsSahamTL
call venv\Scripts\activate
cd 7_machine_learning
python predict.py

echo.
echo [WAIT] Menunggu 5 menit (300 detik)...
timeout /t 300 /nobreak >nul

goto loop