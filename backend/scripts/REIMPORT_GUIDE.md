# 清理并重新导入法律法规数据指南

本指南说明如何使用修复后的导入脚本清理并重新导入法律法规数据。

## 问题说明

之前的导入脚本在解析法条时存在合并问题，导致某些法条的内容包含了相邻法条的内容。现在已经修复了导入脚本的解析逻辑，使用位置索引精确分割法条。

## 使用方法

### 方法1：使用批处理脚本（Windows，推荐）

```bash
cd backend\scripts
reimport_laws.bat
```

脚本会引导你：
1. 输入仓库路径
2. 输入数据库密码
3. 选择清理选项
4. 选择导入范围

### 方法2：使用Python脚本

#### 清理所有数据并重新导入

```bash
cd backend\scripts
python reimport_laws.py --repo-path "E:\Laws\Laws" --password "hjj060618" --clear-all
```

#### 只清理并重新导入特定类型的法律

```bash
# 只清理和导入刑法
python reimport_laws.py --repo-path "E:\Laws\Laws" --password "hjj060618" --clear-types 刑法 --import-types 刑法

# 清理和导入多个类型
python reimport_laws.py --repo-path "E:\Laws\Laws" --password "hjj060618" --clear-types 刑法 民法 --import-types 刑法 民法
```

#### 跳过清理，直接导入（会自动去重）

```bash
python reimport_laws.py --repo-path "E:\Laws\Laws" --password "hjj060618" --skip-clear
```

## 参数说明

- `--repo-path`: LawRefBook/Laws 仓库路径（必需）
- `--password`: 数据库密码（必需）
- `--host`: 数据库主机（默认: localhost）
- `--port`: 数据库端口（默认: 3306）
- `--user`: 数据库用户名（默认: root）
- `--database`: 数据库名称（默认: legal_qa）
- `--clear-all`: 清理所有法条数据
- `--clear-types`: 只清理指定类型的法律（如: 刑法 民法）
- `--import-types`: 只导入指定类型的法律（如: 刑法 民法）
- `--skip-clear`: 跳过清理步骤，直接导入（会自动去重）

## 法律类型列表

可用的法律类型：
- `刑法`
- `民法`
- `行政法`
- `经济法`
- `社会法`
- `程序法`
- `宪法`
- `宪法相关法`
- `行政法规`
- `部门规章`
- `司法解释`
- `案例`
- `其他`

## 示例

### 示例1：完全重新导入

```bash
# 清理所有数据
python reimport_laws.py --repo-path "E:\Laws\Laws" --password "hjj060618" --clear-all
```

### 示例2：只修复刑法相关法条

```bash
# 清理刑法数据并重新导入
python reimport_laws.py --repo-path "E:\Laws\Laws" --password "hjj060618" --clear-types 刑法 --import-types 刑法
```

### 示例3：测试导入（只导入少量数据）

```bash
# 只导入刑法和民法，测试修复效果
python reimport_laws.py --repo-path "E:\Laws\Laws" --password "hjj060618" --clear-types 刑法 民法 --import-types 刑法 民法
```

## 注意事项

1. **备份数据**：在清理数据前，建议先备份数据库
   ```sql
   -- 在Navicat中执行
   CREATE TABLE legal_articles_backup AS SELECT * FROM legal_articles;
   ```

2. **清理确认**：清理操作会要求确认，输入 `yes` 才会执行

3. **导入时间**：完整重新导入可能需要较长时间（取决于数据量）

4. **去重机制**：如果使用 `--skip-clear`，脚本会自动跳过已存在的记录（基于标题和条号）

5. **修复效果**：修复后的脚本使用位置索引精确分割法条，避免了合并问题

## 验证修复效果

导入完成后，可以运行验证脚本检查：

```bash
# 检查是否有合并问题
python check_merged_articles.py

# 检查特定法条
python check_specific_article.py
```

## 常见问题

### Q: 清理后数据会丢失吗？

A: 是的，清理操作会删除指定的法条数据。建议先备份数据库。

### Q: 可以只修复部分法律吗？

A: 可以，使用 `--clear-types` 和 `--import-types` 参数指定要处理的法律类型。

### Q: 导入过程中断怎么办？

A: 可以重新运行脚本，使用 `--skip-clear` 跳过清理，脚本会自动去重。

### Q: 如何验证修复是否成功？

A: 运行 `check_merged_articles.py` 检查是否还有合并问题，或查看具体法条内容。

## 技术支持

如遇到问题，请：
1. 查看错误日志
2. 检查数据库连接配置
3. 确认仓库路径正确
4. 查看项目的 Issues 或联系开发团队

