from ipaddress import AddressValueError, ip_address
from scripts.utils.network import is_valid_hostname
import click
import socket


class HostOrIPAddress(click.ParamType):
    name = "string"

    def convert(self, value, param, ctx):
        try:
            ip = ip_address(value)
            return ip
        except AddressValueError:
            if is_valid_hostname(value):
                ip = socket.gethostbyname(value)
                return ip
            else:
                self.fail("%s is not a valid hostname or IP address" % repr(value), param, ctx)
        except TypeError:
            self.fail(
                "expected string for conversion, got "
                "%s of type %s" % (repr(value), type(value).__name___),
                param,
                ctx,
            )
