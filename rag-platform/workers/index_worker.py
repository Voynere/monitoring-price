from __future__ import annotations

import json
import sys
from pathlib import Path

import pika

from ingestors.smyalichi.code_ingestor import SmyalichiCodeIngestor
from pipeline.config import Settings
from pipeline.parent_child import attach_parent_child, flatten_for_index
from pipeline.indexer import PgVectorIndexer


def enqueue_reindex(root: Path, settings: Settings) -> None:
    params = pika.URLParameters(settings.rabbitmq_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=settings.rag_queue_name, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=settings.rag_queue_name,
        body=json.dumps({"root": str(root)}).encode("utf-8"),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    connection.close()


def handle_message(body: bytes, settings: Settings) -> None:
    payload = json.loads(body.decode("utf-8"))
    root = Path(payload.get("root", ".")).resolve()
    ingestor = SmyalichiCodeIngestor(root)
    chunks = flatten_for_index(attach_parent_child(ingestor.ingest()))
    indexer = PgVectorIndexer(settings)
    indexed = indexer.upsert(chunks)
    print(f"Worker indexed {indexed} chunks from {root}")


def main() -> None:
    settings = Settings()
    params = pika.URLParameters(settings.rabbitmq_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=settings.rag_queue_name, durable=True)

    def callback(ch, method, properties, body):  # noqa: ANN001
        try:
            handle_message(body, settings)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as exc:  # noqa: BLE001
            print(f"Worker failed: {exc}", file=sys.stderr)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=settings.rag_queue_name, on_message_callback=callback)
    print(f"Listening on queue {settings.rag_queue_name}")
    channel.start_consuming()


if __name__ == "__main__":
    main()
