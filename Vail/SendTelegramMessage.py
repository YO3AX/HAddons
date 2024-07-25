import requests
from datetime import datetime
def SendTelegramMessage(p_bot_token, p_recipient,  p_message):
    try:
        def telegram_bot_sendtext(bot_message):
            send_text = 'https://api.telegram.org/bot' + p_bot_token + '/sendMessage?chat_id=' + p_recipient + '&parse_mode=Markdown&text=' + p_message
            response = requests.get(send_text)
            return response.json()
        message = telegram_bot_sendtext(p_message)
    except requests.Error as error:    
        print(datetime.now(),'Request Error:',p_message)
    finally:
        pass
        #print(datetime.now(),': ','Telegram message sent. To: ',p_recipient,'Text: ',p_message)
