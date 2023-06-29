from secret_token import TOKEN
from action_function import Action, create_arguments
import time
from get_wether import weather

aibo = Action(TOKEN)
tenki = weather()

print("開始")


def run():
    time.sleep(3)
    # 1_aiboを指示待ちにする
    aibo.set_mode()
    print("--")

    # 2_吠える
    aibo.play_motion(
        create_arguments(
            "Category", "bark", second_Property="Mode", second_value="NONE"
        )
    )
    print("--")

    flag = True

    while flag == True:
        # 3_人を探し近づく
        aibo.approach_person()
        print("--")
        time.sleep(10)
        for i in range(3):
            try:
                detection = aibo.get_touched_body_part()
                print("--")
                # もし、せなかを触られたら 無限ループを抜ける
                if detection == "body":
                    aibo.play_motion(
                        create_arguments(
                            "Category",
                            "dance",
                            second_Property="Mode",
                            second_value="NONE",
                        )
                    )
                    print("終了")
                    flag = False
                    break
            except:
                print("失敗")


def run_2():
    wether = tenki.get_weather_code()
    # 晴れ
    if wether in [0, 1, 2]:
        aibo.play_motion(
            create_arguments(
                "Category", "happy0rHot", second_Property="Mode", second_value="NONE"
            )
        )
    # 曇り
    elif wether == 3:
        aibo.play_motion(
            create_arguments(
                "Category", "jiggle", second_Property="Mode", second_value="NONE"
            )
        )
    # 雨
    else:
        aibo.play_motion(
            create_arguments(
                "Category", "bad", second_Property="Mode", second_value="NONE"
            )
        )


while True:
    voice = aibo.get_voice()
    if not isinstance(voice, list):
        print(voice)
        # 掃除
        voice_command = voice["voice_command_status"]["command"]
        if voice_command == "usercommand1":
            run()
        # 天気
        elif voice_command == "usercommand2":
            run_2()
