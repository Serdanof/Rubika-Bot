'''Copyright (c) 2023 amirali irvany `MIT LICENSE`'''

from re import sub, findall
from pyrubi import Client
from langdetect import detect
from subprocess import getoutput
from random import choice, randint
from requests import get, exceptions
from better_profanity import profanity

# Enter the guid of your group(s) into this list
groups = [
    '',
]
# No need to change
token = '295809:6517005fc9455'


def main():

    TIMEOUT = 10
    CAPABILITIES = ['img', 'font', 'ai']
    client = Client(session='session', time_out=TIMEOUT)
    for guid in groups:
        if guid.strip() == '':
            groups.remove(guid)

        admins = client.get_all_members(object_guid=guid, just_get_guids=True)
        result = client.get_chat_info(object_guid=guid)
        group_name = result['group']['group_title']
        client.send_text(
            object_guid=guid,
            text=f'The bot was successfully activated in the \'{group_name}\''
        )

    for update in client.on_message(filters=['User', 'Channel']):
        if update.object_guid in groups:
            _me = client.get_me()['user']['user_guid']
            _message_id = client.get_messages_by_id(
                object_guid=update.object_guid,
                message_ids=[update.message_id]
            )
            try:
                _guid_message = client.get_messages_by_id(
                    object_guid=update.object_guid,
                    message_ids=[_message_id['messages'][0]['reply_to_message_id']]
                )
                if (
                    ('ai' in CAPABILITIES) and _me == _guid_message['messages'][0]['author_object_guid']
                ):
                    client.send_text(
                        object_guid=update.object_guid,
                        text='Processing, __please wait..__',
                        message_id=update.message_id
                    )
                    responce = get(f'https://pyrubi.b80.xyz/chat.php?text={update.text}').json()
                    client.send_text(
                        object_guid=update.object_guid,
                        text=responce[0]['text'],
                        message_id=update.message_id
                    )
            except Exception:
                pass

            try:
                if update.text.startswith('+') and ('ai' in CAPABILITIES):
                    if update.text.strip() == '+':
                        client.send_text(
                            object_guid=update.object_guid,
                            text='Please Enter a text\nExample: __+hello__'
                        )
                    else:
                        client.send_text(
                            object_guid=update.object_guid,
                            text='Processing, __please wait..__',
                            message_id=update.message_id
                        )
                        responce = get(f'https://pyrubi.b80.xyz/chat.php?text={update.text[1:]}').json()
                        client.send_text(
                            object_guid=update.object_guid,
                            text=responce[0]['text'],
                            message_id=update.message_id
                        )


                elif update.text.startswith('img') and ('img' in CAPABILITIES):
                    if update.text.strip() == 'img':
                        client.send_text(
                            object_guid=update.object_guid,
                            text='Please Enter a text\nExample: __img wolf__',
                            message_id=update.message_id
                        )
                    elif profanity.contains_profanity(update.text):
                        client.send_text(
                            object_guid=update.object_guid,
                            text='**Your message has been detected as obscene**',
                            message_id=update.message_id
                        )
                    else:
                        client.send_text(
                            object_guid=update.object_guid,
                            text='Processing, __please wait..__',
                            message_id=update.message_id
                        )
                        text = sub('img', '', update.text).strip()
                        try:
                            if detect(text) in ['fa', 'ar', 'ur']:
                                request_text = get(
                                    f'https://one-api.ir/translate/?token={token}&action=google&lang=fa&q={text}').json()

                            _text = request_text['result']
                            request = get(f'https://haji-api.ir/prompts/?text={_text}').json()
                            responce = get(choice(request['result']))
                            with open('.img.png', 'wb') as _file:
                                _file.write(responce.content)

                            client.send_image(
                                object_guid=update.object_guid,
                                file='.img.png',
                                text=f'your image is realy👍\ncontent:\"{_text}\"\ndeveloper: @ohmyz_sh',
                                message_id = update.message_id,
                            )
                        except Exception:
                            client.send_text(
                                object_guid=update.object_guid,
                                text='**There was a problem with us!. Please try again**',
                                message_id=update.message_id
                            )


                elif update.text == '$' or update.text == 'usd':
                    client.send_text(
                        object_guid=update.object_guid,
                        text='Processing, __please wait..__',
                        message_id=update.message_id
                    )
                    responce = get(f'https://one-api.ir/price/?token={token}').json()
                    dollar = responce['result']['currencies']['dollar']
                    euro = responce['result']['currencies']['eur']
                    gold = responce['result']['gold']['geram24']
                    client.send_text(
                        object_guid=update.object_guid,
                        text='💵 **Us Dollar:**\nAverage: __%s__\nMax: __%s__\nMin: __%s__\n\n'
                             '💶 **Euro:**\nAverage: __%s__\nMax: __%s__\nMin: __%s__\n\n' 
                             '🧈 **Gold:**\nAverage: __%s__\nMax: __%s__\nMin: __%s__' % (
                             dollar['p'], dollar['h'], dollar['l'], euro['p'], euro['h'], euro['l'], gold['p'], gold['h'], gold['h']
                        ),
                        message_id=update.message_id
                    )


                elif update.text.startswith('font') and ('font' in CAPABILITIES):
                    if update.text == 'font':
                        client.send_text(
                            object_guid=update.object_guid,
                            text='Please Enter a text\nExample: __font amir__',
                            message_id=update.message_id
                        )
                    else:
                        client.send_text(
                            object_guid=update.object_guid,
                            text='Processing, __please wait..__',
                            message_id=update.message_id
                        )
                        _text = update.text.split('font')[-1]
                        if profanity.contains_profanity(_text):
                            client.send_text(
                                object_guid=update.object_guid,
                                text='',
                                message_id=update.message_id
                            )
                        elif detect(text) in ['fa', 'ar', 'ur']:
                            request = get(f'http://api.codebazan.ir/font/?type=fa&text={_text}').json()
                        else:
                            request = get(f'http://api.codebazan.ir/font/?text={_text}').json()

                        _message_id = client.get_messages_by_id(
                            object_guid=update.object_guid,
                            message_ids=[update.message_id]
                        )
                        user_guid = _message_id['messages'][0]['author_object_guid']
                        for num in range(1, 10):
                            try:
                                client.send_text(
                                    object_guid=user_guid,
                                    text=request['result'][str(num)],
                                    message_id=update.message_id
                                )
                            except KeyError:
                                client.send_text(
                                    object_guid=user_guid,
                                    text=request['Result'][str(num)],
                                    message_id=update.message_id
                                )
                        client.send_text(
                            object_guid=update.object_guid,
                            text='The fonts have been sent to your PV ✅',
                            message_id=update.message_id
                        )


                elif update.text == 'news':
                    client.send_text(
                        object_guid=update.object_guid,
                        text='Processing, __please wait..__',
                        message_id=update.message_id
                    )
                    _responce = get(f'https://one-api.ir/rss/?token={token}&action=irinn').json()
                    responce = choice(_responce['result']['item'])
                    client.send_text(
                        object_guid=update.object_guid,
                        text='**%s**\n\n%s\n\n__%s__' % (
                            responce['title'], responce['description'], responce['pubDate']
                        ),
                        message_id=update.message_id
                    )


                elif update.text == 'joke':
                    responce = get(f'https://one-api.ir/joke/?token={token}').json()
                    client.send_text(
                        object_guid=update.object_guid,
                        text=responce['result'],
                        message_id=update.message_id
                    )


                elif update.text == 'link':
                    info = client.get_chat_info(object_guid=update.object_guid)
                    try:
                        _results = client.get_link(object_guid=info['group']['group_guid'])
                        group_link = _results['join_link']
                        group_title = info['group']['group_title']
                        client.send_text(
                            object_guid=update.object_guid,
                            text=f'The link to the {group_title} group is:\n\n``{group_link}``'
                        )
                    except:
                        client.send_text(
                            object_guid=update.object_guid,
                            text='**Please admin the robot account in the group❗**',
                            message_id=update.message_id
                        )


                elif update.text == 'test':
                    client.send_text(
                        object_guid=update.object_guid,
                        text='The bot is active ✅',
                        message_id=update.message_id
                    )


                elif update.text == 'time':
                    responce = get('http://api.codebazan.ir/time-date/?td=all')
                    client.send_text(
                        object_guid=update.object_guid,
                        text=responce.text,
                        message_id=update.message_id
                    )


                elif update.text == 'ping':
                    _output = getoutput('ping -c 1 4.2.2.4')
                    results = findall(r'time=(.*)\ ', _output)
                    client.send_text(
                        object_guid=update.object_guid,
                        text=f'🌐 Ping now: **{str(results[0])}**',
                        message_id=update.message_id
                    )


                elif update.author_guid in admins:
                    if update.text.startswith('off'):
                        if update.text.strip() == 'off':
                            client.send_text(
                                object_guid=update.object_guid,
                                text='Please enter a text\nExample: __off ai__',
                                message_id=update.message_id
                            )
                        else:
                            value = update.text.split('off')[-1].strip()
                            if value not in CAPABILITIES:
                                client.send_text(
                                    object_guid=update.object_guid,
                                    text='**This feature is already disabled**',
                                    message_id=update.message_id
                                )
                            else:
                                CAPABILITIES.remove(value)
                                client.send_text(
                                    object_guid=update.object_guid,
                                    text=f'Ability {value} Unreachable ✅',
                                    message_id=update.message_id
                                )


                    elif update.text.startswith('on'):
                        if update.text.strip() == 'on':
                            client.send_text(
                                object_guid=update.object_guid,
                                text='Please enter a text\nExample: __on ai__',
                                message_id=update.message_id
                            )
                        else:
                            value = update.text.split('on')[-1].strip()
                            if value in CAPABILITIES:
                                client.send_text(
                                    object_guid=update.object_guid,
                                    text='**This feature is already enabled**',
                                    message_id=update.message_id
                                )
                            else:
                                CAPABILITIES.append(value)
                                client.send_text(
                                    object_guid=update.object_guid,
                                    text=f'Ability {value} became accessible ✅',
                                    message_id=update.message_id
                                )


            except TimeoutError:
                client.send_text(
                    object_guid=update.object_guid,
                    text='timeout-err',
                    message_id=update.message_id
                )

            except Exception as err: print(err)


if __name__ == '__main__':
    main()
