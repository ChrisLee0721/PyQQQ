# 技术债清理计划

## 当前技术债

### 1. tensorcircuit numpy patch

**问题**：全局 monkey-patch `np.reshape` 和 `np.ComplexWarning`，影响同进程所有代码。

**状态**：已改为 `_tc_compat()` 上下文管理器，但仍保留 `_ensure_tc_numpy_compat()` 全局 patch 给测试用。

**清理方案**：
- 等上游 tensorcircuit 修复 numpy 2.x 兼容后删除
- 或：升级 tensorcircuit 到修复版本

### 2. cqlib 委托 native

**问题**：cqlib 不是模拟器，只能构造线路 + 导出 QASM。

**状态**：`_sample` 委托给 native StatevectorEngine，cqlib Circuit 从未真正使用。

**清理方案**：
- 方案 A：保留现状（委托 native），文档说明 cqlib 是构造库
- 方案 B：移除 cqlib 后端，只保留 as QASM 导出工具
- 建议：方案 A（保留，但文档说明）

### 3. i18n 文件过大

**问题**：`_i18n.py` 有 200+ 条消息，维护困难。

**清理方案**：
- 按模块拆分：`_i18n_backends.py`, `_i18n_gates.py`, `_i18n_errors.py`
- 或：用 JSON 文件存储，运行时加载
- 建议：保持现状（Python dict），但按模块注释分组

### 4. 测试覆盖不完整

**问题**：边缘 case 和错误路径测试不足。

**清理方案**：
- 补充自定义门 + 噪声 + 批量的边缘测试
- 补充 qif 嵌套 + cif + cwhile 的错误路径测试
- 补充 GPU 调度 + 能力矩阵的边界测试

### 5. 全局电路栈不支持并发

**问题**：`stack.py` 维护进程级全局电路栈，不支持同进程并发。

**清理方案**：
- 方案 A：保持现状（单进程全局状态）
- 方案 B：加 threading.local() 支持线程隔离
- 建议：方案 A（保持现状，文档说明）

### 6. 参数化电路 IR 不支持符号

**问题**：`Parameter` 类存在但 IR 中 params 是 `Tuple[float, ...]`，不支持符号表达式。

**清理方案**：
- 方案 A：保持现状（运行时绑定参数）
- 方案 B：IR 中 params 支持 `Union[float, Parameter]`
- 建议：方案 A（保持现状，`bind_params` 在运行时替换）

## 清理优先级

| 优先级 | 项 | 原因 |
|---|---|---|
| P0 | 测试覆盖补全 | 质量保障 |
| P1 | cqlib 文档说明 | 避免用户困惑 |
| P2 | i18n 分组 | 维护成本 |
| P3 | tensorcircuit patch | 等上游修复 |
| P3 | 全局栈并发 | 保持现状 |
| P3 | 参数化 IR | 保持现状 |
