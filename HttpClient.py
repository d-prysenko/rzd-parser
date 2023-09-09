import requests


class HttpClient:
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    accept_encoding = 'gzip, deflate, br'
    accept_language = 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    referer = 'https://www.avito.ru/voronezh?q=iphone+xs&s=104'
    cookie = 'u=2xr8k23q.nbwaz7.1if1pgkwew400; _ga=GA1.1.638243561.1675939687; tmr_lvid=69cfde13aaf0a84097295acac62c1317; tmr_lvidTS=1675939686936; _ym_uid=1675939687558811832; uxs_uid=3cd19760-a867-11ed-a013-a97f0408ceed; isCriteoSetNew=true; srv_id=ztXJC3wAE00j287I.Cq4EBRVCakGBh-l6s_iaFn99LMR3vOkGioIoeKG6rzKnQGym196lw1wkrHbX36YiosbY.7I0NnhUPWTeJAnFeFCL0RG0-_ElFsorgS0YrFZMGuLE=.web; luri=voronezh; buyer_location_id=625810; _gcl_au=1.1.1310442130.1694253966; gMltIuegZN2COuSe=EOFGWsm50bhh17prLqaIgdir1V0kgrvN; _ym_d=1694253966; _ym_isad=1; f=5.0c4f4b6d233fb90636b4dd61b04726f147e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a0df103df0c26013a2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b9ad42d01242e34c7968e2978c700f15b6831064c92d93c3903815369ae2d1a81d04dbcad294c152cb0df103df0c26013aba0ac8037e2b74f9268a7bf63aa148d20df103df0c26013a8b1472fe2f9ba6b97b0d53c7afc06d0b71e7cb57bbcb8e0f03c77801b122405c03c77801b122405c03c77801b122405c2ebf3cb6fd35a0ac20f3d16ad0b1c546b892c6c84ad16848a9b4102d42ade879dcb5a55b9498f642b81f1c77c4dcf4df4fb29506e8757e3c4d33506288dc953e92a9876cfd4e1d404525907271a6a0eb4dd39e67d2ac369e38356db14286d21ce2415097439d404746b8ae4e81acb9fa786047a80c779d5146b8ae4e81acb9fa7cf8da616e3c99928db57d0f7c7638d42da10fb74cac1eab3fdb0d9d9f6f145bd1ce76042dff8395312f8fecc8ca5e543486a07687daa291; ft="1RYTXqv+uEsY2Yb9qnxzHbY6sVIZaOxhch4H+eWw49BA7Lgmyvkb4TBrwgfvT248SWY9Z+r0FA51waMLfom0jpzx3vr79nzZb7MSFcRlwYK/d2gnli3nkNeeNcQr3DPURKOMpN9kGO6NKRUWm+xktsIcM2y6Bf6dmJ0+6DwxRP1Y2Y05xhD1Ojwl0SYrA8BJ"; SEARCH_HISTORY_IDS=; buyer_laas_location=625810; utm_medium=cpa; utm_campaign=perf_site_tad_c2c_good_all_aff_160822_955729; advcake_session_id=fa802f28-87f8-cb2b-8eb6-5bcfd7db9a55; advcake_utm_partner=perf_site_tad_c2c_good_all_aff_160822_955729; advcake_click_id=; adrdel=1; adrcid=AxjzPSGVpz6AY5fuUZkJR5A; _ga_ZJDLBTV49B=GS1.1.1694254371.1.1.1694255763.0.0.0; _ga_WW6Q1STJ8M=GS1.1.1694254371.1.1.1694255763.0.0.0; v=1694262353; _ym_visorc=b; adjust_links=adgroup%3Dperf_site_tad_c2c_good_all_aff_160822_955729%26campaign%3Dtrackad_admitad%26creative%3D7be23715f3d3cac26bff8fa9d2967e0e; abp=0; _ga_M29JC28873=GS1.1.1694262342.4.1.1694262391.11.0.0; advcake_track_id=86e7e0c2-5ec7-83cf-4d9e-a3b595a5e08d; advcake_track_url=https%3A%2F%2Fwww.avito.ru%2F%3Favito_campaign_id%3D955729%26utm_campaign%3Dperf_site_tad_c2c_good_all_aff_160822_955729%26utm_content%3D7be23715f3d3cac26bff8fa9d2967e0e%26utm_medium%3Dcpa%26utm_source%3Dtrackad_admitad%26utm_term%3D7be23715f3d3cac26bff8fa9d2967e0e; advcake_utm_webmaster=7be23715f3d3cac26bff8fa9d2967e0e; _buzz_fpc=JTdCJTIycGF0aCUyMiUzQSUyMiUyRiUyMiUyQyUyMmRvbWFpbiUyMiUzQSUyMi53d3cuYXZpdG8ucnUlMjIlMkMlMjJleHBpcmVzJTIyJTNBJTIyTW9uJTJDJTIwMDklMjBTZXAlMjAyMDI0JTIwMTIlM0EyNiUzQTMzJTIwR01UJTIyJTJDJTIyU2FtZVNpdGUlMjIlM0ElMjJMYXglMjIlMkMlMjJ2YWx1ZSUyMiUzQSUyMiU3QiU1QyUyMnVmcCU1QyUyMiUzQSU1QyUyMjllMDA0NmNlZTExZTJhZWE0ZDVlMDk1NTYzNTYzMTI1JTVDJTIyJTJDJTVDJTIyYnJvd3NlclZlcnNpb24lNUMlMjIlM0ElNUMlMjIxMTYuMCU1QyUyMiU3RCUyMiU3RA==; tmr_detect=0%7C1694262394183; buyer_from_page=catalog; _ga_9NLSMYFRV5=GS1.1.1694262342.3.1.1694263645.0.0.0'
    cookie_sx = 'sx=H4sIAAAAAAAC%2F5zQS3IqMQxA0b30mIEty5KV3Vi2Bc0noZv0jxR7f8WAV2GaDZy6dX86h6iCmjlhIW6eWoHorQZP2XPT7uOnm7uPbjrd9wPNJbmyhP4%2BTg0OfRtPe%2BVxPJ%2B7Xde6D0%2BCAVNy8Nh1ztg3x45zrSmZslRtzpTBiq%2BELxmOc1w379brss3rrR4kWLjeLuwDLFv%2BLTuEpxxYzDeTLJAlFYzJk5pI8uoUmF6yXvoAaW2Xsclpm%2Fm2XXvs56mN%2FTBO%2FZtM6SkTEZXKZEISCUkaawtSObpSuMpLXo7fl34apyHAfLweZ%2BUFirtu36jAe32TA%2FNTTubIYoWoHFpNmrM1apQd5pqt%2FalZnjJXrNo8aoq%2BYs0apQFhiRXY1MFLHu7r3uPeJKjRQjbpCfvcAo8DzMv2JkfvH7uuZnWBkTChJ3YxxIDgW2kVJQr%2B%2F7zB7Ws4ryS8fN18o%2Fv2%2BTUcr4PQPpvO7zckPnadJRbODQWBFVTMWRbzRRjUJdW%2F3Eg%2BPGV1HgEiUuTIQurMnFmw5JRbtZd8%2BEzhWqtbmbdbzXo40%2F1zJfCTXKZ4%2BiVHcDE9Hv8CAAD%2F%2F%2F1oLK8rAwAA;'

    def get(self, url):
        headers = {
            'Accept': self.accept,
            'Accept-Encoding': self.accept_encoding,
            'Accept-Language': self.accept_language,
            'Referer': self.referer,
            'User-Agent': self.user_agent,
            'Cookie': self.cookie + self.cookie_sx,
            'Cache-Control': 'max-age=0',
            'If-None-Match': 'W/"1c5827-mFDWYTjo6vV1CDZ78mVmFMxg85o"',
            'Sec-Ch-Ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }

        response = requests.get(url, headers=headers)

        return response