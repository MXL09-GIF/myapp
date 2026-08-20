[app]

title = VIP影视解析
package.name = vipparse
package.domain = org.vipparse

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

requirements = python3,kivy

android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.ndk = 25b
android.sdk = 24

android.arch = arm64-v8a

# 主题
android.theme = dark

[buildozer]
log_level = 2
warn_on_root = 1
