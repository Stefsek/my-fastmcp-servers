# Git Commit Message Style Guidelines

## Core Format
```
<type>[optional scope]: <description>

[optional body]
```

## Required Elements

### Types (Required)
- `feat`: New feature
- `fix`: Bug fix  
- `docs`: Documentation only
- `style`: Formatting/style (no logic changes)
- `refactor`: Code restructuring (no behavior change)
- `perf`: Performance improvement
- `test`: Adding/updating tests
- `build`: Build system/dependency changes
- `ci`: CI/CD configuration changes
- `chore`: Miscellaneous (tooling, configs)
- `revert`: Reverting previous commit

### Scope (Optional)
Affected component/module in parentheses: `feat(auth):`, `fix(api):`, `docs(readme):`

### Description (Required)
Concise summary of the change in imperative mood

## Formatting Rules

### Subject Line
- **Max 50 characters**
- **Capitalize first letter**
- **No ending period**
- **Use imperative mood** ("Add" not "Added" or "Adds")
- Test: "If applied, this commit will [your description]"

### Body (Optional)
- Separate from subject with blank line
- Wrap at 72 characters
- Explain **what** and **why**, not how
- Include breaking changes if any

## Examples by Type

```
feat(auth): add two-factor authentication
fix(api): resolve timeout in user data fetch
docs(readme): update installation instructions
style(components): format code with prettier
refactor(utils): extract validation into separate module
perf(queries): optimize database connection pooling
test(auth): add unit tests for login validation
build(deps): upgrade react from 17 to 18
ci(github): add automated security scanning
chore(config): update eslint configuration
revert: feat(auth): add social login
```

## Breaking Changes
Add `!` after type/scope or include `BREAKING CHANGE:` in body:
```
feat!: remove deprecated v1 API endpoints
```

## Body Examples
```
feat(notifications): add email notification system

Implements email notifications for security events including
password changes and failed login attempts. Uses SendGrid API
for delivery with configurable user preferences.
```

## Anti-Patterns to Avoid
- Vague: "fix bug", "update stuff", "changes"
- Wrong tense: "Fixed bug" (use "Fix bug")
- Too long: Subject lines over 50 characters
- Missing type: "update user validation"
- Ending punctuation: "Add new feature."

## Quick Decision Tree
1. What type of change? → Choose appropriate type prefix
2. Specific component affected? → Add scope in parentheses
3. Describe the change in imperative mood
4. Keep under 50 characters
5. Need more context? → Add body with blank line separation

## LLM Generation Tips
- Always start with type classification
- Focus on the primary change, ignore minor formatting
- Use active, imperative voice
- Be specific but concise
- Include scope when the change affects a particular module/component
