import httpx
import urllib3

from utils.index import getRootPath, mkdir

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def get_img(url: str, file_name, file_path):
    async with httpx.AsyncClient(verify=False) as client:
        res = await client.get(url, headers={'Referer': f'https://www.pixiv.net'})
        if res.status_code == 200:
            mkdir(f'{getRootPath()}/uploads/img/{file_path}')
            with open(f'{getRootPath()}/uploads/img/{file_path}/{file_name}{url[url.rfind('.'):]}', 'wb') as p:
                p.write(res.content)
                print(f'{file_path}/{file_name}{url[url.rfind('.'):]}下载完成')
        else:
            if url.find('.jpg') > -1:
                await get_img(url.replace('.jpg', '.png'), file_name, file_path)
            elif url.find('.png') > -1:
                await get_img(url.replace('.png', '.gif'), file_name, file_path)
