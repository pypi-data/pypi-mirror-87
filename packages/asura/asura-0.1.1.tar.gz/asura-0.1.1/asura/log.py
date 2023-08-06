class ASOR:
	RESET = "\x1b[0m"
	DYELLOW = "\x1b[2;33;40m"
	DRED = "\x1b[2;31;40m"

async def info(text: str):
	print(f"{ASOR.DYELLOW}INFO: {text}{ASOR.RESET}")

async def error(err: str):
	print(f"{ASOR.DRED}ERR:  {err}{ASOR.RESET}")
