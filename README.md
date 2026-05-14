# data-pipeline-monitor

A full-stack data platform learning project.

## 🎯 Project Purpose

This is a structured learning project designed to understand:
- Modern GitHub workflows (issues, PRs, labels, milestones, actions)
- Full-stack development patterns (FastAPI + Vue.js)
- Data platform concepts (catalog, registry, pipelines)
- Agent-driven development practices
- CI/CD with GitHub Actions

## 📚 What You'll Learn

Through this 3-phase project, you'll practice:

- **Phase 1:** Repository foundation, GitHub project management
- **Phase 2:** Dataset Registry module (full-stack implementation)
- **Phase 3:** Pipeline runs & dataset preview (system simulation)

## 🛠 Tech Stack

### Backend
- **FastAPI** - Modern Python API framework
- **Pydantic** - Data validation
- **pytest** - Testing

### Frontend
- **Vue 3** - Progressive framework
- **Vite** - Build tool
- **TypeScript** - Type safety
- **Vitest** - Testing

### DevOps
- **GitHub Actions** - CI/CD
- **Docker** (later phases)
- **Markdown** - Documentation

## 📂 Repository Structure

```
data-pipeline-monitor/
  apps/
    backend/          # FastAPI backend
    frontend/         # Vue 3 frontend
  data/
    pipelines/        # Pipeline definitions
    scripts/          # Utility scripts
  docs/
    architecture/     # System design
    backend/          # Backend docs
    frontend/         # Frontend docs
    workflows/        # GitHub workflows
    adr/              # Architecture decision records
  manifests/
    modules/          # Module manifests
  tests/              # Integration tests
  .github/
    workflows/        # CI/CD workflows
    ISSUE_TEMPLATE/   # Issue templates
  .vscode/            # Workspace settings
  README.md           # This file
  CONTRIBUTING.md     # Contribution guide
  DEVELOPMENT_WORKFLOW.md  # Development process
  AI_AGENT_GUIDE.md   # Agent instructions
  CODEOWNERS          # Code ownership
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### Quick Start

```bash
# Clone repository
git clone <repo-url>
cd data-pipeline-monitor

# Backend setup
cd apps/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest

# Frontend setup (in new terminal)
cd apps/frontend
npm install
npm run test
```

## 📖 Documentation

- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) - Step-by-step dev process
- [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md) - Agent instructions & conventions
- [Architecture](docs/architecture/) - System design

## 🎓 Learning Modules

### M1 - Repository Foundation
Focus: GitHub setup, processes, templates, CI

### M2 - Dataset Registry Module
Focus: Full-stack implementation, API, frontend, testing

### M3 - Pipeline Simulation
Focus: Advanced patterns, system integration

## 🤖 AI/Agent Workflow

This project is designed to be agent-friendly:

- Issues are structured with clear acceptance criteria
- PRs use templates for consistency
- Modules are defined in manifests for agent parsing
- Documentation follows naming conventions

See [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md) for details.

## ✅ Project Status

Currently in **Phase 1: Repository Foundation**

### Current Milestones
- [ ] M1 - Repository Foundation
- [ ] M2 - Dataset Registry Module
- [ ] M3 - Pipeline Simulation

See [Issues](../../issues) and [Project Board](#) for detailed progress.

## 📝 License

MIT License

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

**Version:** 0.1.0 | **Last Updated:** May 2026
