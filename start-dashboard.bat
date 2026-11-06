@echo off
title Capstone - Dashboard
color 0D
cd C:\Users\jacin\Documents\Streaming_AnalyticsSahamTL
call venv\Scripts\activate
cd 6_visualization
echo Starting Streamlit Dashboard...
echo Dashboard akan terbuka di http://localhost:8501
echo.
streamlit run app.py