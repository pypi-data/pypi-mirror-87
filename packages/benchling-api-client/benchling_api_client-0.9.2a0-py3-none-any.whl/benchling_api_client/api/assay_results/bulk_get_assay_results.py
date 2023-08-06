from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.assay_result_bulk_get import AssayResultBulkGet
from ...models.bad_request_error import BadRequestError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    assay_result_ids: str,
) -> Dict[str, Any]:
    url = "{}/assay-results:bulk-get".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    params: Dict[str, Any] = {
        "assayResultIds": assay_result_ids,
    }

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[AssayResultBulkGet, BadRequestError]]:
    if response.status_code == 200:
        return AssayResultBulkGet.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[AssayResultBulkGet, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    assay_result_ids: str,
) -> Response[Union[AssayResultBulkGet, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        assay_result_ids=assay_result_ids,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    assay_result_ids: str,
) -> Optional[Union[AssayResultBulkGet, BadRequestError]]:
    """ Up to 200 IDs can be specified at once. """

    return sync_detailed(
        client=client,
        assay_result_ids=assay_result_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    assay_result_ids: str,
) -> Response[Union[AssayResultBulkGet, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        assay_result_ids=assay_result_ids,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    assay_result_ids: str,
) -> Optional[Union[AssayResultBulkGet, BadRequestError]]:
    """ Up to 200 IDs can be specified at once. """

    return (
        await asyncio_detailed(
            client=client,
            assay_result_ids=assay_result_ids,
        )
    ).parsed
