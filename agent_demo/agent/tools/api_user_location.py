
import requests
from utils.get_hefeng_key import generate_jwt

# 解析高德 rectangle 获得中心点经纬度
def parse_rect_coords(rect_str):
    try:
        left_bottom, right_top = rect_str.split(";")
        lng1, lat1 = left_bottom.split(",")
        lng2, lat2 = right_top.split(",")
        center_lng = (float(lng1) + float(lng2)) / 2
        center_lat = (float(lat1) + float(lat2)) / 2
        return f"{center_lng:.6f},{center_lat:.6f}"
    except:
        return "116.405285,39.904989"

def api_city():
    key = "1c16ea4364a480107d9f8f5f66fc5a15"
    try:
        ip = requests.get("https://api.ip.sb/ip", timeout=3).text.strip()
        url = f"https://restapi.amap.com/v3/ip?ip={ip}&key={key}&output=json"
        res = requests.get(url, timeout=5)
        data = res.json()
        jwt_token = generate_jwt()
        headers = {"Authorization": f"Bearer {jwt_token}"}
        params = {"location": parse_rect_coords(data["rectangle"])}
        r = requests.get("https://pa4ewu4fwv.re.qweatherapi.com/geo/v2/city/lookup", params=params, headers=headers,
                         timeout=10)
        data["location_id"] = r.json()["location"][0]["id"]
        data["city_region"] = r.json()["location"][0]["name"]
    except Exception as e:
        print(f"⚠️ 定位失败：{str(e)}")
    # 修复：支持 北京市、上海市 这种带“市”的名字
    city_en_map = {
        "北京": "Beijing",
        "北京市": "Beijing",
        "上海": "Shanghai",
        "上海市": "Shanghai",
        "广州": "Guangzhou",
        "广州市": "Guangzhou",
        "深圳": "Shenzhen",
        "深圳市": "Shenzhen",
        "杭州": "Hangzhou",
        "杭州市": "Hangzhou",
        "南京": "Nanjing",
        "南京市": "Nanjing",
        "成都": "Chengdu",
        "成都市": "Chengdu",
        "重庆": "Chongqing",
        "重庆市": "Chongqing",
        "武汉": "Wuhan",
        "武汉市": "Wuhan",
        "西安": "Xi'an",
        "西安市": "Xi'an"
    }

    data["city_en"] = city_en_map.get(data["city"], data["city"])
    return data

if __name__ == "__main__":
    city_info = api_city()
    print("中文城市：", city_info["city"])
    print("英文城市：", city_info["city_en"])