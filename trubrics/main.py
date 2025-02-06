import logging
import threading
import time
from datetime import datetime, timedelta, timezone

import requests

from trubrics.logger import trubrics_logger


class Trubrics:
    def __init__(
        self,
        api_key: str,
        host: str = "https://app.trubrics.com/api/ingestion",
        flush_interval: int = 10,
        flush_at: int = 20,
        logger: logging.Logger = trubrics_logger,
    ):
        self.host = host
        self.api_key = api_key
        self.queue: list[dict] = []
        self.flush_interval = flush_interval
        self.flush_at = flush_at
        self.last_flush_time = datetime.now(timezone.utc)
        self.is_flushing = False
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._periodic_flush, daemon=True)
        self._thread.start()
        self.logger = logger

    def track(
        self,
        user_id: str,
        event: str,
        properties: dict | None = None,
        timestamp: datetime | None = None,
    ):
        """
        Track an event.
        Args:
            user_id (str): The ID of the user.
            event (str): The name of the event.
            properties (dict | None): Additional properties to track.
            timestamp (datetime | None): The timestamp of event. If None, the current time in UTC is used. If not a datetime object, the event is ignored.
        """

        if timestamp and not isinstance(timestamp, datetime):
            self.logger.error("Timestamp must be a datetime object. Ignoring event.")
            return

        event_dict = {
            "user_id": user_id,
            "event": event,
            "properties": properties,
            "timestamp": (
                timestamp.isoformat()
                if timestamp
                else datetime.now(timezone.utc).isoformat()
            ),
        }
        with self._lock:
            self.queue.append(event_dict)
            self.logger.info(
                f"Event `{event}` by user `{user_id}` has been added to queue."
            )

    def track_llm(
        self,
        user_id: str,
        prompt: str,
        assistant_id: str,
        generation: str,
        properties: dict | None = None,
        timestamp: datetime | None = None,
        latency: int = 1,
    ):
        """
        Track an LLM prompt and generation.
        Args:
            user_id (str): The ID of the user.
            prompt (str): The prompt given to the LLM.
            assistant_id (str): The ID of the assistant.
            generation (str): The generated response from the LLM.
            properties (dict | None): Additional properties to track.
            timestamp (datetime | None): The timestamp of the generation event. If None, the current time in UTC is used.
            latency (int): The latency in milliseconds between the prompt and the generation. Defaults to 1.
        """
        generation_timestamp = timestamp or datetime.now(timezone.utc)
        prompt_timestamp = generation_timestamp - timedelta(milliseconds=latency)

        self.track(
            event="Prompt",
            user_id=user_id,
            properties={"$text": prompt, **(properties or {})},
            timestamp=prompt_timestamp,
        )

        self.track(
            event="Generation",
            user_id=user_id,
            properties={
                "$text": generation,
                "$assistant_id": assistant_id,
                "$prompt": prompt,
                "latency(ms)": latency,
                **(properties or {}),
            },
            timestamp=generation_timestamp,
        )

    def flush(self):
        """Flush the event queue."""
        events = []
        with self._lock:
            queue_len = len(self.queue)
            if queue_len and not self.is_flushing:
                self.logger.info(f"Flushing {queue_len} events.")

                self.is_flushing = True
                events = self.queue[:]
                self.queue.clear()

        if events:
            success = self._post(events)
            self.last_flush_time = datetime.now(timezone.utc)

            if not success:
                time.sleep(5)
                self.logger.info(f"Retrying flush of {queue_len} events.")

                self._post(events)

        with self._lock:
            self.is_flushing = False

    def close(self):
        """Stop the background thread and perform a final flush of the event queue."""
        self._stop_event.set()
        self._thread.join()
        self.flush()
        self.logger.info("Background thread stopped and final flush completed.")

    def _post(self, events: list[dict]):
        with requests.Session() as session:
            try:
                response = session.post(
                    f"{self.host}/publish_events",
                    headers={
                        "Content-Type": "application/json",
                        "x-api-key": self.api_key,
                    },
                    json=events,
                )
                response.raise_for_status()
                self.logger.info(f"{len(events)} events sent to Trubrics.")
                return True
            except Exception as e:
                self.logger.error(f"Error flushing {len(events)} events: {e}")
                return False

    def _periodic_flush(self):
        while not self._stop_event.is_set():
            time.sleep(1)

            queue_len = len(self.queue)
            now = datetime.now(timezone.utc)
            time_since_last_flush = (now - self.last_flush_time).total_seconds()
            if (
                queue_len >= self.flush_at
                or time_since_last_flush >= self.flush_interval
            ):
                self.flush()
