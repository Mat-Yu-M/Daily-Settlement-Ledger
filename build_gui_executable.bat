@echo off
REM Build script for Daily Settlement Ledger GUI executable
echo Building Daily Settlement Ledger GUI executable...
pyinstaller --onefile --windowed --name "DailySettlementLedgerGUI" ledger_gui.py
echo.
echo Build complete! Executable is located in: dist\DailySettlementLedgerGUI.exe
echo Note: --windowed flag removes the console window for GUI application
pause

