from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.dna_sequence_list import DnaSequenceList
from ...models.sort import Sort
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: Client,
    page_size: Optional[int] = 50,
    next_token: Optional[str] = None,
    sort: Optional[Sort] = Sort.MODIFIEDATDESC,
    modified_at: Optional[str] = None,
    name: Optional[str] = None,
    bases: Optional[str] = None,
    folder_id: Optional[str] = None,
    mentioned_in: Optional[List[str]] = None,
    project_id: Optional[str] = None,
    registry_id: Optional[str] = None,
    schema_id: Optional[str] = None,
    archive_reason: Optional[str] = None,
    mentions: Optional[List[str]] = None,
    ids: Optional[str] = None,
) -> Dict[str, Any]:
    url = "{}/dna-sequences".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    if sort is UNSET:
        json_sort = UNSET
    else:
        json_sort = sort.value if sort else None

    if mentioned_in is None:
        json_mentioned_in = None
    elif mentioned_in is UNSET:
        json_mentioned_in = UNSET
    else:
        json_mentioned_in = mentioned_in

    if mentions is None:
        json_mentions = None
    elif mentions is UNSET:
        json_mentions = UNSET
    else:
        json_mentions = mentions

    params: Dict[str, Any] = {}
    if page_size is not None:
        params["pageSize"] = page_size
    if next_token is not None:
        params["nextToken"] = next_token
    if sort is not None:
        params["sort"] = json_sort
    if modified_at is not None:
        params["modifiedAt"] = modified_at
    if name is not None:
        params["name"] = name
    if bases is not None:
        params["bases"] = bases
    if folder_id is not None:
        params["folderId"] = folder_id
    if mentioned_in is not None:
        params["mentionedIn"] = json_mentioned_in
    if project_id is not None:
        params["projectId"] = project_id
    if registry_id is not None:
        params["registryId"] = registry_id
    if schema_id is not None:
        params["schemaId"] = schema_id
    if archive_reason is not None:
        params["archiveReason"] = archive_reason
    if mentions is not None:
        params["mentions"] = json_mentions
    if ids is not None:
        params["ids"] = ids

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[DnaSequenceList, BadRequestError]]:
    if response.status_code == 200:
        return DnaSequenceList.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[DnaSequenceList, BadRequestError]]:
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
    sort: Optional[Sort] = Sort.MODIFIEDATDESC,
    modified_at: Optional[str] = None,
    name: Optional[str] = None,
    bases: Optional[str] = None,
    folder_id: Optional[str] = None,
    mentioned_in: Optional[List[str]] = None,
    project_id: Optional[str] = None,
    registry_id: Optional[str] = None,
    schema_id: Optional[str] = None,
    archive_reason: Optional[str] = None,
    mentions: Optional[List[str]] = None,
    ids: Optional[str] = None,
) -> Response[Union[DnaSequenceList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        bases=bases,
        folder_id=folder_id,
        mentioned_in=mentioned_in,
        project_id=project_id,
        registry_id=registry_id,
        schema_id=schema_id,
        archive_reason=archive_reason,
        mentions=mentions,
        ids=ids,
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
    sort: Optional[Sort] = Sort.MODIFIEDATDESC,
    modified_at: Optional[str] = None,
    name: Optional[str] = None,
    bases: Optional[str] = None,
    folder_id: Optional[str] = None,
    mentioned_in: Optional[List[str]] = None,
    project_id: Optional[str] = None,
    registry_id: Optional[str] = None,
    schema_id: Optional[str] = None,
    archive_reason: Optional[str] = None,
    mentions: Optional[List[str]] = None,
    ids: Optional[str] = None,
) -> Optional[Union[DnaSequenceList, BadRequestError]]:
    """ List DNA sequences """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        bases=bases,
        folder_id=folder_id,
        mentioned_in=mentioned_in,
        project_id=project_id,
        registry_id=registry_id,
        schema_id=schema_id,
        archive_reason=archive_reason,
        mentions=mentions,
        ids=ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Optional[int] = 50,
    next_token: Optional[str] = None,
    sort: Optional[Sort] = Sort.MODIFIEDATDESC,
    modified_at: Optional[str] = None,
    name: Optional[str] = None,
    bases: Optional[str] = None,
    folder_id: Optional[str] = None,
    mentioned_in: Optional[List[str]] = None,
    project_id: Optional[str] = None,
    registry_id: Optional[str] = None,
    schema_id: Optional[str] = None,
    archive_reason: Optional[str] = None,
    mentions: Optional[List[str]] = None,
    ids: Optional[str] = None,
) -> Response[Union[DnaSequenceList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        bases=bases,
        folder_id=folder_id,
        mentioned_in=mentioned_in,
        project_id=project_id,
        registry_id=registry_id,
        schema_id=schema_id,
        archive_reason=archive_reason,
        mentions=mentions,
        ids=ids,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    page_size: Optional[int] = 50,
    next_token: Optional[str] = None,
    sort: Optional[Sort] = Sort.MODIFIEDATDESC,
    modified_at: Optional[str] = None,
    name: Optional[str] = None,
    bases: Optional[str] = None,
    folder_id: Optional[str] = None,
    mentioned_in: Optional[List[str]] = None,
    project_id: Optional[str] = None,
    registry_id: Optional[str] = None,
    schema_id: Optional[str] = None,
    archive_reason: Optional[str] = None,
    mentions: Optional[List[str]] = None,
    ids: Optional[str] = None,
) -> Optional[Union[DnaSequenceList, BadRequestError]]:
    """ List DNA sequences """

    return (
        await asyncio_detailed(
            client=client,
            page_size=page_size,
            next_token=next_token,
            sort=sort,
            modified_at=modified_at,
            name=name,
            bases=bases,
            folder_id=folder_id,
            mentioned_in=mentioned_in,
            project_id=project_id,
            registry_id=registry_id,
            schema_id=schema_id,
            archive_reason=archive_reason,
            mentions=mentions,
            ids=ids,
        )
    ).parsed
