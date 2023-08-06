# coding=utf-8
from __future__ import unicode_literals

import logging
import threading

import zmq
from om.message import Topic, Message


class Status:
    OK = "ok"
    ERROR = "error"
    OFFLINE = "offline"


class AlertHandler(object):
    def __init__(self, config=None, context=None, pub_socket=None, name=None, version=None):
        self._pub_socket = None
        self._alerts = []
        self.send_lock = threading.RLock()
        self.id_lock = threading.RLock()
        self.log = logging.getLogger(__name__)

        if pub_socket:
            logging.warning("Deprecation Warning: Passing a pub socket to the alert handler is deprecated! "
                            "This is to ensure proper locking of the socket. Please pass a zmq context instead.")

        if config:
            self._version = config.VERSION
            self._name = config.NAME
        else:
            self._version = version
            self._name = name

        if pub_socket:
            self._pub_socket = pub_socket
        else:
            context = context or zmq.Context()
            assert config, "a config must be set to auto-connect to the broker!"
            self._pub_socket = context.socket(zmq.PUB)
            self._pub_socket.connect("tcp://{}:{}".format(config.BROKER_HOST, config.BROKER_SUB_PORT))

    def _send_message(self, alert_id, _status_dict):
        with self.send_lock:
            alert = self._alerts[alert_id]
            _status_dict["alert_meta"].update(dict(sender=self._name))
            old_status = alert["alert_dict"].get("status")
            alert["alert_dict"].update(_status_dict)
            if alert["always_send_alert"] or alert["alert_dict"]["status"] != old_status:
                message = Message(
                    name=self._name,
                    type="alert",
                )
                message.update(alert["alert_dict"])
                package = message['package'] if message["package"] != self._name else ""
                source = message.get("source", "")
                tmp = f"{' from ' if package or source else ''}{package}{'/' if package and source else ''}{source}:"
                self.log.info(f"Send alert{tmp} {message['alert_type']} - {message['status']}")
                message.to_socket(self._pub_socket, Topic.ALERT)
                return True
            return False

    def get_or_add_alert_id(self, source, alert_type, handle_type, package_name=None, version=None,
                            always_send_alert=None):
        """Define an alert with its name parameters

        Args:
            source (str): The source of the error (i.e. which pin, camera)
            alert_type (str): Name of the alert all lower_case with '_' (i.e. high_time_check)
            handle_type (str): How the error should be handled on the server (state, state_change, count)
            package_name (str) (default=config.NAME): You send the error for this package
            version (str) (default=config.VERSION): Current version of the package
            always_send_alert (bool) (default=False): Send every alert or only when there is a change in the status

        Returns:
            alert_id of the saved alert
        """

        assert "-" not in alert_type, "please do not use - in your alert type names"

        alert_dict = dict(source=source, alert_type=alert_type, handle_type=handle_type)
        alert_dict["package"] = package_name or self._name

        with self.id_lock:
            for alert in self._alerts:
                if alert_dict.items() <= alert["alert_dict"].items():
                    if always_send_alert is not None:
                        alert["always_send_alert"] = always_send_alert
                    if version is not None:
                        alert["alert_dict"]["version"] = version
                    return alert["id"]

            v = version if version is not None else self._version
            asa = always_send_alert if always_send_alert is not None else False
            alert = {"alert_dict": alert_dict, "id": len(self._alerts), "always_send_alert": asa, "version": v}
            self._alerts.append(alert)
            return alert["id"]

    def send_with_alert_id(self, alert_id, status, meta, kwargs):
        """ Send a status message on the given alert with the corresponding meta/kwarg arguments
            Returns True if alert was send else False"""
        assert status in [Status.ERROR, Status.OK, Status.OFFLINE]
        _status_dict = {
            "status": status,
            "alert_meta": (meta or {}),
        }
        _status_dict.update(kwargs or {})
        return self._send_message(alert_id, _status_dict)

    def send(self, source, alert_type, handle_type, package_name=None, version=None,
             always_send_alert=None, status=Status.ERROR, meta=None, kwargs=None):
        """Sends an alert to the device serve

        Args:
            source (str): The source of the error (i.e. which pin, camera)
            alert_type (str): Name of the alert all lower_case with '_' (i.e. high_time_check, health_hw_compute_nuc)
            handle_type (str): How the error should be handled on the server (state, state_change, count)
            status (Status/bool): The status you want to send(Status.OK/True, Status.ERROR/False, Status.OFFLINE)
            package_name (str) optional: You can send errors for other packages
            version (str) (default=config.VERSION): Current version of the package
            always_send_alert (bool): Flag to declare if you want to send every alert or only every change in the status
            meta (dict): Meta information
            kwargs (dict): Additional parameters you want to add to the message (i.e. value of error metric)

        Returns:
            True if alert was send else False
        """
        assert "-" not in alert_type, "please do not use - in your alert type names"

        alert_id = self.get_or_add_alert_id(source, alert_type, handle_type, package_name, version, always_send_alert)
        return self.send_with_alert_id(alert_id, status, meta, kwargs)
