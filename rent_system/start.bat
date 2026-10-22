@echo off
chcp 65001 >nul
cd /d %~dp0

echo ============================================
echo   基于Python的房屋租赁管理系统 - 一键启动
echo ============================================

REM ========== 1. 启动 Redis（后台分离启动，切勿前台运行） ==========
set "REDIS_EXE="
if exist "%~dp0redis\Redis-8.10.2-Windows-x64-msys2\redis-server.exe" (
    set "REDIS_EXE=%~dp0redis\Redis-8.10.2-Windows-x64-msys2\redis-server.exe"
) else if exist "%~dp0..\redis\Redis-8.10.2-Windows-x64-msys2\redis-server.exe" (
    set "REDIS_EXE=%~dp0..\redis\Redis-8.10.2-Windows-x64-msys2\redis-server.exe"
)
if defined REDIS_EXE (
    echo [1/4] 启动 Redis 服务（端口 6379，后台分离）...
    start "Redis-Server" "%REDIS_EXE%" --port 6379
) else (
    echo [1/4] 未检测到 Redis，跳过（系统仍可正常运行）
)

REM ========== 2. 准备 Python 环境 ==========
echo [2/4] 检查 Python 虚拟环境...
set "PY=python"
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set "PY=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
)
if not exist "venv\Scripts\python.exe" (
    echo       首次运行，创建虚拟环境 venv ...
    %PY% -m venv venv
)
set "PY=venv\Scripts\python.exe"
echo       安装/更新依赖...
%PY% -m pip install -r requirements.txt --quiet

REM ========== 3. 数据库迁移 ==========
echo [3/4] 数据库迁移...
%PY% manage.py migrate

REM ========== 4. 启动后端与前端 ==========
echo [4/4] 启动 Django（8000）与 Vue 前端（5173）...
start "Django-Server" cmd /k "%PY% manage.py runserver 8000"
start "Vue-Dev" cmd /k "cd /d %~dp0frontend && npm run dev"

timeout /t 3 /nobreak >nul
start "" http://127.0.0.1:5173/
start "" http://127.0.0.1:8000/admin/

echo.
echo ============================================
echo   启动完成！
echo   前端首页:  http://127.0.0.1:5173/
echo   管理后台:  http://127.0.0.1:8000/admin/   ^(账号 admin / admin123456^)
echo.
echo   注意：首次使用前端需先安装 Node.js
echo        （文件夹内 node-v24.22.0-x64-installer.msi）
echo        并在 frontend 目录执行一次 npm install
echo ============================================
pause
