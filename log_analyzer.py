import sys
import json
from collections import defaultdict
from datetime import datetime

def analyze_log(file_path):
    total_requests = 0
    total_response_time = 0
    status_code_counts = defaultdict(int)
    hourly_counts = defaultdict(int)

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            total_requests += 1
            total_response_time += record.get("response_time_ms", 0)

            # 统计状态码
            status = str(record.get("http_status", "unknown"))
            status_code_counts[status] += 1

            # 统计小时
            ts = record.get("timestamp")
            if ts:
                try:
                    dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
                    hourly_counts[dt.hour] += 1
                except ValueError:
                    pass

    # 计算平均响应时间
    average_response_time = (
        total_response_time / total_requests if total_requests > 0 else 0
    )

    # 找出最繁忙的小时
    busiest_hour = max(hourly_counts, key=hourly_counts.get) if hourly_counts else None

    result = {
        "total_requests": total_requests,
        "average_response_time_ms": average_response_time,
        "status_code_counts": dict(status_code_counts),
        "busiest_hour": busiest_hour,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python log_analyzer.py <access.log>")
        sys.exit(1)

    log_file = sys.argv[1]
    analyze_log(log_file)