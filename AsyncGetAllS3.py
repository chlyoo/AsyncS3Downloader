import requests
import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup
from pathlib import Path


async def get_session(objurl, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(objurl) as resp:
            if resp.status == 200:
                output_file = Path(f"asyncoutput/{filename}")
                output_file.parent.mkdir(exist_ok=True, parents=True)
                f = await aiofiles.open(f'asyncoutput/{filename}', mode='wb')
                await f.write(await resp.read())
                await f.close()


async def main():
    url = 'https://<s3xmlpath>.<region>.amazonaws.com/'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='xml')
    content = soup.findAll('Contents')
    future = []
    for _, item in enumerate(content):
        title = item.find('Key').text
        if title.split('/')[-1] == "":
            continue
        objurl = url + title
        future.append(get_session(objurl, title))
    await asyncio.gather(*future)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
