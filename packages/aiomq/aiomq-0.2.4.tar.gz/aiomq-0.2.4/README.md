# aiomq

每个客户端都是节点，与服务端本质应该没有主次区别，仅因为位置的不同，导致承载的代码不同.不同节点数据交互方式应该是多样性的。

渐进式异步任务构建服务，用于快速构建异步任务，定时任务。支持结构有 队列，订阅/监听，分发，RPC。
可视化任务池界面，在线设备，手动触发，下发任务，上报任务。

版本要求
---

python: 3.8.5 以上
aiohttp


---

版本
---

0.2.0 事件基本任务注册和分发和基础的仪表盘, 支持多客户端

如果有更好建议或者写协作开发，请联系

联系方式: **sqxccdy@icloud.com**


```
18.5.4.2.1. Protocol classes
class asyncio.Protocol
The base class for implementing streaming protocols (for use with e.g. TCP and SSL transports).

class asyncio.DatagramProtocol
The base class for implementing datagram protocols (for use with e.g. UDP transports).

class asyncio.SubprocessProtocol
The base class for implementing protocols communicating with child processes (through a set of unidirectional pipes).
```