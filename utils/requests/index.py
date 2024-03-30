import httpx
import urllib3

from utils.index import get_root_path, mkdir
from fake_useragent import UserAgent

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ua = UserAgent()


async def get_img(url: str, file_name, file_path):
    try:
        agent = ua.random
        async with httpx.AsyncClient(verify=False, timeout=None) as client:
            res = await client.get(url, headers={'Referer': f'https://www.pixiv.net', 'User-Agent': agent})
            if res.status_code == 200:
                mkdir(f'{get_root_path()}/uploads/img/{file_path}')
                with open(f'{get_root_path()}/uploads/img/{file_path}/{file_name}{url[url.rfind('.'):]}', 'wb') as p:
                    p.write(res.content)
                    print(f'{file_path}/{file_name}{url[url.rfind('.'):]}下载完成')
            else:
                if url.find('.jpg') > -1:
                    await get_img(url.replace('.jpg', '.png'), file_name, file_path)
                elif url.find('.png') > -1:
                    await get_img(url.replace('.png', '.gif'), file_name, file_path)
    except:
        print('except', agent)
