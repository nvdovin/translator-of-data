import time
import requests
import pandas as pd
import json
import uuid

translated_df = pd.DataFrame(columns=["action_original", "action_translated"]);

df = pd.read_csv('uniq_events.csv', sep=";")

def request_to_api(request: str):
    cookies = {
        'sessionId': '84dac58b-c2a7-4d5a-8e03-fa3e5cbe2213',
        'intercom-id-x55eda6t': '8b1c5502-424f-420e-9dd1-255c3d5abe0a',
        'intercom-device-id-x55eda6t': '1cb6485d-c267-437d-8829-73b0e5938942',
        'render_app_version_affinity': 'dep-cvlu68odl3ps73a075p0',
        '__Host-authjs.csrf-token': '17fb6fc6dbfcc62502e9c11a0fbc909c63bc4a8eee845fba4e0e5010cb778a7e%7C623d7ee76823ee6cbf6bc2519685558a47f0c9aa7e5905072bc614de7f8fe01e',
        'g_state': '{"i_l":0}',
        '__Secure-authjs.callback-url': 'https%3A%2F%2Fwww.blackbox.ai%2F',
        '__Secure-authjs.session-token': 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..hPZnlqSCsIAGsKAI.7gtuF0BDzt9S6S3UKDA9kOa59WUT1i-wMBZH3uEnSfQQkWO5kQiHduEwuDh7BBc8EUvMKUTSVb5pwrpQfGZ7xit2PjUolghbJggu5zFk1VaE6epb1zucTr-cZUxImuOvbOOAnt9sz6U6UN2ZfGYKp9Wnco44wX8TjjVrac6GdmtkAhI1UGi6ktkRKuaqX5RYui1qLT7cEqpvK-aoc99h9VPM8GspXosolIrKjW8C2KsRD5cqOISLePLP_WG0bR2Ki8YbNpf26uqD1wT2R276MMfPggPFEL0u3KHrwOvwFERUKicbf3KbqyfEGt0hRV46W32--27r_s9dD2GLEQSQslyrUMKj7s0LPW8eqzH0653PnPNcyUzaunXTMf9g1S-6_IplvVUz0B_MK-1h-jVhuPOXDbyhyQOge-m1qR0ETJP_uZaJLsqQpb-yvme-e4I4bYzRd2BTwKC-n_ZF0fj7dkR5svvxuHUYlxgy5KQavZ0ET-YWfFMzJODv15EGtrII-ETIwTDtQavk-hMR-oqLH8G0D6kp1s78OEl6Jg.oq2USfY_hP_RhpE2FzFIsQ',
        'intercom-session-x55eda6t': 'cFRWYXRKNCtXWkpESHBqQzFiYnZNSkFLZEZoWnJaV2hqZjFVSkh2a0xwS3UxSmUyNklPd2U5ZzlQS2VJTjREWld5bU9uUkNMTHcxNFQyYWo3ZHF6eHV2QUlOR2x5eHdyc3BHZWIwVzdmTFU9LS1URE5rMGVJLyszeGYzVnVvT24zdy9nPT0=--cb4790e621832dcaa131e34d9df136e9d7ae19fe',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,bg;q=0.6',
        'content-type': 'application/json',
        'origin': 'https://www.blackbox.ai',
        'priority': 'u=1, i',
        'referer': 'https://www.blackbox.ai/',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
        # 'cookie': 'sessionId=84dac58b-c2a7-4d5a-8e03-fa3e5cbe2213; intercom-id-x55eda6t=8b1c5502-424f-420e-9dd1-255c3d5abe0a; intercom-device-id-x55eda6t=1cb6485d-c267-437d-8829-73b0e5938942; render_app_version_affinity=dep-cvlu68odl3ps73a075p0; __Host-authjs.csrf-token=17fb6fc6dbfcc62502e9c11a0fbc909c63bc4a8eee845fba4e0e5010cb778a7e%7C623d7ee76823ee6cbf6bc2519685558a47f0c9aa7e5905072bc614de7f8fe01e; g_state={"i_l":0}; __Secure-authjs.callback-url=https%3A%2F%2Fwww.blackbox.ai%2F; __Secure-authjs.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..hPZnlqSCsIAGsKAI.7gtuF0BDzt9S6S3UKDA9kOa59WUT1i-wMBZH3uEnSfQQkWO5kQiHduEwuDh7BBc8EUvMKUTSVb5pwrpQfGZ7xit2PjUolghbJggu5zFk1VaE6epb1zucTr-cZUxImuOvbOOAnt9sz6U6UN2ZfGYKp9Wnco44wX8TjjVrac6GdmtkAhI1UGi6ktkRKuaqX5RYui1qLT7cEqpvK-aoc99h9VPM8GspXosolIrKjW8C2KsRD5cqOISLePLP_WG0bR2Ki8YbNpf26uqD1wT2R276MMfPggPFEL0u3KHrwOvwFERUKicbf3KbqyfEGt0hRV46W32--27r_s9dD2GLEQSQslyrUMKj7s0LPW8eqzH0653PnPNcyUzaunXTMf9g1S-6_IplvVUz0B_MK-1h-jVhuPOXDbyhyQOge-m1qR0ETJP_uZaJLsqQpb-yvme-e4I4bYzRd2BTwKC-n_ZF0fj7dkR5svvxuHUYlxgy5KQavZ0ET-YWfFMzJODv15EGtrII-ETIwTDtQavk-hMR-oqLH8G0D6kp1s78OEl6Jg.oq2USfY_hP_RhpE2FzFIsQ; intercom-session-x55eda6t=cFRWYXRKNCtXWkpESHBqQzFiYnZNSkFLZEZoWnJaV2hqZjFVSkh2a0xwS3UxSmUyNklPd2U5ZzlQS2VJTjREWld5bU9uUkNMTHcxNFQyYWo3ZHF6eHV2QUlOR2x5eHdyc3BHZWIwVzdmTFU9LS1URE5rMGVJLyszeGYzVnVvT24zdy9nPT0=--cb4790e621832dcaa131e34d9df136e9d7ae19fe',
    }

    json_data = {
        'messages': [
            {
                'id': 'QCr20Xk',
                'content': request,
                'role': 'user',
            },
        ],
        'agentMode': {},
        'id': 'QCr20Xk',
        'previewToken': None,
        'userId': None,
        'codeModelMode': True,
        'trendingAgentMode': {},
        'isMicMode': False,
        'userSystemPrompt': None,
        'maxTokens': 1024,
        'playgroundTopP': None,
        'playgroundTemperature': None,
        'isChromeExt': False,
        'githubToken': '',
        'clickedAnswer2': False,
        'clickedAnswer3': False,
        'clickedForceWebSearch': False,
        'visitFromDelta': False,
        'isMemoryEnabled': False,
        'mobileClient': False,
        'userSelectedModel': None,
        'validated': f'00f37b34-a166-4efb-bce5-1312d87f2f94',
        'imageGenerationMode': False,
        'webSearchModePrompt': False,
        'deepSearchMode': False,
        'domains': None,
        'vscodeClient': False,
        'codeInterpreterMode': False,
        'customProfile': {
            'name': '',
            'occupation': '',
            'traits': [],
            'additionalInfo': '',
            'enableNewChats': False,
        },
        'session': {
            'user': {
                'name': 'Nikita Vdovin',
                'email': 'narmunine@gmail.com',
                'image': 'https://lh3.googleusercontent.com/a/ACg8ocL76qzYVT43eH2_rN3lS4IWC0U6OEeYB0poUZD6rPnXjuKi5QGo=s96-c',
                'id': '104542877676102696926',
            },
            'expires': '2025-05-01T13:25:07.715Z',
        },
        'isPremium': True,
        'subscriptionCache': {
            'status': 'FREE',
            'expiryTimestamp': None,
            'lastChecked': 1743513907352,
            'isTrialSubscription': False,
        },
        'beastMode': False,
        'reasoningMode': False,
    }

    response = requests.post('https://www.blackbox.ai/api/chat', cookies=cookies, headers=headers, json=json_data)
    return response


def get_prompt(json_of_data: str):
    schema = '''
"action_original": "name of the action from Input Data",
"action_translated": "name of the action that the user performed on English"
    '''
    return  f"""
#Answer Instruction:
-Forget everythink you working with before. This is new chat!
-All words in sentences must be translated from Russian into English.
-Do not change the structure of the transmitted sentences.
-Use English accounting vocabulary.
-Answer in the form of the Answer JSON Schema.
-Do not delete special characters such as #, №, >, etc.
-Don't wrap the names in quotation marks.
-In attribute "action" replace "1С, 1C" to "ERP".
-In attribute "action" replace "platina" to "silver".
-In attribute "action" replace all domains .ru and .su to .com.
-In attribute "action" replace 'mmk' to 'erp', 'MMK' to 'ERP', 'ММК' to 'ERP', 'УПД' to 'UTD'.
-If attribute is empty, return empty value.
-Do not format your answer. Just put it raw JSON.

#Answer JSON Schema:
[
//List all groups from the input
{schema}
]

#Input Data
{json_of_data}

#Answer JSON:
"""

def iterater():
    head_bunch = 20
    chunk_size = 10
    i = 0
    array_of_jsons = list()
    df_length = df.size
    znamenatel = df.size
    deserializer = str()

    for row in df["action"]:
        if i < chunk_size and df_length > 0:
            array_of_jsons.append({"action": row})
            i += 1
            df_length -= 1

        else:
            i = 0
            text_json = json.dumps(array_of_jsons, ensure_ascii=False)
            array_of_jsons = list()
            time.sleep(2)
            response = request_to_api(request=get_prompt(text_json))
            try:
                print(f'{round((translated_df.size / znamenatel) * 100, 5)}%')

                while response.status_code != 200:
                    time.sleep(1)
                    print('[log] Waiting for a sec')
                    response = request_to_api(request=get_prompt(text_json))

                deserializer = json.loads(response.text)
                for row_json in deserializer:
                    translated_df.loc[len(translated_df)] = [row_json["action_original"], row_json["action_translated"]]

            except Exception as error:
                print(f'[log] Status code {response.status_code}')
                print(response.text)
                print(f"[log] Error is - {error}")
    for row_json in deserializer:
        translated_df.loc[len(translated_df)] = [row_json["action_original"], row_json["action_translated"]]
    print("[log] Data is translated at all")



iterater()
translated_df.to_csv('transladed_by_blackbox.csv', sep=';', index=False)