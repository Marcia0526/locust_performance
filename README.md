- config配置分布式:
```
locust --config=master.conf
locust --config=worker.conf//有多少个worker,开启多个iterm运行多次此命令

```

- no ui分布式
```
master: 
locust -f es_test.py --headless -u 1000 -r 100 --run-time 1h30m --master --expect-workers=2

worker: 
locust -f es_test.py --headless -u 1000 -r 100 --worker
locust -f es_test.py --headless -u 1000 -r 100 --worker

```

- docker-compose分布式
```
env=test docker-compose up --scale worker=6
http://127.0.0.1:8089/
env=test docker-compose up --scale worker=1 --scale master=1
env=test docker-compose up --scale worker=0 --scale master=0
```





