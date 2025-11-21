@echo off
chcp 65001 >nul
echo ========================================
echo 清理并重新导入法律法规数据
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

REM 设置仓库路径
set REPO_PATH=
set /p REPO_PATH="请输入LawRefBook/Laws仓库路径（默认: E:\Laws\Laws）: "
if "%REPO_PATH%"=="" set REPO_PATH=E:\Laws\Laws

REM 检查仓库路径是否存在
if not exist "%REPO_PATH%" (
    echo [错误] 仓库路径不存在: %REPO_PATH%
    pause
    exit /b 1
)

REM 设置数据库密码
set DB_PASSWORD=
set /p DB_PASSWORD="请输入数据库密码（默认: hjj060618）: "
if "%DB_PASSWORD%"=="" set DB_PASSWORD=hjj060618

REM 选择清理选项
echo.
echo 请选择清理选项:
echo 1. 清理所有法条数据（重新导入全部）
echo 2. 清理指定类型的法条（如：刑法、民法）
echo 3. 跳过清理，直接导入（会自动去重）
set /p CLEAR_OPTION="请输入选项 (1/2/3，默认: 3): "
if "%CLEAR_OPTION%"=="" set CLEAR_OPTION=3

REM 构建命令
set CMD=python reimport_laws.py --repo-path "%REPO_PATH%" --password "%DB_PASSWORD%"

if "%CLEAR_OPTION%"=="1" (
    set CMD=%CMD% --clear-all
) else if "%CLEAR_OPTION%"=="2" (
    set /p CLEAR_TYPES="请输入要清理的法律类型（用空格分隔，如：刑法 民法）: "
    if not "%CLEAR_TYPES%"=="" (
        set CMD=%CMD% --clear-types %CLEAR_TYPES%
    )
) else (
    set CMD=%CMD% --skip-clear
)

REM 询问是否只导入特定类型
set /p IMPORT_TYPES="是否只导入特定类型的法律？（留空导入全部，或用空格分隔，如：刑法 民法）: "
if not "%IMPORT_TYPES%"=="" (
    set CMD=%CMD% --import-types %IMPORT_TYPES%
)

REM 运行脚本
echo.
echo ========================================
echo 开始执行...
echo ========================================
echo.

%CMD%

if errorlevel 1 (
    echo.
    echo [错误] 执行失败
    pause
    exit /b 1
) else (
    echo.
    echo [完成] 操作成功完成！
)

pause

