import requests

def send_telegram_message(token, chat_id, messages):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': str(messages),
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=payload)
    return response.json()


def format_signal_dict(name, signal_dict):
    if not signal_dict:
        return f"*{name}*: No signal"
    lines = [f"*{name}*:"]
    for pair, message in signal_dict.items():
        lines.append(f"- `{message}`")
    return '\n'.join(lines)


last_message = ''

def send_if_changed(token, chat_id, new_message):  #Avoid repetitive message
    global last_message
    if new_message != last_message:
        send_telegram_message(token, chat_id, new_message)
        last_message = new_message
    else:
        print("No new signal — skipped sending.")
