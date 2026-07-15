import time
from typing import Dict

import requests

from prometheus_write.poor_mans_snappy import poor_mans_snappy_compress
from prometheus_write.remote_pb2 import WriteRequest


def millis_since_epoch():
    return int(time.time() * 1000)


def write(name, value, labels: Dict[str, str]|None = None):
    write_request = WriteRequest()

    series = write_request.timeseries.add()

    label = series.labels.add()
    label.name = "__name__"
    label.value = name

    for k, v in labels.items():
        label = series.labels.add()
        label.name = k
        label.value = v

    sample = series.samples.add()
    sample.timestamp = millis_since_epoch()
    sample.value = value

    uncompressed = write_request.SerializeToString()
    compressed = poor_mans_snappy_compress(uncompressed)

    url = "http://datenkrake:9090/api/v1/write"
    headers = {
        "Content-Encoding": "snappy",
        "Content-Type": "application/x-protobuf",
        "X-Prometheus-Remote-Write-Version": "0.1.0",
        "User-Agent": "python write_to_prometheus"
    }

    print(f"sending {uncompressed} as {compressed}")

    response = requests.post(url, headers=headers, data=compressed)
    print(response)
    assert response.status_code == 204, "Expected HTTP status code 204 (No content)"


if __name__ == '__main__':
    write("throwaway_dev_metric", 18, {})
