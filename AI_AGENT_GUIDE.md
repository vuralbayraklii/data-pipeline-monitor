# AI Agent Guide

Instructions and conventions for AI agents working on this project.

## 🤖 Agent Operating Model

### Agent Roles

1. **Planning Agent** - Breaks down tasks into actionable steps
2. **Implementation Agent** - Writes code and creates files
3. **Review Agent** - Validates output against requirements
4. **Documentation Agent** - Maintains docs and progress tracking

This project treats agents as equal team members in the development process.

---

## 📋 How to Work with Agents

### Prompt Structure

When assigning work to an agent, use this format:

```
## Task: [Clear Title]

### Context
- Why is this needed?
- What does success look like?
- Any constraints or dependencies?

### Scope
- Include: What's IN scope
- Exclude: What's NOT in scope

### Requirements
- Acceptance criteria as checklist
- Must-haves vs nice-to-haves

### Resources
- Relevant files/docs
- Related issues/PRs
- Team guidelines (CONTRIBUTING.md, etc.)

### Output Format
- What should the agent deliver?
- Files to create/modify?
- Documentation needed?
```

### Example Agent Prompt

```
## Task: Implement Dataset Registry Backend Endpoints

### Context
Phase 1 requires a working dataset registry backend.
This is part of issue #5 and milestone M2.

### Scope
Include:
- POST /datasets (create)
- GET /datasets (list)
- GET /datasets/{id} (get one)
- Pydantic models
- Basic tests
- OpenAPI doc updates

Exclude:
- Database (use in-memory for now)
- Authentication
- Complex filtering/pagination

### Requirements
- [ ] All endpoints working
- [ ] Pydantic validation on all inputs
- [ ] 80%+ test coverage
- [ ] Type hints on all functions
- [ ] OpenAPI schema auto-generated
- [ ] Docs updated in docs/backend/api.md

### Resources
- See docs/backend/models.md for data structure
- Follow patterns in CONTRIBUTING.md
- Use examples from existing code in app/api/routes/health.py

### Output Format
1. Implementation plan (files to create/modify)
2. Code changes
3. Test output (coverage report)
4. Updated documentation
5. Commit message suggestions
```

---

## 🗂 Module Manifest Format

Agents should understand module structure via `manifests/modules/<name>.json`:

```json
{
  "module_name": "dataset-registry",
  "version": "0.1.0",
  "status": "in-development",
  "description": "Dataset registry backend and frontend",
  
  "backend": {
    "models": [
      "apps/backend/app/models/dataset.py"
    ],
    "routes": [
      "apps/backend/app/api/routes/datasets.py"
    ],
    "tests": [
      "tests/test_datasets.py"
    ]
  },
  
  "frontend": {
    "components": [
      "apps/frontend/src/components/DatasetTable.vue"
    ],
    "services": [
      "apps/frontend/src/services/datasets.ts"
    ],
    "tests": [
      "apps/frontend/src/tests/datasets.spec.ts"
    ]
  },
  
  "documentation": [
    "docs/backend/api.md",
    "docs/backend/models.md",
    "docs/frontend/components.md"
  ],
  
  "endpoints": [
    {
      "method": "POST",
      "path": "/datasets",
      "description": "Create new dataset"
    },
    {
      "method": "GET",
      "path": "/datasets",
      "description": "List all datasets"
    }
  ],
  
  "dependencies": {
    "backend": ["fastapi", "pydantic"],
    "frontend": ["vue", "typescript"]
  }
}
```

**Why this matters for agents:**
- Agents can parse module structure
- Clear file organization
- Easy to find related files
- Scalable as project grows

---

## 📝 Code Generation Standards

### Backend (FastAPI/Python)

When generating backend code:

```python
# ✅ DO: Include type hints and docstrings
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class DatasetCreate(BaseModel):
    """Schema for creating a dataset."""
    name: str
    source: str

class Dataset(DatasetCreate):
    """Schema for a dataset with metadata."""
    id: str
    status: str

router = APIRouter(prefix="/datasets", tags=["datasets"])

@router.post("", response_model=Dataset)
async def create_dataset(dataset: DatasetCreate) -> Dataset:
    """Create a new dataset.
    
    Args:
        dataset: The dataset to create
        
    Returns:
        The created dataset with ID
        
    Raises:
        HTTPException: If validation fails
    """
    # Implementation
    pass

# ❌ DON'T: Skip types or include placeholder comments
def create_dataset(dataset):
    # TODO: implement
    return dataset
```

### Frontend (Vue/TypeScript)

When generating frontend code:

```typescript
// ✅ DO: Use TypeScript interfaces and Composition API
<template>
  <div class="dataset-table">
    <table v-if="datasets.length > 0" class="table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Source</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="dataset in datasets" :key="dataset.id">
          <td>{{ dataset.name }}</td>
          <td>{{ dataset.source }}</td>
          <td>{{ dataset.status }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else class="empty">No datasets found</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Dataset } from '@/services/datasets'
import { fetchDatasets } from '@/services/datasets'

const datasets = ref<Dataset[]>([])
const isLoading = ref(false)
const error = ref<string | null>(null)

onMounted(async () => {
  await loadDatasets()
})

async function loadDatasets(): Promise<void> {
  isLoading.value = true
  error.value = null
  try {
    datasets.value = await fetchDatasets()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Unknown error'
  } finally {
    isLoading.value = false
  }
}
</script>

// ❌ DON'T: Use dynamic imports or skip type checking
// import dataset from 'xxx'  <- path not clear
// const x = ref()           <- no type
```

### Tests

When generating tests:

```python
# ✅ DO: Clear test names, arrange-act-assert pattern
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_dataset_success():
    """Test creating a dataset with valid data."""
    # Arrange
    payload = {
        "name": "sales",
        "source": "s3://bucket/sales"
    }
    
    # Act
    response = client.post("/datasets", json=payload)
    
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "sales"
    assert data["id"] is not None

def test_create_dataset_validation_error():
    """Test creating dataset with missing required field."""
    # Arrange
    payload = {"source": "s3://bucket"}  # missing 'name'
    
    # Act
    response = client.post("/datasets", json=payload)
    
    # Assert
    assert response.status_code == 422

# ❌ DON'T: Generic test names or unclear intent
# def test_1():
#     response = client.post(...)
#     assert response.status_code == 201
```

---

## 📊 Git Integration for Agents

### Commit Message Format

Agents should commit using Conventional Commits:

```
<type>(<scope>): <subject> | <issue#>

<optional detailed body>

<optional footer>
```

Examples:
```
feat(backend): add dataset CRUD endpoints | #5
test(backend): add 12 new tests for dataset module | #5
docs: document dataset registry API | #5
```

### PR Title Format

```
[<type>] <description> (Closes #<issue>)
```

Examples:
```
[feat] Implement dataset registry backend (Closes #5)
[docs] Update API documentation (Closes #7)
```

---

## ✅ Pre-Submission Checklist

Agents should verify before committing:

**Code Quality:**
- [ ] No `TODO` comments left
- [ ] No console.logs, print statements (except logging)
- [ ] No commented-out code
- [ ] Type hints complete
- [ ] Docstrings present
- [ ] Linting passes

**Testing:**
- [ ] Tests pass locally
- [ ] Coverage meets threshold (80%+)
- [ ] Edge cases covered
- [ ] Error paths tested

**Documentation:**
- [ ] README updated if needed
- [ ] API docs updated
- [ ] Code comments clear
- [ ] Module manifest updated

**Git:**
- [ ] Changes are logical
- [ ] Commit messages clear
- [ ] Linked to correct issue

---

## 🔗 Working with Linked Issues

Agents should:

1. **Link to issue:** Reference in PR title and body
   ```
   Closes #5
   Related to #3, #4
   ```

2. **Update issue:** Add progress comments
   ```
   Backend implementation complete: #5
   Now working on frontend...
   ```

3. **Mark as done:** When work complete
   ```
   Closes #5 via PR #42
   ```

---

## 📚 Project Knowledge Base

Agents should reference:

- **CONTRIBUTING.md** - Contribution standards
- **DEVELOPMENT_WORKFLOW.md** - Step-by-step process
- **docs/architecture/** - System design
- **manifests/modules/** - Module structure
- **Existing code** - Patterns to follow

---

## 🚨 Common Issues & Solutions

### Issue: "Where should I put this file?"

**Solution:** Check module manifest
```bash
# Find in manifests/modules/*.json
grep -r "backend.*routes" manifests/
# Answer: apps/backend/app/api/routes/
```

### Issue: "What code style should I use?"

**Solution:** Follow existing patterns
```bash
# Look at similar file
cat apps/backend/app/api/routes/health.py
# Copy style and structure
```

### Issue: "Should I include this dependency?"

**Solution:** Check CONTRIBUTING.md and existing requirements
- Only use approved tech stack
- Minimize dependencies
- Consider if already available

### Issue: "How do I know when I'm done?"

**Solution:** Check acceptance criteria in issue
- Each checkbox in requirements is a test
- Verify all are complete
- Test locally before submitting

---

## 🔄 Agent-to-Agent Communication

When one agent needs to hand off to another:

1. **Document context:**
   ```
   ## Context for Next Agent
   
   Previous work: Implemented backend endpoints
   Current status: Tests passing, docs written
   Next steps: Frontend implementation (issue #5 part 2)
   Blockers: None
   Notes: See manifests/modules/dataset-registry.json for structure
   ```

2. **Create clear handoff:** Use session notes or comments

3. **Update progress:** Mark issue status

---

## 📞 Getting Help

If an agent is stuck:

1. **Check existing documentation** - Answer usually there
2. **Review similar code** - Pattern already exists
3. **Ask in PR comments** - Request clarification
4. **Flag as blocker** - Mark issue with `status:blocked`

---

## 🎓 Learning Resources

Agents should be familiar with:

- [GitHub Docs - Getting Started](https://docs.github.com/en/get-started)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Vue 3 Guide](https://vuejs.org)
- This project's docs in `docs/`

---

## 📈 Success Metrics

Agent work is successful when:

- ✅ All acceptance criteria met
- ✅ Tests passing (80%+ coverage)
- ✅ Code review approved
- ✅ Documentation updated
- ✅ PR merged
- ✅ Issue closed automatically

---

**Last Updated:** May 2026  
**Version:** 1.0
