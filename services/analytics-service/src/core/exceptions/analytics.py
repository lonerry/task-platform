class AnalyticsServiceError(Exception):
    """Базовое исключение для Analytics Service"""
    pass


class DatabaseError(AnalyticsServiceError):
    message: str

    def __init__(self, detail: str) -> None:
        self.message = detail
        super().__init__(detail)


class KafkaConsumerError(AnalyticsServiceError):
    message: str

    def __init__(self, detail: str) -> None:
        self.message = detail
        super().__init__(detail)


class MessageParsingError(AnalyticsServiceError):
    message: str

    def __init__(self, message_content: str, error: str) -> None:
        self.message = f"Failed to parse message: {message_content}. Error: {error}"
        super().__init__(self.message)


class StatsUpdateError(AnalyticsServiceError):
    message: str

    def __init__(self, status: str, error: str) -> None:
        self.message = f"Failed to update stats for status '{status}': {error}"
        super().__init__(self.message)

