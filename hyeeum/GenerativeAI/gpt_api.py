import time
import openai
from openai import OpenAI
from config import settings

def getGPTAPI(user_content, order, alignment="", cnt=0):
    try:
        if order == 1: # 닉네임 생성
            client = openai.OpenAI(api_key=settings.get_env_variable('API_KEY'))
            contents = user_content + "\n Q는 질문이고 A는 답변이야 내용을 읽고 판단하여 {'alignment' : '이사람의 성향을 한줄로 표현', 'nickname' : '성향과 내용으로 이 사람에게 어울리는 한글닉네임 5개'}를 생성해줘"
            chat_completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text",
                             "text": contents
                             }
                        ]
                    }
                ],
                max_tokens=200,
                temperature=1
            )
            get_message = chat_completion.choices[-1].message.content
            print(1)
            print(get_message)
            s = ''
            for i, ch in enumerate(get_message):
                if ch == ' ' and s == '':
                    continue
                elif i+1 < len(get_message) and get_message[i] == ',' and get_message[i + 1] == '\n':
                    continue
                elif i + 1 < len(get_message) and get_message[i] == ' ' and get_message[i] == ':':
                    continue
                elif i + 2 < len(get_message) and get_message[i] == ',' and get_message[i+1] == ' ':
                    continue
                elif ch == '{' or ch == '}' or ch == '\n' or ch == '"' or ch == "'" or ch == "[" or ch == "]":
                    continue
                elif i+1 < len(get_message) and get_message[i] == 'a' and get_message[i+1] == 'l':
                    for j in range(i, len(get_message)):
                        if get_message[j] not in "alignment":
                            break
                    s += ch
                elif i+1 < len(get_message) and get_message[i] == 'n' and get_message[i+1] == 'i':
                    for j in range(i, len(get_message)):
                        if get_message[j] not in "nickname":
                            break
                    s += '\n'
                    s += ch
                else:
                    s += ch

            return s

        # 내용을 듣고 다음 질문 생성하기
        elif order == 2: # GPT 질문 문구 생성
            client = openai.OpenAI(api_key=settings.get_env_variable('API_KEY'))
            contents = user_content + "\n Q는 질문이고 A는 답변이야 내용을 읽는데 "+ "이 사람의 성향은 " + alignment + "야 이 성향도 고려해서 다음 질문을 대화를 이끌어갈 짧은 한문장으로 생성해줘 Q. 다음 질문 생성 형식으로 보내줘 답변에는 성향에 대한 말을 절대 넣지 마"
            chat_completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                {
                    "role": "user",
                    "content": [
                        {
                        "type": "text",
                        "text": contents
                        }
                    ]
                }],
                max_tokens=200,
                temperature=0.5
            )

            get_message = chat_completion.choices[-1].message.content
            print(2)
            print(get_message)
            s = ''
            for i, ch in enumerate(get_message):
                if i-2 >= 0 and ch == ' ' and get_message[i-1] == '.' and get_message[i-2] == 'Q':
                    s = ''
                elif i-1 >= 0 and ch == '.' and get_message[i-1] == 'Q':
                    s = ''
                else:
                    s += ch


            return s

        #emotion, 위로의 말 생성
        elif order == 3:
            client = openai.OpenAI(api_key=settings.get_env_variable('API_KEY'))
            contents = user_content + "\n Q는 질문이고 A는 답변이야 이 사람의 성향은" + alignment + "이고 다음 내용을 읽고 이 사람의 {'emotion': '감정[기쁨,화남,슬픔,즐거움]중 내용을 읽고 판단하여 택1', 'consolation': '위로의 말'} 이 형식으로 생성해줘, 답변에는 성향을 파악하는 얘기를 절대 하지마, 형식 꼭 맞춰줘"
            chat_completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": contents
                            }
                        ]
                    }
                ],
                max_tokens=300,
                temperature=1
            )

            get_message = chat_completion.choices[-1].message.content
            print(3)
            print(get_message)
            s = ''
            for i, ch in enumerate(get_message):
                if ch == ' ' and s == '':
                    continue
                elif i + 1 < len(get_message) and get_message[i] == ' ' and get_message[i] == ':':
                    continue
                elif i + 1 < len(get_message) and get_message[i] == ',' and get_message[i + 1] == '\n':
                    continue
                elif i + 2 < len(get_message) and get_message[i] == ',' and get_message[i+1] == ' ':
                    continue
                elif ch == '{' or ch == '}' or ch == '\n' or ch == '"' or ch == "'":
                    continue
                elif i + 1 < len(get_message) and get_message[i] == 'e' and get_message[i + 1] == 'm':
                    for j in range(i, len(get_message)):
                        if get_message[j] not in "emotion":
                            break
                    s += ch
                elif i + 1 < len(get_message) and get_message[i] == 'c' and get_message[i + 1] == 'o':
                    for j in range(i, len(get_message)):
                        if get_message[j] not in "consolation":
                            break
                    s += '\n'
                    s += ch
                else:
                    s += ch

            return s

        elif order == 4:
            client = openai.OpenAI(api_key=settings.get_env_variable('API_KEY'))
            contents = user_content + "\n Q는 질문이고 A는 답변이야, 사용자의 감정 빈도가 이렇다고 했을 때, 내용과 연계하여 이번주는 어땟는지 코멘트 남겨줘 형식은 Comment : 할말 으로 해줘"
            chat_completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text",
                             "text": contents
                             }
                        ]
                    }
                ],
                max_tokens=400,
                temperature=0.5
            )
            get_message = chat_completion.choices[-1].message.content

            print(get_message)
            s = ''
            for i, ch in enumerate(get_message):
                if ch == ' ' and s == '':
                    continue
                elif i + 1 < len(get_message) and get_message[i] == ',' and get_message[i + 1] == '\n':
                    continue
                elif i + 1 < len(get_message) and get_message[i] == ' ' and get_message[i] == ':':
                    continue
                elif ch == '{' or ch == '}' or ch == '\n' or ch == '"' or ch == "'" or ch == "[" or ch == "]":
                    continue
                elif i + 1 < len(get_message) and (get_message[i] == 'C' or get_message[i] == 'c') and get_message[i + 1] == 'o':
                    for j in range(i, len(get_message)):
                        if get_message[j] not in ("Comment" or "comment"):
                            break
                    s += ch
                else:
                    s += ch

            return s

    except Exception as e:
        print(e)
        if e == "context_length_exceeded":
            return "context_length_exceeded"

        if cnt>5:
            # "open ai 에러입니다. 잠시 후 다시 사용해주세요."
            return 400

        time.sleep(5)

        return getGPTAPI(user_content, order, alignment, cnt+1)