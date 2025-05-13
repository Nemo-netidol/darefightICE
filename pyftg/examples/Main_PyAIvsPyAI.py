import asyncio

import typer
from typing_extensions import Annotated, Optional

from KickAI import KickAI
from OneSecondAI import OneSecondAI
from pyftg.socket.aio.gateway import Gateway
from pyftg.utils.logging import DEBUG, set_logging
from DisplayInfo import DisplayInfo

app = typer.Typer(pretty_exceptions_enable=False)


async def start_process(host: str, port: int, character: str = "ZEN", game_num: int = 1):
    gateway = Gateway(host, port)
    agent1 = OneSecondAI()
    agent2 = DisplayInfo()
    gateway.register_ai("OneSecondAI", agent1)
    gateway.register_ai("DisplayInfo", agent2)
    await gateway.run_game([character, character], ["OneSecondAI", "DisplayInfo"], game_num)


@app.command()
def main(
        host: Annotated[Optional[str], typer.Option(help="Host used by DareFightingICE")] = "127.0.0.1",
        port: Annotated[Optional[int], typer.Option(help="Port used by DareFightingICE")] = 31415):
    asyncio.run(start_process(host, port))


if __name__ == '__main__':
    set_logging(log_level=DEBUG)
    app()
