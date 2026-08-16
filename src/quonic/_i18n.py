"""User-facing string localization (English default, Chinese optional).

Runtime messages — error text, terminal reports, the interactive setup guide —
are centralized here. Source-code docstrings and comments are NOT localized
(they stay English; see the surrounding docs).

Language selection, in priority order:

1. ``set_language("zh")`` called at runtime.
2. The ``QUONIC_LANG`` environment variable (``"en"`` or ``"zh"``).

``tr(key, **fmt)`` looks up the current language's template and interpolates
the given keyword arguments via ``str.format``. Missing keys fall back to
English, then to the raw key, so an untranslated message never crashes.
"""

from __future__ import annotations

import os
from typing import Any, Dict

_LANGUAGES = ("en", "zh")

# fmt: off
_MESSAGES: Dict[str, Dict[str, str]] = {
    # --------------------------------------------------------- setup guide
    "setup.default_name": {
        "en": "this backend",
        "zh": "该后端",
    },
    "setup.login_fallback": {
        "en": "login",
        "zh": "登录",
    },
    "setup.configuring": {
        "en": "Configuring {name} backend (one-time, ~1 min)...",
        "zh": "正在配置 {name} 后端（一次性，约 1 分钟）...",
    },
    "setup.missing_dep": {
        "en": "\n[1/3] Missing dependency {pkg}",
        "zh": "\n[1/3] 缺少依赖 {pkg}",
    },
    "setup.will_run": {
        "en": "      Will run: pip install '{install}'",
        "zh": "      将执行：pip install '{install}'",
    },
    "setup.press_enter_install": {
        "en": "      Press Enter to install, type n to skip",
        "zh": "      回车开始安装，输入 n 跳过",
    },
    "setup.conflict_detected": {
        "en": "\n[2/3] Detected {pkg} {installed}, conflicts with requirement {constraint}",
        "zh": "\n[2/3] 检测到 {pkg} {installed}，与要求 {constraint} 冲突",
    },
    "setup.need_login": {
        "en": "\n[3/3] Login required (runs {cmd}, browser authorization)",
        "zh": "\n[3/3] 需要登录（运行 {cmd}，浏览器授权）",
    },
    "setup.press_enter_login": {
        "en": "      Press Enter to log in, type n to skip",
        "zh": "      回车开始登录，输入 n 跳过",
    },
    "setup.logged_in": {
        "en": "      OK: logged in",
        "zh": "      ✓ 已登录",
    },
    "setup.login_incomplete": {
        "en": "      Login incomplete, please run {cmd} manually",
        "zh": "      登录未完成，请手动运行 {cmd}",
    },
    "setup.ready": {
        "en": "\n{name} backend is ready.",
        "zh": "\n✓ {name} 后端已就绪。",
    },
    "setup.not_ready": {
        "en": "\nConfiguration incomplete, retry the guide later.",
        "zh": "\n配置未完成，可稍后重试引导。",
    },
    "setup.how_to_handle": {
        "en": "      How to handle:",
        "zh": "      处理方式：",
    },
    "setup.opt_downgrade": {
        "en": "        Enter = downgrade {pkg} to {constraint} (affects current env)",
        "zh": "        回车 = 回退 {pkg} 到 {constraint}（影响当前环境）",
    },
    "setup.opt_venv": {
        "en": "        2    = create isolated venv (recommended, avoids conflicts)",
        "zh": "        2    = 创建独立虚拟环境（推荐，隔离冲突）",
    },
    "setup.opt_skip": {
        "en": "        3    = skip, I'll handle it myself",
        "zh": "        3    = 跳过，我自行处理",
    },
    "setup.prompt_input": {
        "en": "      Please enter",
        "zh": "      请输入",
    },
    "setup.will_run_pip": {
        "en": "      Will run: pip install '{pkg}{constraint}'",
        "zh": "      执行：pip install '{pkg}{constraint}'",
    },
    "setup.venv_create": {
        "en": "      Create isolated venv (avoids conflicts):",
        "zh": "      创建独立虚拟环境（隔离冲突）：",
    },
    "setup.venv_rerun": {
        "en": "      Then rerun your program in the activated environment.",
        "zh": "      然后在激活的环境里重新运行你的程序。",
    },
    "setup.confirm_hint": {
        "en": " [Enter=yes / n=no] ",
        "zh": " [回车=是 / n=否] ",
    },
    "setup.menu_suffix": {
        "en": ": ",
        "zh": "：",
    },

    # ------------------------------------------------------------- qshow
    "show.empty_circuit": {
        "en": "(current circuit is empty; build it first with qgate(...))",
        "zh": "（当前电路为空，请先用 qgate(...) 构建电路）",
    },
    "show.noise_cost": {
        "en": "Note: depolarizing noise uses density_matrix (4^n resources); "
              "reference machine exceeds budget at n>={infeasible}. "
              "Current n={n}, may be slow or run out of memory.",
        "zh": "提示：去极化噪声走 density_matrix（4^n 资源），"
              "参考机实测 n>={infeasible} 时已超预算。当前 n={n}，可能很慢或内存不足。",
    },
    "show.circuit_resources": {
        "en": "Circuit resources:",
        "zh": "电路资源:",
    },
    "show.gate_count": {
        "en": "  gates: {n}",
        "zh": "  门数: {n}",
    },
    "show.depth": {
        "en": "  depth: {n}",
        "zh": "  深度: {n}",
    },
    "show.qubit_count": {
        "en": "  qubits: {n}",
        "zh": "  量子比特: {n}",
    },
    "show.backend_header": {
        "en": "backend: {name} | ",
        "zh": "后端: {name} | ",
    },
    "show.shots": {
        "en": "shots: {shots}",
        "zh": "shots: {shots}",
    },
    "show.result": {
        "en": "Result:",
        "zh": "结果:",
    },

    # ---------------------------------------------------------- benchmark
    "bench.capabilities": {
        "en": "Capability matrix:",
        "zh": "能力矩阵：",
    },
    "bench.performance": {
        "en": "\nPerformance data:",
        "zh": "\n性能数据：",
    },
    "bench.decision": {
        "en": "\nDerived decision table:",
        "zh": "\n推导的决策表：",
    },
    "bench.general": {
        "en": "\nHigh-treewidth non-Clifford (statevector checkpoints):",
        "zh": "\n高树宽非 Clifford（statevector 验证点）：",
    },
    "bench.noise": {
        "en": "\nNoise (density_matrix, 4^n cost):",
        "zh": "\n噪声（density_matrix，4^n 成本）：",
    },
    "bench.infeasible": {
        "en": "  Infeasible threshold (>{budget}s): {infeasible_n}",
        "zh": "  不可行阈值（>{budget}s）：{infeasible_n}",
    },
    "bench.written": {
        "en": "\nWritten to {output}",
        "zh": "\n已写入 {output}",
    },

    # -------------------------------------------------------- setup errors
    "err.parse_constraint": {
        "en": "Cannot parse version constraint '{constraint}'",
        "zh": "无法解析版本约束 '{constraint}'",
    },
    "err.need_install": {
        "en": "Using {name} backend requires installing {pkg}:\n"
              "    pip install '{install}'\n"
              "or run python -m quonic.setup for guided setup",
        "zh": "使用 {name} 后端需要安装 {pkg}：\n"
              "    pip install '{install}'\n"
              "或运行 python -m quonic.setup 一键引导配置",
    },
    "err.conflict": {
        "en": "{name} backend has version conflict: {pkg} currently {installed}, "
              "requires {constraint}.\n"
              "Run python -m quonic.setup to resolve (downgrade / venv / skip)",
        "zh": "{name} 后端存在版本冲突：{pkg} 当前 {installed}，要求 {constraint}。\n"
              "可运行 python -m quonic.setup 引导处理（回退 / 建虚拟环境 / 跳过）",
    },
    "err.need_login": {
        "en": "Using {name} backend requires one-time login:\n"
              "    run {cmd}\n"
              "or run python -m quonic.setup for guided setup",
        "zh": "使用 {name} 后端需要先登录（一次性）：\n"
              "    运行 {cmd}\n"
              "或运行 python -m quonic.setup 一键引导配置",
    },

    # ------------------------------------------------------- backend errors
    "err.unknown_backend": {
        "en": "Unknown backend '{name}'. Available engines: {engines}",
        "zh": "未知的后端 '{name}'。当前可用引擎：{engines}",
    },
    "err.no_method_support": {
        "en": "No backend supports method '{method}'",
        "zh": "没有任何后端支持方法 '{method}'",
    },
    "err.device_alias_conflict": {
        "en": "backend='{backend}' already specifies device '{alias_device}', "
              "cannot also pass device='{device}'",
        "zh": "backend='{backend}' 已指定设备 '{alias_device}'，"
              "不能同时再传 device='{device}'",
    },
    "err.device_only_qi": {
        "en": "device is only valid for backend='qi' (Quantum Inspire hardware/cloud "
              "simulator); current backend='{backend}' is a local simulator",
        "zh": "device 参数仅对 backend='qi'（Quantum Inspire 真机/云模拟器）有效；"
              "当前 backend='{backend}' 是本地模拟器，无需指定设备",
    },
    "err.qi_noise": {
        "en": "qi backend runs real hardware and cannot inject noise; use the qiskit "
              "backend (Aer density_matrix) to simulate depolarizing noise",
        "zh": "qi 后端运行真实硬件，无法注入噪声 noise；"
              "请用 qiskit 后端（Aer density_matrix）模拟去极化噪声",
    },
    "err.qi_cwhile": {
        "en": "qi backend does not support cwhile (classical feedback loop); real "
              "hardware cannot read back per-shot, use the native backend",
        "zh": "qi 后端不支持 cwhile（经典反馈循环）；"
              "真实硬件无法逐 shot 动态回读，请用 native 后端",
    },
    "err.qi_cif": {
        "en": "qi backend does not support cif (mid-circuit measurement + classical "
              "branch); superconducting hardware has no mid-circuit feedback, use "
              "qiskit or native backend",
        "zh": "qi 后端不支持 cif（中段测量 + 经典分支）；"
              "超导真机无中段测量反馈，请用 qiskit 或 native 后端",
    },
    "err.native_method": {
        "en": "native backend does not support method '{method}', available: {engines}",
        "zh": "native 后端不支持方法 '{method}'，可用：{engines}",
    },
    "err.native_ctrl": {
        "en": "native backend classical control flow (cif/creg/cwhile) only supports "
              "statevector / density_matrix methods, current method='{method}'",
        "zh": "native 后端的经典控制流（cif/creg/cwhile）仅支持 "
              "statevector / density_matrix 方法，当前 method='{method}'",
    },
    "err.cwhile_limit": {
        "en": "cwhile loop exceeded safety limit (100000 iterations); condition "
              "creg={creg!r} may never be satisfied",
        "zh": "cwhile 循环超过安全上限（100000 次），条件 creg={creg!r} 可能一直未满足",
    },
    "err.cirq_missing": {
        "en": "cirq backend requires cirq:\n"
              "    pip install 'quonic[cirq]'\n"
              "or: pip install cirq",
        "zh": "使用 cirq 后端需要安装 cirq：\n"
              "    pip install 'quonic[cirq]'\n"
              "或： pip install cirq",
    },
    "err.cirq_ctrl": {
        "en": "cirq backend does not support classical control flow "
              "(cif/cmeasure/cwhile); use qiskit or native backend",
        "zh": "cirq 后端暂不支持经典控制流（cif/cmeasure/cwhile）；"
              "请改用 qiskit 或 native 后端",
    },
    "err.cirq_gate": {
        "en": "Cirq backend does not support gate '{name}'",
        "zh": "Cirq 后端暂不支持门 '{name}'",
    },
    "err.qiskit_missing": {
        "en": "qiskit backend requires qiskit and qiskit-aer:\n"
              "    pip install 'quonic[qiskit]'\n"
              "or: pip install qiskit qiskit-aer",
        "zh": "使用 qiskit 后端需要安装 qiskit 和 qiskit-aer：\n"
              "    pip install 'quonic[qiskit]'\n"
              "或： pip install qiskit qiskit-aer",
    },
    "err.qiskit_cwhile": {
        "en": "qiskit backend does not support cwhile (classical feedback loop); "
              "use native backend",
        "zh": "qiskit 后端暂不支持 cwhile（经典反馈循环）；请用 native 后端",
    },
    "err.qiskit_gate": {
        "en": "Qiskit backend does not support gate '{name}'",
        "zh": "Qiskit 后端暂不支持门 '{name}'",
    },
    "err.pennylane_missing": {
        "en": "pennylane backend requires pennylane:\n"
              "    pip install 'quonic[pennylane]'\n"
              "or: pip install pennylane",
        "zh": "使用 pennylane 后端需要安装 pennylane：\n"
              "    pip install 'quonic[pennylane]'\n"
              "或： pip install pennylane",
    },
    "err.pennylane_ctrl": {
        "en": "pennylane backend does not support classical control flow "
              "(cif/cmeasure/cwhile); use qiskit or native backend",
        "zh": "pennylane 后端暂不支持经典控制流（cif/cmeasure/cwhile）；"
              "请改用 qiskit 或 native 后端",
    },
    "err.pennylane_gate": {
        "en": "PennyLane backend does not support gate '{name}'",
        "zh": "PennyLane 后端暂不支持门 '{name}'",
    },

    # -------------------------------------------------------- core errors
    "err.gate_angle": {
        "en": "parameterized gate rotation angle must be a number (radians), "
              "got {theta!r} ({type})",
        "zh": "参数化门的旋转角必须是数字（弧度），收到 {theta!r}（{type}）",
    },
    "err.unknown_gate": {
        "en": "Unknown gate '{gate}'. Available: {gates}",
        "zh": "未知的量子门 '{gate}'。可用门：{gates}",
    },
    "err.qgate_arg": {
        "en": "qgate's first argument must be a Gate object or gate name string, "
              "got {type}",
        "zh": "qgate 的第一个参数必须是门对象或门名字符串，收到 {type}",
    },
    "err.qgate_arity": {
        "en": "gate {name} requires {expected} qubits but got {actual}: {qubits}",
        "zh": "门 {name} 需要 {expected} 个量子比特，但给了 {actual} 个：{qubits}",
    },
    "err.unknown_axis": {
        "en": "unknown rotation axis '{axis}'",
        "zh": "未知旋转轴 '{axis}'",
    },
    "err.sim_unsupported_gate": {
        "en": "statevector simulator does not support gate '{name}'",
        "zh": "态矢量模拟器暂不支持门 '{name}'",
    },
    "err.pauli_len": {
        "en": "Pauli string length {actual} does not match qubit count {expected}",
        "zh": "泡利串长度 {actual} 与量子比特数 {expected} 不一致",
    },
    "err.noise_prob": {
        "en": "depolarizing probability {name} must be in [0, 1], got {p}",
        "zh": "去极化概率 {name} 需在 [0, 1] 内，收到 {p}",
    },
    "err.noise_arg": {
        "en": "noise must be a NoiseModel, a probability in [0,1], or None",
        "zh": "noise 参数必须是 NoiseModel、一个 [0,1] 内的概率数值，或 None",
    },
    "err.compare_qint": {
        "en": "comparator requires a QInt register, got {type}",
        "zh": "比较器需要 QInt 寄存器，收到 {type}",
    },
    "err.qshow_arg": {
        "en": "qshow's first argument must be a Result object (construct with "
              "Result.from_counts / Result.from_value), or leave empty to run the "
              "current circuit",
        "zh": "qshow 的第一个参数必须是 Result 对象（可用 Result.from_counts / "
              "Result.from_value 构造），或留空以运行当前电路",
    },
    "err.unknown_result_kind": {
        "en": "Unknown Result kind '{kind}'",
        "zh": "未知的 Result 类型 '{kind}'",
    },

    # --------------------------------------------------------- qif errors
    "err.qif_single_bit": {
        "en": "{kind} branch only supports single-qubit gates, {which} got {name}",
        "zh": "MVP 的 {kind} 分支只支持单比特门，{which} 收到 {name}",
    },
    "err.qif_unitary": {
        "en": "{kind} branch requires a unitary gate, cannot be measurement gate "
              "'measure'",
        "zh": "{kind} 分支需要酉门，不能是测量门 'measure'",
    },
    "err.qif_missing_then": {
        "en": "qif missing then branch (call .then(...) before .else_(...))",
        "zh": "qif 缺少 then 分支（先 .then(...) 再 .else_(...)）",
    },
    "err.qif_missing_else": {
        "en": "qif missing else branch (call .else_(...))",
        "zh": "qif 缺少 else 分支（请调用 .else_(...)）",
    },
    "err.qif_same_target": {
        "en": "MVP qif requires then/else branches on the same target qubit, "
              "got {tt} and {ft}",
        "zh": "MVP 的 qif 要求 then/else 分支作用在同一目标比特，收到 {tt} 与 {ft}",
    },
    "err.qif_ctrl_eq_target": {
        "en": "qif control and target qubits cannot be the same",
        "zh": "qif 的控制比特与目标比特不能相同",
    },
    "err.controlled_single": {
        "en": "controlled target gate must be single-qubit, got {name}",
        "zh": "controlled 的目标门必须是单比特门，收到 {name}",
    },
    "err.controlled_unitary": {
        "en": "controlled requires a unitary gate, cannot be measurement gate "
              "'measure'",
        "zh": "controlled 需要酉门，不能是测量门 'measure'",
    },
    "err.controlled_ctrl_eq_target": {
        "en": "controlled control and target qubits cannot be the same",
        "zh": "controlled 的控制比特与目标比特不能相同",
    },
    "err.creg_name": {
        "en": "creg name must be a non-empty string, got {name!r}",
        "zh": "creg 名必须是非空字符串，收到 {name!r}",
    },
    "err.cif_missing_then": {
        "en": "cif missing then branch (call .then(...) before .else_(...))",
        "zh": "cif 缺少 then 分支（先 .then(...) 再 .else_(...)）",
    },
    "err.cif_missing_else": {
        "en": "cif missing else branch (call .else_(...))",
        "zh": "cif 缺少 else 分支（请调用 .else_(...)）",
    },
    "err.cif_same_target": {
        "en": "MVP cif requires then/else branches on the same target qubit, "
              "got {tt} and {ft}",
        "zh": "MVP 的 cif 要求 then/else 分支作用在同一目标比特，收到 {tt} 与 {ft}",
    },
    "err.cif_ctrl_eq_target": {
        "en": "cif control and target qubits cannot be the same",
        "zh": "cif 的控制比特与目标比特不能相同",
    },
    "err.cwhile_cond": {
        "en": "cwhile condition must be a classical bit declared with creg(), "
              "got {cond!r}",
        "zh": "cwhile 的条件必须是 creg() 声明的经典位，收到 {cond!r}",
    },
    "err.cwhile_until": {
        "en": "cwhile until must be 0 or 1, got {until}",
        "zh": "cwhile 的 until 只能是 0 或 1，收到 {until}",
    },
    "err.cwhile_max_iters": {
        "en": "cwhile max_iters must be >= 1, got {max_iters}",
        "zh": "cwhile 的 max_iters 必须 >= 1，收到 {max_iters}",
    },

    # -------------------------------------------------------- topology
    "err.topology_nonneg": {
        "en": "qubit count must be non-negative, got {n}",
        "zh": "量子比特数需非负，收到 {n}",
    },
    "err.topology_self_loop": {
        "en": "self-loop edge ({u}, {v}) is invalid",
        "zh": "自环边 ({u}, {v}) 不合法",
    },
    "err.topology_out_of_range": {
        "en": "edge ({u}, {v}) is out of qubit range [0, {n})",
        "zh": "边 ({u}, {v}) 超出量子比特范围 [0, {n})",
    },

    # --------------------------------------------------------- compiler
    "err.routing": {
        "en": "circuit cannot be mapped to coupling map ({map}): the following "
              "gates have disconnected qubit pairs — {detail}",
        "zh": "电路无法映射到耦合图（{map}）：以下门的量子比特对不相连 —— {detail}",
    },
    "err.routing_cwhile": {
        "en": "SWAP routing does not support cwhile (classical feedback loop); run "
              "with native backend directly, or unroll the loop before routing",
        "zh": "SWAP 路由暂不支持 cwhile（经典反馈循环）；"
              "请改用 native 后端直接运行，或在路由前展开循环",
    },
    "err.routing_disconnected": {
        "en": "coupling map is disconnected, cannot route {name}{qubits}",
        "zh": "耦合图不连通，无法路由 {name}{qubits}",
    },
    "err.routing_etc": {
        "en": " and {n} more gates",
        "zh": " 等 {n} 个门",
    },

    # ------------------------------------------------------- simulators
    "err.density_gate": {
        "en": "density matrix engine does not support gate '{name}'",
        "zh": "密度矩阵引擎暂不支持门 '{name}'",
    },
    "err.stabilizer_gate": {
        "en": "stabilizer engine does not support gate '{name}'",
        "zh": "稳定子引擎暂不支持门 '{name}'",
    },
    "err.stabilizer_measure": {
        "en": "deterministic measurement failed: Z_q not in stabilizer group",
        "zh": "确定性测量失败：Z_q 不在稳定子群内",
    },
    "err.mps_swap": {
        "en": "MPS engine only supports swap on adjacent qubits",
        "zh": "MPS 引擎仅支持相邻量子比特的 swap 门",
    },
    "err.mps_gate": {
        "en": "MPS engine does not support gate '{name}'",
        "zh": "MPS 引擎暂不支持门 '{name}'",
    },
    "err.self_gate": {
        "en": "native engine does not support single-qubit gate '{name}'",
        "zh": "自研引擎暂不支持单比特门 '{name}'",
    },

    # ------------------------------------------------------- algorithms
    "err.vqe_scipy": {
        "en": "VQE requires scipy:\n"
              "    pip install 'quonic[algorithms]'\n"
              "or: pip install scipy",
        "zh": "使用 VQE 需要安装 scipy：\n"
              "    pip install 'quonic[algorithms]'\n"
              "或： pip install scipy",
    },
    "err.qaoa_scipy": {
        "en": "QAOA requires scipy:\n"
              "    pip install 'quonic[algorithms]'\n"
              "or: pip install scipy",
        "zh": "使用 QAOA 需要安装 scipy：\n"
              "    pip install 'quonic[algorithms]'\n"
              "或： pip install scipy",
    },
    "err.oracle_len": {
        "en": "marked bitstring '{oracle}' length {n} does not match qubit count "
              "{n_qubits}",
        "zh": "标记比特串 '{oracle}' 长度 {n} 与量子比特数 {n_qubits} 不一致",
    },
    "err.oracle_n_qubits": {
        "en": "oracle qubit count {n} does not match n_qubits={n_qubits}",
        "zh": "神谕的量子比特数 {n} 与 n_qubits={n_qubits} 不一致",
    },
    "err.oracle_empty": {
        "en": "oracle marks no states, cannot count",
        "zh": "神谕没有标记任何状态，无法计数",
    },
    "err.oracle_type": {
        "en": "oracle must be a marked bitstring, @oracle-decorated object, or "
              "predicate function",
        "zh": "oracle 必须是标记比特串、@oracle 装饰器产物或谓词函数",
    },
    "err.mark_state_bitstring": {
        "en": "mark_state requires a bitstring of only 0/1, got {bitstring!r}",
        "zh": "mark_state 需要只含 0/1 的比特串，收到 {bitstring!r}",
    },
    "err.oracle_n_qubits_positive": {
        "en": "n_qubits must be a positive integer, got {n_qubits!r}",
        "zh": "n_qubits 必须是正整数，收到 {n_qubits!r}",
    },
    "err.hamiltonian_imag": {
        "en": "Hamiltonian coefficient {coeff} has non-negligible imaginary part; "
              "current VQE only supports real coefficients",
        "zh": "哈密顿量系数 {coeff} 含不可忽略的虚部，当前 VQE 仅支持实系数",
    },
    "err.shor_n": {
        "en": "N must be >= 2, got {N}",
        "zh": "N 必须 >= 2，收到 {N}",
    },
    "err.shor_failed": {
        "en": "Shor's algorithm failed to find a factor of {N}; increase shots / "
              "attempts, or try a different N",
        "zh": "Shor 算法未能找到 {N} 的因子；请增加 shots / attempts，或更换 N",
    },

    # ------------------------------------------------------------ misc core
    "err.stack_empty": {
        "en": "circuit stack is already at the bottom, cannot pop further",
        "zh": "电路栈已到底层，无法继续 pop",
    },
    "err.qint_n_bits": {
        "en": "n_bits must be a positive integer, got {n_bits!r}",
        "zh": "n_bits 必须是正整数，收到 {n_bits!r}",
    },
    "err.qint_value_range": {
        "en": "value out of range for a {n_bits}-bit integer [0, {max}), got {value}",
        "zh": "value 超出 {n_bits} 位整数范围 [0, {max})，收到 {value}",
    },
    "err.qint_superposition": {
        "en": "quantum integer is in superposition; cannot convert to int directly "
              "— run qshow() to measure first",
        "zh": "量子整数处于叠加态，无法直接转成 int；请先 qshow() 测量后读取结果",
    },
    "err.statevector_gate": {
        "en": "statevector engine does not support gate '{name}'",
        "zh": "态矢量引擎暂不支持门 '{name}'",
    },

    # ------------------------------------------------------------- viz
    "err.viz_matplotlib": {
        "en": "visualization requires matplotlib:\n"
              "    pip install 'quonic[viz]'\n"
              "or: pip install matplotlib",
        "zh": "使用可视化需要安装 matplotlib：\n"
              "    pip install 'quonic[viz]'\n"
              "或： pip install matplotlib",
    },
    "err.viz_history": {
        "en": "Result has no convergence history. Run with "
              "vqe(..., record_history=True) or qaoa_maxcut(..., record_history=True), "
              "or pass an energy list directly.",
        "zh": "Result 里没有收敛轨迹。请用 vqe(..., record_history=True) 或 "
              "qaoa_maxcut(..., record_history=True) 运行，或直接传入能量列表。",
    },
    "err.viz_marked": {
        "en": "marked must be a 0/1 bitstring of length {n_qubits}, got {marked!r}",
        "zh": "marked 需为长度 {n_qubits} 的 0/1 比特串，收到 {marked!r}",
    },
    "err.viz_gate_matrix": {
        "en": "plot_gate_matrix requires a Gate, GateOperation, or gate name string",
        "zh": "plot_gate_matrix 需要 Gate / GateOperation / 门名字符串",
    },
    "err.viz_measure_unitary": {
        "en": "measurement gate has no unitary matrix",
        "zh": "测量门没有酉矩阵",
    },
    "err.viz_counts": {
        "en": "plot_counts requires a Result (counts) or a dict histogram",
        "zh": "plot_counts 需要 Result（counts）或 dict 直方图",
    },
    "err.viz_no_perf": {
        "en": "no measured data for class '{cls}'; run the benchmark calibration first",
        "zh": "没有 '{cls}' 类别的实测数据，请先运行基准校准",
    },
    "err.viz_bloch_norm": {
        "en": "Bloch vector norm must be ≤ 1",
        "zh": "布洛赫向量模长需 ≤ 1",
    },
    "err.viz_bloch_single": {
        "en": "Bloch sphere only accepts a single-qubit state (2 complex amplitudes) "
              "or a 3D Bloch vector",
        "zh": "布洛赫球只接受单比特态（2 个复振幅）或 3 维布洛赫向量",
    },
    "err.viz_state_input": {
        "en": "unrecognized quantum state input (need 1D statevector / 2D density "
              "matrix / engine / Circuit)",
        "zh": "无法识别的量子态输入（需 1D 态矢量 / 2D 密度矩阵 / 引擎 / Circuit）",
    },
    "err.viz_concurrence": {
        "en": "concurrence is only defined for 2-qubit states (needs a 4×4 density "
              "matrix)",
        "zh": "并发度只对 2 比特态定义（需 4×4 密度矩阵）",
    },
    "err.viz_partition": {
        "en": "partition must be a non-empty subset of qubit indices [0, {n}), got "
              "{partition}",
        "zh": "partition 需为 [0, {n}) 的非空比特下标子集，收到 {partition}",
    },
}
# fmt: on

_current = os.environ.get("QUONIC_LANG", "en").strip().lower()
if _current not in _LANGUAGES:
    _current = "en"


def get_language() -> str:
    """Return the current language code ("en" or "zh")."""
    return _current


def set_language(lang: str) -> None:
    """Switch the runtime message language ("en" or "zh")."""
    global _current
    key = lang.strip().lower()
    if key not in _LANGUAGES:
        raise ValueError(
            f"unknown language '{lang}' (supported: {', '.join(sorted(_LANGUAGES))})"
        )
    _current = key


def tr(key: str, **fmt: Any) -> str:
    """Translate *key* for the current language and interpolate *fmt*.

    Falls back to English, then to the raw key, so a missing translation never
    raises at runtime.
    """
    entry = _MESSAGES.get(key)
    if entry is None:
        return key
    template = entry.get(_current) or entry.get("en")
    if template is None:
        return key
    return template.format(**fmt) if fmt else template
