from miservice import MiAccount, MiNAService, MiIOService, miio_command, miio_command_help
from aiohttp import ClientSession

from config import MIuser,MIpw
import os 
from pathlib import Path
import sys 
import json
import asyncio

print("test cli")

def test_account():
    print("acount")
    asyncio.run((main("hello")))


async def main(args):
    try:
        async with ClientSession() as session:
            env = os.environ
            account = MiAccount(session,MIuser,MIpw, os.path.join(str(Path.home()), '.mi.token'))
            if args.startswith('mina'):
                service = MiNAService(account)
                result = await service.device_list()
                if len(args) > 4:
                    await service.send_message(result, -1, args[4:])
            else:
                service = MiIOService(account)
                result = await miio_command(service, env.get('MI_DID'), args, sys.argv[0] + ' ')
            if not isinstance(result, str):
                result = json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        result = e
    print(result)


if __name__ == '__main__':
    test_account()