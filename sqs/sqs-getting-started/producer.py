import boto3
import sys

sqs_client = boto3.client("sqs", region_name="ap-southeast-1")

queue_url= sys.argv[1]
message_number = int(sys.argv[2])

def sqs_send_message(message_body):

    res = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )

    print("Sent message " + res["MessageId"] + " with body: " + message_body)

def main():
    print("Connect to SQS queue: " + queue_url)
    print("Start put message to queue:")

    for i in range (0, message_number):
        message_body = "test message number " + str(i)
        sqs_send_message(message_body)

    print("--End--")

if __name__ == "__main__":
    main()
