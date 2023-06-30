import pika, requests, json


def callback(ch, method, properties, body):
    print("Enviando")
    my_json = body.decode('utf8')
    print("Mensagem recebida: ", my_json)
    data = json.loads(my_json)

    bname = data.get("bucketName")
    fName = data.get("fileName")
    rId = data.get("idApp")

    URL = f"http://localhost:8000/convert/{fName}"
    print("Enviando para ", URL)
    r = requests.get(url=URL)

    dataMsg = r.json()

    print(dataMsg)

    if dataMsg.get("message") == "Conversão finalizada e arquivo salvo no MinIO":
        print("Publicando mensagem de sucesso")
        channel_send.basic_publish(exchange='convert', routing_key='convert_queue.ready', body=bytes(str(rId), 'utf-8'))
    else:
        print("Publicando mensagem de falha")
        channel_send.basic_publish(exchange='convert', routing_key='convert_queue.error', body=bytes(str(rId), 'utf-8'))



url = 'amqp://myuser:mypassword@localhost:5672/%2f'
params = pika.URLParameters(url)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel_send = connection.channel()

channel.queue_declare(queue='convert_queue.ready', durable=True)
channel.queue_declare(queue='convert_queue.error', durable=True)
channel.basic_consume(queue='convert_queue', on_message_callback=callback, auto_ack=True)


print("Aguardando mensagens. Pressione CTRL+C para sair.")

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

# Fechar a conexão com o RabbitMQ
connection.close()