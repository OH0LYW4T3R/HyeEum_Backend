from openai import OpenAI
from config import settings

def getDALLE(user_content, emotion="", cnt=0):
    try:
        content = user_content + " 기분은 " + emotion + "이고 " + "이 내용을 읽고 이 내용과 감정을 연관하여 그림으로 나타내줘 그림 안에 글자 넣지마"
        #content = user_content + " 이 내용을 읽고 이 내용과 너가 판단한 감정을 연관하여 그림으로 나타내줘 그림 안에 글자 넣지마"
        client = OpenAI(api_key=settings.get_env_variable('API_KEY'))

        response = client.images.generate(
            model="dall-e-3",
            prompt=content,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[-1].url
        return image_url

    except Exception as e:
        print(e)
        if e == "context_length_exceeded":
            return "context_length_exceeded"


        if cnt > 5:
            # "open ai 에러입니다. 잠시 후 다시 사용해주세요."
            return 400

        return getDALLE(user_content, emotion, cnt+1)