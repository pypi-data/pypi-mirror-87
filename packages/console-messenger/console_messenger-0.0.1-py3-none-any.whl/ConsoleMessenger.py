import sys
from rich.console import Console as cmd

class ConsoleMessage:
    def __init__(self):
        self.console = cmd()
    
    def danger(self, err, err_type=False):
        if not err_type:
            try:
                err_type = sys.exc_info()[0].__name__
            except:
                err_type= "Error"
        self.console.print(
            f"[bold #c82333]{err_type}[/bold #c82333] : "+
            f"[#c82333]{err}[/#c82333]"
        )
    
    def success(self, head, message):
        self.console.print(
            f"[bold #218838]{head}[/bold #218838] : "+
            f"[#218838]{message}[/#218838]"
        )
    
    def warning(self, head, message):
        self.console.print(
            f"[bold #e0a800]{head}[/bold #e0a800] : "+
            f"[#e0a800]{message}[/#e0a800]"
        )

    def info(self, head, message):
        self.console.print(
            f"[bold #138496]{head}[/bold #138496] : "+
            f"[#138496]{message}[/#138496]"
        )

    def dark(self, head, message):
        self.console.print(
            f"[bold #23272b]{head}[/bold #23272b] : "+
            f"[bold #23272b]{message}[/bold #23272b]"
        )