class HealthCheckService:
    async def status(self):
        return {"status": "ok"}
