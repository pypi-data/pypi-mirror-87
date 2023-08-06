from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.plate_list import PlateList
from ...models.sort12 import Sort12
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: Client,
    page_size: Optional[int] = 50,
    next_token: Optional[str] = None,
    sort: Optional[Sort12] = Sort12.MODIFIEDATDESC,
    schema_id: Optional[str] = None,
    modified_at: Optional[str] = None,
    name: Optional[str] = None,
    name_includes: Optional[str] = None,
    ancestor_storage_id: Optional[str] = None,
    storage_contents_id: Optional[str] = None,
    storage_contents_ids: Optional[List[str]] = None,
    archive_reason: Optional[str] = None,
    ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Dict[str, Any]:
    url = "{}/plates".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    if sort is UNSET:
        json_sort = UNSET
    else:
        json_sort = sort.value if sort else None

    if storage_contents_ids is None:
        json_storage_contents_ids = None
    elif storage_contents_ids is UNSET:
        json_storage_contents_ids = UNSET
    else:
        json_storage_contents_ids = storage_contents_ids

    params: Dict[str, Any] = {}
    if page_size is not None:
        params["pageSize"] = page_size
    if next_token is not None:
        params["nextToken"] = next_token
    if sort is not None:
        params["sort"] = json_sort
    if schema_id is not None:
        params["schemaId"] = schema_id
    if modified_at is not None:
        params["modifiedAt"] = modified_at
    if name is not None:
        params["name"] = name
    if name_includes is not None:
        params["nameIncludes"] = name_includes
    if ancestor_storage_id is not None:
        params["ancestorStorageId"] = ancestor_storage_id
    if storage_contents_id is not None:
        params["storageContentsId"] = storage_contents_id
    if storage_contents_ids is not None:
        params["storageContentsIds"] = json_storage_contents_ids
    if archive_reason is not None:
        params["archiveReason"] = archive_reason
    if ids is not None:
        params["ids"] = ids
    if barcodes is not None:
        params["barcodes"] = barcodes

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[PlateList, BadRequestError]]:
    if response.status_code == 200:
        return PlateList.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[PlateList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    page_size: Optional[int] = 50,
    next_token: Optional[str] = None,
    sort: Optional[Sort12] = Sort12.MODIFIEDATDESC,
    schema_id: Optional[str] = None,
    modified_at: Optional[str] = None,
    name: Optional[str] = None,
    name_includes: Optional[str] = None,
    ancestor_storage_id: Optional[str] = None,
    storage_contents_id: Optional[str] = None,
    storage_contents_ids: Optional[List[str]] = None,
    archive_reason: Optional[str] = None,
    ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Response[Union[PlateList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        schema_id=schema_id,
        modified_at=modified_at,
        name=name,
        name_includes=name_includes,
        ancestor_storage_id=ancestor_storage_id,
        storage_contents_id=storage_contents_id,
        storage_contents_ids=storage_contents_ids,
        archive_reason=archive_reason,
        ids=ids,
        barcodes=barcodes,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    page_size: Optional[int] = 50,
    next_token: Optional[str] = None,
    sort: Optional[Sort12] = Sort12.MODIFIEDATDESC,
    schema_id: Optional[str] = None,
    modified_at: Optional[str] = None,
    name: Optional[str] = None,
    name_includes: Optional[str] = None,
    ancestor_storage_id: Optional[str] = None,
    storage_contents_id: Optional[str] = None,
    storage_contents_ids: Optional[List[str]] = None,
    archive_reason: Optional[str] = None,
    ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Optional[Union[PlateList, BadRequestError]]:
    """ List plates """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        schema_id=schema_id,
        modified_at=modified_at,
        name=name,
        name_includes=name_includes,
        ancestor_storage_id=ancestor_storage_id,
        storage_contents_id=storage_contents_id,
        storage_contents_ids=storage_contents_ids,
        archive_reason=archive_reason,
        ids=ids,
        barcodes=barcodes,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Optional[int] = 50,
    next_token: Optional[str] = None,
    sort: Optional[Sort12] = Sort12.MODIFIEDATDESC,
    schema_id: Optional[str] = None,
    modified_at: Optional[str] = None,
    name: Optional[str] = None,
    name_includes: Optional[str] = None,
    ancestor_storage_id: Optional[str] = None,
    storage_contents_id: Optional[str] = None,
    storage_contents_ids: Optional[List[str]] = None,
    archive_reason: Optional[str] = None,
    ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Response[Union[PlateList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        schema_id=schema_id,
        modified_at=modified_at,
        name=name,
        name_includes=name_includes,
        ancestor_storage_id=ancestor_storage_id,
        storage_contents_id=storage_contents_id,
        storage_contents_ids=storage_contents_ids,
        archive_reason=archive_reason,
        ids=ids,
        barcodes=barcodes,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    page_size: Optional[int] = 50,
    next_token: Optional[str] = None,
    sort: Optional[Sort12] = Sort12.MODIFIEDATDESC,
    schema_id: Optional[str] = None,
    modified_at: Optional[str] = None,
    name: Optional[str] = None,
    name_includes: Optional[str] = None,
    ancestor_storage_id: Optional[str] = None,
    storage_contents_id: Optional[str] = None,
    storage_contents_ids: Optional[List[str]] = None,
    archive_reason: Optional[str] = None,
    ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Optional[Union[PlateList, BadRequestError]]:
    """ List plates """

    return (
        await asyncio_detailed(
            client=client,
            page_size=page_size,
            next_token=next_token,
            sort=sort,
            schema_id=schema_id,
            modified_at=modified_at,
            name=name,
            name_includes=name_includes,
            ancestor_storage_id=ancestor_storage_id,
            storage_contents_id=storage_contents_id,
            storage_contents_ids=storage_contents_ids,
            archive_reason=archive_reason,
            ids=ids,
            barcodes=barcodes,
        )
    ).parsed
