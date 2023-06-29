from aiboapi import Aibo


def create_arguments(
    first_Property: str,
    first_value: str,
    second_Property: str = None,
    second_value: str = None,
    enqueue: bool = None,
) -> str:
    result = '{"arguments":{"' + first_Property + '":"' + first_value + '"'
    try:
        if second_Property is not None and second_value is not None:
            result += f',"{second_Property}":"{second_value}"'
        elif second_Property is not None or second_value is not None:
            raise TypeError
        if enqueue:
            result += ',"Enqueue":true'
        result += "}}"
        return result
    except TypeError:
        print("引数の数が正しくありません。")
        print("argumentsにはPropertyとvalueの２つを指定してください。")


class Action:
    def __init__(self, token: str) -> None:
        self.token = token

    def change_posture(self, posture: str) -> dict:
        """指定されたポーズになります
        Parameters
        ----------
        posture : str
                back: おなかを見せる\n
                crouch: しゃがむ\n
                down: 伏せる\n
                down_and_lengthen_behind: 寝転がる\n
                down_and_shorten_behind: 足を曲げて寝転がる\n
                sit_and_raise_both_hands: 両方の前足をあげる\n
                sit: すわる\n
                sleep: 寝る姿勢になる\n
                stand: 立つ\n
                stand_straight: まっすぐ立つ\n
        Returns
        -------
        dict
            result
        """
        data = create_arguments("FinalPosture", posture)
        result = Aibo(self.token).ask_action(API_NAME="change_posture", arguments=data)
        return result

    def set_mode(self) -> dict:
        """指示待ち状態にする"""
        data = create_arguments("ModeName", "DEVELOPMENT")
        result = Aibo(self.token).ask_action(API_NAME="set_mode", arguments=data)
        return result

    def approach_person(self) -> dict:
        """指定した距離まで近づく"""
        result = Aibo(self.token).ask_action(
            API_NAME="approach_person",
            arguments='{"arguments":{"DistanceFromTarget":0.5}}',
        )
        return result

    def get_touched_body_part(self) -> str:
        """触られた場所を取得します

        Returns
        -------
        str
                belly: おなか\n
                body: せなか\n
                chin: あご\n
                head: あたま

        """
        result = Aibo(self.token).ask_action(API_NAME="body_touched_status")
        if result != []:
            touched_body_part = result["body_touched_status"]["body_part"]
        else:
            touched_body_part = result
        return touched_body_part

    def play_motion(self, arguments) -> dict:
        """指定された動作を行います。

        Parameters
        ----------
        arguments :
            create_arguments関数を入力

        Returns
        -------
        dict
            result
        """
        result = Aibo(self.token).ask_action(
            API_NAME="play_motion", arguments=arguments
        )
        return result

    def get_voice(self):
        result = Aibo(self.token).ask_action(API_NAME="voice_command_status")
        return result
