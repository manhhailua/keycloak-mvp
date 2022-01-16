from httpx import AsyncClient

keycloak_client = AsyncClient(base_url="http://localhost:9080")
