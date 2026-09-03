# Code Rules

## Dependency Flow

```
presentation → application → infrastructure
                   ↑               |
                   └───────────────┘
                   (via Protocols/ABCs)
```

Infrastructure implements interfaces defined in applications (Dependency Inversion).

---

## Singular vs Plural Package Names

**Recommendation: Singular**

| Aspect                   | Singular                                                                        | Plural                                     |
| ------------------------ | ------------------------------------------------------------------------------- | ------------------------------------------ |
| Python stdlib convention | ✅ `collections`, `typing`, `dataclasses` are exceptions, but most are singular | Mixed                                      |
| Import readability       | ✅ `from application.model import User`                                         | `from applications.models import User`     |
| Java/C# influence        | —                                                                               | ✅ (Django uses `models`, `views`)         |
| Consistency              | ✅ Easier to enforce                                                            | Debates on edge cases (`utils` vs `util`?) |

**Verdict:** Go **singular**. It's cleaner and avoids the "is it `util` or `utils`?" debates.

---

## The 10 Rules of Robust Python

> Principles for code that fails safely, tests easily, and evolves gracefully.

---

### 1. Fail Closed

Any failure in logic, connectivity, or validation **must deny access / abort operation**. Never fail open. Explicit is better than silent.

```python
# ✅ Good
if not is_authorized(user, resource):
    raise AccessDeniedError("Unauthorized")

# ❌ Bad
try:
    check_auth(user)
except Exception:
    pass  # Fails open
```

---

### 2. No Recursion

All tree/graph traversals **must use iterative stacks**. Recursion hides depth, blows stacks, and defies static analysis.

```python
# ✅ Good
def traverse(root: Node) -> list[Node]:
    stack = [root]
    result = []
    while stack:
        node = stack.pop()
        result.append(node)
        stack.extend(node.children)
    return result

# ❌ Bad
def traverse(node: Node) -> list[Node]:
    return [node] + [traverse(c) for c in node.children]
```

---

### 3. Bound All Loops

Every `while` loop **must have a hard exit**: `MAX_ITERATIONS`, `TIMEOUT_SECONDS`, or finite collection. Infinite loops are forbidden.

```python
# ✅ Good
MAX_ITERATIONS = 10_000
iterations = 0
while not done and iterations < MAX_ITERATIONS:
    iterations += 1
    # ...
if iterations >= MAX_ITERATIONS:
    raise TimeoutError("Loop bound exceeded")

# ❌ Very Bad
while not True:
    # ...

# ❌ Bad
while not done:
    # ...
```

---

### 4. Validate at the Boundary

Validate **all external input once**, at entry points. Use `TypeGuard` for runtime checks. Internal code assumes valid data.

```python
# ✅ Good — validation at API boundary
def create_user(data: dict[str, Any]) -> User:
    if not is_valid_user_input(data):  # TypeGuard
        raise ValidationError("Invalid input")
    return _create_user_internal(data)  # Trusts input

# ❌ Bad — validation scattered everywhere
def _internal_helper(data: dict) -> None:
    if "name" not in data:  # Redundant
        raise ...
```

---

### 5. Pure Functions First

Business logic **must be pure**: deterministic, no side effects, no I/O. Side effects live at the edges. Pure functions are trivially testable.

```python
# ✅ Good — pure logic, impure shell
def calculate_discount(price: Decimal, tier: Tier) -> Decimal:
    """Pure: same input = same output."""
    return price * DISCOUNT_RATES[tier]

def apply_discount(order_id: str, repo: OrderRepo) -> None:
    """Impure shell: I/O at edges."""
    order = repo.get(order_id)
    order.discount = calculate_discount(order.price, order.tier)
    repo.save(order)

# ❌ Bad — I/O mixed with logic
def calculate_and_save_discount(order_id: str) -> None:
    order = db.query(order_id)  # I/O inside
    order.discount = order.price * 0.1
    db.save(order)  # I/O inside
```

---

### 6. Inject Dependencies

**Never instantiate collaborators internally**. Pass them in. This enables testing, composition, and flexibility.

```python
# ✅ Good — dependencies injected
class OrderService:
    def __init__(self, repo: OrderRepository, notifier: Notifier) -> None:
        self._repo = repo
        self._notifier = notifier

# ❌ Bad — hidden dependencies
class OrderService:
    def __init__(self) -> None:
        self._repo = PostgresOrderRepository()  # Hardcoded
        self._notifier = EmailNotifier()        # Untestable
```

---

### 7. Compose, Don't Inherit

**Maximum 2 levels of inheritance**. Prefer composition and Protocols. Use ABCs only when enforcement is required.

```python
# ✅ Good — composition + protocol
class PaymentProcessor:
    def __init__(self, gateway: PaymentGateway, logger: Logger) -> None:
        self._gateway = gateway
        self._logger = logger

# ⚠️ Acceptable — shallow inheritance
class Animal(ABC): ...
class Dog(Animal): ...

# ❌ Bad — deep hierarchy
class Animal: ...
class Mammal(Animal): ...
class Canine(Mammal): ...
class Dog(Canine): ...
class Labrador(Dog): ...
```

---

### 8. Abstract Last

**No interface until two implementations exist**. Premature abstraction creates waste. Let patterns emerge from duplication.

```python
# ✅ Good — abstract after second impl
class PostgresRepo: ...
class MongoRepo: ...
# NOW create Protocol/ABC

# ❌ Bad — speculative abstraction
class Repository(ABC): ...  # Only one impl exists
class PostgresRepo(Repository): ...
```

---

### 9. No Magic

Forbidden in business logic: `eval()`, `exec()`, `getattr()` on untrusted keys, `**kwargs` passthrough, dynamic imports. Explicit beats clever.

```python
# ✅ Good — explicit dispatch
HANDLERS: dict[str, Handler] = {
    "create": CreateHandler(),
    "delete": DeleteHandler(),
}
handler = HANDLERS.get(action)
if handler is None:
    raise ValueError(f"Unknown action: {action}")

# ❌ Bad — magic dispatch
handler = getattr(self, f"handle_{action}")()  # Arbitrary method call
```

---

### 10. Test Behavior, Not Implementation

Focus on *what* the simulation does, not *how* it's calculated.

- **TDD for Logic**: Mandate test-first for the `core/` and `game/` layers. Write the state assertion before the math.
- **Vanilla BDD**: Use `Given/When/Then` for MDP transitions (State + Action → New State + Reward).
- **Engine Mocks**: Injected engines must use `spec=True` to ensure the logic interacts correctly with the renderer/audio interface without triggering hardware.
- **Headless Only**: All logic tests must run without a GPU or Window context.

---

## Configuration vs. Constants

To maintain simulation integrity and architectural flexibility:

1.  **Constants in Core**: Use `src/mygame/core/constant.py` for values like `GRAVITY` or `FRICTION`. This keeps the "Laws of Physics" local to the simulation.
2.  **Config in Engine**: Use `src/mygame/engine/config.py` for hardware-specific values like `WINDOW_WIDTH` or `FPS`.
3.  **No Config in Logic**: `core/physics.py` and `game/gameplay.py` **must never** import from `engine/config.py`.
4.  **Engine Injection**: The `engine/` package is the only place allowed to import `pyray`. The rest of the app receives the engine as a dependency, allowing for a "Headless" vs "Human" rendered environment.

---


### Quick Reference Card

| #   | Rule                   | Key Phrase                   |
| --- | ---------------------- | ---------------------------- |
| 1   | Fail Closed            | Deny on error                |
| 2   | No Recursion           | Iterative stacks             |
| 3   | Bound All Loops        | `MAX_ITERATIONS`             |
| 4   | Validate at Boundary   | TypeGuard at entry           |
| 5   | Pure Functions First   | Logic without I/O            |
| 6   | Inject Dependencies    | Pass, don't construct        |
| 7   | Compose, Don't Inherit | Max 2 levels                 |
| 8   | Abstract Last          | Two impls, then interface    |
| 9   | No Magic               | No `eval`, `exec`, `getattr` |
| 10  | Test the Invariants    | Property-based + `spec=True` |

---

## Commit Guidelines

### Commit Frequency

1. **One Logical Unit = One Commit**
   - A single feature, fix, refactor, or doc change
   - If you can't describe it in 50 chars, it's too big

2. **Maximum Scope per Commit**
   - ≤ 5 files changed (soft limit)
   - ≤ 200 lines changed (soft limit)
   - If exceeded, split semantically

3. **Commit Triggers**
   - ✅ Completed a function/class that works in isolation
   - ✅ Fixed a single bug
   - ✅ Refactored one module
   - ✅ Added/updated tests for one unit
   - ✅ Updated docs for one feature
   - ❌ "WIP", "fix stuff", "updates"

---

### Semantic Splitting Strategy

When changes are too large, split by:

| Priority | Split By | Example                                             |
| -------- | -------- | --------------------------------------------------- |
| 1        | Layer    | `feat(api): add endpoint` → `feat(core): add logic` |
| 2        | Domain   | `feat(user): ...` → `feat(order): ...`              |
| 3        | Type     | `feat: ...` → `test: ...` → `docs: ...`             |

---

### Pre-commit Workflow

All commits pass through prek hooks. Before committing:

1. **Stage changes**: `git add <files>`
2. **Run prek**: Automatic on `git commit`
3. **If hooks fail**: Fix issues, re-stage, retry
4. **If hooks modify files**: Re-stage modified files, retry

---

### Quick Commands

```bash
# Check before committing (optional, hooks run anyway)
prek run --staged

# Fix and retry
git add -u && git commit

# Bypass in emergency (RARE — requires justification)
git commit --no-verify -m "hotfix: critical prod fix [skip-hooks]"
```

---

### Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Types

| Type       | Description                  |
| ---------- | ---------------------------- |
| `feat`     | New feature                  |
| `fix`      | Bug fix                      |
| `refactor` | Code change (no feature/fix) |
| `perf`     | Performance improvement      |
| `test`     | Adding/updating tests        |
| `docs`     | Documentation only           |
| `chore`    | Build, CI, dependencies      |
| `ci`       | CI configuration             |
| `style`    | Formatting (no logic change) |

#### Scopes

| Scope    | Description                     |
| -------- | ------------------------------- |
| `api`    | Public API (`mylib/api/`)       |
| `core`   | Core algorithms (`mylib/core/`) |
| `typing` | Type definitions                |
| `cli`    | CLI commands                    |
| `deps`   | Dependencies                    |

---

## Post actions

```markdown
# Actions

## Commit Discipline

1. **Commit after each logical unit of work**
   - One feature, fix, refactor, or test suite
   - Maximum ~5 files or ~200 lines (soft limit)

2. **Semantic splitting** — If changes span multiple concerns:
   | Order | Commit |
   |-------|--------|
   | 1 | Core logic / models |
   | 2 | API / interface |
   | 3 | Tests |
   | 4 | Documentation |

3. **Pre-commit compliance**
   - All commits must pass prek hooks
   - Run `make commit-check` before committing
   - If hooks auto-fix files, re-stage and retry

4. **Message format** — Conventional Commits:
```

---

## Tool Stack

| Tool         | Replaces                     | Purpose                         |
| ------------ | ---------------------------- | ------------------------------- |
| **uv**       | pip, pip-tools, venv, poetry | Fast package/project management |
| **ruff**     | black, isort, flake8, pylint | Linting + formatting            |
| **ty check** | —                            | Type checking                   |
| **pytest**   | unittest                     | Testing                         |
| **just**     | make                         | Command runner                  |
| **prek**     | pre-commit                   | Pre commit hooks                |

---
