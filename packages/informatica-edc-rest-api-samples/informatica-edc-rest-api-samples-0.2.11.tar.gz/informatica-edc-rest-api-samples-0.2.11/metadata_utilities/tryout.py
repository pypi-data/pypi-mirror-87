instrumentation_key = "3f2e5fa7-7803-46c5-b8ad-3324eb4dca52"

import logging

# for trace messages
from opencensus.ext.azure.log_exporter import AzureLogHandler
# for events
from opencensus.ext.azure.log_exporter import AzureEventHandler

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey=' + instrumentation_key)
)
logger.addHandler(AzureEventHandler(connection_string="InstrumentationKey=" + instrumentation_key))
properties = {'custom_dimensions': {'demo_key1': 'value_1', 'demo_key2': 'value_2'}}
logger.setLevel(logging.INFO)

# Use properties in logging statements
logger.info('this is info', extra=properties)
logger.error('this is an error demo', extra=properties)
logger.fatal('fatal error demo', extra=properties)

logger.error('this is a demo')
logger.fatal('fatal error demo')
