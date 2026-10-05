@echo off
echo ===============================================
echo   BOUTIQUE LM - DEPLOY WIZARD
echo ===============================================
echo.
echo 1. Effettua il login a Google/Firebase...
call npx firebase login
echo.
echo 2. Seleziona il progetto Firebase (Boutique LM)...
echo    (Se richiesto, seleziona 'boutique-lm' dalla lista)
call npx firebase use --add
echo.
echo 3. Pubblicazione online in corso...
call npx firebase deploy
echo.
echo ===============================================
echo   Finito! Se non ci sono errori rosso, il sito e' online.
echo ===============================================
pause
