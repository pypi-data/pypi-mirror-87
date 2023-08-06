# coding: utf-8

__author__ = "Ondrej Jurcak"

import logging
from configparser import ConfigParser

from aws_xray_sdk import global_sdk_config
from aws_xray_sdk.core import xray_recorder, patch_all, patch
from aws_xray_sdk.core.utils import stacktrace
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
from aws_xray_sdk.ext.flask_sqlalchemy.query import XRayFlaskSqlAlchemy
from aws_xray_sdk.ext.util import construct_xray_header, inject_trace_header
from celery import signals


class XRaySettingsConfigParser:

    def __init__(self, settings):
        if "XRAY" in settings:
            xray = settings["XRAY"]
            self.enabled = xray.get("ENABLED", False)
            self.service_name = xray.get("SERVICE_NAME")
            self.plugins = xray.get("PLUGINS", "'ECSPlugin', 'EC2Plugin'")
            self.sampling = xray.get("SAMPLING", False)
            self.stream_sql = xray.get("STREAM_SQL", True)
            self.daemon = xray.get("DAEMON", "xray-daemon:2000")
            self.patch_modules = xray.get("PATCH_MODULES", None)
            self.logging_enabled = xray.get("LOGGING_ENABLED", False)
            self.sqlalchemy = xray.get("SQLALCHEMY", False)
            self.middleware = xray.get("MIDDLEWARE", True)
        else:
            self.enabled = False
            self.service_name = None
            self.plugins = "'ECSPlugin', 'EC2Plugin'"
            self.sampling = False
            self.stream_sql = True
            self.daemon = "xray-daemon:2000"
            self.patch_modules = None
            self.logging_enabled = False
            self.sqlalchemy = False
            self.middleware = True


class XRaySettingsLazySettings:
    def __init__(self, settings):
        self.enabled = settings.XRAY_ENABLED
        self.service_name = settings.XRAY_SERVICE_NAME
        self.plugins = settings.XRAY_PLUGINS
        self.sampling = settings.XRAY_SAMPLING
        self.stream_sql = settings.XRAY_STREAM_SQL
        self.daemon = settings.XRAY_DAEMON
        self.patch_modules = settings.XRAY_PATCH_MODULES
        self.logging_enabled = settings.XRAY_LOGGING_ENABLED
        self.sqlalchemy = settings.XRAY_SQLALCHEMY
        self.middleware = settings.XRAY_MIDDLEWARE


class XRayConfigurator:

    def __init__(self, settings, application=None) -> None:
        if isinstance(settings, ConfigParser):
            self.settings = XRaySettingsConfigParser(settings)
        else:
            self.settings = XRaySettingsLazySettings(settings)

        if not self.settings.enabled:
            return
        self._init_xray(self.settings)

        if application:
            if self.settings.sqlalchemy:
                logging.info("XRayFlaskSqlAlchemy enabled")
                XRayFlaskSqlAlchemy(application)
            if self.settings.middleware:
                XRayMiddleware(application, xray_recorder)

    def _init_xray(self, settings):
        if settings.enabled:
            logging.info("xray sdk enabled " + str(settings.enabled))
            global_sdk_config.set_sdk_enabled(True)
            xray_recorder.configure(service=settings.service_name,
                                    plugins=eval(settings.plugins),
                                    sampling=settings.sampling,
                                    stream_sql=settings.stream_sql,
                                    daemon_address=settings.daemon,
                                    context_missing="LOG_ERROR")
            if not settings.patch_modules:
                patch_all()
            else:
                patch(eval(settings.patch_modules))

            if settings.logging_enabled:
                logging.info("XRay logging enabled")
                logging.getLogger("aws_xray_sdk").setLevel(logging.DEBUG)
            else:
                logging.info("XRay logging disabled")
                logging.getLogger("aws_xray_sdk").setLevel(logging.NOTSET)
        else:
            logging.info("xray sdk disabled")
            global_sdk_config.set_sdk_enabled(False)


@signals.task_prerun.connect
def task_prerun(task_id, task, *args, **kwargs):
    logging.info("task prerun task_id: " + task_id)
    xray_header = construct_xray_header(task.request)
    logging.info("xray header constructed. Root: {}, Parent: {}".format(xray_header.root, xray_header.parent))
    segment = xray_recorder.begin_segment(
        name=task.name,
        traceid=xray_header.root,
        parent_id=xray_header.parent,
    )
    segment.save_origin_trace_header(xray_header)
    segment.put_metadata('task_id', task_id, namespace='celery')


@signals.task_postrun.connect()
def task_postrun(task_id, *args, **kwargs):
    logging.info("task post run task_id: " + task_id)
    xray_recorder.end_segment()


@signals.before_task_publish.connect
def before_task_publish(sender, headers, **kwargs):
    logging.info("before taskpublish sender: " + sender)
    subsegment = xray_recorder.begin_subsegment(
        name=sender,
        namespace='remote',
    )

    if subsegment is None:
        logging.info("task taskpublish not in segment")
        return
    subsegment.put_metadata('task_id', headers.get("id"), namespace='celery')
    inject_trace_header(headers, subsegment)


@signals.after_task_publish.connect
def xray_after_task_publish(**kwargs):
    logging.info("after task publish")
    xray_recorder.end_subsegment()


@signals.task_failure.connect
def xray_task_failure(einfo, **kwargs):
    logging.info("task_failure")
    segment = xray_recorder.current_segment()
    if segment is None:
        logging.info("task failure not in segment")
        return
    if einfo:
        stack = stacktrace.get_stacktrace(limit=xray_recorder.max_trace_back)
        try:
            segment.add_exception(einfo.exception, stack)
        except FileNotFoundError as e: # os.getcwd() crashes sometimes we need to handle this issue
            logging.info("File not found error whne segment.add_exception")
