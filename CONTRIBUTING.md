# Contributing to QuoNic

Thanks for helping make quantum programming as simple as writing Python. All contributions — bug reports, feature requests, code, docs — are welcome.

[中文指南](#中文)

---

## Ways to contribute

- **Report a bug** — open an issue with a minimal reproduction and the backend/method you used.
- **Propose a feature** — open an issue describing the use case and the API you'd like to see.
- **Submit code** — new backends, gates, algorithms, scheduler features, visualizations, or bug fixes.
- **Improve docs** — fix typos, clarify examples, or translate (see [Language conventions](#language--i18n-conventions)).

## Development setup

```bash
git clone https://github.com/ChrisLee0721/QuoNic.git
cd QuoNic
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -e '.[dev]'
```

The `dev` extra installs `pytest`, `ruff`, and the numeric/plotting dependencies needed to run the test suite. To run the full suite including backend-specific tests, also install the backends you care about:

```bash
pip install -e '.[qiskit,cirq,pennylane,algorithms,viz]'
```

Backend tests use `pytest.importorskip`, so missing backends skip their tests rather than fail.

## Running tests and lint

```bash
pytest                 # run the whole suite (testpaths = tests)
ruff check src tests   # lint (E/F/I/W rules, line length 100)
```

Add tests for any new behavior. Existing tests live in `tests/` and mirror the public API.

## Code style

- Target Python 3.9; do **not** use `X | Y` union syntax or builtin generics in annotations. Use `typing` imports (`List`, `Dict`, `Optional`, `Union`, `FrozenSet`, ...).
- Put `from __future__ import annotations` at the top of every module.
- Type third-party objects (numpy arrays, etc.) as `Any` rather than importing their types.
- Follow `ruff check src tests`; it must pass.
- Keep docstrings and comments in English (see below).

## Language & i18n conventions

QuoNic is bilingual by design, with a strict split:

- **Source docstrings and comments** — English only.
- **Runtime strings** (errors, reports, the setup guide) — English by default, Chinese optional. They are centralized in `src/quonic/_i18n.py`. To add a user-facing message:
  1. Add a key to the `_MESSAGES` dict with `en` and `zh` entries.
  2. Call `tr("your.key", **fmt)` in the code instead of a hardcoded string.
  3. Never hardcode a raw error/report string.

The user-facing language is selected via the `QUONIC_LANG` environment variable (`en` or `zh`) or `quonic.set_language()`.

## Adding a backend

Backends subclass `quonic.backends.Backend` and implement `run()`:

```python
from quonic.backends import Backend
from quonic.ir import Circuit
from quonic.result import Result

class MyBackend(Backend):
    name = "mybackend"
    methods = frozenset({"statevector"})

    def run(self, circuit, shots=1024, noise=None, method="statevector"):
        # translate the Circuit into your engine, run it, and return
        return Result.from_counts({...})
```

Then:

1. Register it in the `_REGISTRY` dict in `src/quonic/backends/__init__.py`.
2. Add an optional dependency group in `pyproject.toml` (e.g. `[project.optional-dependencies] mybackend = [...]`).
3. Raise `tr("err.<name>_missing")` style messages when the dependency is absent (see the existing backends).
4. Add tests in `tests/`.

## Commit messages

Write concise, imperative commit subjects in English, e.g. `Add Cirq backend`, `Fix PennyLane set_shots compatibility`. Reference an issue number when relevant.

## Pull requests

- Keep PRs small and focused on one change.
- Ensure `pytest` and `ruff check src tests` pass.
- Update docs if you change public behavior.

---

## License

By contributing you agree that your work is licensed under the [Apache License 2.0](LICENSE).

---

## 中文

# 为 QuoNic 做贡献

感谢你让量子编程变得像写 Python 一样简单。任何形式的贡献——Bug 报告、功能建议、代码、文档——都欢迎。

[English guide](#contributing-to-quonic)

---

## 参与方式

- **报告 Bug** —— 提 issue，附上最小复现步骤和所用的 backend / method。
- **提出功能建议** —— 提 issue，描述使用场景和期望的 API。
- **提交代码** —— 新后端、新门、算法、调度器功能、可视化，或 Bug 修复。
- **完善文档** —— 修错别字、澄清示例，或翻译（见[语言约定](#语言与-i18n-约定)）。

## 开发环境

```bash
git clone https://github.com/ChrisLee0721/QuoNic.git
cd QuoNic
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -e '.[dev]'
```

`dev` 依赖组会装 `pytest`、`ruff` 以及跑测试所需的数值/绘图依赖。要跑包含后端相关测试的完整套件，再装你关心的后端：

```bash
pip install -e '.[qiskit,cirq,pennylane,algorithms,viz]'
```

后端测试用 `pytest.importorskip`，缺包时跳过而非失败。

## 跑测试与 lint

```bash
pytest                 # 跑完整套件（testpaths = tests）
ruff check src tests   # lint（E/F/I/W 规则，行长 100）
```

新行为都要补测试。现有测试在 `tests/`，与公开 API 一一对应。

## 代码风格

- 目标 Python 3.9；注解里**不要**用 `X | Y` 联合语法或内建泛型，用 `typing` 导入（`List`、`Dict`、`Optional`、`Union`、`FrozenSet`…）。
- 每个模块顶部加 `from __future__ import annotations`。
- 第三方对象（numpy 数组等）类型标注为 `Any`，不引入其类型。
- `ruff check src tests` 必须通过。
- docstring 与注释保持英文（见下）。

## 语言与 i18n 约定

QuoNic 天生双语，但严格分层：

- **源码 docstring 与注释** —— 只用英文。
- **运行时字符串**（报错、报告、引导文案）—— 默认英文、可选中文，集中在 `src/quonic/_i18n.py`。新增一条用户可见文案：
  1. 在 `_MESSAGES` 字典加一个含 `en` 与 `zh` 的 key。
  2. 代码里用 `tr("your.key", **fmt)` 而非硬编码字符串。
  3. 绝不硬编码原始报错/报告字符串。

用户语言通过 `QUONIC_LANG` 环境变量（`en` 或 `zh`）或 `quonic.set_language()` 切换。

## 新增后端

后端继承 `quonic.backends.Backend` 并实现 `run()`：

```python
from quonic.backends import Backend
from quonic.ir import Circuit
from quonic.result import Result

class MyBackend(Backend):
    name = "mybackend"
    methods = frozenset({"statevector"})

    def run(self, circuit, shots=1024, noise=None, method="statevector"):
        # 把 Circuit 翻译成你的引擎、运行、返回
        return Result.from_counts({...})
```

然后：

1. 在 `src/quonic/backends/__init__.py` 的 `_REGISTRY` 里注册它。
2. 在 `pyproject.toml` 加一个可选依赖组（如 `[project.optional-dependencies] mybackend = [...]`）。
3. 缺依赖时抛 `tr("err.<name>_missing")` 风格的消息（参考现有后端）。
4. 在 `tests/` 补测试。

## 提交信息

提交主题用简洁的英文祈使句，例如 `Add Cirq backend`、`Fix PennyLane set_shots compatibility`。相关时引用 issue 编号。

## Pull Request

- PR 保持小而聚焦，一次只改一件事。
- 确保 `pytest` 和 `ruff check src tests` 都通过。
- 改了公开行为就同步更新文档。

---

## 许可证

提交即表示你同意你的成果按 [Apache License 2.0](LICENSE) 授权。
