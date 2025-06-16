import sys
import typer
import traceback
from nikke_cjjc_automator.core import entry, NikkeAutomator
from nikke_cjjc_automator.view.menu import select_mode

app = typer.Typer(add_completion=False, no_args_is_help=False)

def entry_cli():
    NikkeAutomator.ensure_admin()
    args = [a for a in sys.argv[1:] if not a.endswith('.exe')]
    if not args or not any(a.startswith('-') or a.isdigit() for a in args):
        mode = NikkeAutomator.select_mode()
        entry(mode)
        return
    app()

@app.command()
def run(mode: int = typer.Option(None, help="Run mode: 1=Prediction, 2=Review, 3=Anti-Buy")):
    """
    NIKKE Automation Script CLI
    If mode is not specified, the interactive menu will be shown.
    """
    if isinstance(mode, tuple) or mode is None:
        mode = NikkeAutomator.select_mode()
    entry(mode)

if __name__ == "__main__":
    try:
        entry_cli()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        traceback.print_exc()
        NikkeAutomator.notify_error(str(e))
        input("Press Enter to exit...")
        raise
