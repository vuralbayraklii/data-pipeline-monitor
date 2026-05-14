# Contributing Guide

This document describes the development workflow and practices for the data-pipeline-monitor project.

## 📋 Quick Reference

- **Branch Naming:** `type/descriptive-name`
- **Commit Format:** Conventional Commits (`feat:`, `fix:`, `docs:`, etc.)
- **PR Template:** Mandatory (auto-generated)
- **Testing:** Required before PR
- **Documentation:** Update alongside code changes

## 🔄 Development Workflow

### Step 1: Pick an Issue

1. Browse [Issues](../../issues)
2. Assign yourself to an issue
3. Review acceptance criteria
4. Leave a comment: "Starting on this"

### Step 2: Create a Branch

Follow this naming convention:

```
feature/descriptive-name          # New feature
bugfix/bug-description            # Bug fix
docs/documentation-topic          # Documentation
chore/maintenance-task            # Maintenance
refactor/module-name-cleanup      # Refactoring
```

Example:
```bash
git checkout -b feature/dataset-registry-backend
```

### Step 3: Develop

- Make small, logical commits
- Follow the commit message format
- Write tests alongside code
- Update documentation as needed

#### Commit Message Format

Use Conventional Commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `test` - Test additions/changes
- `refactor` - Code refactoring
- `chore` - Build, dependencies, etc.

**Examples:**
```
feat(backend): add dataset list endpoint
fix(frontend): correct table sorting behavior
docs: update dataset registry documentation
test: add dataset creation tests
```

### Step 4: Test Locally

```bash
# Backend
cd apps/backend
pytest

# Frontend
cd apps/frontend
npm run test
```

### Step 5: Push & Create Pull Request

```bash
git push -u origin feature/your-branch-name
```

Then open a PR on GitHub. The template will guide you through:
- What changed
- Why it changed
- How to test it
- Related issue(s)
- Documentation updates

### Step 6: CI & Review

1. GitHub Actions will run automatically
2. Ensure all checks pass (tests, linting)
3. Request review from team members (or respond to bot comments)
4. Address feedback in new commits

### Step 7: Merge

Once approved:
1. Squash or keep commits as per discussion
2. Merge to `main`
3. Delete your branch
4. Verify linked issue closes automatically

---

## ✅ Code Standards

### Backend (Python/FastAPI)

- Use **type hints** for all functions
- Follow **PEP 8** style guide
- Use **pytest** for tests
- Minimum test coverage: 80%
- Use **Pydantic** for data validation

Example:
```python
from pydantic import BaseModel
from fastapi import FastAPI

class Dataset(BaseModel):
    name: str
    source: str
    status: str

app = FastAPI()

@app.post("/datasets")
async def create_dataset(dataset: Dataset) -> Dataset:
    """Create a new dataset."""
    return dataset
```

### Frontend (Vue/TypeScript)

- Use **TypeScript** for type safety
- Use **Composition API** (Vue 3)
- Follow **Vue 3 style guide**
- Use **Vitest** for tests
- Format with **Prettier**

Example:
```typescript
<template>
  <div class="dataset-table">
    <table>
      <tr v-for="dataset in datasets" :key="dataset.id">
        <td>{{ dataset.name }}</td>
      </tr>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Dataset {
  id: string
  name: string
  source: string
}

const datasets = ref<Dataset[]>([])

onMounted(async () => {
  // Fetch datasets
})
</script>
```

---

## 📚 Documentation Standards

### When to Update Docs

- ✅ New feature = update docs
- ✅ API changes = update docs
- ✅ New module = create module manifest
- ✅ Breaking changes = update CHANGELOG

### Documentation Files

- **Architecture:** [docs/architecture/](docs/architecture/)
- **Backend:** [docs/backend/](docs/backend/)
- **Frontend:** [docs/frontend/](docs/frontend/)
- **Workflows:** [docs/workflows/](docs/workflows/)

---

## 🧪 Testing Requirements

### Backend Tests

```bash
cd apps/backend
pytest --cov=app --cov-report=html
```

### Frontend Tests

```bash
cd apps/frontend
npm run test:coverage
```

### Integration Tests

```bash
cd tests
# Run full integration suite
```

---

## 🔍 Code Review Checklist

Reviewers should verify:

- [ ] Code follows style guides
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No unnecessary dependencies added
- [ ] Commits are logically organized
- [ ] PR description is clear
- [ ] Related issue is linked
- [ ] No hardcoded values or secrets

---

## 🚀 Deployment Process

(To be defined in later phases)

---

## ❓ Questions?

- Check [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md)
- See [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md) for agent-specific guidance
- Open a [Discussion](../../discussions)

---

**Last Updated:** May 2026
