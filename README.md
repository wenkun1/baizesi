AI实现流程自动化

## 运行方式

旧轮询入口：

```bash
python main.py
```

企业微信实时读取方式：

```bash
python wechat_main.py
```

默认读取：

```text
http://192.168.80.12:8060/api/v1/wechat-archive/chat/history?limit=1
```

常用参数：

```bash
python wechat_main.py --interval 2
python wechat_main.py --process-existing
python wechat_main.py --once --process-existing --source E:\Project\furongxiaomei\wechat_history.json
```

企业微信入口默认会在启动时记录当前接口返回的已有消息，从下一条新消息开始处理，避免重放启动前的历史消息。需要回放当前已有消息时使用 `--process-existing`。

企业微信入口会按 `from_user` 作为用户账号，首次进线自动写入 `ai_user`，每个用户单独维护会话和消息队列，并按消息时间的全局顺序先来后到处理，同时过滤 `assistant@chinasns.com` 自己发出的历史消息。
