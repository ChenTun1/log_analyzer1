#!/usr/bin/env python3
import sys
import json
from collections import defaultdict
from datetime import datetime
from typing import Dict, Any


def analyze_log(file_path: str) -> None:
    total_requests = 0
    total_response_time = 0
    status_code_counts = defaultdict(int)
    hourly_counts = defaultdict(int)

    invalid_json_lines = 0
    invalid_timestamp_lines = 0

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue

                try:
                    record: Dict[str, Any] = json.loads(line)
                except json.JSONDecodeError:
                    invalid_json_lines += 1
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
                        invalid_timestamp_lines += 1
                        continue
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 未找到。", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"错误: 文件 '{file_path}' 无法读取，请检查权限。", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {e}", file=sys.stderr)
        sys.exit(1)

    # 计算平均响应时间
    average_response_time = (
        round(total_response_time / total_requests, 2) if total_requests > 0 else 0
    )

    # 找出最繁忙的小时
    busiest_hour = max(hourly_counts, key=hourly_counts.get) if hourly_counts else None

    result = {
        "total_requests": total_requests,
        "average_response_time_ms": average_response_time,
        "status_code_counts": dict(status_code_counts),
        "busiest_hour": busiest_hour,
        "invalid_json_lines": invalid_json_lines,
        "invalid_timestamp_lines": invalid_timestamp_lines,
    }

    print("分析完成！")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python log_analyzer.py access.log", file=sys.stderr)
        sys.exit(1)

    log_file = sys.argv[1]
    analyze_log(log_file)
