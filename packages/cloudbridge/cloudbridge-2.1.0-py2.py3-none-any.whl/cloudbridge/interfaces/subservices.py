from abc import ABCMeta
from abc import abstractmethod

from cloudbridge.interfaces.resources import PageableObjectMixin


class BucketObjectSubService(PageableObjectMixin):
    """
    A container service for objects within a bucket.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, name):
        """
        Retrieve a given object from this bucket.

        :type name: ``str``
        :param name: The identifier of the object to retrieve

        :rtype: :class:``.BucketObject``
        :return: The BucketObject or ``None`` if it cannot be found.
        """
        pass

    @abstractmethod
    # pylint:disable=arguments-differ
    def list(self, limit=None, marker=None, prefix=None):
        """
        List objects in this bucket.

        :type limit: ``int``
        :param limit: Maximum number of elements to return.

        :type marker: ``int``
        :param marker: Fetch results after this offset.

        :type prefix: ``str``
        :param prefix: Prefix criteria by which to filter listed objects.

        :rtype: List of ``objects`` of :class:``.BucketObject``
        :return: List of all available BucketObjects within this bucket.
        """
        pass

    @abstractmethod
    def find(self, **kwargs):
        """
        Search for an object by a given list of attributes.

        Supported attributes: ``name``

        :rtype: List of ``objects`` of :class:`.BucketObject`
        :return: A list of BucketObjects matching the supplied attributes.

        :type limit: ``int``
        :param limit: Maximum number of elements to return.

        :type marker: ``int``
        :param marker: Fetch results after this offset.
        """
        pass

    @abstractmethod
    def create(self, name):
        """
        Create a new object within this bucket.

        :rtype: :class:``.BucketObject``
        :return: The newly created bucket object
        """
        pass


class GatewaySubService(PageableObjectMixin):
    """
    Manage internet gateway resources.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_or_create(self):
        """
        Creates new or returns an existing internet gateway for a network.

        The returned gateway object can subsequently be attached to a router to
        provide internet routing to a network.

        :rtype: ``object``  of :class:`.InternetGateway` or ``None``
        :return: an InternetGateway object of ``None`` if not found.
        """
        pass

    @abstractmethod
    def delete(self, gateway):
        """
        Delete a gateway.

        :type gateway: :class:`.Gateway` object
        :param gateway: Gateway object to delete.
        """
        pass

    @abstractmethod
    def list(self, limit=None, marker=None):
        """
        List all available internet gateways.

        :rtype: ``list`` of :class:`.InternetGateway` or ``None``
        :return: Current list of internet gateways.
        """
        pass


class FloatingIPSubService(PageableObjectMixin):
    """
    Base interface for a FloatingIP Service.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, fip_id):
        """
        Returns a FloatingIP given its ID or ``None`` if not found.

        :type fip_id: ``str``
        :param fip_id: The ID of the FloatingIP to retrieve.

        :rtype: ``object`` of :class:`.FloatingIP`
        :return: a FloatingIP object
        """
        pass

    @abstractmethod
    def list(self, limit=None, marker=None):
        """
        List floating (i.e., static) IP addresses.

        :rtype: ``list`` of :class:`.FloatingIP`
        :return: list of FloatingIP objects
        """
        pass

    @abstractmethod
    def find(self, **kwargs):
        """
        Searches for a FloatingIP by a given list of attributes.

        Supported attributes: name, public_ip

        Example:

        .. code-block:: python

            fip = provider.networking.gateways.get('id').floating_ips.find(
                        public_ip='public_ip')


        :rtype: List of ``object`` of :class:`.FloatingIP`
        :return: A list of FloatingIP objects matching the supplied attributes.
        """
        pass

    @abstractmethod
    def create(self):
        """
        Allocate a new floating (i.e., static) IP address.

        :rtype: ``object`` of :class:`.FloatingIP`
        :return:  A FloatingIP object
        """
        pass

    @abstractmethod
    def delete(self, fip_id):
        """
        Delete an existing FloatingIP.

        :type fip_id: ``str``
        :param fip_id: The ID of the FloatingIP to be deleted.
        """
        pass


class VMFirewallRuleSubService(PageableObjectMixin):
    """
    Base interface for Firewall rules.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, rule_id):
        """
        Return a firewall rule given its ID.

        Returns ``None`` if the rule does not exist.

        Example:

        .. code-block:: python

            fw = provider.security.vm_firewalls.get('my_fw_id')
            rule = fw.rules.get('rule_id')
            print(rule.id, rule.label)

        :type rule_id: str
        :param rule_id: The ID of the desired firewall rule

        :rtype: :class:`.FirewallRule`
        :return:  a FirewallRule instance
        """
        pass

    @abstractmethod
    def list(self, limit=None, marker=None):
        """
        List all firewall rules associated with this firewall.

        :rtype: ``list`` of :class:`.FirewallRule`
        :return:  list of Firewall rule objects
        """
        pass

    @abstractmethod
    def create(self, direction, protocol=None, from_port=None,
               to_port=None, cidr=None, src_dest_fw=None):
        """
        Create a VM firewall rule.

        If a matching rule already exists, return it.

        Example:

        .. code-block:: python
            from cloudbridge.interfaces.resources import TrafficDirection
            from cloudbridge.interfaces.resources import BaseNetwork

            fw = provider.security.vm_firewalls.get('my_fw_id')
            fw.rules.create(TrafficDirection.INBOUND, protocol='tcp',
                            from_port=80, to_port=80,
                            cidr=BaseNetwork.CB_DEFAULT_IPV4RANGE)
            fw.rules.create(TrafficDirection.INBOUND, src_dest_fw=fw)
            fw.rules.create(TrafficDirection.OUTBOUND, src_dest_fw=fw)

        You need to pass in either ``src_dest_fw`` OR ``protocol`` AND
        ``from_port``, ``to_port``, ``cidr``. In other words, either
        you are authorizing another group or you are authorizing some
        IP-based rule.

        :type direction: :class:``.TrafficDirection``
        :param direction: Either ``TrafficDirection.INBOUND`` |
                          ``TrafficDirection.OUTBOUND``

        :type protocol: ``str``
        :param protocol: Either ``tcp`` | ``udp`` | ``icmp``.

        :type from_port: ``int``
        :param from_port: The beginning port number you are enabling.

        :type to_port: ``int``
        :param to_port: The ending port number you are enabling.

        :type cidr: ``str`` or list of ``str``
        :param cidr: The CIDR block you are providing access to.

        :type src_dest_fw: :class:`.VMFirewall`
        :param src_dest_fw: The VM firewall object which is the
                            source/destination of the traffic, depending on
                            whether it's ingress/egress traffic.

        :rtype: :class:`.VMFirewallRule`
        :return: Rule object if successful or ``None``.
        """
        pass

    @abstractmethod
    def find(self, **kwargs):
        """
        Find a firewall rule filtered by the given parameters.

        :type label: str
        :param label: The label of the VM firewall to retrieve.

        :type protocol: ``str``
        :param protocol: Either ``tcp`` | ``udp`` | ``icmp``.

        :type from_port: ``int``
        :param from_port: The beginning port number you are enabling.

        :type to_port: ``int``
        :param to_port: The ending port number you are enabling.

        :type cidr: ``str`` or list of ``str``
        :param cidr: The CIDR block you are providing access to.

        :type src_dest_fw: :class:`.VMFirewall`
        :param src_dest_fw: The VM firewall object which is the
                            source/destination of the traffic, depending on
                            whether it's ingress/egress traffic.

        :type src_dest_fw_id: :class:`.str`
        :param src_dest_fw_id: The VM firewall id which is the
                               source/destination of the traffic, depending on
                               whether it's ingress/egress traffic.

        :rtype: list of :class:`VMFirewallRule`
        :return: A list of VMFirewall objects or an empty list if none
                 found.
        """
        pass

    @abstractmethod
    def delete(self, rule_id):
        """
        Delete an existing VMFirewall rule.

        :type rule_id: str
        :param rule_id: The VM firewall rule to be deleted.
        """
        pass


class SubnetSubService(PageableObjectMixin):
    """
    Base interface for a Subnet Service.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, subnet_id):
        """
        Returns a Subnet given its ID or ``None`` if not found.

        :type subnet_id: ``str``
        :param subnet_id: The ID of the Subnet to retrieve.

        :rtype: ``object`` of :class:`.Subnet`
        :return: a Subnet object
        """
        pass

    @abstractmethod
    def list(self, limit=None, marker=None):
        """
        List subnets within the network holding this subservice.

        :rtype: ``list`` of :class:`.Subnet`
        :return: list of Subnet objects
        """
        pass

    @abstractmethod
    def find(self, **kwargs):
        """
        Searches for a Subnet by a given list of attributes.

        Supported attributes: label

        Example:

        .. code-block:: python

            subnet = provider.networking.networks.get('id').subnets.find(
                        label='my-subnet')


        :rtype: List of ``object`` of :class:`.Subnet`
        :return: A list of Subnet objects matching the supplied attributes.
        """
        pass

    @abstractmethod
    def create(self, label, cidr_block):
        """
        Create a new subnet within the network holding this subservice.

        :type label: ``str``
        :param label: The subnet label.

        :type cidr_block: ``str``
        :param cidr_block: CIDR block within the Network to assign to the
                           subnet.

        :rtype: ``object`` of :class:`.Subnet`
        :return:  A Subnet object
        """
        pass

    @abstractmethod
    def delete(self, subnet_id):
        """
        Delete an existing Subnet.

        :type subnet_id: ``str``
        :param subnet_id: The ID of the Subnet to be deleted.
        """
        pass


class DnsRecordSubService(PageableObjectMixin):
    """
    Base interface for a Dns Record Service.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, record_id):
        """
        Returns a Dns Record given its ID or ``None`` if not found.

        :type record_id: ``str``
        :param record_id: The ID of the DnsRecord to retrieve.

        :rtype: ``object`` of :class:`.DnsRecord`
        :return: a DnsRecord object
        """
        pass

    @abstractmethod
    def list(self, limit=None, marker=None):
        """
        List Dns Records within the Dns Zone holding this subservice.

        :rtype: ``list`` of :class:`.DnsRecord`
        :return: list of DnsRecord objects
        """
        pass

    @abstractmethod
    def find(self, **kwargs):
        """
        Searches for a DnsRecord by a given list of attributes.

        Supported attributes: label

        Example:

        .. code-block:: python

            subnet = provider.networking.dns.host_zones.get('id').records.find(
                        label='my-label')


        :rtype: List of ``object`` of :class:`.DnsRecord`
        :return: A list of DnsRecord objects matching the supplied attributes.
        """
        pass

    @abstractmethod
    def create(self, label, type, data, ttl=None):
        """
        Create a new DnsRecord within the Dns Zone holding this subservice.

        :type label: ``str``
        :param label: The record label.

        :type type: ``str``
        :param type: The DnsRecord type. (e.g. A, CNAME, MX etc)

        :type data: ``str``
        :param data: The corresponding value for the record.

        :type data: ``int``
        :param data: The ttl (in seconds) for thisrecord.

        :rtype: ``object`` of :class:`.DnsRecord`
        :return:  A DnsRecord object
        """
        pass

    @abstractmethod
    def delete(self, record_id):
        """
        Delete an existing DnsRecord.

        :type record_id: ``str``
        :param record_id: The ID of the DnsRecord to be deleted.
        """
        pass
