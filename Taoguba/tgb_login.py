import requests

login_url = 'https://sso.taoguba.com.cn/web/login/submitAli'


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'cookie': 'UM_distinctid=17400765cb728-034a859c29eee5-31667305-1fa400-17400765cb8b0d; JSESSIONID=BB80AE0ECB8481F8C99C4E6236BC5332; CNZZDATA1574657=cnzz_eid%3D1839152243-1597730592-https%253A%252F%252Fwww.taoguba.com.cn%252F%26ntime%3D1597881822; Hm_lvt_cc6a63a887a7d811c92b7cc41c441837=1600397946; __gads=ID=106b9d387cc49239:T=1600397965:S=ALNI_MbQSxh8dj8GTY_vy7mo9aoKJWOMUA; Hm_lpvt_cc6a63a887a7d811c92b7cc41c441837=1600398164; JSESSIONID=2571ec2e-e731-4958-830a-1cf5e6d4f33d'
}

datas = {
    'userName': 'ruiyang',
    'password': 'qazwsxedc',
    'save': 'Y',
    # 'checkCode': '''%7B%22a%22%3A%22FFFF0N00000000008F3B%22%2C%22c%22%3A%221597735975432%3A0.229879656198418%22%2C%22d%22%3A%22nvc_register%22%2C%22j%22%3A%7B%22test%22%3A1%7D%2C%22h%22%3A%7B%22umidToken%22%3A%22T2gAx0gGCrb2tGbr2i07TMUfxTK93k7M_yWCCOGmqn8WDZCQV8ds-0KGh-PDKOUYsSj857UBnZrZCm-abIxiz6Ja%22%7D%2C%22b%22%3A%22134%236yiw7gXwXGMifCY8U6DjoX0D3QROwKOlAOzBtZ26EXkMnWPrV%2BWy9I7mWQbOeO5Dfzyr%2FTxcKajSsAuSHmPrniAC5h98f2KsFcHPTFJiB%2BHyrfMXJ%2Bmk%2BJdqKXL3ZtWwTq1qijRmNyd3OOH8qkuj%2BtXXqcp7ZrG%2B%2BcnsAHlzYXwtn625A4PU%2BXr2qTqAZrXtYqb76SIc%2Bk%2BXm2ZS%2Ff3IbCIJA6Nkr4bjvGf3tsBmovlNhQPh9OXMMUMKowlliGBjePirp4%2F4a%2BjEG51JJI7XjzQH%2Bc9EVMjZxpAFVfDAkxtJUvAu4GNgQux6vvBTktMqW3iFYZYbGPNoU6jDKTgfUZgl2xUEntMMC2jQMMJJeUGRwopumRFvI3Fi6v%2F7h9ROzlLWij1a9Up3EgumLQSsiwWHokHXFaTrvhXsVMcKjoOyb6KdQ2dvyrS5RTVNrLu02ys3aO%2FzhrIbuSzUTYahTuICqF4ObtscA7tNYHpJMbntyXKvjWdyAuNd0d%2FgxlyWjWh%2BGya%2F36UA%2FmNwlea5%2BdbpAyiYDVf2Vj8YsrGT9pGjMnN7Mc0GVbyoMmXSIYtZhVxS5KI4uRByTYkTPODh3hgHFdZKzC5M0z6hiLOz00x%2BYcEekhAYz6LNvxZ9rkmHa6VDvmwn1J5HEA8REyc8qy3phcipw92EHlcRGjP3pL9Iul2x7csjiBQWPaVanyDiEg2bvMtm0bSm8%2FXV0SalsKR%2F%2BUMggLo5iNN7uQXexSxKwFuzGyeF8WDrEYHghNAj7UjeleJAAM5qJjS%2B4oOmJ9wOk%2BaztbiejMi5OZQIYLsF6eVpnrlywMn%2FyDfgbU%2FUkfvlYTNm4Dfc7bmB1UpD3c9rcm2Iqdnsc7o3Cwqrx3wHha00vxfc6rRq%2B0GzNlKC6NbwOs68Vgm2GYqifSYlrlv%2F4C2vmtUtnVIAorC9QnY4yKeg3m8nzC8CigyRKRq%2Bj7hCoF6OEr0k7dd6qRYXoTVoCV3Uaj90HdzTq7d52cykVwui%2FG5sSBWxiVY5FtZ9JDwuLUfmWcq%2B9%2FUoTjKJCZ4asn4b2ea78jH%2BqM%2BHkuOGV5ckd2B%2Bf0eD%2BKtPmYQ1NAC0W8FqrOnIfgQoFM9mEbAs1SJNAOlLMKFtAGLQ4tlT7iApI9EOP%2Fc8kdlew3tfhQ%2F%2BauN9IPVuIBW2OrkN17x4MJF1Z8IEa2IHjQR4Ub6YLORjpEEsGuhsaPfHxg8C%2FZ1eG7fvqplaOYKs7cI7qTviUkf4X%2B6Y9Z2gz4qH0MmRUH%2BBRNEVXgsCTxXXABvev2n4KXCGqV4kJ3Xf6OxQS5kxSEWi2DRb3Phx0%2Bl20CojWw%2BatCQugUPZL4k6Xnkj7M1xyotxO%2Blts8ZDPVn%2Bgp%2BOfXJHA9lgnjr%2BONgW5OU9872nWVfcOn1CZuWssxAXVL%2B%2Bhv46JizjCbLsApew4UFWX%2FaKpYf7HPUd5sVzDFTioASdmBCs08n0%2BcB%2B6PJ8V4y%2FAKexX12IeFXdLHcUCtDsyfxxiLyTZf9V719wQYIDbs1aUDJ3Hp0zySBWEHSfwBMqRtMoAS%2Bxt8SXoFyQeYUjY5TdI9G8BZBf1v6lnNlcDSqveDoEyzEg8xHU1REqYfSreTFiNKrqK3AL%2BWCiw66r3JN54Yrfc6upV4i9cP%2FVae5hQo9vi8iLdYlKMB%2FAk%2BFiNEQwhLhrTSwTPoW%3D%22%2C%22e%22%3A%22dYtaKVdoy_iTjvuwv1b4j-GxI8UkJkFuH-4bd8Mx8Ud8HrSwXuZFd4GK42pMeixiuQ7T0s_9RvPaZJFku8H6KusGZWPZRtWxsq8NEAV2oIASuFtbvYxF_RvYhFM29-WozYu7_acRq_dT5_XggWfSY8ja4qxpZCvHWuQKx3_T9gw02Hm7TFWTkgahFFpZA5OTqOfDIhNmVgs8gZTdTnmxZQ%22%7D''',
    'checkCode': '''%7B%22a%22%3A%22FFFF0N00000000008F3B%22%2C%22c%22%3A%221600398163387%3A0.4095522122064379%22%2C%22d%22%3A%22nvc_register%22%2C%22j%22%3A%7B%22test%22%3A1%7D%2C%22h%22%3A%7B%22umidToken%22%3A%22T2gAaWujrcnoC8Jbt8VnT9aBBTMtKmpKsuzDRfi6dOBPKCnOQf81tvpSv6lnhtN1-mvNYJyAXX1-Ox11p0d_G9ik%22%7D%2C%22b%22%3A%22137%23yYc9hE9oUIgegO7CIc4o6dhWIn9bs2vvJrh4lexdPw6CQV2V4L5nX%2F5WgWVFAKSN5L53VywLxz01oXHppIquXBMWRHiru4H3SM%2F%2FbkTRJeG89FbaIn9BIaZIIHmOvBntPpTVHaAM8yCJvAZ0dCRFI7Lm5Zv0z2aaC3PFD1RoSZlUbb3PPboPf%2BluwWvGJpB%2Bzgrv30JuLauTJz5Es5awr9FrS4%2FQidZ4YQ8EIs1s51CyyfcUyliYwKAo66xACD7wEwvPvefs0fdV5UX2WA2HBVqeu19wViifbVNjIr8cydHEd%2Ftzh%2BlNbJ20Pk78OlpOb8YjuNa2TBVsRjptA2r1VVpv98jxumaqArn4pLIJVZJB8yHF0NsRmKURXoSqDFovjZeoaptOVN3Wuz%2FkbgbHTyewjRm3SM3MYOcmUiL8IVIoN3Njemv%2FXDOgjkLrzqIgKzDhBfAm4FYvvJzf16VeOozy0gDc1kyTnUbyvClPDMSOsi5zSWhwPeTi%2FiRCLtg4W%2B6fcsV7y0qDTqfSBFMl2J6uEqgWf4j9GXm%2B9wpWw3PBUt6wEGzb9rWu2ed%2B218VQkRuF4fG63Gq%2B%2FtLHmAcM58iFOi6MSMCr3bsczBVORZhY2dAG6Ie2frbuSvonelzbvTXy5dBGI%2BFllxp2nJyE1mxx0ZF32jsE0w8ACYRKwWqKeVKYiw2s6baYqaRoX%2BeKQ56utcNwVE3m19Oouxfny4ViBnPGU7tbGrVo9c2%2BdqEaf%2FoXdU4GLVHZvARY1XpzpTxZcv4Dfx11CaWvtdgpyH6iy0uxGFZar8ReXKvdgQo39y5PSvR23kqAeh4H8QU7Uo4DqzvoXVzzT7Uz%2BZLsfTw3s1tNAEvULHvrpf1VqY18XVKto0fJD2XuyNa%2BFZofkzlRXH79U%2FSJIoSI4rAVf%2Fx9KBzExE5K0CdBdjc7bzkci%2FuIpp8HAoO%2BuP0DYdesc%2F5wurbv%2BrqOzPhLomxNZKnR6ypvs7fBtGhRMQtZKLQ4eDLuEjlQkvX4CGO0Z2zXr7%2FOINfqwKrJlOH3KRIFm1265rDRIEO4nWULy3jPDmZDr7qMSQFE9t4iyA1vvjQ%2F2lzBkflvAqBlQcHh7aHafTRtW2n7HnjWDqAlOBRun6kXF9AnTqFOaV1H2Elfy5ZWtjLnUrlR9dwbIKofFa%2Bxqw0qOnFoj6mjWUOwX%2F8Z8CTzaWeFg%2BmIhwE%2Fwc9Ma%2F0yJcwFNAAhC7A57m7gl69xoqNE0VpqP8Sg3K3hO3HarvxfsBlmau1MxcuAVxU3qgv8h4zw4iG9ywkTDw7zpdZ3GtkNyk%2BxlNTNTAerOf5iRImWlzUS%2FKdXuHd%2F0sEZiEaHnKBYfazeyF%2FGpS77pQ9fahKR%2BrzQcjVGkKle9eLvlcOp94VhMBZq7wH%2BONjs13pAG%2FrjVT07AF01Pfx%2BcQPs%2F5OCOd41BNUwCMTpr8c3%2B5DjoJcYBdCalYnbLQsoUFKg6SJ4STNn4KUg7LcX1mZtXOKCAkAnPlg4GQ5VxE%2BmHn9mLlpTxAXhqm83zUnV1OZ61IbCQucUq5cBk07AijufwdGPPlnxhehMulSBnBXrl3niDDPRlE2mB4jpP39U%2F6KkqGK6BbqHFzPpn1wKgZSYnW%2BU0HDP0hgvSt99MLx8%2FXyTeQ%2F7ZwNtmZzqeUJqVa5%2BDHRyuZg5vfIPAlE0yZjg%2FoQU5LTcMDgUznV%2BkEQhnnfuDx1zkIp%2Fwc%2FmuxGmlSoGGr67JcroYPkOWVbPW7c%2BL9rm4OMA%2BiRuBA%2Btfyh76I6LJTtxaiQFPGgQMbEcGAROMMC4q2yRHpnmVjySd4JrMQA95d8d%2BAT%2BVgYQpnLdcEWoD85ncOqn0ZzOGzZ7pWZG9%2BBKF63OkKWKf%2FdLCFkEN1wBxU%2BYgX3lbQFyFghB0Jc1IeivpkdDTJT1lEApppWQon0%2BGDpFUTqg9oi%2BtiVYSUS1lQyqdicQDJL5%2F6MpRJs1Iey%2BtiVYllY%2F6LbNEwhQj1JW4zN%2FAf7pAyBK3w4nrxl1H0hppimQofo%2BqFVpkUm1AlN5tipYSUS1qQipXpcQeno%2BKI%2FO5Ts6BqXEn1zwrAEIbBQW%2BeCmwlVX1%2FVgnO86OhUsq0ir%2FYViKbxZJF%2BY4ZhOSYXYotLsVTvi9HfLn0Dgc4U1R6yUcxPvlBkUWnGU6UeGHmKwz%2BBPWscJrk0xF9JM3uE4Ytdjezfg3h1EduZ2PCqJLLvhSJwnnXquc7QKclPWwvRlmgB1TIEYGolRpZL9vgcBO1dVlrDZXYuj73m4RzkIUu4dNZNag6xhqpMnev86%2FbfNYZTgjx4e2j9nr0PAPkw6zUwPxBtt7SIQlwfdqpnehIeUysCn8j8xySOjgYqMIZpkmPIWmLwWnAfoq4%2B%2FNyxajdZWST%2BLvujU5ZepAuL3EPe%2BBUAHipYgdth1TT41feNZg5ZRbeisPNFWOcSBHxKoRRrD%2BA81JD%2BobkcpIPccznN4Ln%2BjKV1JHM95q%2FvvTq4MglFWLESM%2BpboQNp%22%2C%22e%22%3A%22dYtaKVdoy_iTjvuwv1b4j_8h10UR4rIG81oCjDAIlS_Pbs73V5pIs2uCDz9klg-QaI-4VKxA2I59p2hiNXwz9s_u_mZ3UybIiVv6vOIE4nHpWS8emKQ2rGNjAlZMl8YrJLRNyDimjECWquFccEOvHP17rgtyt7AHsl-T2oMv3z7KKOJmYOQrh3hU5Gd1tZdXIaFiPJWPmLxj0DLbGURm4A%22%7D'''

}

resp = requests.post(login_url, data=datas, headers=headers)
print(resp)
if resp and resp.status_code == 200:
    print(resp.text)
