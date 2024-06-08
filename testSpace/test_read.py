# %%
import base64

import openai


CHATGPT_API_KEY_PATH = "../../private/openai/chatGPT_api.txt"
FORMAT = """
Read the receipt image and return a list with item names, quantities, unit prices, and totals. Also, return the total amount, tax rate, tax amount, and total with tax. Format:
[[[item name, quantity, unit price, total], ...], [total amount, tax rate, tax amount, total with tax]]
"""

def read_keyFile():
    try:
        with open(CHATGPT_API_KEY_PATH, 'r', encoding='utf-8') as file:
            key = file.readline().strip()
        return key
    except FileNotFoundError:
        return "ファイルが見つかりません。"
    except Exception as e:
        return f"エラーが発生しました: {e}"

# 画像をbase64にエンコードする関数
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def main():
    # 画像のパス
    image_path = "../images/test.jpg"

    # 画像をbase64にエンコードする
    base64_image = encode_image(image_path)

    # OpenAI APIのクライアントを作成する.
    openai.api_key = read_keyFile()

    # チャットの応答を生成する
    response = openai.chat.completions.create(
        # model の名前は gpt-4-vision-preview.
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": FORMAT},  # ここに質問を書く
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"},  # 画像の指定の仕方がちょい複雑
                ],
            }
        ],
        max_tokens=300,
    )

    # 応答を表示する
    print(response.choices[0])

main()