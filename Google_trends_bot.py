import requests
import time
from pytrends.request import TrendReq

pytrend = TrendReq()

token = str(os.environ.get("TGGOOGLETOKEN"))


def gtrends(keyword):
    pytrend.build_payload(kw_list=[keyword])
    related_queries = pytrend.related_queries()

    result_top = str(list(related_queries.values())[0]['top'])
    result_rising = str(list(related_queries.values())[0]['rising'])

    full_result = "Топ запросов: \n\n" + good_view(result_top) + "\n========================\nРастущие запросы: \n\n" + good_view(result_rising)
    return full_result

def good_view(google_resp_part):
    new_str = ""
    result_list = google_resp_part.split("\n")[1:]
    for x in result_list:
        item_text = x[2:-7].lstrip(" ") + "\n"
        item_num = "------------ Оценка: " + x[-7:].lstrip(" ") + "\n\n"
        new_str += item_text + item_num
    return new_str


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method='getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update


google_trends_bot = BotHandler(token)


def main():
    print("Start\n")
    new_update_id = 0
    sleep_time = 3
    check = True
    while True:
        time.sleep(sleep_time)

        last_update = google_trends_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']


        if check:
            new_update_id = last_update_id
            check = False

        if new_update_id != last_update_id and "/start" in last_chat_text.lower():
            google_trends_bot.send_message(last_chat_id, "Привет, этот бот\nприсылает статистику\nGoogle trends \n\n Пиши любой запрос:\n (Ответ через 15 секунд)")
            new_update_id = last_update_id
            sleep_time = 15

        if new_update_id != last_update_id and "/123" in last_chat_text.lower():
            google_trends_bot.send_message("@test_dotparsed", "Привет, этот бот\nприсылает статистику\nGoogle trends \n\n Пиши любой запрос:\n (Ответ через 15 секунд)")


        if new_update_id != last_update_id and "/help" in last_chat_text.lower():
            google_trends_bot.send_message(last_chat_id, "Привет, этот бот\nприсылает статистику\nGoogle trends \n\n Пиши любой запрос:\n (Ответ через 15 секунд)")
            new_update_id = last_update_id

        if new_update_id != last_update_id and "/" not in last_chat_text:
            new_keyword = last_chat_text.lower()
            google_trends_bot.send_message(last_chat_id, "загрузка...")
            google_trends_bot.send_message(last_chat_id, str(gtrends(new_keyword)))

            new_update_id = last_update_id
            print(last_chat_name + ";" + new_keyword)


if __name__ == '__main__':
    main()