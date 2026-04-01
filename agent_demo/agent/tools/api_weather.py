
import requests
from agent.tools.api_user_location import api_city
from utils.get_hefeng_key import generate_jwt

def api_weather(location_id):
    try:
        jwt_token = generate_jwt()
        headers = {"Authorization": f"Bearer {jwt_token}"}
        params = {"location": location_id, "lang": "zh"}
        resp = requests.get("https://pa4ewu4fwv.re.qweatherapi.com/v7/weather/now",
                            params=params, headers=headers, timeout=10)
        data = resp.json()
        if data.get("code") != "200":
            return {"错误": data}

        now = data["now"]
        return {
            "温度": f"{now['temp']}℃",
            "体感": f"{now['feelsLike']}℃",
            "天气": now["text"],
            "风向": now["windDir"],
            "风力": f"{now['windScale']}级",
            "湿度": f"{now['humidity']}%",
            "更新时间": now["obsTime"]
        }
    except Exception as e:
        return {"错误": f"获取天气失败：{str(e)}"}

if __name__ == "__main__":
    try:
        city_info = api_city()
        weather = api_weather(city_info["location_id"])
        print("\n🌤️ 天气信息：")
        print(weather)
    except Exception as e:
        print("❌ 运行异常：", str(e))