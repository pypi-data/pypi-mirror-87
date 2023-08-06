import os
import platform
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt

from .report_slack import (
    post,
    post_error,
    post_training_result,
    post_training_result_no_image,
)
from ..sftp import SftpServerInfo, upload_files


def acc_loss_plot(
    acc_list: List[float],
    loss_list: List[float],
    val_acc_list: List[float],
    val_loss_list: List[float],
    model_weight_file_name: str,
    target_folder: str,
) -> Tuple[str, str, str]:
    """
    Plot graphs with acc and loss.

    Parameters
    ----------
    acc_list : List[float]
        List of accuracy values on training.
    loss_list : List[float]
        List of loss values on training.
    val_acc_list : List[float]
        List of validation accuracy values on training.
    val_loss_list : List[float]
        List of validation loss values on training.
    model_weight_file_name : str
        Model weight file name.
    target_folder : str
        Target folder to save images.

    Returns
    -------
    Tuple[str, str, str]
        Tuple of "target folder", "accuracy plot graph file name", "loss plot graph file name"

    Notes
    -----
    .. versionadded:: 0.1.4
    """
    epochs = range(1, len(acc_list) + 1)

    acc_file_name = "{}_acc_history.png".format(model_weight_file_name)
    acc_file = os.path.join(target_folder, acc_file_name)
    loss_file_name = "{}_loss_history.png".format(model_weight_file_name)
    loss_file = os.path.join(target_folder, loss_file_name)

    plt.plot(epochs, acc_list, "bo", label="Training acc")
    plt.plot(epochs, val_acc_list, "b", label="Validation acc")
    plt.title("Training and validation accuracy")
    plt.legend()
    plt.savefig(acc_file, dpi=144)

    plt.figure()

    plt.plot(epochs, loss_list, "bo", label="Training loss")
    plt.plot(epochs, val_loss_list, "b", label="Validation loss")
    plt.title("Training and validation loss")
    plt.legend()
    plt.savefig(loss_file, dpi=144)

    return target_folder, acc_file_name, loss_file_name


def write_training_result_txt(
    model: str,
    model_weight_file_name: str,
    test_loss: float,
    test_acc: float,
    acc_list: List[float],
    loss_list: List[float],
    val_acc_list: List[float],
    val_loss_list: List[float],
    apply_cb_early_stopping_after: int,
    target_folder: str,
) -> None:
    """
    Create txt files for training, validation and test.

    Parameters
    ----------
    model : str
        Model name.
    model_weight_file_name : str
        Model weight file name.
    test_loss : float
        Loss value after test.
    test_acc : float
        Accuracy value after test.
    acc_list : List[float]
        List of accuracy values on training.
    loss_list : List[float]
        List of loss values on training.
    val_acc_list : List[float]
        List of validation accuracy values on training.
    val_loss_list : List[float]
        List of validation loss values on training.
    apply_cb_early_stopping_after : int
        Callback works after `apply_cb_early_stopping_after`.
    target_folder : str
        Target folder to save resulting txt file.

    Notes
    -----
    .. versionadded:: 0.1.4
    """
    f = open(
        os.path.join(
            target_folder, "{}_test_result.txt".format(model_weight_file_name)
        ),
        "w+",
    )

    f.write("# Model Information\r\n")
    f.write("- model: %s\r\n" % model)
    f.write("- model weight file name: %s\r\n" % model_weight_file_name)

    f.write("---\r\n")

    f.write("# Training\r\n")
    val_loss_list_after_cb: List[float] = val_loss_list[apply_cb_early_stopping_after:]
    val_loss_smallest = sorted(val_loss_list_after_cb.copy())[0]
    val_loss_smallest_at = val_loss_list_after_cb.index(val_loss_smallest)
    f.write("- total steps: {}\r\n".format(len(val_loss_list_after_cb)))
    f.write("- step of result: {}\r\n".format(val_loss_smallest_at))
    f.write(
        "- loss: {}\r\n".format(
            loss_list[val_loss_smallest_at + apply_cb_early_stopping_after]
        )
    )
    f.write("- validation loss: {}\r\n".format(val_loss_smallest))
    f.write(
        "- accuracy: {}\r\n".format(
            acc_list[val_loss_smallest_at + apply_cb_early_stopping_after]
        )
    )
    f.write(
        "- validation accuracy: {}\r\n".format(
            val_acc_list[val_loss_smallest_at + apply_cb_early_stopping_after]
        )
    )

    f.write("---\r\n")

    f.write("# Test\r\n")
    f.write("- test loss: {}\r\n".format(test_loss))
    f.write("- test accuracy: {}\r\n".format(test_acc))

    f.close()


def post_via_slack(
    slack_webhook_url: str, notification_text: str, title: str, contents: str
) -> None:
    """
    Send a message using Slack.

    Parameters
    ----------
    slack_webhook_url : str
        Webhook url for Slack.
    notification_text : str
        Text for Slack notification.
    title : str
        Slack message Title.
    contents : str
        Slack message Contents.
    
    Notes
    -----
    .. versionadded:: 0.1.4
    """
    post(
        webhook_url=slack_webhook_url,
        title=title,
        notification_text=notification_text,
        server_name=platform.node(),
        contents=contents,
    )


def post_error_via_slack(
    slack_webhook_url: str, notification_text: str, message: str, traceback_message: str
) -> None:
    """
    Send an error message using Slack.

    Parameters
    ----------
    slack_webhook_url : str
        Webhook url for Slack.
    notification_text : str
        Text for Slack notification.
    message : str
        Slack message Title.
    traceback_message : str
        Slack message for traceback.

    Notes
    -----
    .. versionadded:: 0.1.4

    Examples
    --------
    >>> import traceback
    >>> import os
        ...
    >>> try:
        ...
    >>> webhool_url: Optional[str] = os.environ.get('SLACK_IN_APP_WEB_HOOK_URL')
    >>> except Exception as e:
    >>>     post_error_via_slack(webhook_url, "Error occurred during training.", str(e), traceback.format_exc())
    """
    post_error(
        webhook_url=slack_webhook_url,
        notification_text=notification_text,
        server_name=platform.node(),
        message=message,
        traceback=traceback_message,
    )


def post_training_success_via_slack(
    slack_webhook_url: str,
    notification_text: str,
    model: str,
    model_weight_file_name: str,
    test_loss: float,
    test_acc: float,
    acc_list: List[float],
    loss_list: List[float],
    val_acc_list: List[float],
    val_loss_list: List[float],
    apply_cb_early_stopping_after: int = 0,
    image_sftp_info_optional: Optional[SftpServerInfo] = None,
    image__local_path__sftp_remote_path__tuple_optional: Optional[
        Tuple[str, str]
    ] = None,
    image__loss_plot_file__acc_plot_file__tuple_optional: Optional[
        Tuple[str, str]
    ] = None,
):
    """
    Send an training success message using Slack.

    If the image informations(`image_sftp_info_optional`, `image__local_path__sftp_remote_path__tuple_optional`, `image__loss_plot_file__acc_plot_file__tuple_optional`) are not `None`, the images are also sent.

    Parameters
    ----------
    slack_webhook_url : str
        Webhook url for Slack.
    notification_text : str
        Text for Slack notification.
    model : str
        Model name.
    model_weight_file_name : str
        Model weight file name.
    test_loss : float
        Loss value after test.
    test_acc : float
        Accuracy value after test.
    acc_list : List[float]
        List of accuracy values on training.
    loss_list : List[float]
        List of loss values on training.
    val_acc_list : List[float]
        List of validation accuracy values on training.
    val_loss_list : List[float]
        List of validation loss values on training.
    apply_cb_early_stopping_after : int
        Callback works after `apply_cb_early_stopping_after`. by default 0
    image_sftp_info_optional : Optional[SftpServerInfo]
        Sftp Server Information. by default None
    image__local_path__sftp_remote_path__tuple_optional : Optional[Tuple[str, str]]
        Local path and Remote Path for images. by default None
    image__loss_plot_file__acc_plot_file__tuple_optional : Optional[Tuple[str, str]]
        Image file names for loss and acc plot graphs. by default None
    
    Notes
    -----
    .. versionadded:: 0.1.4
    """
    __post_training_success_via_slack_with_image(
        slack_webhook_url,
        notification_text,
        model,
        model_weight_file_name,
        test_loss,
        test_acc,
        acc_list,
        loss_list,
        val_acc_list,
        val_loss_list,
        apply_cb_early_stopping_after,
        image_sftp_info_optional,
        image__local_path__sftp_remote_path__tuple_optional[0],
        image__local_path__sftp_remote_path__tuple_optional[1],
        image__loss_plot_file__acc_plot_file__tuple_optional[0],
        image__loss_plot_file__acc_plot_file__tuple_optional[1],
    ) if (
        image_sftp_info_optional
        and image__local_path__sftp_remote_path__tuple_optional
        and image__loss_plot_file__acc_plot_file__tuple_optional
    ) else __post_training_success_via_slack_without_image(
        slack_webhook_url,
        notification_text,
        model,
        model_weight_file_name,
        test_loss,
        test_acc,
        acc_list,
        loss_list,
        val_acc_list,
        val_loss_list,
        apply_cb_early_stopping_after,
    )


def __post_training_success_via_slack_with_image(
    slack_webhook_url: str,
    notification_text: str,
    model: str,
    model_name: str,
    test_loss: float,
    test_acc: float,
    acc_list: List[float],
    loss_list: List[float],
    val_acc_list: List[float],
    val_loss_list: List[float],
    apply_cb_early_stopping_after: int,
    image_sftp_info: SftpServerInfo,
    img_local_path: str,
    img_sftp_remote_path: str,
    loss_plot_img_name: str,
    acc_plot_img_name: str,
):
    upload_files(
        image_sftp_info,
        [loss_plot_img_name, acc_plot_img_name],
        img_local_path,
        img_sftp_remote_path,
    )

    image_http_hostname = "http://{}".format(image_sftp_info.host_name)
    val_loss_list_after_cb: List[float] = val_loss_list[apply_cb_early_stopping_after:]
    val_loss_smallest = sorted(val_loss_list_after_cb.copy())[0]
    val_loss_smallest_at = val_loss_list_after_cb.index(val_loss_smallest)
    post_training_result(
        webhook_url=slack_webhook_url,
        notification_text=notification_text,
        server_name=platform.node(),
        model=model,
        model_file=model_name,
        total_steps=len(val_loss_list_after_cb),
        step_of_result=val_loss_smallest_at,
        loss=loss_list[val_loss_smallest_at + apply_cb_early_stopping_after],
        val_loss=val_loss_smallest,
        acc=acc_list[val_loss_smallest_at + apply_cb_early_stopping_after],
        val_acc=val_acc_list[val_loss_smallest_at + apply_cb_early_stopping_after],
        test_loss=test_loss,
        test_acc=test_acc,
        image_host_addr=image_http_hostname,
        loss_plot_img_name=loss_plot_img_name,
        acc_plot_img_name=acc_plot_img_name,
    )


def __post_training_success_via_slack_without_image(
    slack_webhook_url: str,
    notification_text: str,
    model: str,
    model_name: str,
    test_loss: float,
    test_acc: float,
    acc_list: List[float],
    loss_list: List[float],
    val_acc_list: List[float],
    val_loss_list: List[float],
    apply_cb_early_stopping_after: int,
):
    val_loss_list_after_cb: List[float] = val_loss_list[apply_cb_early_stopping_after:]
    val_loss_smallest = sorted(val_loss_list_after_cb.copy())[0]
    val_loss_smallest_at = val_loss_list_after_cb.index(val_loss_smallest)
    post_training_result_no_image(
        webhook_url=slack_webhook_url,
        notification_text=notification_text,
        server_name=platform.node(),
        model=model,
        model_file=model_name,
        total_steps=len(val_loss_list_after_cb),
        step_of_result=val_loss_smallest_at,
        loss=loss_list[val_loss_smallest_at + apply_cb_early_stopping_after],
        val_loss=val_loss_smallest,
        acc=acc_list[val_loss_smallest_at + apply_cb_early_stopping_after],
        val_acc=val_acc_list[val_loss_smallest_at + apply_cb_early_stopping_after],
        test_loss=test_loss,
        test_acc=test_acc,
    )
