from typing import Any, Dict, Optional, cast

import httpx

from ...client import Client
from ...models.entry_external_file import EntryExternalFile
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    entry_id: str,
    external_file_id: str,
) -> Dict[str, Any]:
    url = "{}/entries/{entry_id}/external-files/{external_file_id}".format(
        client.base_url, entry_id=entry_id, external_file_id=external_file_id
    )

    headers: Dict[str, Any] = client.get_headers()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[EntryExternalFile]:
    if response.status_code == 200:
        return EntryExternalFile.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[EntryExternalFile]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    entry_id: str,
    external_file_id: str,
) -> Response[EntryExternalFile]:
    kwargs = _get_kwargs(
        client=client,
        entry_id=entry_id,
        external_file_id=external_file_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    entry_id: str,
    external_file_id: str,
) -> Optional[EntryExternalFile]:
    """Retrieves the metadata for an external file. Use the 'downloadURL' to download the actual file. (See ExternalFile Resource for details.)"""

    return sync_detailed(
        client=client,
        entry_id=entry_id,
        external_file_id=external_file_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    entry_id: str,
    external_file_id: str,
) -> Response[EntryExternalFile]:
    kwargs = _get_kwargs(
        client=client,
        entry_id=entry_id,
        external_file_id=external_file_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    entry_id: str,
    external_file_id: str,
) -> Optional[EntryExternalFile]:
    """Retrieves the metadata for an external file. Use the 'downloadURL' to download the actual file. (See ExternalFile Resource for details.)"""

    return (
        await asyncio_detailed(
            client=client,
            entry_id=entry_id,
            external_file_id=external_file_id,
        )
    ).parsed
