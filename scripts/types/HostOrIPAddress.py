import click
import socket


class HostOrIPAddress(click.ParamType):

    def convert(self, value, param, ctx):
        try:
            ips = (socket.getaddrinfo(value, 0, 0, 0, socket.IPPROTO_TCP))
            # Return IP address from first match
            return ips[0][4][0]
        except IndexError, socket.error:
            self.fail("%s is not a valid hostname or IP address" % repr(value), param, ctx)
        except TypeError:
            self.fail(
                "expected string for conversion, got "
                "%s of type %s" % (repr(value), type(value)),
                param,
                ctx,
            )
