from datetime import datetime, timezone

from make87_messages.text.text_plain_pb2 import PlainText
from make87 import initialize, get_provider, resolve_endpoint_name


def main():
    initialize()
    endpoint_name = resolve_endpoint_name(name="PROVIDER_ENDPOINT")
    endpoint = get_provider(name=endpoint_name, requester_message_type=PlainText, provider_message_type=PlainText)

    def callback(message: PlainText) -> PlainText:
        received_dt = datetime.now(tz=timezone.utc)
        publish_dt = message.timestamp.ToDatetime().replace(tzinfo=timezone.utc)
        print(
            f"Received message '{message.body}'. Sent at {publish_dt}. Received at {received_dt}. Took {(received_dt - publish_dt).total_seconds()} seconds."
        )

        return PlainText(body=message.body[::-1])

    endpoint.provide(callback)


if __name__ == "__main__":
    main()
