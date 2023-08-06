import asyncio
from coordml_runner.entry import Entry
from coordml_runner.config import load_config
import logging
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='config.yaml')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    config = load_config(args.config)
    entry = Entry(config)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(entry.start())


