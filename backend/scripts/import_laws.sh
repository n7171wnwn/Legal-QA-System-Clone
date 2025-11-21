#!/bin/bash

echo "========================================"
echo "法律法规数据导入工具"
echo "========================================"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到Python3，请先安装Python 3.7+"
    exit 1
fi

# 检查依赖是否安装
echo "[1/4] 检查Python依赖..."
if ! python3 -c "import pymysql" &> /dev/null; then
    echo "[2/4] 安装Python依赖..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[错误] 依赖安装失败"
        exit 1
    fi
else
    echo "[1/4] Python依赖已安装"
fi

# 设置仓库路径
read -p "请输入LawRefBook/Laws仓库路径（或直接回车使用默认路径 ~/Laws）: " REPO_PATH
if [ -z "$REPO_PATH" ]; then
    REPO_PATH="$HOME/Laws"
fi

# 检查仓库路径是否存在
if [ ! -d "$REPO_PATH" ]; then
    echo ""
    echo "[提示] 仓库路径不存在: $REPO_PATH"
    read -p "是否要克隆仓库？(y/n): " CLONE_REPO
    if [ "$CLONE_REPO" = "y" ] || [ "$CLONE_REPO" = "Y" ]; then
        echo "[3/4] 正在克隆仓库..."
        git clone --depth 1 https://github.com/LawRefBook/Laws.git "$REPO_PATH"
        if [ $? -ne 0 ]; then
            echo "[错误] 克隆仓库失败"
            exit 1
        fi
    else
        echo "已取消"
        exit 0
    fi
else
    echo "[2/4] 仓库路径存在: $REPO_PATH"
fi

# 设置数据库密码
read -p "请输入数据库密码（默认: hjj060618）: " DB_PASSWORD
if [ -z "$DB_PASSWORD" ]; then
    DB_PASSWORD="hjj060618"
fi

# 运行导入脚本
echo ""
echo "[3/4] 开始导入数据..."
echo "========================================"
python3 import_laws_data.py --repo-path "$REPO_PATH" --password "$DB_PASSWORD"

if [ $? -ne 0 ]; then
    echo ""
    echo "[错误] 导入失败"
    exit 1
else
    echo ""
    echo "[4/4] 导入完成！"
    echo "========================================"
fi

