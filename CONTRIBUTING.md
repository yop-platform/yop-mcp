# Contributing to YOP MCP Server

感谢您对 YOP MCP Server 项目的关注！我们欢迎所有形式的贡献，包括但不限于代码、文档、测试、问题报告和功能建议。

## 🚀 快速开始

### 开发环境设置

1. **Fork 并克隆仓库**
   ```bash
   git clone http://gitlab.yeepay.com/your-username/yop-mcp.git
   cd yop-mcp
   ```

2. **安装 uv 包管理器**
   ```bash
   # Windows
   pip install uv
   
   # Linux/Mac
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **安装依赖**
   ```bash
   uv sync --all-extras
   ```

4. **安装 pre-commit hooks**
   ```bash
   uv run pre-commit install
   ```

5. **运行测试确保环境正常**
   ```bash
   uv run pytest
   ```

## 📝 贡献类型

### 🐛 Bug 报告
- 使用 [Bug Report Template](http://gitlab.yeepay.com/yop/yop-mcp/-/issues/new?issuable_template=bug_report)
- 提供详细的重现步骤
- 包含错误信息和环境信息
- 如果可能，提供最小重现示例

### ✨ 功能请求
- 使用 [Feature Request Template](http://gitlab.yeepay.com/yop/yop-mcp/-/issues/new?issuable_template=feature_request)
- 清楚描述功能需求和使用场景
- 解释为什么这个功能对项目有价值

### 📚 文档改进
- 修复文档中的错误或不准确信息
- 添加缺失的文档
- 改进现有文档的清晰度
- 添加使用示例

### 🧪 测试
- 增加测试覆盖率
- 改进现有测试
- 添加集成测试
- 性能测试

## 🔧 开发流程

### 1. 创建分支
```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

### 2. 开发规范

#### 代码风格
- 使用 [Black](https://black.readthedocs.io/) 进行代码格式化
- 使用 [isort](https://pycqa.github.io/isort/) 进行导入排序
- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 编码规范
- 使用类型注解（Type Hints）

#### 提交信息规范
使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

类型包括：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式化（不影响功能）
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat(api): add new certificate validation function

Add support for SM2 certificate validation with enhanced error handling.

Closes #123
```

### 3. 测试要求

#### 单元测试
- 新功能必须包含相应的单元测试
- 测试覆盖率不低于 80%
- 使用 pytest 框架

```bash
# 运行测试
uv run pytest

# 运行测试并生成覆盖率报告
uv run pytest --cov=tools --cov=main --cov-report=html
```

#### 集成测试
- 对于涉及外部API的功能，提供mock测试
- 确保测试在CI环境中能够稳定运行

### 4. 代码质量检查

在提交前，请确保通过所有质量检查：

```bash
# 代码格式化
uv run black .
uv run isort .

# 代码检查
uv run flake8 .
uv run mypy tools/ main.py --ignore-missing-imports
uv run pylint tools/ main.py

# 安全检查
uv run bandit -r tools/ main.py

# 运行所有检查
uv run pre-commit run --all-files
```

### 5. 提交 Pull Request

1. **推送分支**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **创建 Pull Request**
   - 使用清晰的标题和描述
   - 引用相关的 Issue
   - 添加适当的标签
   - 请求代码审查

3. **PR 模板**
   ```markdown
   ## 变更描述
   简要描述此PR的变更内容

   ## 变更类型
   - [ ] Bug 修复
   - [ ] 新功能
   - [ ] 文档更新
   - [ ] 代码重构
   - [ ] 测试改进

   ## 测试
   - [ ] 已添加/更新单元测试
   - [ ] 所有测试通过
   - [ ] 手动测试通过

   ## 检查清单
   - [ ] 代码遵循项目规范
   - [ ] 已更新相关文档
   - [ ] 已添加必要的测试
   - [ ] 通过所有CI检查

   ## 相关Issue
   Closes #issue_number
   ```

## 🔍 代码审查

### 审查标准
- 代码功能正确性
- 代码可读性和可维护性
- 测试覆盖率和质量
- 文档完整性
- 性能影响
- 安全性考虑

### 审查流程
1. 自动化检查必须通过
2. 至少一位维护者审查
3. 解决所有审查意见
4. 最终批准后合并

## 📋 发布流程

### 版本号规范
遵循 [Semantic Versioning](https://semver.org/)：
- `MAJOR.MINOR.PATCH`
- MAJOR: 不兼容的API变更
- MINOR: 向后兼容的功能性新增
- PATCH: 向后兼容的问题修正

### 发布步骤
1. 更新 CHANGELOG.md
2. 更新版本号
3. 创建 Git tag
4. 触发自动发布流程

## 🤝 社区准则

### 行为准则
- 尊重所有参与者
- 建设性的讨论和反馈
- 包容不同的观点和经验
- 专注于对社区最有利的事情

### 沟通渠道
- **Issues**: 用于bug报告和功能请求
- **Pull Requests**: 用于代码贡献讨论
- **Discussions**: 用于一般性讨论和问题

## 📞 获取帮助

如果您在贡献过程中遇到问题，可以通过以下方式获取帮助：

- 查看 [FAQ](README.md#常见问题)
- 搜索现有的 [Issues](http://gitlab.yeepay.com/yop/yop-mcp/-/issues)
- 创建新的 Issue 寻求帮助
- 联系项目维护者

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！您的贡献让这个项目变得更好。

---

**Happy Coding! 🎉**
