from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock, mainthread
from kivy.uix.popup import Popup
import threading
# from kivy_webview import WebView


# 解析线程
class ParseWorker(threading.Thread):
    def __init__(self, url, callback):
        super().__init__()
        self.url = url
        self.callback = callback
        self.parse_api = "https://jx.xmflv.cc/?url="

    def run(self):
        play_url = self.parse_api + self.url
        self.callback(play_url)


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 12
        self.spacing = 10

        # 标题
        self.title_label = Label(
            text="🎬 VIP影视解析",
            font_size=24,
            color=(1, 0.42, 0.42, 1),
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.title_label)

        # 链接输入框
        self.input_box = TextInput(
            hint_text="请粘贴腾讯/爱奇艺/优酷等影视分享链接",
            size_hint_y=None,
            height=44,
            background_color=(0.18, 0.18, 0.18, 1),
            foreground_color=(1,1,1,1)
        )
        self.add_widget(self.input_box)

        # 平台快捷按钮行
        platform_container = GridLayout(cols=3, size_hint_y=None, height=140, spacing=6)
        platforms = [
            ("腾讯视频", "https://v.qq.com/x/cover/xxx.html"),
            ("爱奇艺", "https://www.iqiyi.com/v_xxx.html"),
            ("优酷", "https://v.youku.com/v_show/id_xxx.html"),
            ("芒果TV", "https://www.mgtv.com/b/xxx.html"),
            ("搜狐", "https://tv.sohu.com/v/xxx.html"),
        ]
        for name, link in platforms:
            btn = Button(text=name, background_color=(0.22,0.22,0.22,1))
            btn.bind(on_press=lambda inst, u=link:self.input_box.text=u)
            platform_container.add_widget(btn)
        self.add_widget(platform_container)

        # 解析按钮
        self.parse_btn = Button(
            text="🚀 解析视频",
            size_hint_y=None,
            height=50,
            background_color=(1,0.42,0.42,1)
        )
        self.parse_btn.bind(on_press=self.on_click_parse)
        self.add_widget(self.parse_btn)

        # 状态提示
        self.status_label = Label(text="等待解析...", size_hint_y=None, height=32, color=(1,1,1,1))
        self.add_widget(self.status_label)

        # WebView网页播放器
        # self.webview = WebView()
        # self.add_widget(self.webview)

    def show_msg(self, title, msg):
        popup = Popup(title=title, content=Label(text=msg), size_hint=(0.8,0.4))
        popup.open()

    def on_parse_done(self, play_url):
        # 回调回到UI线程更新界面
        @mainthread
        def update():
            self.status_label.text = "✅ 解析成功！正在加载播放器..."
            self.parse_btn.disabled = False
            # self.webview.load_url(play_url)
        update()

    def on_click_parse(self, instance):
        url = self.input_box.text.strip()
        if not url:
            self.show_msg("提示", "请先粘贴视频链接！")
            return
        if not url.startswith("http"):
            self.show_msg("错误", "请输入正确的http链接")
            return

        self.status_label.text = "⏳ 正在解析中，请稍候..."
        self.parse_btn.disabled = True
        worker = ParseWorker(url, self.on_parse_done)
        worker.start()


class VipParseApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    VipParseApp().run()
