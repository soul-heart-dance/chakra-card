# app.py
# 讓「訪客抽卡」成為預設首頁，不跟管理頁混在一起
from pages.chakra_draw import render

if __name__ == "__main__":
    render()