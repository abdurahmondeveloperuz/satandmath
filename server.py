import aiohttp
import asyncio

url = "https://rankingsofstudents.fly.dev/api/set_class"

headers = {
    "X-API-Key": "AGHD-8954-BCFQ-5651",
    "Content-Type": "application/json"
}

params = {
    "class_id": '000'
}

data = {
    "class_name": "Class Name",
    "students": [
        {
            "first_name": "John",
            "last_name": "⠀",
            "score": 95.0
        },
        {
            "first_name": "John",
            "last_name": "⠀",
            "score": 95.0,
            "image": "https://i.ibb.co/SRBFZ37/49422432-97e1-4ef1-aecd-7147fe002a4c.jpg"
        },
        {
            "first_name": "John",
            "last_name": "⠀",
            "score": 95.0,
            "image": "https://marketplace.canva.com/EAFHfL_zPBk/1/0/1600w/canva-yellow-inspiration-modern-instagram-profile-picture-kpZhUIzCx_w.jpg",
            "profile_url": "https://t.me/abdurahmondev1"
        },
        
    ]
}





async def postRatings(data, params, headers=headers, url=url):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, params=params, json=data) as response:
            return response

# postRatings(data=data, params=params)
