import boto3
import sys

sqs_client=boto3.client("sqs")

queue_url=sys.argv[1]
number_of_message=int(sys.argv[2])

try:
    wait_time_seconds=int(sys.argv[3])
except IndexError:
    wait_time_seconds=0
    

def sqs_receive_message():

    res = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=number_of_message,
            WaitTimeSeconds=wait_time_seconds
        )
    if "Messages" in res:
        for message in res["Messages"]:
            show_message(message)
            sqs_delete_message(message["ReceiptHandle"])
    else:
        print ("get empty list of messages")


def sqs_delete_message(receipt_handle):

    res = sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )

    print("deleted message")

def show_message(message):
    msg_id = message["MessageId"]
    msg_body = message["Body"]
    msg_receipt_handle = message["ReceiptHandle"]

    print("message ID: " + msg_id + " --- " + msg_body)
#     print("message handle ID: " + msg_receipt_handle)


def main():
    print("receive message from queue: " + queue_url + " with wait_time_seconds = " + str(wait_time_seconds))
    sqs_receive_message()
    print("---End---")


if __name__ == "__main__":
    main()
