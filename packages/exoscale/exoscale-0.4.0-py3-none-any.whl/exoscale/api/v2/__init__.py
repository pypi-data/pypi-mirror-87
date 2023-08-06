#!/usr/bin/env python3
# Automatically generated file by swagger_to. DO NOT EDIT OR APPEND ANYTHING!
"""Implements the client for instance-pool."""

# pylint: skip-file
# pydocstyle: add-ignore=D105,D107,D401

import contextlib
import json
from typing import Any, BinaryIO, Dict, List, MutableMapping, Optional, cast

import requests
import requests.auth


class RemoteCaller:
    """Executes the remote calls to the server."""

    def __init__(self, url_prefix: str, auth: Optional[requests.auth.AuthBase] = None) -> None:
        self.url_prefix = url_prefix
        self.auth = auth

    def delete-load-balancer-service(
            self,
            id: str,
            service_id: str) -> bytes:
        """
        Delete a single load balancer service from a load balancer

        :param id:
        :param service_id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/load-balancer/',
            str(id),
            '/service/',
            '{',
            'service-id}'])

        resp = requests.request(
            method='delete',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def update-load-balancer-service(
            self,
            id: str,
            service_id: str) -> bytes:
        """
        Update a load balancer service name

        :param id:
        :param service_id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/load-balancer/',
            str(id),
            '/service/',
            '{',
            'service-id}'])

        resp = requests.request(
            method='put',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def get-load-balancer-service(
            self,
            id: str,
            service_id: str) -> bytes:
        """
        Show load balancer service details

        :param id:
        :param service_id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/load-balancer/',
            str(id),
            '/service/',
            '{',
            'service-id}'])

        resp = requests.request(
            method='get',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def create-snapshot(
            self,
            id: str) -> bytes:
        """
        Create a snapshot for a Compute instance

        :param id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/instance/',
            str(id),
            ':create-snapshot'])

        resp = requests.request(
            method='post',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def delete-rule-from-security-group(
            self,
            id: str,
            rule_id: str) -> bytes:
        """
        Delete rule from Security Group

        :param id:
        :param rule_id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/security-group/',
            str(id),
            '/rules/',
            '{',
            'rule-id}'])

        resp = requests.request(
            method='delete',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def create-load-balancer(self) -> bytes:
        """
        Create a new load balancer

        :return: 200
        """
        url = self.url_prefix + '/load-balancer'

        resp = requests.request(method='post', url=url, auth=self.auth)

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def list-load-balancers(self) -> bytes:
        """
        List load balancers

        :return: 200
        """
        url = self.url_prefix + '/load-balancer'

        resp = requests.request(method='get', url=url, auth=self.auth)

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def create-security-group(self) -> bytes:
        """
        Create Security Group

        :return: 200
        """
        url = self.url_prefix + '/security-group'

        resp = requests.request(method='post', url=url, auth=self.auth)

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def list-security-groups(self) -> bytes:
        """
        List Security Groups

        :return: 200
        """
        url = self.url_prefix + '/security-group'

        resp = requests.request(method='get', url=url, auth=self.auth)

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def get-instance-type(
            self,
            id: str) -> bytes:
        """
        Show instance type details

        :param id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/instance-type/',
            str(id)])

        resp = requests.request(
            method='get',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def list-zones(self) -> bytes:
        """
        List zones

        :return: 200
        """
        url = self.url_prefix + '/zone'

        resp = requests.request(method='get', url=url, auth=self.auth)

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def list-instance-pools(self) -> bytes:
        """
        List Instance Pools

        :return: 200
        """
        url = self.url_prefix + '/instance-pool'

        resp = requests.request(method='get', url=url, auth=self.auth)

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def create-instance-pool(self) -> bytes:
        """
        Create an Instance Pool

        :return: 200
        """
        url = self.url_prefix + '/instance-pool'

        resp = requests.request(method='post', url=url, auth=self.auth)

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def list-instance-types(self) -> bytes:
        """
        List Compute instance types

        :return: 200
        """
        url = self.url_prefix + '/instance-type'

        resp = requests.request(method='get', url=url, auth=self.auth)

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def delete-instance-pool(
            self,
            id: str) -> bytes:
        """
        Delete an Instance Pool

        :param id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/instance-pool/',
            str(id)])

        resp = requests.request(
            method='delete',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def get-instance-pool(
            self,
            id: str) -> bytes:
        """
        Retrieve an Instance Pool's details

        :param id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/instance-pool/',
            str(id)])

        resp = requests.request(
            method='get',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def update-instance-pool(
            self,
            id: str) -> bytes:
        """
        Update an Instance Pool

        :param id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/instance-pool/',
            str(id)])

        resp = requests.request(
            method='put',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def delete-cdn-configuration(
            self,
            bucket: str) -> bytes:
        """
        Delete a CDN configuration

        :param bucket:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/cdn-configuration/',
            str(bucket)])

        resp = requests.request(
            method='delete',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def get-security-group(
            self,
            id: str) -> bytes:
        """
        Show Compute security group details

        :param id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/security-group/',
            str(id)])

        resp = requests.request(
            method='get',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def delete-security-group(
            self,
            id: str) -> bytes:
        """
        Delete Security Group

        :param id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/security-group/',
            str(id)])

        resp = requests.request(
            method='delete',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def ping(self) -> bytes:
        """
        Ping

        :return: 200
        """
        url = self.url_prefix + '/ping'

        resp = requests.request(method='get', url=url, auth=self.auth)

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def get-export-snapshot(
            self,
            id: str) -> bytes:
        """
        Gets the snapshot export result. The snapshot must already be exported. Returns transient data.

        :param id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/snapshot/',
            str(id),
            ':export'])

        resp = requests.request(
            method='get',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def export-snapshot(
            self,
            id: str) -> bytes:
        """
        Export snapshot

        :param id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/snapshot/',
            str(id),
            ':export'])

        resp = requests.request(
            method='post',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def delete-snapshot(
            self,
            id: str) -> bytes:
        """
        Delete snapshot

        :param id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/snapshot/',
            str(id)])

        resp = requests.request(
            method='delete',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def get-snapshot(
            self,
            id: str) -> bytes:
        """
        Show compute snapshot details

        :param id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/snapshot/',
            str(id)])

        resp = requests.request(
            method='get',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def add-rule-to-security-group(
            self,
            id: str) -> bytes:
        """
        Create rule in Security Group

        :param id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/security-group/',
            str(id),
            '/rules'])

        resp = requests.request(
            method='post',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def list-snapshots(self) -> bytes:
        """
        List snapshots

        :return: 200
        """
        url = self.url_prefix + '/snapshot'

        resp = requests.request(method='get', url=url, auth=self.auth)

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def get-operation(
            self,
            id: str) -> bytes:
        """
        Lookup operation status by ID

        :param id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/operation/',
            str(id)])

        resp = requests.request(
            method='get',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def get-template(
            self,
            id: str) -> bytes:
        """
        Show template details

        :param id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/template/',
            str(id)])

        resp = requests.request(
            method='get',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def evict-instance-pool-members(
            self,
            id: str) -> bytes:
        """
        Shrink an Instance Pool by evicting specific members

        :param id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/instance-pool/',
            str(id),
            ':evict'])

        resp = requests.request(
            method='post',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def add-service-to-load-balancer(
            self,
            id: str) -> bytes:
        """
        Add a single service to a load balancer

        :param id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/load-balancer/',
            str(id),
            '/service'])

        resp = requests.request(
            method='post',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def list-cdn-configurations(self) -> bytes:
        """
        List CDN configurations

        :return: 200
        """
        url = self.url_prefix + '/cdn-configuration'

        resp = requests.request(method='get', url=url, auth=self.auth)

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def create-cdn-configuration(self) -> bytes:
        """
        Create a new CDN configuration

        :return: 200
        """
        url = self.url_prefix + '/cdn-configuration'

        resp = requests.request(method='post', url=url, auth=self.auth)

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def update-load-balancer(
            self,
            id: str) -> bytes:
        """
        Update a load balancer

        :param id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/load-balancer/',
            str(id)])

        resp = requests.request(
            method='put',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def delete-load-balancer(
            self,
            id: str) -> bytes:
        """
        Delete a load balancer

        :param id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/load-balancer/',
            str(id)])

        resp = requests.request(
            method='delete',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def get-load-balancer(
            self,
            id: str) -> bytes:
        """
        Show load balancer details

        :param id:

        :return: 200
        """
        url = "".join([
            self.url_prefix,
            '/load-balancer/',
            str(id)])

        resp = requests.request(
            method='get',
            url=url,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def version(self) -> bytes:
        """
        Version

        :return: 200
        """
        url = self.url_prefix + '/version'

        resp = requests.request(method='get', url=url, auth=self.auth)

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def create-instance(
            self,
            start: Optional[bool] = None) -> bytes:
        """
        Create Compute instance

        :param start:

        :return: 200
        """
        url = self.url_prefix + '/instance'

        params = {}  # type: Dict[str, str]

        if start is not None:
            params['start'] = json.dumps(start)

        resp = requests.request(
            method='post',
            url=url,
            params=params,
            auth=self.auth,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content


# Automatically generated file by swagger_to. DO NOT EDIT OR APPEND ANYTHING!
