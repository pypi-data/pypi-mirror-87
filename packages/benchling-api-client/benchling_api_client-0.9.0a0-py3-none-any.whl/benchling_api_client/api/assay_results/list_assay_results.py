import datetime
from typing import Any, Dict, Optional, cast

import httpx

from ...client import Client
from ...models.assay_result_list import AssayResultList
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: Client,
    schema_id: str,
    min_created_time: Optional[datetime.datetime] = None,
    max_created_time: Optional[datetime.datetime] = None,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
    entity_ids: Optional[str] = None,
    assay_run_ids: Optional[str] = None,
) -> Dict[str, Any]:
    url = "{}/assay-results".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    if min_created_time is UNSET:
        json_min_created_time = UNSET
    else:
        json_min_created_time = min_created_time.isoformat() if min_created_time else None

    if max_created_time is UNSET:
        json_max_created_time = UNSET
    else:
        json_max_created_time = max_created_time.isoformat() if max_created_time else None

    params: Dict[str, Any] = {
        "schemaId": schema_id,
    }
    if min_created_time is not None:
        params["minCreatedTime"] = json_min_created_time
    if max_created_time is not None:
        params["maxCreatedTime"] = json_max_created_time
    if next_token is not None:
        params["nextToken"] = next_token
    if page_size is not None:
        params["pageSize"] = page_size
    if entity_ids is not None:
        params["entityIds"] = entity_ids
    if assay_run_ids is not None:
        params["assayRunIds"] = assay_run_ids

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[AssayResultList]:
    if response.status_code == 200:
        return AssayResultList.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[AssayResultList]:
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
    min_created_time: Optional[datetime.datetime] = None,
    max_created_time: Optional[datetime.datetime] = None,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
    entity_ids: Optional[str] = None,
    assay_run_ids: Optional[str] = None,
) -> Response[AssayResultList]:
    kwargs = _get_kwargs(
        client=client,
        schema_id=schema_id,
        min_created_time=min_created_time,
        max_created_time=max_created_time,
        next_token=next_token,
        page_size=page_size,
        entity_ids=entity_ids,
        assay_run_ids=assay_run_ids,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    schema_id: str,
    min_created_time: Optional[datetime.datetime] = None,
    max_created_time: Optional[datetime.datetime] = None,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
    entity_ids: Optional[str] = None,
    assay_run_ids: Optional[str] = None,
) -> Optional[AssayResultList]:
    """  """

    return sync_detailed(
        client=client,
        schema_id=schema_id,
        min_created_time=min_created_time,
        max_created_time=max_created_time,
        next_token=next_token,
        page_size=page_size,
        entity_ids=entity_ids,
        assay_run_ids=assay_run_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    schema_id: str,
    min_created_time: Optional[datetime.datetime] = None,
    max_created_time: Optional[datetime.datetime] = None,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
    entity_ids: Optional[str] = None,
    assay_run_ids: Optional[str] = None,
) -> Response[AssayResultList]:
    kwargs = _get_kwargs(
        client=client,
        schema_id=schema_id,
        min_created_time=min_created_time,
        max_created_time=max_created_time,
        next_token=next_token,
        page_size=page_size,
        entity_ids=entity_ids,
        assay_run_ids=assay_run_ids,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    schema_id: str,
    min_created_time: Optional[datetime.datetime] = None,
    max_created_time: Optional[datetime.datetime] = None,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
    entity_ids: Optional[str] = None,
    assay_run_ids: Optional[str] = None,
) -> Optional[AssayResultList]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            schema_id=schema_id,
            min_created_time=min_created_time,
            max_created_time=max_created_time,
            next_token=next_token,
            page_size=page_size,
            entity_ids=entity_ids,
            assay_run_ids=assay_run_ids,
        )
    ).parsed
