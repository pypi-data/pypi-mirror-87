# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pulpcore.client.pulp_npm.configuration import Configuration


class RepositoryVersionResponse(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'pulp_href': 'str',
        'pulp_created': 'datetime',
        'number': 'int',
        'base_version': 'str',
        'content_summary': 'ContentSummaryResponse'
    }

    attribute_map = {
        'pulp_href': 'pulp_href',
        'pulp_created': 'pulp_created',
        'number': 'number',
        'base_version': 'base_version',
        'content_summary': 'content_summary'
    }

    def __init__(self, pulp_href=None, pulp_created=None, number=None, base_version=None, content_summary=None, local_vars_configuration=None):  # noqa: E501
        """RepositoryVersionResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._pulp_href = None
        self._pulp_created = None
        self._number = None
        self._base_version = None
        self._content_summary = None
        self.discriminator = None

        if pulp_href is not None:
            self.pulp_href = pulp_href
        if pulp_created is not None:
            self.pulp_created = pulp_created
        if number is not None:
            self.number = number
        if base_version is not None:
            self.base_version = base_version
        if content_summary is not None:
            self.content_summary = content_summary

    @property
    def pulp_href(self):
        """Gets the pulp_href of this RepositoryVersionResponse.  # noqa: E501


        :return: The pulp_href of this RepositoryVersionResponse.  # noqa: E501
        :rtype: str
        """
        return self._pulp_href

    @pulp_href.setter
    def pulp_href(self, pulp_href):
        """Sets the pulp_href of this RepositoryVersionResponse.


        :param pulp_href: The pulp_href of this RepositoryVersionResponse.  # noqa: E501
        :type: str
        """

        self._pulp_href = pulp_href

    @property
    def pulp_created(self):
        """Gets the pulp_created of this RepositoryVersionResponse.  # noqa: E501

        Timestamp of creation.  # noqa: E501

        :return: The pulp_created of this RepositoryVersionResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._pulp_created

    @pulp_created.setter
    def pulp_created(self, pulp_created):
        """Sets the pulp_created of this RepositoryVersionResponse.

        Timestamp of creation.  # noqa: E501

        :param pulp_created: The pulp_created of this RepositoryVersionResponse.  # noqa: E501
        :type: datetime
        """

        self._pulp_created = pulp_created

    @property
    def number(self):
        """Gets the number of this RepositoryVersionResponse.  # noqa: E501


        :return: The number of this RepositoryVersionResponse.  # noqa: E501
        :rtype: int
        """
        return self._number

    @number.setter
    def number(self, number):
        """Sets the number of this RepositoryVersionResponse.


        :param number: The number of this RepositoryVersionResponse.  # noqa: E501
        :type: int
        """

        self._number = number

    @property
    def base_version(self):
        """Gets the base_version of this RepositoryVersionResponse.  # noqa: E501

        A repository version whose content was used as the initial set of content for this repository version  # noqa: E501

        :return: The base_version of this RepositoryVersionResponse.  # noqa: E501
        :rtype: str
        """
        return self._base_version

    @base_version.setter
    def base_version(self, base_version):
        """Sets the base_version of this RepositoryVersionResponse.

        A repository version whose content was used as the initial set of content for this repository version  # noqa: E501

        :param base_version: The base_version of this RepositoryVersionResponse.  # noqa: E501
        :type: str
        """

        self._base_version = base_version

    @property
    def content_summary(self):
        """Gets the content_summary of this RepositoryVersionResponse.  # noqa: E501

        Various count summaries of the content in the version and the HREF to view them.  # noqa: E501

        :return: The content_summary of this RepositoryVersionResponse.  # noqa: E501
        :rtype: ContentSummaryResponse
        """
        return self._content_summary

    @content_summary.setter
    def content_summary(self, content_summary):
        """Sets the content_summary of this RepositoryVersionResponse.

        Various count summaries of the content in the version and the HREF to view them.  # noqa: E501

        :param content_summary: The content_summary of this RepositoryVersionResponse.  # noqa: E501
        :type: ContentSummaryResponse
        """

        self._content_summary = content_summary

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RepositoryVersionResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RepositoryVersionResponse):
            return True

        return self.to_dict() != other.to_dict()
