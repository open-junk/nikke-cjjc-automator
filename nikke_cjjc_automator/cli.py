import sys
import typer
from nikke_cjjc_automator.main import main, NikkeAutomator
from nikke_cjjc_automator.view.menu import select_mode

app = typer.Typer(add_completion=False, no_args_is_help=False)

def main_cli():
    NikkeAutomator.ensure_admin()
    args = [a for a in sys.argv[1:] if not a.endswith('.exe')]
    if not args or not any(a.startswith('-') or a.isdigit() for a in args):
        mode = NikkeAutomator.select_mode()
        main(mode)
        return
    app()

@app.command()
def run(mode: int = typer.Option(None, help="運行模式: 1=預測, 2=復盤, 3=反買")):
    """
    NIKKE 自動化腳本 CLI
    若未指定 mode，將進入互動式選單。
    """
    if isinstance(mode, tuple) or mode is None:
        mode = NikkeAutomator.select_mode()
    main(mode)

if __name__ == "__main__":
    try:
        main_cli()
    except KeyboardInterrupt:
        sys.exit(0)
