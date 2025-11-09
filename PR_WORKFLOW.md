# Pull Request Workflow Documentation
## PR-Based Collaboration Strategy

This document outlines the pull request (PR) workflow used in this project to ensure code quality and collaborative development.

---

## Branch Strategy

### Branch Naming Convention

**Consistent Pattern**: `eda-<country>` or `task-<number>`

- ✅ `setup-task` - Initial setup and configuration
- ✅ `eda-benin` - Benin EDA development
- ✅ `eda-sierraleone` - Sierra Leone EDA development  
- ✅ `eda-togo` - Togo EDA development

**Note**: All country branches follow the `eda-<country>` pattern for consistency.

---

## Pull Request Workflow

### Step 1: Create Feature Branch

```bash
# Create and switch to new branch
git checkout -b eda-benin

# Or from main
git checkout main
git pull origin main
git checkout -b eda-benin
```

### Step 2: Develop Feature

- Make changes on feature branch
- Commit frequently with descriptive messages
- Push to remote branch

```bash
git add .
git commit -m "feat: Add comprehensive EDA notebook for Benin dataset"
git push origin eda-benin
```

### Step 3: Create Pull Request

1. Go to GitHub repository
2. Click "New Pull Request"
3. Select base branch: `main`
4. Select compare branch: `eda-benin`
5. Add PR title and description
6. Request review if needed
7. Link related issues if applicable

### Step 4: PR Review Process

- **CI/CD Check**: Automated tests run on PR
- **Code Review**: Review changes
- **Address Feedback**: Make requested changes
- **Update PR**: Push additional commits if needed

### Step 5: Merge PR

- Once approved and CI passes, merge PR
- Options:
  - **Merge commit**: Creates merge commit
  - **Squash and merge**: Combines commits into one
  - **Rebase and merge**: Linear history

### Step 6: Clean Up

```bash
# Switch to main
git checkout main

# Pull latest changes
git pull origin main

# Delete local branch (optional)
git branch -d eda-benin

# Delete remote branch (optional)
git push origin --delete eda-benin
```

---

## PR Templates

### Feature PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Refactoring

## Related Tasks
- Task #X: Description

## Testing
- [ ] Code tested locally
- [ ] CI/CD pipeline passes
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Tests added/updated
```

---

## Example PRs Created

### PR #1: Initial Project Setup
- **From**: `setup-task`
- **To**: `main`
- **Description**: Initial repository setup, structure, and CI/CD configuration
- **Status**: ✅ Merged

### PR #2: Benin EDA Notebook
- **From**: `eda-benin`
- **To**: `main`
- **Description**: Comprehensive EDA notebook for Benin dataset
- **Status**: ✅ Merged

### PR #3: Sierra Leone EDA Notebook
- **From**: `eda-sierraleone`
- **To**: `main`
- **Description**: Comprehensive EDA notebook for Sierra Leone dataset
- **Status**: ✅ Merged

### PR #4: Togo EDA Notebook
- **From**: `eda-togo`
- **To**: `main`
- **Description**: Comprehensive EDA notebook for Togo dataset
- **Status**: ✅ Merged

---

## Benefits of PR Workflow

1. **Code Quality**: Review process catches issues early
2. **Collaboration**: Team members can review and suggest improvements
3. **Documentation**: PR descriptions document changes
4. **CI/CD Integration**: Automated tests run on every PR
5. **History**: Clear record of changes and decisions
6. **Safety**: Changes isolated in branches before merging

---

## Best Practices

1. **Small PRs**: Keep PRs focused and manageable
2. **Clear Descriptions**: Explain what and why
3. **Review Promptly**: Respond to review feedback quickly
4. **Test Before PR**: Ensure code works locally
5. **Update Documentation**: Keep docs in sync with code
6. **Follow Naming**: Use consistent branch naming convention

---

**Last Updated**: November 2025  
**Status**: Active Workflow

