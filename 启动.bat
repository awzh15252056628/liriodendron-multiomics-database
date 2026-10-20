@echo off
chcp 65001 >nul
title 鹅掌楸数据库 - 启动中...
cd /d "%~dp0"

echo ================================================
echo   鹅掌楸多组学数据库 LMDB  v3.0
echo   正在启动基因组查询服务...
echo ================================================
echo.

:: ── 查找 Python ──────────────────────────────────────────────────
set PYTHON=

:: 1. 检查 PATH 中的 python
python --version >nul 2>&1
if %errorlevel%==0 (
    set PYTHON=python
    goto :found
)

:: 2. 检查 PATH 中的 python3
python3 --version >nul 2>&1
if %errorlevel%==0 (
    set PYTHON=python3
    goto :found
)

:: 3. 搜索常见安装位置
for %%P in (
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python39\python.exe"
    "C:\Python313\python.exe"
    "C:\Python312\python.exe"
    "C:\Python311\python.exe"
    "C:\Python310\python.exe"
    "C:\Python39\python.exe"
    "F:\pymol\python.exe"
    "%USERPROFILE%\Anaconda3\python.exe"
    "%USERPROFILE%\miniconda3\python.exe"
    "C:\ProgramData\Anaconda3\python.exe"
    "C:\ProgramData\miniconda3\python.exe"
    "%LOCALAPPDATA%\anaconda3\python.exe"
    "%LOCALAPPDATA%\miniconda3\python.exe"
) do (
    if exist %%P (
        set PYTHON=%%P
        goto :found
    )
)

:: 4. No Python: open the static page directly.
echo [INFO] Python not found. Opening index.html directly...
where node >nul 2>&1
if not errorlevel 1 if exist "%~dp0..\preview-liriodendron.cjs" (
    start "LMDB local preview" /min node "%~dp0..\preview-liriodendron.cjs" "%~dp0" 8765
    timeout /t 1 /nobreak >nul
    start "" "http://localhost:8765/"
    exit /b 0
)
start "" "%~dp0index.html"
exit /b 0

:found
echo [OK] Python: %PYTHON%
echo.

:: ── 检查端口是否已占用 ────────────────────────────────────────────
netstat -ano | findstr ":7788 " >nul 2>&1
if %errorlevel%==0 (
    echo [INFO] 基因组服务器已在运行 (port 7788)
    goto :open_browser
)

:: ── 启动基因组查询服务器 (后台窗口) ────────────────────────────────
echo [启动] 基因组序列查询服务器...
start "LMDB 基因组服务器" /min %PYTHON% "%~dp0genome_server.py"

:: ── 等待服务器就绪 ────────────────────────────────────────────────
echo [等待] 服务器初始化中 (最多15秒)...
set /a tries=0
:wait_loop
timeout /t 1 /nobreak >nul
set /a tries+=1
%PYTHON% -c "import urllib.request; urllib.request.urlopen('http://localhost:7788/ping', timeout=2)" >nul 2>&1
if %errorlevel%==0 goto :server_ready
if %tries% lss 15 goto :wait_loop

echo [警告] 服务器启动较慢，将继续打开数据库...
echo        基因序列查询功能将在服务器就绪后自动可用。
goto :open_browser

:server_ready
echo [OK] 基因组服务器已就绪！
echo.

:open_browser
:: ── 打开数据库主页 ────────────────────────────────────────────────
echo [打开] 数据库主页...
start "" "%~dp0index.html"

echo.
echo ================================================
echo   数据库已启动！请在浏览器中使用。
echo   基因组服务: http://localhost:7788
echo   关闭此窗口不会停止基因组服务器。
echo ================================================
echo.
timeout /t 3 /nobreak >nul
exit /b 0
