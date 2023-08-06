from typing import Any, Dict, List, Optional, cast

import httpx

from ...client import Client
from ...models.assay_run_list_bulk_get import AssayRunListBulkGet
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    assay_run_ids: List[str],
) -> Dict[str, Any]:
    url = "{}/assay-runs:bulk-get".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_assay_run_ids = assay_run_ids

    params: Dict[str, Any] = {
        "assayRunIds": json_assay_run_ids,
    }

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[AssayRunListBulkGet]:
    if response.status_code == 200:
        return AssayRunListBulkGet.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[AssayRunListBulkGet]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    assay_run_ids: List[str],
) -> Response[AssayRunListBulkGet]:
    kwargs = _get_kwargs(
        client=client,
        assay_run_ids=assay_run_ids,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    assay_run_ids: List[str],
) -> Optional[AssayRunListBulkGet]:
    """  """

    return sync_detailed(
        client=client,
        assay_run_ids=assay_run_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    assay_run_ids: List[str],
) -> Response[AssayRunListBulkGet]:
    kwargs = _get_kwargs(
        client=client,
        assay_run_ids=assay_run_ids,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    assay_run_ids: List[str],
) -> Optional[AssayRunListBulkGet]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            assay_run_ids=assay_run_ids,
        )
    ).parsed
