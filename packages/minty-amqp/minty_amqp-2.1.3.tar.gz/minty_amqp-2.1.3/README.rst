.. _readme:

Introduction
============

AMQP Consumer service framework.

Getting started
---------------

Main::
  
  def main():
      amqp = AMQPLoader(
          domains=[insert_domains_here],
          command_wrapper_middleware=[insert_wrapper_classes_here],
          config_path="config.conf",
      )
      amqp.start_client()

Create consumer::

  from minty_amqp.consumer import BaseConsumer

  class ConsumerPrint(BaseConsumer):
    def __call__(self, message):
        print("Message:", message.body, "consumer_touch")
        message.ack()

package.conf example::

  <amqp>
    url = 'http://0.0.0.0:5672'
    <consumer_settings>
          routing_keys = "zsnl.v2.*.*"
          queue_name = "legacy_logging_queue_test"
          exchange  =  "minty_exchange"
          qos_prefetching =  1
          consumer_class = "zsnl_amqp_consumers.consumers.LegacyLoggingConsumer"
          number_of_channels = 1
          <dead_letter_exchange>
            exchange = "minty_retry_exchange"
            retry_time_ms = 10000
          </dead_letter_exchange> 
    </consumer_settings>  
  </amqp>

note: dead_letter_exchange config is optional



More documentation
------------------

Please see the generated documentation via CI for more information about this
module and how to contribute in our online documentation. Open index.html
when you get there:
`<https://gitlab.com/minty-python/minty_amqp/-/jobs/artifacts/master/browse/tmp/docs?job=qa>`_


Contributing
------------

Please read `CONTRIBUTING.md <https://gitlab.com/minty-python/minty_amqp/blob/master/CONTRIBUTING.md>`_
for details on our code of conduct, and the process for submitting pull requests to us.

Versioning
----------

We use `SemVer <https://semver.org/>`_ for versioning. For the versions
available, see the
`tags on this repository <https://gitlab.com/minty-python/minty_amqp/tags/>`_

License
-------

Copyright (c) Minty Team and all persons listed in the file `CONTRIBUTORS`

This project is licensed under the EUPL, v1.2. See the `EUPL-1.2.txt` in the
`LICENSES` directory for details.

.. SPDX-FileCopyrightText: 2020 Mintlab B.V.
..
.. SPDX-License-Identifier: EUPL-1.2
