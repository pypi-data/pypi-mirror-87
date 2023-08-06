<h1 align = "center">:rocket: App :facepunch:</h1>

---

## Install
```bash
pip install -U appzoo
```
## Usage
- Rest Api
```python
import jieba
from iapp import App

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
- Scheduler
```python
from iapp.scheduler import Scheduler
    def task1(x):
        print(x)
        import logging
        import time
        logging.warning(f'Task1: {time.ctime()}')


    def task2():
        import logging
        import time
        logging.warning(f'Task2: {time.ctime()}')


    def task3():
        return 1 / 0


    def my_listener(event):
        if event.exception:
            print(event.traceback)
            print('任务出错了！！！！！！')
        else:
            print('任务照常运行...')


    scheduler = Scheduler()
    scheduler.add_job(task1, 'interval', seconds=3, args=('定时任务',))
    scheduler.add_job(task2, 'interval', seconds=5)
    scheduler.add_job(task3, 'interval', seconds=1)

    scheduler.add_listener(my_listener)
    scheduler.start()

    while 1:
        pass

```

---
# TODO
- add logger
