# Insighta.ai Requirement:

## Abstract

Insighta.ai 是一个评分系统，它从ContextPilot等基于AI的效能功能读取数据，基于特有的评分体系为
用户返回对于某一工具使用的熟练程度的评分，并将评分返回给数据来源方。

## Function
系统分为3个模块：
1. 注册模块，需要分析的来源方到我方注册pipeline，该pipeline最终可以获取到目标数据；留到2.0实现。
2. 数据采集模块，用于从来源方接口采集数据，来源方需要自行对数据进行脱敏处理；
3. 数据分析模块，调用评分引擎对用户上下文信息进行打分，保存打分结果；
4. 数据展示模块，提供接口，调用方传入用户地址获取打分信息；
5. 定时任务模块，定时从注册方抓取数据，然后调用引擎进行打分；
6. 安全认证，与注册模块衔接，为注册用户分配密钥。该密钥用于注册用户查询评分结果使用；2.0实现。
7. 接入BNB域名系统，可以在展示用户域名信息的位置展示其专业技能评分；
8. 接入BNB存储系统，将评分存储到BNB储存系统。

## 采集模块实现
你现在是一个Python开发者，帮我实现一个信息采集模块功能。数据采集一共有三个接口，他们的curl调用命令如下：
list address: curl -X GET https://main-wjaxre4ena-uc.a.run.app/usage_addresses
usage by address: curl -X GET https://main-wjaxre4ena-uc.a.run.app/usage_records/<address>
google storage bucket: https://storage.googleapis.com/contextpilot/summary_data/<session_id>.json

请设计mysql数据表用于存储上述采集而来的数据。
要注意不用重复采集和存储，输出内容只应该包含Python代码和数据库脚本，在代码之外不应该包含任何文字内容。
