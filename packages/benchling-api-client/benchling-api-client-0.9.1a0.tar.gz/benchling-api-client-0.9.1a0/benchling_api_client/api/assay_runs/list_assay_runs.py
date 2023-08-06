from typing import Any, Dict, Optional, cast

import httpx

from ...client import Client
from ...models.assay_run_list import AssayRunList
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    schema_id: str,
    min_created_time: Optional[int] = None,
    max_created_time: Optional[int] = None,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
) -> Dict[str, Any]:
    url = "{}/assay-runs".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    params: Dict[str, Any] = {
        "schemaId": schema_id,
    }
    if min_created_time is not None:
        params["minCreatedTime"] = min_created_time
    if max_created_time is not None:
        params["maxCreatedTime"] = max_created_time
    if next_token is not None:
        params["nextToken"] = next_token
    if page_size is not None:
        params["pageSize"] = page_size

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[AssayRunList]:
    if response.status_code == 200:
        return AssayRunList.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[AssayRunList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    schema_id: str,
    min_created_time: Optional[int] = None,
    max_created_time: Optional[int] = None,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
) -> Response[AssayRunList]:
    kwargs = _get_kwargs(
        client=client,
        schema_id=schema_id,
        min_created_time=min_created_time,
        max_created_time=max_created_time,
        next_token=next_token,
        page_size=page_size,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    schema_id: str,
    min_created_time: Optional[int] = None,
    max_created_time: Optional[int] = None,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
) -> Optional[AssayRunList]:
    """  """

    return sync_detailed(
        client=client,
        schema_id=schema_id,
        min_created_time=min_created_time,
        max_created_time=max_created_time,
        next_token=next_token,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    schema_id: str,
    min_created_time: Optional[int] = None,
    max_created_time: Optional[int] = None,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
) -> Response[AssayRunList]:
    kwargs = _get_kwargs(
        client=client,
        schema_id=schema_id,
        min_created_time=min_created_time,
        max_created_time=max_created_time,
        next_token=next_token,
        page_size=page_size,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    schema_id: str,
    min_created_time: Optional[int] = None,
    max_created_time: Optional[int] = None,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
) -> Optional[AssayRunList]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            schema_id=schema_id,
            min_created_time=min_created_time,
            max_created_time=max_created_time,
            next_token=next_token,
            page_size=page_size,
        )
    ).parsed
