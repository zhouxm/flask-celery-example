> backend='redis://:109321@10.35.163.24:6379/7’,    # 返回值存入数据库  
> broker='redis://:109321@10.35.163.24:6379/8')      #   :密码@host/post/db

- Windows的Celery只支持到3.1.25
```shell script
pip install celery==4.3.0   
pip install eventlet  
celery -A app.tasks.meta.tasks worker -l info -P eventlet  
celery -A app.tasks.meta.tasks worker  --loglevel=info  
celery -A app.celery worker --loglevel=info  

```  
```python
tasks.task_name.delay()  
t.ready()  
t.get()  
t.get(timeout=11)  
t.get(propagate=False)  
t.traceback  

CELERY_TIMEZONE='Asia/Shanghai'
CELERY_ENABLE_UTC=True
# 官网推荐消息序列化方式为json
CELERY_ACCEPT_CONTENT=['json']
CELERY_TASK_SERIALIZER='json'
CELERY_RESULT_SERIALIZER='json'

```

> 请求耗时（比如大量的数据库插入，发送验证邮件等）
利用Celery来后台处理耗时任务可以保证Flask能够较快响应而且不被阻塞，同时减轻了数据库的高峰写入压力
操作数据库，操作完成后记得释放数据库连接，例如Session.remove

## Celery是专注实时处理和任务调度的分布式任务队列。
- 主要应用场景：
1. web应用，当需要触发事件需要较长时间处理完成，可以交给celery进行异步执行，执行完后返回结果，这段时间不用等待，提高系统的吞吐量和响应时间
2. 成任务时，需要额外的事件处理，如发送邮件等
3. 后台定时任务处理，celery可以帮助我们在不同服务器进行定时任务管理
