# 法律法规数据导入指南

本指南说明如何从 [LawRefBook/Laws](https://github.com/LawRefBook/Laws) 仓库导入法律法规数据到本项目的数据库中。

## 前置要求

1. Python 3.7+
2. MySQL 数据库已创建并运行
3. 已安装项目依赖

## 步骤 1: 克隆 LawRefBook/Laws 仓库

首先需要将 LawRefBook/Laws 仓库克隆到本地：

```bash
# 在项目根目录或任意位置克隆仓库
git clone https://github.com/LawRefBook/Laws.git

# 或者使用浅克隆（更快）
git clone --depth 1 https://github.com/LawRefBook/Laws.git
```

## 步骤 2: 安装 Python 依赖

```bash
cd backend/scripts
pip install -r requirements.txt
```

或者使用 pip3：

```bash
pip3 install -r requirements.txt
```

## 步骤 3: 配置数据库连接

编辑导入脚本或使用命令行参数指定数据库连接信息。

### 方法 1: 使用命令行参数（推荐）

```bash
python import_laws_data.py \
    --repo-path /path/to/Laws \
    --host localhost \
    --port 3306 \
    --user root \
    --password your_password \
    --database legal_qa
```

### 方法 2: 修改脚本中的默认配置

编辑 `import_laws_data.py` 文件，修改 `DEFAULT_DB_CONFIG` 字典：

```python
DEFAULT_DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'your_password',
    'database': 'legal_qa',
    'charset': 'utf8mb4'
}
```

然后运行：

```bash
python import_laws_data.py --repo-path /path/to/Laws
```

## 步骤 4: 运行导入脚本

```bash
cd backend/scripts
python import_laws_data.py --repo-path /path/to/Laws --password your_password
```

## 导入说明

### 数据映射

脚本会自动将 LawRefBook/Laws 仓库中的分类映射到数据库中的 `law_type` 字段：

- `刑法` → `刑法`
- `民法典` → `民法`
- `民法商法` → `民法`
- `宪法` → `宪法`
- `行政法` → `行政法`
- `经济法` → `经济法`
- `社会法` → `社会法`
- `诉讼与非诉讼程序法` → `程序法`
- `部门规章` → `部门规章`
- `司法解释` → `司法解释`
- `案例` → `案例`
- `其他` → `其他`

### 数据解析

脚本会：

1. 扫描指定目录下的所有 `.md` 文件
2. 解析文件内容，提取：
   - 法律名称（从文件名或文件标题）
   - 法条编号（第 X 条、第 X 章等）
   - 法条内容
   - 发布机构（如果存在）
   - 发布日期（如果存在）
3. 将数据导入到 `legal_articles` 表

### 去重机制

脚本会自动检查数据库中是否已存在相同的记录（基于 `title` 和 `article_number`），如果已存在则跳过，避免重复导入。

## 示例

### Windows 示例

```powershell
# 克隆仓库
git clone https://github.com/LawRefBook/Laws.git E:\Laws

# 安装依赖
cd backend\scripts
pip install -r requirements.txt

# 运行导入
python import_laws_data.py --repo-path E:\Laws --password hjj060618
```

### Linux/Mac 示例

```bash
# 克隆仓库
git clone https://github.com/LawRefBook/Laws.git ~/Laws

# 安装依赖
cd backend/scripts
pip3 install -r requirements.txt

# 运行导入
python3 import_laws_data.py --repo-path ~/Laws --password your_password
```

## 导入结果

导入完成后，脚本会显示统计信息：

```
==================================================
导入完成！统计信息：
  总文件数: 150
  成功导入: 1250 条法条
  跳过记录: 50 条（已存在）
  错误数量: 2
```

## 验证导入结果

导入完成后，可以通过以下方式验证：

1. **使用数据库客户端**（如 Navicat、MySQL Workbench）：

   ```sql
   SELECT COUNT(*) FROM legal_articles;
   SELECT law_type, COUNT(*) FROM legal_articles GROUP BY law_type;
   ```

2. **通过 API 接口**：

   ```bash
   curl http://localhost:8080/api/legal/article/search?keyword=刑法
   ```

3. **通过管理后台**：
   访问管理后台的知识库管理页面查看导入的数据

## 常见问题

### 1. 连接数据库失败

**错误**: `数据库连接失败`

**解决方案**:

- 检查 MySQL 服务是否运行
- 确认数据库连接信息（主机、端口、用户名、密码）正确
- 确认数据库 `legal_qa` 已创建

### 2. 编码问题

**错误**: 中文乱码

**解决方案**:

- 确保数据库使用 `utf8mb4` 字符集
- 确保 Python 脚本使用 UTF-8 编码保存

### 3. 文件解析失败

**错误**: 某些文件无法解析

**解决方案**:

- 检查文件编码是否为 UTF-8
- 查看错误日志了解具体原因
- 某些特殊格式的文件可能需要手动处理

### 4. 导入速度慢

**解决方案**:

- 可以分批导入，先导入特定分类
- 对于大型仓库，考虑使用数据库批量插入优化

## 增量更新

如果需要更新已导入的数据：

1. 更新 LawRefBook/Laws 仓库：

   ```bash
   cd /path/to/Laws
   git pull
   ```

2. 重新运行导入脚本（会自动跳过已存在的记录）

## 注意事项

1. **备份数据库**：在导入大量数据前，建议先备份数据库
2. **磁盘空间**：确保有足够的磁盘空间存储数据
3. **导入时间**：大型仓库的导入可能需要较长时间，请耐心等待
4. **数据验证**：导入后建议抽样检查数据质量

## 技术支持

如遇到问题，请：

1. 查看错误日志
2. 检查数据库连接配置
3. 确认仓库路径正确
4. 查看项目的 Issues 或联系开发团队
