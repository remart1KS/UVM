from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Button, TextArea
import tempfile
import os
from uvm_asm import parse_program, assemble
from uvm_interp import execute

DEMO = """
load_const 10
load_const 42
write_value
load_const 10
read_value 0
load_const 10
bitreverse 1
"""


class UVMApp(App):
    CSS = """
    Screen {
        background: #1e1e1e;
    }
    TextArea {
        height: 1fr;
        margin: 1;
    }
    Button {
        width: 100%;
        margin: 1;
        height: 3;
    }
    """

    def compose(self) -> ComposeResult:
        yield TextArea(text=DEMO, id="code", language="text")
        yield Button("Run", id="run", variant="primary")
        yield TextArea(id="output", read_only=True)

    @on(Button.Pressed, "#run")
    def run_program(self):
        try:
            code = self.query_one("#code").text
            IR = parse_program(code)
            bytecode = assemble(IR)
            memory = execute(bytecode)
            out = "Memory[0:20]: " + str(memory[:20])
            self.query_one("#output").text = out
        except Exception as e:
            self.query_one("#output").text = f"Error: {e}"


if __name__ == "__main__":
    app = UVMApp()
    app.run()
