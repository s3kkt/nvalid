from typing import Optional
import asyncio
import subprocess
import argparse
from config import env_vars, read_config
from lib.slack import send_message as slack_send
from pathlib import Path
import os


def parse_arguments():
    parser = argparse.ArgumentParser(
            description="Nginx config validation tool"
            )
    parser.add_argument(
            "--config",
            type=Path,
            action="store",
            help='path to configuration file'
            )
    local_config = parser.parse_args().config
    return local_config


async def check_config(mpath, mname, fail_timeout, channel, url, check_timeout):
    metric = mpath + mname
    try:
        os.makedirs(mpath)
    except FileExistsError:
        pass
    notification_task: Optional[asyncio.Task] = None
    # https://pypi.org/project/aiofile/
    with open(metric, "w") as metric:
        while True:
            # https://docs.python.org/3/library/asyncio-subprocess.html
            check = subprocess.run(["nginx -t"], shell=True, stderr=subprocess.PIPE)
            if check.returncode != 0:
                text = "Error: " + str(check.stderr.decode('utf-8'))
                color = "danger"
                metric.write("mymetric_name" + ' ' + "1" + "\n")
                if notification_task is None:
                    notification_task = asyncio.create_task(send_notification(text, channel, url, color, fail_timeout))
            else:
                if notification_task and not notification_task.done():
                    notification_task.cancel()
                    notification_task = None
                    await slack_send(
                        "Resolved: configuration file test is successful!", channel=channel, url=url, color="good"
                    )
                metric.write("mymetric_name" + ' ' + "0" + "\n")
            await asyncio.sleep(check_timeout)


async def send_notification(text, channel, url, color, fail_timeout):
    while True:
        await slack_send(text, channel=channel, url=url, color=color)
        await asyncio.sleep(fail_timeout)


async def main():
    if parse_arguments():
        conf = read_config(parse_arguments())
    else:
        conf = env_vars
    try:
        print(f"""
Nginx validation tool started with config: {conf}\n\
Metric path: {conf["metric_path"]}{conf["metric_name"]}""")
        await check_config(
            mpath=conf["metric_path"],
            mname=conf["metric_name"],
            fail_timeout=conf["fail_timeout"],
            channel=conf["slack_chan"],
            url=conf["slack_url"],
            check_timeout=conf["check_timeout"]
        )
    except Exception as ex:
        print(f"execution failure: {str(ex)}")

if __name__ == "__main__":
    asyncio.run(main())
