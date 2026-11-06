@echo off
title Capstone Project - Start All Services
color 0A

echo ============================================================
echo    CAPSTONE PROJECT - START ALL SERVICES
echo    Real-Time Stock Market Streaming Analytics
echo ============================================================
echo.

REM ============ STEP 1: PostgreSQL ============
echo [1/4] Starting PostgreSQL...
C:\PostgreSQL\17\bin\pg_ctl -D C:\PostgreSQL\17\data status >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    C:\PostgreSQL\17\bin\pg_ctl -D C:\PostgreSQL\17\data -l C:\PostgreSQL\17\logfile.txt start
    echo       PostgreSQL started.
) else (
    echo       PostgreSQL already running.
)
timeout /t 3 /nobreak >nul

REM ============ STEP 2: Kafka Server ============
echo.
echo [2/4] Starting Kafka Server...
start "KAFKA SERVER" cmd /k "color 0E && cd C:\kafka && bin\windows\kafka-server-start.bat config\kraft\server-saham-tl.properties"
echo       Waiting 20 seconds for Kafka to be ready...
timeout /t 20 /nobreak >nul

REM ============ STEP 3: Kafka Producer ============
echo.
echo [3/4] Starting Kafka Producer...
start "KAFKA PRODUCER" cmd /k "color 0B && cd C:\Users\jacin\Documents\Streaming_AnalyticsSahamTL && venv\Scripts\activate && cd 2_data_ingestion && python kafka_producer.py"
timeout /t 5 /nobreak >nul

REM ============ STEP 4: Spark Streaming ============
echo.
echo [4/4] Starting Spark Streaming...
start "SPARK STREAMING" cmd /k "color 0D && cd C:\Users\jacin\Documents\Streaming_AnalyticsSahamTL && venv\Scripts\activate && cd 3_stream_processing && python spark_streaming.py"
timeout /t 10 /nobreak >nul

echo.
echo ============================================================
echo    ALL SERVICES STARTED!
echo ============================================================
echo.
echo    Windows yang terbuka:
echo      1. PostgreSQL (background)
echo      2. KAFKA SERVER  (kuning)
echo      3. KAFKA PRODUCER (biru)
echo      4. SPARK STREAMING (ungu)
echo.
echo    Untuk dashboard, jalankan manual di CMD baru:
echo      cd C:\Users\jacin\Documents\Streaming_AnalyticsSahamTL
echo      venv\Scripts\activate
echo      cd 6_visualization
echo      streamlit run app.py
echo.
echo ============================================================
echo.
pause