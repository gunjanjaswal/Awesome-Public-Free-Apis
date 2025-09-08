@echo off
REM Setup Git hooks for the repository

REM Create hooks directory if it doesn't exist
if not exist .git\hooks mkdir .git\hooks

REM Copy pre-commit hook
copy /Y .github\hooks\pre-commit .git\hooks\
echo Git hooks installed successfully!
