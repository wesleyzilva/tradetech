@echo off
REM ============================================================
REM  rodar_analise.bat — Executa todos os scripts de análise
REM  TradeTech / DadosCandlesBacktest
REM
REM  Uso manual:
REM    rodar_analise.bat
REM
REM  Agendamento (Windows Task Scheduler):
REM    schtasks /create /tn "TradeTech-Analise" /tr "C:\caminho\rodar_analise.bat" ^
REM             /sc DAILY /st 08:00 /ru SYSTEM
REM
REM  Para remover agendamento:
REM    schtasks /delete /tn "TradeTech-Analise" /f
REM ============================================================

setlocal

REM ── Configuração ─────────────────────────────────────────────
set PYTHON="C:\Program Files\Python312\python.exe"
set BASE_DIR=%~dp0DadosCandlesBacktest
set LOG_FILE=%~dp0DadosCandlesBacktest\analise_%date:~-4%-%date:~3,2%-%date:~0,2%.log

REM ── Cabeçalho do log ─────────────────────────────────────────
echo ============================================ > "%LOG_FILE%"
echo  TradeTech — Analise Automatizada           >> "%LOG_FILE%"
echo  Data: %date%  Hora: %time%                 >> "%LOG_FILE%"
echo ============================================ >> "%LOG_FILE%"

echo.
echo [TradeTech] Iniciando analise...
echo [TradeTech] Log: %LOG_FILE%
echo.

REM ── 1. Detector de areas S/R (novo) ──────────────────────────
echo [1/3] Detector de Areas (5min + 15min)...
cd /d "%BASE_DIR%"
%PYTHON% detector_areas.py --ativo todos --tfs 5min 15min >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo   [ERRO] detector_areas.py falhou. Ver log.
) else (
    echo   [OK] Areas geradas: areas_wdo.json / areas_win.json
)

REM ── 2. Tabela de cenarios de entrada ─────────────────────────
echo [2/3] Tabela de Cenarios...
%PYTHON% tabela_cenarios.py >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo   [ERRO] tabela_cenarios.py falhou. Ver log.
) else (
    echo   [OK] Tabela gerada
)

REM ── 3. Analise estatistica completa (mais lenta) ──────────────
echo [3/3] Analise Estatistica Completa...
%PYTHON% analise_forca_sl.py >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo   [ERRO] analise_forca_sl.py falhou. Ver log.
) else (
    echo   [OK] Resultados: resultados_analise_forca.json / stats_forte_vs_exaust.json
)

echo.
echo [TradeTech] Concluido. Resultados em: %BASE_DIR%
echo Fim: %time% >> "%LOG_FILE%"

REM ── Pausa apenas se executado manualmente (não via scheduler) ─
if "%1"=="--no-pause" goto :eof
pause
