import ssl
import certifi
ssl._create_default_https_context = ssl.create_default_context
import os
os.environ['SSL_CERT_FILE'] = certifi.where()
import flet as ft


def main(page: ft.Page):
    page.title = "Calc App"
    page.window.width = 400
    page.window.height = 650
    page.window.resizable = False
    page.padding = 10
    page.bgcolor = ft.Colors.GREY_100

    operand1 = 0
    operand2 = 0
    operator = ""
    new_operand = True
    variables = {"A": None, "B": None}
    var_displays = {}

    operation_display = ft.Text(value="", color=ft.Colors.GREY_500, size=13)
    result = ft.Text(value="0", color=ft.Colors.GREY_900, size=25, weight=ft.FontWeight.W_300)

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

    def make_var_button(letter):
        display = ft.Text(f"{letter} = ?", color=ft.Colors.GREY_600, size=12)
        var_displays[letter] = display

        def insert_var(e):
            nonlocal new_operand
            val = variables.get(letter)
            if val is not None:
                if result.value == "0" or new_operand:
                    result.value = str(int(val) if val == int(val) else val)
                    new_operand = False
                else:
                    result.value += str(int(val) if val == int(val) else val)
            else:
                result.value = f"{letter}=?"
            page.update()

        def open_dialog(e):
            inp = ft.TextField(
                label=f"Valor para {letter}",
                keyboard_type=ft.KeyboardType.NUMBER,
                autofocus=True,
                color=ft.Colors.GREY_900,
                label_style=ft.TextStyle(color=ft.Colors.GREY_600),
                border_color=ft.Colors.GREY_400,
                focused_border_color=ft.Colors.GREY_700,
            )

            def save(e):
                try:
                    variables[letter] = float(inp.value)
                    v = variables[letter]
                    var_displays[letter].value = f"{letter} = {int(v) if v == int(v) else v}"
                except ValueError:
                    variables[letter] = None
                    var_displays[letter].value = f"{letter} = ?"
                page.close(dialog)
                page.update()

            def cancel(e):
                page.close(dialog)

            dialog = ft.AlertDialog(
                title=ft.Text(f"Definir {letter}", color=ft.Colors.GREY_900),
                bgcolor=ft.Colors.WHITE,
                content=inp,
                actions=[
                    ft.TextButton("Cancelar", on_click=cancel,
                                  style=ft.ButtonStyle(color=ft.Colors.GREY_500)),
                    ft.TextButton("Guardar", on_click=save,
                                  style=ft.ButtonStyle(color=ft.Colors.GREY_800)),
                ],
            )
            page.open(dialog)
            page.update()

        return ft.Row(
            controls=[
                display,
                ft.ElevatedButton(
                    content=ft.Text(letter),
                    on_click=insert_var,
                    expand=2,
                    bgcolor=ft.Colors.GREY_300,
                    color=ft.Colors.GREY_900,
                    elevation=0,
                ),
                ft.TextButton(
                    f"Def {letter}",
                    on_click=open_dialog,
                    style=ft.ButtonStyle(color=ft.Colors.GREY_600),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    # Estilos de botones — Tema Minimalista claro
    class CalcButton(ft.ElevatedButton):

        def __init__(self, content, on_click, expand=1, bgcolor=None, color=None):
        
        # Guardamos el color original para restaurarlo al salir
            self._base_bgcolor = bgcolor

            def on_hover(e):
            # Si el mouse entra (data=="true"), aclaramos el color
            # Si sale (data=="false"), volvemos al original
                e.control.bgcolor = ft.Colors.GREY_400 if e.data == "true" else self._base_bgcolor
                e.control.update()

            super().__init__(
                content=ft.Text(content, size=18, weight=ft.FontWeight.W_400),
                on_click=on_click,
                on_hover=on_hover,   # ← NUEVO: evento hover
                expand=expand,
                bgcolor=bgcolor,
                color=color,
                elevation=0,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
            ),
        
            )

    class DigitButton(CalcButton):
        def __init__(self, content, expand=1):
            super().__init__(
                content=content,
                on_click=button_clicked,
                expand=expand,
                bgcolor=ft.Colors.WHITE,
                color=ft.Colors.GREY_900,
            )

    class ActionButton(CalcButton):
        def __init__(self, content, expand=1):
            super().__init__(
                content=content,
                on_click=button_clicked,
                expand=expand,
                bgcolor=ft.Colors.GREY_800,
                color=ft.Colors.WHITE,
            )

    class ExtraActionButton(CalcButton):
        def __init__(self, content, expand=1):
            super().__init__(
                content=content,
                on_click=button_clicked,
                expand=expand,
                bgcolor=ft.Colors.GREY_300,
                color=ft.Colors.GREY_800,
            )

    page.add(
        ft.Container(
            width=350,
            bgcolor=ft.Colors.GREY_100,
            border_radius=ft.border_radius.all(24),
            padding=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=20,
                color=ft.Colors.GREY_300,
                offset=ft.Offset(0, 4),
            ),
            content=ft.Column(
                spacing=10,
                controls=[
                    # Display
                    ft.Container(
                        bgcolor=ft.Colors.WHITE,
                        border_radius=ft.border_radius.all(16),
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



