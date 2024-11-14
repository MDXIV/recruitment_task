import os
import yaml
import requests
from openai import OpenAI

def write_to_file(file_name, content):
    f = open(file_name, "wb")
    f.write(content.encode("utf-8"))
    f.close()

def get_chat_response(client, prompt, conversation_history, seed, temperature):
    conversation_history.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        messages=conversation_history,
        model="gpt-4o-mini",
        seed=seed,
        temperature=temperature
    )
    conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
    return conversation_history, response

if __name__ == "__main__":
    with open('config.yaml', 'r') as file:
        try:
            yaml_settings = yaml.safe_load(file)
            os.environ['OPENAI_API_KEY'] = yaml_settings['openai_key']
        except yaml.YAMLError as exc:
            print(exc)

    web_data = requests.get(f'https://cdn.oxido.pl/hr/Zadanie%20dla%20JJunior%20AI%20Developera%20-%20tresc%20artykulu.txt')
    if web_data.status_code != 200:
        raise Exception("Error: cannot featch server")

    conversation_history = []

    text = web_data.content.decode('utf-8', 'ignore')

    client = OpenAI(api_key = os.environ['OPENAI_API_KEY'])

    prompt = f"""Do podanego tekstu napisz używając kodu HTML stronę www, strona nie może mieć kodu CSS oraz JavaScript. Umieść tag <img> z atrybutem  src=\"image_placeholder.jpg\" w najbardziej odpowiednich miejscach, 
    dodaj do nich atrybut alt z dokładnym tekstem który możemy użyć do wygenerowania grafiki. Zwrócony kod powinien zawierać wyłącznie zawartość do wstawienia pomiędzy tagami <body> i </body> bez znaczników <body>. 
    Opowiedz powinna zawierać tylko czysty kod. Oto tekst: {text}"""
    conversation_history, response = get_chat_response(client, prompt, conversation_history, 52, 0.5)
    write_to_file("artykul.html", response.choices[0].message.content[8:-4])

    prompt = """Napisz najbardziej odpowiedni szablon dla wcześniej napisanego kodu. Możesz korzystać z CSS, stylów, JavaScript, Bootstrap, FontAwesome oraz innych zewnętrznych bibliotek. 
     Strona powinna wyglądać kreatywnie i mieć lekko przyciemniony kontrast. Powinna dobrze wyświetlać się na telefonach oraz komputerach stacjonarnych.
    Skrypty umieść w sekcji <head>. Sekcja <body> nie może zawierać żadnej treści, powinna być całkowicie pusta. Opowiedz powinna zawierać tylko sam kod bez żadnych komentarzy."""
    conversation_history.append({"role": "user", "content": prompt})
    conversation_history, response = get_chat_response(client, prompt, conversation_history, 52, 0.9)
    write_to_file("szablon.html", response.choices[0].message.content[8:-4])

    prompt = "Teraz połącz pierwszy i ostatni napisany kod. Bez żadnych komentarzy tylko sam kod."
    conversation_history, response = get_chat_response(client, prompt, conversation_history, 52, 0.7)
    write_to_file("podglad.html", response.choices[0].message.content[8:-4])
    