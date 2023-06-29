from typing import Any, Dict
import requests
from const import GEOCODING_BASE_URL, WEATHER_BASE_URL, WEATHER_CODE_DICT


class weather:
    def __init__(self) -> None:
        self.geocoding_base_url = GEOCODING_BASE_URL
        self.weather_base_url = WEATHER_BASE_URL
        self.weather_code_dict = WEATHER_CODE_DICT

    def geocoding(self, admin1: str, count: int = 5) -> Dict[str, Any]:
        """県名から緯度と経度を取得する

        Args:
                admin1 (str): 県名
                count (int, optional):取得件数 Defaults to 5.

        Returns:
                dict: {"admin1":admin1, # 県名
                                "latitude":latitude, # 緯度
                                "longitude":longitude} # 経度

        test:
            >>> weather().geocoding("Kanagawa")
            {'admin1': 'Kanagawa', 'latitude': 35.47081, 'longitude': 139.6336}
            >>> weather().geocoding("Tokyo")
            {'admin1': 'Tokyo', 'latitude': 35.6895, 'longitude': 139.69171}
        """
        params = {"name": admin1, "count": count}
        res = requests.get(self.geocoding_base_url, params=params)
        res_json = res.json()
        for i in range(len(res_json["results"])):
            # 複数の結果から県名が一致しているものを探す
            if res_json["results"][i]["admin1"] == admin1:
                admin1 = res_json["results"][i]["admin1"]
                latitude = res_json["results"][i]["latitude"]
                longitude = res_json["results"][i]["longitude"]
                res_dict = {
                    "admin1": admin1,
                    "latitude": latitude,
                    "longitude": longitude,
                }
                return res_dict

    def get_weather_code(self, latitude: int = 35.69, longitude: int = 139.69) -> int:
        """天気コードを取得します

        Args:
                latitude (int, optional): 緯度. Defaults to 35.69.
                longitude (int, optional): 経度. Defaults to 139.69.

        Returns:
                int: 天気コード

        test:
            >>> weather().get_weather_code()
            "レスポンスエラー"
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true",
            "timezone": "auto",
        }
        res = requests.get(self.weather_base_url, params=params)
        if res.status_code == requests.codes.ok:
            res_json = res.json()
            # jsonから天気コードを取得
            weather_code = res_json["current_weather"]["weathercode"]
            return weather_code
        else:
            return print("レスポンスエラー")

    def get_weather_by_code(self, weather_code: int) -> Dict[int, int]:
        if weather_code in self.weather_code_dict.keys():
            for i in self.weather_code_dict.keys():
                if weather_code == i:
                    return self.weather_code_dict[i]
        else:
            return print("天気コードが見つかりませんでした。")

    def get_weather(self, weather_code: int = None, admin1: str = None) -> str:
        """天気を取得する

        Args:
            weather_code (int, optional): 天気コードから天気に変換します. Defaults to None.
            admin1 (str, optional): 県から天気を取得します。. Defaults to None.

        Returns:
            dict: 天気
        """
        if weather_code is not None and admin1 is None:
            print("res_by_weather_code")
            return self.get_weather_by_code(weather_code)

        elif admin1 is not None and weather_code is None:
            geocoding = self.geocoding(admin1)
            print("res_by_admin1")

            return self.get_weather_by_code(
                self.get_weather_code(geocoding["latitude"], geocoding["longitude"])
            )
        else:
            print("エラー")
