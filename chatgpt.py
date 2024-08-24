from openai import OpenAI
from datetime import datetime


def parse_text(question):
    now = datetime.now()
    current_date = now.date()
    current_time = now.time()
    date_str = current_date.strftime("%Y%m%d")
    time_str = current_time.strftime("%H%M")

    # question = "내일 2시에 부산에서 서울로가는 표 사줘."

    prompt = f"당신은 버스 예약 요청을을 서버에서 원하는 형식으로 변환해주는 AI assistant입니다. 아래의 instruction을 따라서 주어진 텍스트에서 json 형식으로 작성하십시오.\n\n-----\n\nInstruction : 주어진 문장에서 찾아야 할 정보와 그 내용은 다음과 같아. \'departDate\' : 출발 날짜 \n\'departTime\' : 출발 시간 \'departOption\' : 출발 옵션. 가장 빠른 시간의 표를 찾으려면 0, 1시간 뒤 까지의 표를 찾으려면 1, 2시간 뒤 까지의 표를 찾으려면 2. 최대 2까지밖에 없음. \'from\' : 버스 출발 지역 \'to\' : 버스 도착 지역 \n\n-----\n\nTemplate 은 다음과 같습니다. 당신은 {{answer}}에 들어갈 부분만 생성하면 됩니다. \n\nGiven information \nDate: YYYYMMDD \nTime: HHMM \n\nQuery : {{question}} \nAnswer : {{answer}}\n\n-----\n\nexample 1 \n\nGiven information \nDate: 20240421 \nTime: 1723 \nQuery : \'내일 1시에 역 도착해서 2시간 이내에 있는 표 구해줘. 밥 먹고 서울에서 부산으로 갈거야\' \nAnswer: {{\'departDate\' : \'20240422\', \'departTime\' : \'1500\', departOption\' : \'0\', \'from\' : \'서울\', \'to\' : \'부산\' }} \n\nexample 2 \n\nGiven information \nDate: 20240124 \nTime: 1801 \nQuery : \'1시간 뒤에 대구에서 전주 가려고 하는데, 표 있어?\'\nAnswer: {{\'departDate\' : \'20240124\', \'departTime\' : \'1801\', departOption\' : \'1\', \'from\' : \'대구\', \'to\' : \'전주\' }}\n\nexample 3\n\nGiven information \nDate: 20240401\nTime: 1110\nQuery : \'지금 가장 빠른 시간에 부산에서 여수 가는 표 찾아줘.\'\nAnswer: {{\'departDate\' : \'20240401\', \'departTime\' : \'1110\', departOption\' : \'0\', \'from\' : \'부산\', \'to\' : \'여수\' }}\n\n-----\n\nGiven information\n\nDate: {date_str}\nTime: {time_str}\n\nQuery : {question}\nAnswer:{{answer}}"

    # Initialize the OpenAI client
    client = OpenAI(api_key="your openai api key")

    # Set up the conversation messages
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": question}
    ]

    # Call the ChatCompletion.create method
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=messages
    )

    # Print the response
    answer = response.choices[0].message.content

    return eval(answer.split("Answer: ")[1])
