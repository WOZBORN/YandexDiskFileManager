import aiohttp
from flask import current_app
from typing import Any, Dict


class YandexDiskAPI:
    """Класс для взаимодействия с API Яндекс Диска."""

    @staticmethod
    async def get_files(public_key: str, path: str = "/") -> Dict[str, Any]:
        """
        Получение списка файлов с Яндекс.Диска по публичному ключу.

        Args:
            public_key (str): Публичный ключ ресурса на Яндекс.Диске.
            path (str): Путь к файлу или папке внутри общего ресурса (по умолчанию — корень).

        Returns:
            Dict[str, Any]: JSON-ответ от API, содержащий список файлов и метаданные.

        Raises:
            Exception: Если API возвращает ошибочный статус.
        """
        base_url = current_app.config['YANDEX_API_BASE_URL']
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"OAuth {current_app.config['YANDEX_OAUTH_TOKEN']}",
        }
        params = {
            "public_key": public_key,
            "path": path,  # Указываем путь
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, headers=headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_message = await response.text()
                    raise Exception(f"Ошибка API: {response.status} - {error_message}")
