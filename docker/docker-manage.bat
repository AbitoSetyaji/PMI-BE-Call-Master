@echo off
REM PMI Emergency Call System - Docker Management Script for Windows

:MENU
cls
echo ========================================
echo   PMI Emergency Call System - Docker
echo ========================================
echo.
echo Please select an option:
echo.
echo 1. Start services
echo 2. Stop services
echo 3. Restart services
echo 4. View logs
echo 5. Check status
echo 6. Access MySQL shell
echo 7. Run migrations
echo 8. Initialize transport system
echo 9. Show credentials
echo 10. Reset all (WARNING: deletes all data)
echo 0. Exit
echo.

set /p choice="Enter your choice: "

if "%choice%"=="1" goto START
if "%choice%"=="2" goto STOP
if "%choice%"=="3" goto RESTART
if "%choice%"=="4" goto LOGS
if "%choice%"=="5" goto STATUS
if "%choice%"=="6" goto MYSQL
if "%choice%"=="7" goto MIGRATE
if "%choice%"=="8" goto INIT
if "%choice%"=="9" goto CREDS
if "%choice%"=="10" goto RESET
if "%choice%"=="0" goto EXIT
goto INVALID

:START
echo.
echo Starting PMI Emergency Call System...
docker-compose up -d --build
echo.
echo Services started successfully!
echo View logs with: docker-compose logs -f
echo API available at: http://localhost:8000
echo API Docs at: http://localhost:8000/docs
pause
goto MENU

:STOP
echo.
echo Stopping services...
docker-compose down
echo.
echo Services stopped
pause
goto MENU

:RESTART
echo.
echo Restarting services...
docker-compose restart
echo.
echo Services restarted
pause
goto MENU

:LOGS
echo.
echo Viewing logs (Press Ctrl+C to exit)...
docker-compose logs -f
pause
goto MENU

:STATUS
echo.
echo Service Status:
docker-compose ps
echo.
pause
goto MENU

:MYSQL
echo.
echo Connecting to MySQL...
docker-compose exec mysql mysql -u pmi_user -ppmi_password pmi_emergency
pause
goto MENU

:MIGRATE
echo.
echo Running database migrations...
docker-compose exec app alembic upgrade head
echo.
echo Migrations completed
pause
goto MENU

:INIT
echo.
echo Initializing transport system...
docker-compose exec app python init_transport_system.py
echo.
echo Transport system initialized
pause
goto MENU

:CREDS
cls
echo ========================================
echo   Default User Credentials
echo ========================================
echo.
echo Admin User:
echo    Email: admin@pmi.org
echo    Password: admin123
echo.
echo Driver User:
echo    Email: driver@pmi.org
echo    Password: driver123
echo.
echo Reporter User:
echo    Email: reporter@pmi.org
echo    Password: reporter123
echo.
echo ========================================
echo   Database Credentials
echo ========================================
echo.
echo    Host: localhost
echo    Port: 3306
echo    Database: pmi_emergency
echo    User: pmi_user
echo    Password: pmi_password
echo.
pause
goto MENU

:RESET
echo.
echo WARNING: This will delete ALL data!
set /p confirm="Are you sure you want to continue? (yes/no): "
if /i "%confirm%"=="yes" (
    echo.
    echo Removing all containers and volumes...
    docker-compose down -v
    echo.
    echo Everything has been reset
) else (
    echo Cancelled
)
pause
goto MENU

:INVALID
echo.
echo Invalid option. Please try again.
pause
goto MENU

:EXIT
echo.
echo Goodbye!
exit
