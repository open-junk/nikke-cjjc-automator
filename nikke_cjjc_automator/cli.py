import typer
from nikke_cjjc_automator.main import main
from nikke_cjjc_automator.view.menu import select_mode

app = typer.Typer()

# 取得互動式選單的說明文字
try:
    MODE_HELP = "\n".join([
        f"{val}: {label}" for label, val in select_mode.__defaults__[0]["choices"]
    ])
except Exception:
    MODE_HELP = None

@app.command()
def run(
    mode: int = typer.Option(
        1,
        help=f"運行模式：\n{MODE_HELP}\n(預設 1)" if MODE_HELP else "運行模式 (預設 1)"
    )
):
    """運行 NIKKE CJJC 自動化腳本。"""
    print(f"[DEBUG] CLI run() called, mode = {mode}")
    main(mode)

if __name__ == "__main__":
    app()
