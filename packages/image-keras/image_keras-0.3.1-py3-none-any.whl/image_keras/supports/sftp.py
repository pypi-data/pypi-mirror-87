import os
import socket
from typing import List, Optional

import paramiko


class SftpServerInfo:
    """
    A Structure which has informations for ftp server.

    Attributes
    ----------
    host_name : str
        Host name for sftp server.
        Should not include like "sftp://", "http://", "https://" etc.
        ex) test.commonpy.net
    host_port : int
        22
    username : str
        User name which can access to sftp server.
    password : str
        Password for username.

    Notes
    -----
    .. versionadded:: 0.1.4
    """

    def __init__(self, host_name: str, host_port: int, username: str, password: str):
        self.host_name: str = host_name
        self.host_port: int = host_port
        self.username: str = username
        self.password: str = password


def __connect(sftp_server_info: SftpServerInfo) -> paramiko.Transport:
    transport = paramiko.Transport(
        (sftp_server_info.host_name, sftp_server_info.host_port)
    )
    transport.connect(
        None,
        sftp_server_info.username,
        sftp_server_info.password,
        gss_host=socket.getfqdn(sftp_server_info.host_name),
    )
    return transport


def __get_sftp_client(transport: paramiko.Transport):
    return paramiko.SFTPClient.from_transport(transport)


def __disconnect(transport: paramiko.Transport):
    transport.close()


def __upload(
    sftp_client: paramiko.SFTPClient, filename: str, local_path: str, remote_path: str
):
    with open(os.path.join(local_path, filename), "rb") as f:
        data = f.read()
    sftp_client.open(os.path.join(remote_path, filename), "wb").write(data)


def upload_file(
    sftp_server_info: SftpServerInfo,
    filename: str,
    local_path: str,
    remote_path: str,
) -> Optional[str]:
    """
    Upload file via sftp connection.

    Parameters
    ----------
    sftp_server_info : SftpServerInfo
        Info for sftp server.
    filename : str
        File name to upload.
    local_path : str
        Local path of `filename`.
    remote_path : str
        Remote path of `filename`.

    Returns
    -------
    Optional[str]
        `None` for no error, `str` message will be return if error exists.

    Notes
    -----
    .. versionadded:: 0.1.4

    Examples
    --------
    >>> sftp_server_info = SftpServerInfo("sftp.server.address", 22, "username", "password")
    >>> upload_file(sftp_server_info, "014_01_16_linear.png", "..", os.path.join("web", "images"))
    """
    try:
        t = __connect(sftp_server_info)
        sftp_client = __get_sftp_client(t)
        __upload(sftp_client, filename, local_path, remote_path)  # type: ignore
        __disconnect(t)
    except Exception as e:
        try:
            __disconnect(t)  # type: ignore
        except:
            pass
        return "*** Caught exception: %s: %s" % (e.__class__, e)


def upload_files(
    sftp_server_info: SftpServerInfo,
    filenames: List[str],
    local_path: str,
    remote_path: str,
) -> Optional[str]:
    """
    Upload file via sftp connection.

    Parameters
    ----------
    sftp_server_info : SftpServerInfo
        Info for sftp server.
    filenames : List[str]
        File names to upload.
    local_path : str
        Local path of `filenames`.
    remote_path : str
        Remote path of `filenames`.

    Returns
    -------
    Optional[str]
        `None` for no error, `str` message will be return if error exists.

    Notes
    -----
    .. versionadded:: 0.1.4

    Examples
    --------
    >>> import os
    >>> sftp_server_info = SftpServerInfo("sftp.server.address", 22, "username", "password")
    >>> upload_files(sftp_server_info, ["014_01_16_linear.png"], "..", os.path.join("web", "images"))
    """
    try:
        t = __connect(sftp_server_info)
        sftp_client = __get_sftp_client(t)
        for filename in filenames:
            __upload(sftp_client, filename, local_path, remote_path)  # type: ignore
        __disconnect(t)
    except Exception as e:
        try:
            __disconnect(t)  # type: ignore
        except:
            pass
        return "*** Caught exception: %s: %s" % (e.__class__, e)
