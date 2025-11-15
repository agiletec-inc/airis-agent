# Airis Agent 命令指南

Airis Agent 为 Claude Code 提供 21 个命令：用于工作流的 `/airis:*` 命令和用于专家的 `@agent-*`。

## 命令类型

| 类型 | 使用位置 | 格式 | 示例 |
|------|------------|--------|---------|
| **斜杠命令** | Claude Code | `/airis:[command]` | `/airis:implement "feature"` |
| **智能体** | Claude Code | `@agent-[name]` | `@agent-security "review"` |
| **安装命令** | 终端 | `Airis Agent [command]` | `Airis Agent install` |

## 快速测试
```bash
# 终端：验证安装
python3 -m Airis Agent --version
# Claude Code CLI 验证：claude --version

# Claude Code：测试命令
/airis:brainstorm "test project"    # 应该询问发现性问题
/airis:analyze README.md           # 应该提供分析
```

**工作流**：`/airis:brainstorm "idea"` → `/airis:implement "feature"` → `/airis:test`

## 🎯 理解 Airis Agent 命令

## Airis Agent 如何工作

Airis Agent 提供行为上下文文件，Claude Code 通过读取这些文件来采用专门的行为。当您键入 `/airis:implement` 时，Claude Code 读取 `implement.md` 上下文文件并遵循其行为指令。

**Airis Agent 命令不是由软件执行的** - 它们是上下文触发器，通过读取框架中的专门指令文件来修改 Claude Code 的行为。

### 命令类型：
- **斜杠命令** (`/airis:*`)：触发工作流模式和行为模式
- **智能体调用** (`@agent-*`)：手动激活特定领域专家
- **标志** (`--think`、`--safe-mode`)：修改命令行为和深度

### 上下文机制：
1. **用户输入**：您输入 `/airis:implement "auth system"`
2. **上下文加载**：Claude Code 读取 `~/.claude/superagent/Commands/implement.md`
3. **行为采用**：Claude 运用专业知识进行工具选择和验证
4. **增强输出**：带有安全考虑和最佳实践的结构化实现

**关键要点**：这通过上下文管理而不是传统的软件执行来创建复杂的开发工作流。

### 安装命令 vs 使用命令

**🖥️ 终端命令** （实际 CLI 软件）：
- `Airis Agent install` - 安装框架组件
- `Airis Agent update` - 更新现有安装
- `Airis Agent uninstall` - 卸载框架安装
- `python3 -m Airis Agent --version` - 检查安装状态

**💬 Claude Code 命令** （上下文触发器）：
- `/airis:brainstorm` - 激活需求发现上下文
- `/airis:implement` - 激活特性开发上下文
- `@agent-security` - 激活安全专家上下文
- 所有命令仅在 Claude Code 聊天界面中工作


> **快速开始**：尝试 `/airis:brainstorm "your project idea"` → `/airis:implement "feature name"` → `/airis:test` 体验核心工作流。

## 🧪 Testing Your Setup

### 🖥️ 终端验证（在终端/CMD 中运行）
```bash
# 验证 Airis Agent 是否正常工作（主要方法）
python3 -m Airis Agent --version
# 示例输出：Airis Agent 4.1.5

# Claude Code CLI 版本检查
claude --version

# 检查已安装的组件
python3 -m Airis Agent install --list-components | grep mcp
# 示例输出：显示已安装的 MCP 组件
```

### 💬 Claude Code 测试（在 Claude Code 聊天中输入）
```
# 测试基本 /airis: 命令
/airis:brainstorm "test project"
# 示例行为：开始交互式需求发现

# 测试命令帮助
/airis:help
# 示例行为：显示可用命令列表
```

**如果测试失败**：检查 [安装指南](../getting-started/installation.md) 或 [故障排除](#troubleshooting)

### 📝 Command Quick Reference

| Command Type | Where to Run | Format | Purpose | Example |
|-------------|--------------|--------|---------|----------|
| **🖥️ 安装** | 终端/CMD | `Airis Agent [command]` | 设置和维护 | `Airis Agent install` |
| **🔧 配置** | 终端/CMD | `python3 -m Airis Agent [command]` | 高级配置 | `python3 -m Airis Agent --version` |
| **💬 斜杠命令** | Claude Code | `/airis:[command]` | 工作流自动化 | `/airis:implement "feature"` |
| **🤖 智能体调用** | Claude Code | `@agent-[name]` | 手动专家激活 | `@agent-security "review"` |
| **⚡ 增强标志** | Claude Code | `/airis:[command] --flags` | 行为修改 | `/airis:analyze --think-hard` |

> **记住**：所有 `/airis:` 命令和 `@agent-` 调用都在 Claude Code 聊天中工作，而不是在您的终端中。它们触发 Claude Code 从 Airis Agent 框架中读取特定的上下文文件。

## 目录

- [基本命令](#essential-commands) - 从这里开始（8 个核心命令）
- [常用工作流](#common-workflows) - 有效的命令组合
- [完整命令参考](#full-command-reference) - 所有 21 个命令按类别组织
- [故障排除](#troubleshooting) - 常见问题和解决方案
- [命令索引](#command-index) - 按类别查找命令

---

## 基本命令

**立即提高生产力的核心工作流命令：**

### `/airis:brainstorm` - 项目发现
**目的**：交互式需求发现和项目规划
**语法**：`/airis:brainstorm "您的想法"` `[--strategy systematic|creative]`

**使用案例**：
- 新项目规划：`/airis:brainstorm "e-commerce platform"`
- 特性探索：`/airis:brainstorm "user authentication system"`
- 问题解决：`/airis:brainstorm "slow database queries"``

### `/airis:implement` - 功能开发  
**目的**: 通过智能专家路由进行全栈功能实现  
**语法**: `/airis:implement "feature description"` `[--type frontend|backend|fullstack] [--focus security|performance]`  

**使用场景**:
- 身份验证: `/airis:implement "JWT login system"`
- UI 组件: `/airis:implement "responsive dashboard"`
- APIs: `/airis:implement "REST user endpoints"`
- 数据库: `/airis:implement "user schema with relationships"`

### `/airis:analyze` - 代码评估
**目的**: 跨质量、安全性和性能的综合代码分析  
**语法**: `/airis:analyze [path]` `[--focus quality|security|performance|architecture]`

**使用场景**:
- 项目健康: `/airis:analyze .`
- 安全审计: `/airis:analyze --focus security`
- 性能评审: `/airis:analyze --focus performance`

### `/airis:troubleshoot` - 问题诊断
**目的**: 系统化问题诊断与根本原因分析  
**语法**: `/airis:troubleshoot "问题描述"` `[--type build|runtime|performance]`

**使用场景**:
- 运行时错误: `/airis:troubleshoot "登录时出现500错误"`
- 构建失败: `/airis:troubleshoot --type build`
- 性能问题: `/airis:troubleshoot "页面加载缓慢"`

### `/airis:test` - 质量保证
**目的**: 全面测试与覆盖率分析  
**语法**: `/airis:test` `[--type unit|integration|e2e] [--coverage] [--fix]`

**使用场景**:
- 完整测试套件: `/airis:test --coverage`
- 单元测试: `/airis:test --type unit --watch`
- 端到端验证: `/airis:test --type e2e`

### `/airis:improve` - 代码增强  
**目的**: 应用系统化的代码改进和优化  
**语法**: `/airis:improve [path]` `[--type performance|quality|security] [--preview]`

**使用场景**:
- 常规改进: `/airis:improve src/`
- 性能优化: `/airis:improve --type performance`
- 安全加固: `/airis:improve --type security`

### `/airis:document` - 文档生成
**目的**: 为代码和API生成全面的文档  
**语法**: `/airis:document [path]` `[--type api|user-guide|technical] [--format markdown|html]`

**使用场景**:
- API文档: `/airis:document --type api`
- 用户指南: `/airis:document --type user-guide`
- 技术文档: `/airis:document --type technical`

### `/airis:workflow` - 实现规划
**目的**: 从需求生成结构化的实现计划  
**语法**: `/airis:workflow "功能描述"` `[--strategy agile|waterfall] [--format markdown]`

**使用场景**:
- 功能规划: `/airis:workflow "用户身份验证"`
- 冲刺规划: `/airis:workflow --strategy agile`
- 架构规划: `/airis:workflow "微服务迁移"`

---

## 常用工作流

**经过验证的命令组合：**

### 新项目设置
```bash
/airis:brainstorm "项目概念"              # 定义需求
/airis:design "系统架构"                  # 创建技术设计  
/airis:workflow "实现计划"                # 制定开发路线图
```

### 功能开发
```bash
/airis:implement "功能名称"               # 构建功能
/airis:test --coverage                   # 通过测试验证
/airis:document --type api               # 生成文档  
```

### 代码质量改进
```bash
/airis:analyze --focus quality           # 评估当前状态
/airis:improve --preview                 # 预览改进
/airis:test --coverage                   # 验证变更
```

### Bug调查
```bash
/airis:troubleshoot "问题描述"            # 诊断问题
/airis:analyze --focus problem-area      # 深度分析
/airis:improve --fix --safe-mode         # 应用针对性修复
```

## 完整命令参考

### 开发命令
| 命令 | 目的 | 最适用于 |
|---------|---------|----------|
| **workflow** | 实现规划 | 项目路线图，冲刺规划 |
| **implement** | 功能开发 | 全栈功能，API开发 |
| **build** | 项目编译 | CI/CD，生产构建 |
| **design** | 系统架构 | API规范，数据库模式 |

### 分析命令  
| 命令 | 目的 | 最适用于 |
|---------|---------|----------|
| **analyze** | 代码评估 | 质量审计，安全评审 |
| **troubleshoot** | 问题诊断 | Bug调查，性能问题 |
| **explain** | 代码解释 | 学习，代码评审 |

### 质量命令
| 命令 | 目的 | 最适用于 |
|---------|---------|----------|
| **improve** | 代码增强 | 性能优化，重构 |
| **cleanup** | 技术债务 | 清理无用代码，组织整理 |
| **test** | 质量保证 | 测试自动化，覆盖率分析 |
| **document** | 文档生成 | API文档，用户指南 |

### 项目管理
| 命令 | 目的 | 最适用于 |
|---------|---------|----------|
| **estimate** | 项目估算 | 时间线规划，资源分配 |
| **task** | 任务管理 | 复杂工作流，任务跟踪 |
| **spawn** | 元编排 | 大型项目，并行执行 |

### 实用工具命令
| 命令 | 目的 | 最适用于 |
|---------|---------|----------|
| **git** | 版本控制 | 提交管理，分支策略 |
| **index** | 命令发现 | 探索功能，查找命令 |

### 会话命令  
| 命令 | 目的 | 最适用于 |
|---------|---------|----------|
| **load** | 上下文加载 | 会话初始化，项目启用 |
| **save** | 会话持久化 | 检查点，上下文保存 |
| **reflect** | 任务验证 | 进度评估，完成验证 |
| **select-tool** | 工具优化 | 性能优化，工具选择 |

---

## 命令索引

**按功能分类：**
- **规划**: brainstorm, design, workflow, estimate
- **开发**: implement, build, git
- **分析**: analyze, troubleshoot, explain  
- **质量**: improve, cleanup, test, document
- **管理**: task, spawn, load, save, reflect
- **工具**: index, select-tool

**按复杂度分类：**
- **初学者**: brainstorm, implement, analyze, test
- **中级**: workflow, design, improve, document  
- **高级**: spawn, task, select-tool, reflect

## 故障排除

**命令问题：**
- **命令未找到**: 验证安装: `python3 -m Airis Agent --version`
- **无响应**: 重启 Claude Code 会话
- **处理延迟**: 使用 `--no-mcp` 测试不使用 MCP 服务器

**快速修复：**
- 重置会话: `/airis:load` 重新初始化
- 检查状态: `Airis Agent install --list-components`
- 获取帮助: [故障排除指南](../reference/troubleshooting.md)

## 下一步

- [标志指南](flags.md) - 控制命令行为
- [智能体指南](agents.md) - 专家激活
- [示例手册](../reference/examples-cookbook.md) - 真实使用模式