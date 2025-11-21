# 数据导入脚本

本目录包含用于从外部数据源导入法律法规数据的脚本。

## 文件说明

### 主要脚本

- `import_laws_data.py` - 主要的 Python 导入脚本（已修复法条合并问题）
- `reimport_laws.py` - 清理并重新导入脚本（推荐用于修复数据）
- `requirements.txt` - Python 依赖包列表

### 快速启动脚本

- `import_laws.bat` - Windows 快速启动脚本（首次导入）
- `import_laws.sh` - Linux/Mac 快速启动脚本（首次导入）
- `reimport_laws.bat` - Windows 重新导入脚本（修复数据）

### 工具脚本

- `check_database.py` - 检查数据库中的数据
- `check_merged_articles.py` - 检查是否有合并的法条
- `fix_merged_articles.py` - 修复合并的法条（实验性）
- `verify_import.py` - 验证导入结果

### 文档

- `IMPORT_GUIDE.md` - 详细的导入指南
- `REIMPORT_GUIDE.md` - 清理并重新导入指南
- `如何查看导入的数据.md` - 查看数据指南

## 快速开始

### 首次导入数据

#### Windows

```bash
cd backend/scripts
import_laws.bat
```

#### Linux/Mac

```bash
cd backend/scripts
chmod +x import_laws.sh
./import_laws.sh
```

### 修复数据（清理并重新导入）

#### Windows（推荐）

```bash
cd backend/scripts
reimport_laws.bat
```

#### 手动运行

```bash
# 清理所有数据并重新导入
python reimport_laws.py --repo-path "E:\Laws\Laws" --password "hjj060618" --clear-all

# 只修复特定类型的法律（如刑法）
python reimport_laws.py --repo-path "E:\Laws\Laws" --password "hjj060618" --clear-types 刑法 --import-types 刑法
```

## 详细文档

- [IMPORT_GUIDE.md](IMPORT_GUIDE.md) - 首次导入指南
- [REIMPORT_GUIDE.md](REIMPORT_GUIDE.md) - 清理并重新导入指南（修复数据）

## 重要提示

⚠️ **如果发现法条合并问题**（第一条包含第二条的内容），请使用 `reimport_laws.py` 脚本清理并重新导入数据。修复后的导入脚本使用位置索引精确分割法条，避免了合并问题。
