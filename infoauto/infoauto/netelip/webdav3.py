from webdav3.client import WebDavXmlUtils, Client
import lxml.etree as etree
from webdav3.exceptions import RemoteResourceNotFound, MethodNotSupported
from webdav3.urn import Urn


@staticmethod
def extract_response_for_path(content, path, hostname):
    """Extracts single response for specified remote resource.

    :param content: raw content of response as string.
    :param path: the path to needed remote resource.
    :param hostname: the server hostname.
    :return: XML object of response for the remote resource defined by path.
    """
    try:
        tree = etree.fromstring(content)
        responses = tree.findall("{DAV:}response")

        n_path = Urn.normalize_path(path)

        for resp in responses:
            href = resp.findtext("{DAV:}href")
            if n_path in href:  # Urn.compare_path(n_path, href) is True:
                return resp
        raise RemoteResourceNotFound(path)
    except etree.XMLSyntaxError:
        raise MethodNotSupported(name="is_dir", server=hostname)


setattr(WebDavXmlUtils, 'extract_response_for_path', extract_response_for_path)


class WebDAVClient(Client):
    pass
