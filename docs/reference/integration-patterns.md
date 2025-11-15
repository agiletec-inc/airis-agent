# Airis Agent Integration Patterns Collection

**Status**: ✅ **Status: Current** - Context patterns for framework integration and tool coordination.

**Context Integration Guide**: Patterns for using Airis Agent commands effectively with different frameworks and tools. Remember: Airis Agent provides context to Claude Code - all actual work is done by Claude.

## Overview and Usage Guide

**Purpose**: Effective patterns for using Airis Agent context with various development frameworks and tools.

**What This Is**: Command combinations and flag patterns that work well for specific technologies
**What This Isn't**: Performance optimization or parallel execution (no code runs)

**Key Principle**: Airis Agent tells Claude Code WHAT to do and HOW to think about it. Claude Code does the actual work.

## Framework Context Patterns

### React Development Patterns

```bash
# React development with appropriate context
/airis:implement "React 18 application with TypeScript" --c7
# Context7 MCP can provide React documentation if available
# Magic MCP can help with UI components if configured

# What Actually Happens:
# 1. Claude reads implement.md for implementation patterns
# 2. --c7 flag suggests using Context7 MCP for documentation
# 3. Claude generates React code based on these contexts

# Component development pattern
@agent-frontend-architect "design component architecture"
/airis:implement "reusable component library"

# Testing pattern for React
/airis:test --focus react
# Claude will suggest React Testing Library patterns
```

### Node.js Backend Patterns

```bash
# Node.js backend development patterns
/airis:implement "Express.js API with TypeScript" --c7
# Claude will create Express API following Node.js patterns

# What This Means:
# - Claude reads context about backend patterns
# - Suggests appropriate middleware and structure
# - NOT running or optimizing any code

# Database integration pattern
/airis:implement "database models with Prisma"
@agent-backend-architect "review database schema"

# API testing pattern
/airis:test --focus api
# Claude suggests API testing approaches
```

### Python Development Patterns

```bash
# Python web development
/airis:implement "FastAPI application" --c7
@agent-python-expert "review implementation"

# What Happens:
# - Claude uses Python-specific context
# - Follows FastAPI patterns from context
# - Generates code (doesn't run it)

# Data science context
/airis:implement "data analysis pipeline"
@agent-python-expert "optimize pandas operations"
# Claude provides optimization suggestions (not actual optimization)

# Testing patterns
/airis:test --focus python
# Claude suggests pytest patterns
```

### Full-Stack Development Patterns

```bash
# Full-stack application pattern
/airis:brainstorm "full-stack application architecture"
@agent-system-architect "design system components"

# Frontend implementation
/airis:implement "React frontend with TypeScript"
@agent-frontend-architect "review component structure"

# Backend implementation
/airis:implement "Node.js API with authentication"
@agent-backend-architect "review API design"

# Integration
/airis:implement "connect frontend to backend API"
```

## Tool Coordination Patterns

### Using MCP Servers Effectively

```bash
# Context7 for documentation
/airis:explain "React hooks" --c7
# If Context7 is configured, it may fetch React docs

# Sequential for complex reasoning
/airis:troubleshoot "complex bug" --seq
# Sequential MCP helps with structured problem-solving

# Magic for UI components
/airis:implement "UI components" --magic
# Magic MCP can help generate modern UI patterns

# No MCP for simple tasks
/airis:implement "utility function" --no-mcp
# Uses only Claude's built-in knowledge
```

### Agent and Command Combinations

```bash
# Security-focused development
@agent-security "review authentication requirements"
/airis:implement "secure authentication system"
/airis:analyze --focus security

# Quality-focused workflow
/airis:implement "new feature"
@agent-quality-engineer "review code quality"
/airis:test --focus quality

# Architecture-focused approach
@agent-system-architect "design microservices"
/airis:design "service boundaries"
/airis:implement "service communication"
```

## Common Integration Patterns

### API Development Pattern

```bash
# Step 1: Design
/airis:design "REST API structure"

# Step 2: Implementation
/airis:implement "API endpoints with validation"

# Step 3: Documentation
/airis:document --type api

# Step 4: Testing
/airis:test --focus api
```

### Database Integration Pattern

```bash
# Schema design
@agent-backend-architect "design database schema"

# Model implementation
/airis:implement "database models"

# Migration creation
/airis:implement "database migrations"

# Query optimization suggestions
@agent-backend-architect "suggest query optimizations"
# Note: Claude suggests optimizations, doesn't actually optimize
```

### Testing Strategy Pattern

```bash
# Test planning
/airis:design "testing strategy"

# Unit tests
/airis:test --type unit

# Integration tests
/airis:test --type integration

# E2E test suggestions
/airis:test --type e2e
# Claude provides test code, not execution
```

## Technology-Specific Patterns

### React + TypeScript Pattern

```bash
# Project setup guidance
/airis:implement "React TypeScript project structure"

# Component development
/airis:implement "TypeScript React components with props validation"

# State management
@agent-frontend-architect "recommend state management approach"
/airis:implement "state management with Zustand/Redux"

# Testing
/airis:test --focus react --type unit
```

### Python FastAPI Pattern

```bash
# API structure
/airis:implement "FastAPI project structure"

# Endpoint development
@agent-python-expert "implement async endpoints"

# Database integration
/airis:implement "SQLAlchemy models with Alembic"

# Testing
/airis:test --focus python --type integration
```

### Node.js Microservices Pattern

```bash
# Architecture design
@agent-system-architect "design microservices architecture"

# Service implementation
/airis:implement "user service with Express"
/airis:implement "auth service with JWT"

# Inter-service communication
/airis:implement "service communication patterns"

# Testing approach
/airis:test --focus microservices
```

## Troubleshooting Patterns

### Debugging Workflow

```bash
# Problem analysis
/airis:troubleshoot "describe the issue"

# Root cause investigation
@agent-root-cause-analyst "analyze symptoms"

# Solution implementation
/airis:implement "fix based on analysis"

# Verification
/airis:test --validate
```

### Code Review Pattern

```bash
# Code analysis
/airis:analyze code/ --focus quality

# Security review
@agent-security "review for vulnerabilities"

# Performance review
@agent-performance-engineer "suggest improvements"
# Note: Suggestions only, no actual performance measurement

# Implementation of improvements
/airis:improve code/ --fix
```

## Important Clarifications

### What These Patterns DO

- ✅ Provide structured approaches to development tasks
- ✅ Combine commands and agents effectively
- ✅ Suggest appropriate tools and frameworks
- ✅ Guide Claude to generate better code

### What These Patterns DON'T DO

- ❌ Execute code or measure performance
- ❌ Run tests or deploy applications
- ❌ Optimize actual execution speed
- ❌ Provide real monitoring or metrics
- ❌ Coordinate parallel processes (everything is sequential text)

## Best Practices

### Effective Pattern Usage

1. **Start with context**: Use `/airis:load` to establish project understanding
2. **Layer expertise**: Combine general commands with specific agents
3. **Focus appropriately**: Use `--focus` flags for targeted results
4. **Manage scope**: Work on specific modules rather than entire codebases
5. **Document decisions**: Use `/airis:save` to create summaries

### Pattern Selection

- **Simple tasks**: Use basic commands without MCP
- **Complex tasks**: Add appropriate agents and MCP servers
- **Security-critical**: Always include `@agent-security`
- **UI development**: Consider `--magic` flag if configured
- **Documentation needs**: Use `--c7` for framework docs

## Summary

These integration patterns show how to combine Airis Agent commands, agents, and flags effectively for different development scenarios. Remember that all patterns are about providing better context to Claude Code - the actual code generation, not execution, is what Claude does based on these contexts.