日志格式要求
日志文件中每行需为一个 JSON 对象，包含以下字段：

timestamp: ISO 格式的时间戳（如 "2025-08-27T10:15:30Z"）
user_id: 用户唯一标识符
response_time_ms: 响应时间（毫秒）
http_status: HTTP 状态码

示例日志 (access.log):

json
{"timestamp": "2025-08-27T10:15:30Z", "user_id": "u001", "response_time_ms": 120, "http_status": 200}
{"timestamp": "2025-08-27T10:16:10Z", "user_id": "u002", "response_time_ms": 250, "http_status": 404}
{"timestamp": "2025-08-27T11:05:00Z", "user_id": "u001", "response_time_ms": 150, "http_status": 200}

环境要求
Python 3.7 或更高版本
无需安装额外依赖库
快速使用
将 log_analyzer.py 保存到工作目录
在终端执行以下命令：

bash
python log_analyzer.py access.log

示例输出:

json
{
  "total_requests": 5,
  "average_response_time_ms": 200.0,
  "status_code_counts": {
    "200": 3,
    "404": 1,
    "500": 1
  },
  "busiest_hour": 11
}
实现原理
核心处理流程
流式读取：采用逐行读取方式处理日志，避免占用过多内存
数据解析：使用 json.loads() 解析每行日志为字典对象
指标计算：
总请求数：通过计数器累加
平均响应时间：累计总响应时间后计算平均值
状态码分布：使用字典记录各状态码出现次数
繁忙时段分析：解析时间戳提取小时信息，统计每小时请求量
性能考量
采用字典（哈希表）存储中间结果，利用其 O (1) 的平均插入和查询复杂度，确保高效的频率统计。
高级优化建议
对于超大型日志文件（10GB 以上），可考虑以下优化方案：

并行处理
使用 multiprocessing 或 concurrent.futures 进行多进程分块处理
各进程处理完后汇总统计结果
解析优化
替换 JSON 解析库为更快的 orjson 或 ujson
实现自定义解析器处理固定格式日志
