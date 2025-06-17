# YOP MCP Server Makefile
# 提供常用的开发命令

.PHONY: help install install-dev test test-cov lint format type-check security clean run docs pre-commit all-checks

# 默认目标
help: ## 显示帮助信息
	@echo "YOP MCP Server - 可用命令:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# 安装和环境设置
install: ## 安装生产依赖
	uv sync

install-dev: ## 安装开发依赖
	uv sync --extra dev --extra test

# 测试相关
test: ## 运行测试
	uv run pytest

test-cov: ## 运行测试并生成覆盖率报告
	uv run pytest --cov=tools --cov=main --cov-report=html --cov-report=term-missing

test-watch: ## 监视文件变化并自动运行测试
	uv run pytest-watch

# 代码质量
lint: ## 运行代码检查
	uv run flake8 tools/ main.py --max-line-length=127 --extend-ignore=E203,W503
	uv run pylint tools/ main.py --disable=C0114,C0115,C0116 --max-line-length=127

format: ## 格式化代码
	uv run black .
	uv run isort .

format-check: ## 检查代码格式
	uv run black --check .
	uv run isort --check-only .

type-check: ## 类型检查
	uv run mypy tools/ main.py --ignore-missing-imports

# 安全检查
security: ## 运行安全检查
	uv run bandit -r tools/ main.py
	uv run safety check

security-report: ## 生成安全检查报告
	uv run bandit -r tools/ main.py -f json -o bandit-report.json
	uv run safety check --json --output safety-report.json

# 预提交检查
pre-commit: ## 运行预提交检查
	uv run pre-commit run --all-files

pre-commit-install: ## 安装预提交钩子
	uv run pre-commit install

# 综合检查
all-checks: format-check lint type-check security test ## 运行所有检查

# 运行和开发
run: ## 运行MCP服务器
	uv run main.py

run-dev: ## 开发模式运行（带调试信息）
	DEBUG=1 uv run main.py

# 文档
docs: ## 生成文档
	@echo "生成API文档..."
	uv run python -m pydoc -w tools/
	uv run python -m pydoc -w main

docs-serve: ## 启动文档服务器
	uv run python -m http.server 8000 -d .

# 清理
clean: ## 清理临时文件
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml

clean-all: clean ## 清理所有文件（包括虚拟环境）
	rm -rf .venv/

# 构建和发布
build: ## 构建包
	uv build

build-check: ## 检查构建
	uv build
	uv run twine check dist/*

# 依赖管理
deps-update: ## 更新依赖
	uv lock --upgrade
	uv sync --extra dev --extra test

deps-audit: ## 审计依赖安全性
	uv add safety && uv run safety check

# 开发环境初始化
init: install-dev pre-commit-install ## 初始化开发环境
	@echo "开发环境初始化完成！"
	@echo "运行 'make help' 查看可用命令"

# CI/CD 相关
ci-test: ## CI环境测试
	uv run pytest --cov=tools --cov=main --cov-report=xml

ci-lint: ## CI环境代码检查
	uv run flake8 tools/ main.py --count --select=E9,F63,F7,F82 --show-source --statistics
	uv run flake8 tools/ main.py --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# 版本管理
version: ## 显示当前版本
	@grep version pyproject.toml | head -1 | cut -d'"' -f2

bump-patch: ## 增加补丁版本号
	@echo "当前版本: $$(make version)"
	@echo "请手动更新 pyproject.toml 中的版本号"

bump-minor: ## 增加次版本号
	@echo "当前版本: $$(make version)"
	@echo "请手动更新 pyproject.toml 中的版本号"

bump-major: ## 增加主版本号
	@echo "当前版本: $$(make version)"
	@echo "请手动更新 pyproject.toml 中的版本号"

# 快速开发命令
dev: install-dev ## 快速开始开发
	@echo "开发环境已准备就绪！"
	@echo "运行 'make run' 启动服务器"
	@echo "运行 'make test' 运行测试"

# 发布前检查
release-check: all-checks build-check ## 发布前完整检查
	@echo "发布前检查完成！"
	@echo "如果所有检查都通过，可以进行发布"
