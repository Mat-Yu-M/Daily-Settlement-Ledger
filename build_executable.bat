@echo off
REM Build script for Daily Settlement Ledger executable
echo Building Daily Settlement Ledger executable...
pyinstaller --onefile --console --name "DailySettlementLedger" ledger.py
echo.
echo Build complete! Executable is located in: dist\DailySettlementLedger.exe
pause

