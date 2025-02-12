@echo off
@REM Debug: python -i script.py %1  --  -i (interactive mode) keeps Python running after script finishes, allowing to inspect variables and manually run additional commands
start /b python script.py %1
exit