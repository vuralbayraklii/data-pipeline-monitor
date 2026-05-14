# Development Workflow

Complete step-by-step guide for developing in this project.

## 📌 Overview

The development workflow follows this sequence:

```
Issue → Branch → Develop → Commit → Test → Docs → PR → Review → Merge
```

---

## 🎯 Phase 1: Issue Management

### 1.1 Understanding the Issue

Each issue includes:
- **Title:** Clear, descriptive
- **Description:** Context and what needs to be done
- **Acceptance Criteria:** Specific requirements to meet
- **Labels:** Type and area (e.g., `type:feature`, `area:backend`)
- **Milestone:** Which phase/sprint

### 1.2 Claiming an Issue

1. Read the issue fully
2. Check acceptance criteria
3. Assign yourself: "I'll work on this"
4. Move to "In Progress" on project board

### Example Issue Review

```markdown
## Title
Implement dataset registry backend endpoints

## Description
We need basic CRUD endpoints for the dataset registry.

## Acceptance Criteria
- [ ] POST /datasets - Create dataset
- [ ] GET /datasets - List all datasets
- [ ] GET /datasets/{id} - Get single dataset
- [ ] Pydantic models for validation
- [ ] 80% test coverage
- [ ] OpenAPI docs generated

## Tasks
- Backend endpoints
- Data models
- Tests
- Documentation
```

---

## 🌿 Phase 2: Branch Management

### 2.1 Creating a Branch

**Naming Pattern:**
```
<type>/<descriptive-name>
```

**Valid Types:**
- `feature/` - New functionality
- `bugfix/` - Bug fixes
- `docs/` - Documentation only
- `chore/` - Maintenance, dependencies
- `refactor/` - Code reorganization

### 2.2 Branch Creation Commands

```bash
# Update main branch
git checkout main
git pull origin main

# Create new branch
git checkout -b feature/dataset-registry-backend

# Or: Create and push
git push -u origin feature/dataset-registry-backend
```

### 2.3 Branch Hygiene

- One issue = one branch
- Branch from latest `main`
- Keep branch short-lived (under 1 week ideally)
- Delete after merge

---

## 💻 Phase 3: Development

### 3.1 File Structure for Your Changes

**Example: Dataset Registry Feature**

```
apps/
  backend/
    app/
      models/
        dataset.py          # ← Data model
      api/
        routes/
          datasets.py       # ← API endpoints
  frontend/
    src/
      components/
        DatasetTable.vue    # ← UI component
      services/
        datasets.ts         # ← API client
      tests/
        datasets.spec.ts    # ← Tests

tests/
  integration/
    test_dataset_flow.py    # ← Integration tests
```

### 3.2 Development Best Practices

#### Start Small
- Implement one endpoint at a time
- Test each part as you go
- Don't wait until the end to test

#### Use Type Hints (Backend)
```python
from typing import List
from pydantic import BaseModel

class DatasetCreate(BaseModel):
    name: str
    source: str

async def create_dataset(dataset: DatasetCreate) -> Dataset:
    ...
```

#### Use TypeScript (Frontend)
```typescript
interface Dataset {
  id: string
  name: string
  source: string
  status: 'active' | 'archived'
}
```

#### Write Tests Alongside Code
```python
# In tests/test_datasets.py
def test_create_dataset():
    dataset = Dataset(name="sales", source="s3://bucket")
    assert dataset.name == "sales"
```

#### Reference the Issue
Keep issue number visible:
```
# Working on issue #5: Dataset Registry
```

---

## 📝 Phase 4: Committing Changes

### 4.1 Commit Message Format

Use Conventional Commits:

```
<type>(<scope>): <subject>

<optional body>

<optional footer>
```

### 4.2 Examples

**Single file change:**
```
feat(backend): add dataset creation endpoint
```

**Multiple related changes:**
```
feat(backend): implement dataset registry endpoints

- Add POST /datasets for creation
- Add GET /datasets for listing  
- Add GET /datasets/{id} for retrieval
- Implement Pydantic validation

Closes #5
```

**Documentation:**
```
docs: add dataset registry API documentation
```

**Bugfix:**
```
fix(frontend): correct dataset table sorting

The table was sorting by string comparison instead of date.
Now uses proper date comparison for status updates.
```

### 4.3 When to Commit

Commit after:
- ✅ Adding a complete feature
- ✅ Writing tests for that feature
- ✅ Fixing a specific bug
- ✅ Updating related documentation

**NOT after:**
- ❌ Every 5 lines of code
- ❌ Partial implementations
- ❌ Code that doesn't run

### 4.4 Commit Commands

```bash
# Stage specific files
git add app/models/dataset.py
git add app/api/routes/datasets.py

# Or stage all changes
git add .

# Commit with message
git commit -m "feat(backend): add dataset registry endpoints"

# View commits
git log --oneline -10
```

---

## 🧪 Phase 5: Testing

### 5.1 Backend Testing

```bash
cd apps/backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_datasets.py

# Run with coverage
pytest --cov=app --cov-report=html

# Run and show output
pytest -v -s
```

### 5.2 Frontend Testing

```bash
cd apps/frontend

# Run all tests
npm run test

# Run specific test
npm run test -- datasets.spec.ts

# Run with coverage
npm run test:coverage

# Watch mode
npm run test:watch
```

### 5.3 What Tests Should Cover

- ✅ Happy path (normal operation)
- ✅ Error cases (validation errors)
- ✅ Edge cases (empty data, null values)
- ✅ Integration points (API calls)

**Example Backend Test:**
```python
def test_create_dataset_with_valid_data():
    """Happy path: create dataset with all fields."""
    payload = {
        "name": "sales",
        "source": "s3://bucket/sales"
    }
    response = client.post("/datasets", json=payload)
    assert response.status_code == 201
    assert response.json()["name"] == "sales"

def test_create_dataset_missing_name():
    """Error case: missing required field."""
    payload = {"source": "s3://bucket"}
    response = client.post("/datasets", json=payload)
    assert response.status_code == 422

def test_list_empty_datasets():
    """Edge case: list when no datasets exist."""
    response = client.get("/datasets")
    assert response.status_code == 200
    assert response.json() == []
```

---

## 📚 Phase 6: Documentation

### 6.1 When to Update Docs

**Always update documentation when:**
- Adding new API endpoints
- Changing data models
- Adding new frontend pages
- Modifying workflows
- Making breaking changes

### 6.2 What to Document

#### Backend API
File: `docs/backend/api.md`

```markdown
## Dataset Endpoints

### POST /datasets
Create a new dataset

**Request Body:**
- name (string, required)
- source (string, required)

**Response:**
```json
{
  "id": "uuid",
  "name": "sales",
  "status": "active"
}
```

### GET /datasets
List all datasets

**Query Parameters:**
- status (optional): filter by status
- limit (optional, default 50): page size

**Response:**
```json
[{...}, {...}]
```
```

#### Frontend Components
File: `docs/frontend/components.md`

```markdown
## DatasetTable Component

Displays a table of datasets with sorting and filtering.

**Props:**
- datasets: Dataset[] - Array of datasets
- loading: boolean - Show loading state
- sortBy: string - Current sort column

**Events:**
- @dataset-selected - User selected a dataset
- @refresh - User clicked refresh button

**Usage:**
```vue
<DatasetTable 
  :datasets="datasets"
  :loading="isLoading"
  @dataset-selected="handleSelect"
/>
```
```

### 6.3 Docs Structure

```
docs/
  architecture/     # System design
  backend/          # Backend docs
    api.md          # API endpoints
    models.md       # Data models
    setup.md        # Backend setup
  frontend/         # Frontend docs
    components.md   # Component library
    setup.md        # Frontend setup
  workflows/        # Processes
    github.md       # GitHub workflows
```

---

## 🔀 Phase 7: Pull Request

### 7.1 Before Opening PR

Checklist:
- [ ] Code is complete and working
- [ ] All tests pass locally
- [ ] Documentation updated
- [ ] Branch is up to date with main
- [ ] No debug code or console.logs
- [ ] No secrets or credentials

### 7.2 Opening a Pull Request

```bash
# Push your branch
git push origin feature/your-branch

# GitHub will show a prompt to open PR
# Or go to repo and click "New Pull Request"
```

### 7.3 PR Template

The PR template guides you:

```markdown
## Description
What does this PR do? (2-3 sentences)

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Refactoring

## Related Issue
Closes #5

## Testing Done
How did you test this? What scenarios?

## Docs Updated
- [ ] API documentation
- [ ] Architecture docs
- [ ] Code comments

## Screenshots/Logs
(If applicable - UI changes, error logs, etc.)

## Checklist
- [ ] Code follows style guide
- [ ] Tests pass
- [ ] No breaking changes
- [ ] Documentation is updated
```

### 7.4 PR Best Practices

- **One issue per PR** - Easier to review
- **Focused scope** - Don't mix concerns
- **Clear description** - Explain the "why"
- **Link the issue** - Use "Closes #5"
- **Responsive** - Address feedback quickly

---

## ✅ Phase 8: CI/CD & Review

### 8.1 GitHub Actions

When you push, actions run automatically:

1. **Tests** - Run pytest and npm test
2. **Linting** - Code style checks
3. **Build** - Verify builds succeed

**Monitoring:**
- Check PR for status indicator
- Click "Details" to see logs
- Fix failing checks before requesting review

### 8.2 Code Review

**What to expect:**
- Reviewers check logic, style, tests
- Comments on specific lines
- Approval or "Request Changes"

**Responding to comments:**
- Reply with explanation or fix
- Push new commits (don't force-push)
- Re-request review after changes

**Example comment flow:**
```
Reviewer: "This should use async/await"
You:      "Good point, I'll update"
You:      (push new commit)
You:      (click "Re-request review")
Reviewer: ✅ Approved
```

---

## 🎉 Phase 9: Merge & Close

### 9.1 Merge Criteria

PR can merge when:
- ✅ All checks pass
- ✅ At least one approval (if required)
- ✅ No conflicts with main
- ✅ Code coverage maintained

### 9.2 Merging

**On GitHub:**
1. Scroll to merge button
2. Choose merge strategy:
   - **Squash & merge** - One commit (usually)
   - **Create merge commit** - Keep history
   - **Rebase & merge** - Linear history
3. Click merge
4. Delete branch

**Result:**
- PR closes automatically
- Linked issue closes automatically
- Branch is deleted

### 9.3 Post-Merge

```bash
# Pull latest main
git checkout main
git pull origin main

# Verify merge
git log --oneline -5

# Clean up local branch
git branch -d feature/your-branch
```

---

## 📊 Tracking Progress

### Milestone Progress
- Check milestone to see completed issues
- Update issue status on project board
- Note blockers in comments

### When Stuck
1. Comment on issue describing blocker
2. Link related issues
3. Ask questions clearly
4. Request help/guidance

---

## 🔁 Complete Example Walkthrough

### Issue: Implement Dataset Registry Backend

```bash
# 1. Create branch
git checkout -b feature/dataset-registry

# 2. Create models
# app/models/dataset.py
# - Add Dataset, DatasetCreate classes

# 3. Write endpoint
# app/api/routes/datasets.py
# - Add POST /datasets
# - Add GET /datasets

# 4. Commit
git add .
git commit -m "feat(backend): add dataset models and endpoints"

# 5. Write tests
# tests/test_datasets.py
# - Test create endpoint
# - Test list endpoint

# 6. Run tests
pytest --cov

# 7. Commit tests
git add tests/
git commit -m "test(backend): add dataset endpoint tests"

# 8. Update docs
# docs/backend/api.md
# - Document endpoints

# 9. Commit docs
git add docs/
git commit -m "docs: add dataset endpoint documentation"

# 10. Push
git push -u origin feature/dataset-registry

# 11. Open PR on GitHub
# - Fill template
# - Link issue: "Closes #5"

# 12. Wait for CI
# - Tests pass ✅
# - Linting passes ✅

# 13. Request review

# 14. Address feedback

# 15. Merge when approved

# 16. Verify issue auto-closes
```

---

## ⚙️ Workflow Checklist

Print this and check off as you go:

**Planning:**
- [ ] Issue clearly understood
- [ ] Acceptance criteria noted
- [ ] Assigned to self

**Development:**
- [ ] Branch created from latest main
- [ ] Code written with types
- [ ] Tests added
- [ ] Tests passing locally
- [ ] Docs updated

**Submission:**
- [ ] Branch pushed
- [ ] PR created with template filled
- [ ] Issue linked (Closes #X)
- [ ] CI checks passing

**Review:**
- [ ] Responded to feedback
- [ ] Re-requested review if needed
- [ ] Approved by reviewer(s)

**Closure:**
- [ ] PR merged
- [ ] Branch deleted
- [ ] Issue auto-closed
- [ ] Main pulled locally

---

**For more info:** See [CONTRIBUTING.md](CONTRIBUTING.md) and [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md)

**Last Updated:** May 2026
