#!/usr/bin/env python3

import os
import asyncio
import logging
import time
from prometheus_client import Gauge, start_http_server
from pyoverkiz.client import OverkizClient
from pyoverkiz.const import SUPPORTED_SERVERS
from pyoverkiz.enums import DataType, Server

# Reading environment variables
USERNAME = os.getenv("OVERKIZ_USERNAME", "default_username")
PASSWORD = os.getenv("OVERKIZ_PASSWORD", "default_password")
SERVER_TYPE = os.getenv("OVERKIZ_SERVERTYPE", "ATLANTIC_COZYTOUCH")
LOOP_INTERVAL = int(os.getenv("OVERKIZ_LOOP_INTERVAL", 60))
PROMETHEUS_PORT = int(os.getenv("OVERKIZ_PROMETHEUS_PORT", 8500))

# Logging
logger = logging.getLogger(__name__)

# Prometheus metrics
_BASE_LABELS = ["device_id", "device_label", "metric_namespace", "metric_name"]
OVERKIZ_EXPORTER = Gauge("exporter", "", ["status"], namespace="overkiz")
OVERKIZ_MEASURABLE = Gauge("measurable", "", _BASE_LABELS, namespace="overkiz")
OVERKIZ_LABELS = Gauge("labels", "", _BASE_LABELS + ["label"], namespace="overkiz")


async def update_metrics(username, password, server_type):
    server = SUPPORTED_SERVERS[Server[server_type]]
    async with OverkizClient(username, password, server=server) as client:
        try:
            await client.login()
        except Exception:
            logger.error("%r/%r => couldn't connect", server, username)
            return

        devices = await client.get_devices()

        metric_count = metric_ignored = 0
        for device in devices:
            for state in device.states:
                if state.value and not isinstance(state.value, dict):
                    namespace, name = state.name.split(":")
                    lbl = [device.id, device.label, namespace, name]
                    if state.type in {DataType.FLOAT, DataType.INTEGER}:
                        OVERKIZ_MEASURABLE.labels(*lbl).set(state.value)
                    else:
                        OVERKIZ_LABELS.labels(*lbl, state.value).set(1)
                    metric_count += 1
                else:
                    metric_ignored += 1
        OVERKIZ_EXPORTER.labels(status="ok").inc()
        logger.debug(
            "%r/%r wrote %d metric, ignored %d",
            server,
            username,
            metric_count,
            metric_ignored,
        )


async def main() -> None:
    start_http_server(PROMETHEUS_PORT)
    OVERKIZ_EXPORTER.labels(status="loop_interval").set(LOOP_INTERVAL)
    OVERKIZ_EXPORTER.labels(status="credentials_count").set(1)
    while True:
        OVERKIZ_LABELS.clear()
        OVERKIZ_EXPORTER.labels(status="ok").set(0)
        OVERKIZ_EXPORTER.labels(status="nok").set(0)
        try:
            await update_metrics(USERNAME, PASSWORD, SERVER_TYPE)
        except Exception:
            OVERKIZ_EXPORTER.labels(status="nok").inc()
        time.sleep(LOOP_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
