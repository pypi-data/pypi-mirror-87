# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2019 SerialLab Corp.  All rights reserved.
import socket
from quartet_output.models import EPCISOutputCriteria
from quartet_capture.rules import RuleContext
from urllib.parse import urlparse

# mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = "10.80.209.106"
# port = 9100
# try:
#     mysocket.connect((host, port))  # connecting to host
#     mysocket.send(b"^XA^A0N,50,50^FO50,50^FDSocket Test^FS^XZ")  # using bytes
#     mysocket.close()  # closing connection
# except:
#     print("Error with the connection")


class SocketTransportMixin:

    def socket_send(self, data, rule_context: RuleContext,
                    output_criteria: EPCISOutputCriteria,
                    info):
        """
        Sends data over a socket
        :param data: The data to send (as bytes)
        :param rule_context: The rule context
        :param output_criteria: The output criteria supplying the urn
        :param info: The info function for logging
        :return: None
        """
        mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        parsed_url = urlparse(output_criteria.end_point.urn)
        host = parsed_url.netloc.split(":")[0]
        port = parsed_url.port

        info('Connecting to host %s ', output_criteria.end_point.urn)
        mysocket.connect((host, port))  # connecting to host
        info('Sending data: %s (may be truncated for display purposes)',
                  data[:1000])
        mysocket.send(
            bytes(data))  # using bytes
        mysocket.close()  # closing connection
