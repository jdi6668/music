import whisper
import pandas as pd

def mp3_to_word_timestamp(mp3_path: str, model_size: str = "small"):
    # 加载模型：tiny/base/small/medium/large，越大识别越准、速度越慢
    model = whisper.load_model(model_size)
    # 开启字粒度时间戳，指定中文
    result = model.transcribe(
        audio=mp3_path,
        word_timestamps=True,
        language="zh",
        verbose=False
    )

    word_list = []
    # 遍历所有语音片段
    for segment in result["segments"]:
        # 遍历片段内每一个字
        for word_data in segment["words"]:
            word = word_data["word"].strip()
            start_sec = round(word_data["start"], 2)
            end_sec = round(word_data["end"], 2)
            duration_sec = round(end_sec - start_sec, 2)

            item = {
                "汉字": word,
                "开始时间(秒)": start_sec,
                "结束时间(秒)": end_sec,
                "持续时长(秒)": duration_sec
            }
            word_list.append(item)
            # 控制台实时打印
            print(f"字：{word:4} | 起始：{start_sec}s | 结束：{end_sec}s | 时长：{duration_sec}s")

    # 导出Excel
    df = pd.DataFrame(word_list)
    excel_name = mp3_path.replace(".mp3", "_字时间戳.xlsx")
    df.to_excel(excel_name, index=False)
    print(f"\n识别完成！数据已导出至：{excel_name}")
    return word_list

if __name__ == "__main__":
    # 替换成你的mp3文件路径
    AUDIO_FILE = "heisemaoyi.mp3"
    mp3_to_word_timestamp(AUDIO_FILE, model_size="small")