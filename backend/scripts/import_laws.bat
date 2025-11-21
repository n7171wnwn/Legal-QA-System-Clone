@echo off
chcp 65001 >nul
echo ========================================
echo 法律法规数据导入工具
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo [1/4] 检查Python依赖...
pip show pymysql >nul 2>&1
if errorlevel 1 (
    echo [2/4] 安装Python依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo [1/4] Python依赖已安装
)

REM 设置仓库路径
set REPO_PATH=
set /p REPO_PATH="请输入LawRefBook/Laws仓库路径（或直接回车使用默认路径 E:\Laws）: "
if "%REPO_PATH%"=="" set REPO_PATH=E:\Laws

REM 检查仓库路径是否存在
if not exist "%REPO_PATH%" (
    echo.
    echo [提示] 仓库路径不存在: %REPO_PATH%
    echo 是否要克隆仓库？
    set /p CLONE_REPO="输入 y 克隆仓库，或 n 退出: "
    if /i "%CLONE_REPO%"=="y" (
        echo [3/4] 正在克隆仓库...
        git clone --depth 1 https://github.com/LawRefBook/Laws.git "%REPO_PATH%"
        if errorlevel 1 (
            echo [错误] 克隆仓库失败
            pause
            exit /b 1
        )
    ) else (
        echo 已取消
        pause
        exit /b 0
    )
) else (
    echo [2/4] 仓库路径存在: %REPO_PATH%
)

REM 设置数据库密码
set DB_PASSWORD=
set /p DB_PASSWORD="请输入数据库密码（默认: hjj060618）: "
if "%DB_PASSWORD%"=="" set DB_PASSWORD=hjj060618

REM 运行导入脚本
echo.
echo [3/4] 开始导入数据...
echo ========================================
python import_laws_data.py --repo-path "%REPO_PATH%" --password "%DB_PASSWORD%"

if errorlevel 1 (
    echo.
    echo [错误] 导入失败
    pause
    exit /b 1
) else (
    echo.
    echo [4/4] 导入完成！
    echo ========================================
)

pause

