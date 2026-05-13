import ssl
import certifi
ssl._create_default_https_context = ssl.create_default_context
import os
os.environ['SSL_CERT_FILE'] = certifi.where()
import flet as ft

FONDO           = ft.Colors.BLUE_300
FONDO_DISPLAY   = ft.Colors.BLUE
FONDO_BTN_NUM   = ft.Colors.PINK_200
FONDO_BTN_OP    = ft.Colors.BLUE_300
FONDO_BTN_EXTRA = ft.Colors.BLUE_300
HOVER_NUM       = ft.Colors.GREEN_900
HOVER_OP        = ft.Colors.GREEN_700
HOVER_EXTRA     = ft.Colors.BLACK
COLOR_TEXTO     = ft.Colors.BLACK
COLOR_OP_TEXTO  = ft.Colors.BLACK
COLOR_EXTRA_TX  = ft.Colors.BLACK
COLOR_DISPLAY   = ft.Colors.BLACK
COLOR_OPERACION = ft.Colors.BLACK
BORDE_COLOR     = ft.Colors.RED
FUENTE          = "Courier New"



def main(page: ft.Page):
    page.title = "Calc App"
    page.window.width = 400
    page.window.height = 550
    page.window.resizable = False
    page.padding = 10
    page.bgcolor = FONDO

    operand1 = 0
    operand2 = 0
    operator = ""
    new_operand = True

    operation_display = ft.Text(value="", color=COLOR_OPERACION, size=13, font_family=FUENTE)
    result = ft.Text(value="0", color=COLOR_DISPLAY, size=25,
                     weight=ft.FontWeight.W_300, font_family=FUENTE)

    def button_clicked(e):
        nonlocal operand1, operand2, operator, new_operand
        data = e.control.content.value

        if data.isdigit() or data == ".":
            if result.value == "0" or new_operand:
                result.value = data
                new_operand = False
            else:
                result.value = result.value + data

        elif data in ["+", "-", "x", "/"]:
            operand1 = float(result.value)
            operator = data
            operation_display.value = f"{operand1} {operator}"
            new_operand = True

        elif data == "=":
            operand2 = float(result.value)
            operation_display.value = f"{operand1} {operator} {operand2} ="
            if operator == "+":
                result.value = str(operand1 + operand2)
            elif operator == "-":
                result.value = str(operand1 - operand2)
            elif operator == "x":
                result.value = str(operand1 * operand2)
            elif operator == "/":
                result.value = str(operand1 / operand2) if operand2 != 0 else "Error"
            new_operand = True

        elif data == "AC":
            result.value = "0"
            operation_display.value = ""
            operand1 = 0
            operand2 = 0
            operator = ""
            new_operand = True

        elif data == "+/-":
            if float(result.value) > 0:
                result.value = "-" + result.value
            elif float(result.value) < 0:
                result.value = result.value[1:]

        elif data == "%":
            result.value = str(float(result.value) / 100)

        page.update()

    def on_keyboard(e: ft.KeyboardEvent):
        nonlocal operand1, operand2, operator, new_operand

        key_map = {
            "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
            "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
            "Numpad 0": "0", "Numpad 1": "1", "Numpad 2": "2",
            "Numpad 3": "3", "Numpad 4": "4", "Numpad 5": "5",
            "Numpad 6": "6", "Numpad 7": "7", "Numpad 8": "8",
            "Numpad 9": "9",
            ".": ".", ",": ".", "Numpad Decimal": ".",
            "+": "+", "-": "-", "x": "x", "/": "/",
            "Numpad Add": "+", "Numpad Subtract": "-",
            "Numpad Multiply": "x", "Numpad Divide": "/",
            "Enter": "=", "Numpad Enter": "=",
            "Escape": "AC", "Backspace": "AC",
            "%": "%",
        }

        key = e.key
        if key not in key_map:
            return
        data = key_map[key]

        if data.isdigit() or data == ".":
            if result.value == "0" or new_operand:
                result.value = data
                new_operand = False
            else:
                result.value = result.value + data

        elif data in ["+", "-", "x", "/"]:
            operand1 = float(result.value)
            operator = data
            operation_display.value = f"{operand1} {operator}"
            new_operand = True

        elif data == "=":
            operand2 = float(result.value)
            operation_display.value = f"{operand1} {operator} {operand2} ="
            if operator == "+":
                result.value = str(operand1 + operand2)
            elif operator == "-":
                result.value = str(operand1 - operand2)
            elif operator == "x":
                result.value = str(operand1 * operand2)
            elif operator == "/":
                result.value = str(operand1 / operand2) if operand2 != 0 else "Error"
            new_operand = True

        elif data == "AC":
            result.value = "0"
            operation_display.value = ""
            operand1 = 0
            operand2 = 0
            operator = ""
            new_operand = True

        elif data == "%":
            result.value = str(float(result.value) / 100)

        page.update()

    page.on_keyboard_event = on_keyboard

    class CalcButton(ft.ElevatedButton):
        def __init__(self, content, on_click, expand=1, bgcolor=None, color=None, hover_color=None):
            self._base_bgcolor = bgcolor
            self._hover_color = hover_color

            def on_hover(e):
                e.control.bgcolor = self._hover_color if e.data == "true" else self._base_bgcolor
                e.control.update()

            super().__init__(
                content=ft.Text(content, size=18, weight=ft.FontWeight.W_400, font_family=FUENTE),
                on_click=on_click,
                on_hover=on_hover,
                expand=expand,
                bgcolor=bgcolor,
                color=color,
                elevation=0,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
            )

    class DigitButton(CalcButton):
        def __init__(self, content, expand=1):
            super().__init__(content=content, on_click=button_clicked, expand=expand,
                             bgcolor=FONDO_BTN_NUM, color=COLOR_TEXTO, hover_color=HOVER_NUM)

    class ActionButton(CalcButton):
        def __init__(self, content, expand=1):
            super().__init__(content=content, on_click=button_clicked, expand=expand,
                             bgcolor=FONDO_BTN_OP, color=COLOR_OP_TEXTO, hover_color=HOVER_OP)

    class ExtraActionButton(CalcButton):
        def __init__(self, content, expand=1):
            super().__init__(content=content, on_click=button_clicked, expand=expand,
                             bgcolor=FONDO_BTN_EXTRA, color=COLOR_EXTRA_TX, hover_color=HOVER_EXTRA)

    page.add(
        ft.Container(
            width=350,
            bgcolor=FONDO,
            border_radius=ft.border_radius.all(24),
            padding=20,
            border=ft.border.all(1, BORDE_COLOR),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=20,
                color=BORDE_COLOR,
                offset=ft.Offset(0, 4),
            ),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Container(
                        bgcolor=FONDO_DISPLAY,
                        border_radius=ft.border_radius.all(16),
                        border=ft.border.all(1, BORDE_COLOR),
                        padding=ft.padding.symmetric(horizontal=16, vertical=12),
                        content=ft.Column(
                            spacing=2,
                            controls=[
                                ft.Row(controls=[operation_display],
                                       alignment=ft.MainAxisAlignment.END),
                                ft.Row(controls=[result],
                                       alignment=ft.MainAxisAlignment.END),
                            ]
                        ),
                    ),
                    ft.Row(controls=[
                        ExtraActionButton(content="AC"),
                        ExtraActionButton(content="+/-"),
                        ExtraActionButton(content="%"),
                        ActionButton(content="/"),
                    ]),
                    ft.Row(controls=[
                        DigitButton(content="7"),
                        DigitButton(content="8"),
                        DigitButton(content="9"),
                        ActionButton(content="x"),
                    ]),
                    ft.Row(controls=[
                        DigitButton(content="4"),
                        DigitButton(content="5"),
                        DigitButton(content="6"),
                        ActionButton(content="-"),
                    ]),
                    ft.Row(controls=[
                        DigitButton(content="1"),
                        DigitButton(content="2"),
                        DigitButton(content="3"),
                        ActionButton(content="+"),
                    ]),
                    ft.Row(controls=[
                        DigitButton(content="0", expand=2),
                        DigitButton(content="."),
                        ActionButton(content="="),
                    ]),
                ]
            ),
        )
    )


if __name__ == "__main__":
    ft.app(target=main)