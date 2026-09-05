# -*- coding: utf-8 -*-
"""简易计算器 - Kivy 跨平台版（Windows 可调试，可打包 APK）"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

Window.size = (460, 640)
Window.clearcolor = (0.12, 0.14, 0.17, 1)

# 布局参数：显示屏拉高、按钮行压扁
DISPLAY_H = 160       # 显示屏高度
BTN_ROW_H = 60        # 每行按钮高度
BTN_FONT = "22sp"     # 按钮字号
DISPLAY_FONT = "48sp"  # 显示屏字号


class CalculatorApp(App):
    def build(self):
        self.expr = ""

        self.display = Label(
            text="0",
            font_size=DISPLAY_FONT,
            halign="right",
            valign="middle",
            size_hint=(None, None),
            height=DISPLAY_H,
            color=(1, 1, 1, 1),
            text_size=(Window.size[0] - 20, DISPLAY_H),
        )

        layout = BoxLayout(orientation="vertical", padding=10, spacing=6)
        layout.add_widget(self.display)

        rows = [
            ["C", "(", ")", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "+"],            
            ["1", "2", "3", "-"],
            ["0", ".", "=", "⌫"],
        ]

        for row in rows:
            row_layout = BoxLayout(
                size_hint=(1, None),
                height=BTN_ROW_H,
                spacing=6,
            )
            for t in row:
                btn = Button(
                    text=t,
                    font_size=BTN_FONT,
                    background_color=self._btn_color(t),
                )
                btn.bind(on_press=lambda _, t=t: self.on_click(t))
                row_layout.add_widget(btn)
            layout.add_widget(row_layout)

        Window.bind(on_key=self.on_key)
        return layout

    @staticmethod
    def _btn_color(t):
        if t in {"+", "-", "*", "/", "(", ")"}:
            return (0.96, 0.62, 0.04, 1)  # 运算符：橙
        if t in {"C", "⌫"}:
            return (0.78, 0.20, 0.20, 1)  # 功能键：红
        if t == "=":
            return (0.18, 0.66, 0.34, 1)  # 等号：绿
        return (0.22, 0.28, 0.34, 1)      # 数字：深灰

    def on_key(self, window, key, *_):
        if key in (13, 271):   # Enter
            self.on_click("=")
        elif key == 8:          # Backspace
            self.on_click("⌫")
        elif key == 27:         # Esc
            self.on_click("C")

    def on_click(self, t):
        if t == "C":
            self.expr = ""
            self.display.text = "0"
        elif t == "⌫":
            self.expr = self.expr[:-1]
            self.display.text = self.expr if self.expr else "0"
        elif t == "=":
            self.calculate()
        else:
            self.expr += t
            self.display.text = self.expr

    def calculate(self):
        try:
            result = eval(self.expr, {"__builtins__": {}}, {})
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.expr = str(result)
            self.display.text = self.expr
        except ZeroDivisionError:
            self.display.text = "错误：除数为 0"
            self.expr = ""
        except Exception:
            self.display.text = "错误"
            self.expr = ""


if __name__ == "__main__":
    CalculatorApp().run()
