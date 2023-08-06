from datetime import datetime
import json

import requests


def request_slack_json(url: str, data: str) -> None:
    response = requests.post(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    if response.status_code != 200:
        raise ValueError(
            "Request to slack returned an error %s, the response is:\n%s"
            % (response.status_code, response.text)
        )


def post(
    webhook_url: str,
    title: str,
    notification_text: str,
    server_name: str,
    contents: str,
) -> None:
    slack_data = json.dumps(
        {
            "text": notification_text,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "📌 Server *{}* at {}".format(
                            server_name, str(datetime.now())[:19]
                        ),
                    },
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "# *{}*".format(title)},
                },
                {"type": "section", "text": {"type": "mrkdwn", "text": contents}},
            ],
        }
    )
    request_slack_json(webhook_url, slack_data)


def post_error(
    webhook_url: str,
    notification_text: str,
    server_name: str,
    message: str,
    traceback: str,
) -> None:
    slack_data = json.dumps(
        {
            "text": notification_text,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "📌 Server *{}* at {}".format(
                            server_name, str(datetime.now())[:19]
                        ),
                    },
                },
                {"type": "section", "text": {"type": "mrkdwn", "text": "# *Error*"}},
                {"type": "section", "text": {"type": "mrkdwn", "text": "## Message"}},
                {"type": "section", "text": {"type": "mrkdwn", "text": message}},
                {"type": "section", "text": {"type": "mrkdwn", "text": "## Traceback"}},
                {"type": "section", "text": {"type": "mrkdwn", "text": traceback}},
            ],
        }
    )
    request_slack_json(webhook_url, slack_data)


def post_training_result(
    webhook_url: str,
    notification_text: str,
    server_name: str,
    model: str,
    model_file: str,
    total_steps: int,
    step_of_result: int,
    loss: float,
    val_loss: float,
    acc: float,
    val_acc: float,
    test_loss: float,
    test_acc: float,
    image_host_addr: str,
    loss_plot_img_name: str,
    acc_plot_img_name: str,
) -> None:
    slack_data = json.dumps(
        {
            "text": notification_text,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "📌 Server *{}* at {}".format(
                            server_name, str(datetime.now())[:19]
                        ),
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Training* completed on *{}*".format(server_name),
                    },
                },
                {
                    "type": "section",
                    "fields": [{"type": "mrkdwn", "text": "# *Model Information*"}],
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "• model: {}\n• model file: `{}`".format(
                                model, model_file
                            ),
                        }
                    ],
                },
                {
                    "type": "section",
                    "fields": [{"type": "mrkdwn", "text": "# *Training*"}],
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "• total steps: {}\n• step of result: {}\n• loss: {}\n• validation loss: {}\n• accuracy: {}\n• validation accuracy: {}".format(
                                total_steps,
                                step_of_result,
                                loss,
                                val_loss,
                                acc,
                                val_acc,
                            ),
                        }
                    ],
                },
                {
                    "type": "image",
                    "title": {"type": "plain_text", "text": "Loss plot."},
                    "image_url": "{}/{}".format(image_host_addr, loss_plot_img_name),
                    "alt_text": "Loss plot.",
                },
                {
                    "type": "image",
                    "title": {"type": "plain_text", "text": "Accuracy plot."},
                    "image_url": "{}/{}".format(image_host_addr, acc_plot_img_name),
                    "alt_text": "Accuracy plot.",
                },
                {"type": "section", "fields": [{"type": "mrkdwn", "text": "# *Test*"}]},
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "• test loss: {}\n• test accuracy: {}\n".format(
                                test_loss, test_acc
                            ),
                        }
                    ],
                },
                {"type": "divider"},
            ],
        }
    )
    request_slack_json(webhook_url, slack_data)


def post_training_result_no_image(
    webhook_url: str,
    notification_text: str,
    server_name: str,
    model: str,
    model_file: str,
    total_steps: int,
    step_of_result: int,
    loss: float,
    val_loss: float,
    acc: float,
    val_acc: float,
    test_loss: float,
    test_acc: float,
) -> None:
    slack_data = json.dumps(
        {
            "text": notification_text,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "📌 Server *{}* at {}".format(
                            server_name, str(datetime.now())[:19]
                        ),
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Training* completed on *{}*".format(server_name),
                    },
                },
                {
                    "type": "section",
                    "fields": [{"type": "mrkdwn", "text": "# *Model Information*"}],
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "• model: {}\n• model file: `{}`".format(
                                model, model_file
                            ),
                        }
                    ],
                },
                {
                    "type": "section",
                    "fields": [{"type": "mrkdwn", "text": "# *Training*"}],
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "• total steps: {}\n• step of result: {}\n• loss: {}\n• validation loss: {}\n• accuracy: {}\n• validation accuracy: {}".format(
                                total_steps,
                                step_of_result,
                                loss,
                                val_loss,
                                acc,
                                val_acc,
                            ),
                        }
                    ],
                },
                {"type": "section", "fields": [{"type": "mrkdwn", "text": "# *Test*"}]},
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "• test loss: {}\n• test accuracy: {}\n".format(
                                test_loss, test_acc
                            ),
                        }
                    ],
                },
                {"type": "divider"},
            ],
        }
    )
    request_slack_json(webhook_url, slack_data)

