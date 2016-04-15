from flask import Flask, request, Response

from kik import KikApi, Configuration
from kik.messages import messages_from_json, TextMessage

app = Flask(__name__)
kik = KikApi('valescobot', 'b21fceb8-90ab-4599-8004-43b336f33054')

kik.set_configuration(Configuration(webhook='https://dry-dawn-97641.herokuapp.com/'))

@app.route('/incoming', methods=['POST'])
def incoming():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)

    messages = messages_from_json(request.json['messages'])

    for message in messages:
        if isinstance(message, TextMessage):
            kik.send_messages([
                TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body=message.body
                )
            ])

        return Response(status=200)


if __name__ == "__main__":
    app.run(port=8080, debug=True)