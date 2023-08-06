[![Downloads](http://pepy.tech/badge/AppZoo)](http://pepy.tech/project/AppZoo)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/jie-yuan/appzoo/apps_streamlit/demo.py)

<h1 align = "center">:rocket: AppZoo :facepunch:</h1>

---



## Install
```bash
pip install -U appzoo
```
## Usage
- Rest Api
```python
import jieba
from appzoo import App

pred1 = lambda **kwargs: kwargs['x'] + kwargs['y']
pred2 = lambda x=1, y=1: x - y
pred3 = lambda text='小米是家不错的公司': jieba.lcut(text)

app = App(verbose=True)
app.add_route("/", pred1, result_key='result')
app.add_route("/f1", pred1, version="1")
app.add_route("/f2", pred2, version="2")
app.add_route("/f3", pred3, version="3")

app.run()
```

- Fast Api
```bash
app-run - fastapi demo.py
app-run - fastapi -- --help
```

- [Streamlit App](https://share.streamlit.io/jie-yuan/appzoo/apps_streamlit/demo.py)
```bash
app-run - streamlit demo.py
app-run - streamlit -- --help
```


---
## TODO
- add logger: 采样
- add scheduler
- add 监听服务
- add rpc服务
