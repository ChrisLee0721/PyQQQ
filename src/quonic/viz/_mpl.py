"""matplotlib 懒加载 + 通用绘图辅助。

可视化是可选能力：`import quonic` 不引入 matplotlib，只有真正调用某个
plot_* 函数时才加载。中文字体配置、保存 / 显示收尾都收敛在这里。
"""

_MPL = None


def _plt():
    """懒加载 matplotlib.pyplot；未安装时给出中文提示。"""
    global _MPL
    if _MPL is None:
        try:
            import matplotlib.pyplot as plt

            _configure_chinese_font()
            _MPL = plt
        except ImportError as e:
            raise ImportError(
                "使用可视化需要安装 matplotlib：\n"
                "    pip install 'quonic[viz]'\n"
                "或： pip install matplotlib"
            ) from e
    return _MPL


def _configure_chinese_font():
    """尝试启用中文字体（找不到则静默回退英文，不影响绘图）。"""
    import matplotlib
    from matplotlib import font_manager

    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in (
        "Microsoft YaHei",
        "SimHei",
        "PingFang SC",
        "Noto Sans CJK SC",
        "WenQuanYi Micro Hei",
    ):
        if name in available:
            matplotlib.rcParams["font.sans-serif"] = [name, "DejaVu Sans"]
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


def finalize(fig, ax=None, show=False, save=None, title=None):
    """统一收尾：设标题、保存、显示，返回 ax（未提供 ax 时返回 fig）。"""
    if title is not None and ax is not None:
        ax.set_title(title)
    if save:
        fig.savefig(save, bbox_inches="tight", dpi=120)
    if show:
        _plt().show()
    return ax if ax is not None else fig


def new_ax(figsize=(6, 4)):
    """新建 figure + ax 的便捷入口。"""
    plt = _plt()
    fig, ax = plt.subplots(figsize=figsize)
    return fig, ax
