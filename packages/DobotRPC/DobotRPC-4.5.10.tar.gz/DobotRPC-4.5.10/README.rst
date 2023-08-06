***This version is relevant for Dobotlink 5.0.0***

DobotRPC is a dobotlink communication module based on websocket and
JSON-RPC . It provides python ports to communicate with dobotlink and
allows developers to communicate with the GUI. Here is a more detailed
list of the package contents:

-  The file contains both RPCClient and RPCServer files that users can
   call upon their own needs
-  DobotlinkAdapter: The adapter module is used to adapt to the new set
   of interfaces

Utils

-  Loggers: Loggers information

Examples
--------

-  Users can communicate synchronously or asynchronously.The
   asynchronous mode is as follows:

::

    # Async demo
    from DobotRPC import DobotlinkAdapter, RPCClient, loggers
    # The asyncio module provides infrastructure for writing single-threaded concurrent code using coroutines, multiplexing I/O access over sockets and other resources, running network clients and servers, and other related primitives.
    import asyncio


    # Coroutines function
    async def main(dobotlink_async):
        # Display information with Dobotlink
        await dobotlink_async.api.ShowMessage(title="Async Demo Message",
                                            message="Async Demo is running.")

        # Search for available ports
        res = await dobotlink_async.Magician.SearchDobot()

        # Get ports
        if len(res) < 1:
            return
        port_name = res[0]["portName"]

        # Connect
        await dobotlink_async.Magician.ConnectDobot(portName=port_name)

        # PTP
        await dobotlink_async.Magician.SetPTPCmd(portName=port_name,
                                                ptpMode=0,
                                                x=230,
                                                y=50,
                                                z=0,
                                                r=20)
        # Disconnect
        await dobotlink_async.Magician.DisconnectDobot(portName=port_name,
                                                    queueStop=True,
                                                    queueClear=True)


    if __name__ == "__main__":

        loggers.set_level(loggers.DEBUG)
        # Get the Eventloop reference
        loop = asyncio.get_event_loop()
        # Initializes, connects to dobotlink, and is executed before the Loop runs
        dobotlink_async = DobotlinkAdapter(RPCClient(loop=loop), is_sync=False)
        # Perform coroutines
        loop.run_until_complete(main(dobotlink_async))

-  The synchronization mode is as follows:

::

    # Sync Demo
    from DobotRPC import RPCClient, DobotlinkAdapter, loggers


    def main(dobotlink_sync):
        # Display information with Dobotlink
        dobotlink_sync.api.ShowMessage(title="Sync Demo Message",
                                    message="Sync Demo is running.")

        # Search for available ports
        res = dobotlink_sync.Magician.SearchDobot()

        # Get ports
        if len(res) < 1:
            return
        port_name = res[0]["portName"]

        # Connect
        dobotlink_sync.Magician.ConnectDobot(portName=port_name)

        # PTP
        dobotlink_sync.Magician.SetPTPCmd(portName=port_name,
                                        ptpMode=0,
                                        x=230,
                                        y=50,
                                        z=0,
                                        r=20)

        # Disconnect
        dobotlink_sync.Magician.DisconnectDobot(portName=port_name)


    if __name__ == "__main__":
        loggers.set_level(loggers.DEBUG)
        # Initialize, connect to dobotlink
        dobotlink_sync = DobotlinkAdapter(RPCClient(), is_sync=True)

        main(dobotlink_sync)


Installtion
-----------

To install DobotRPC, type:

::

    pip install DobotRPC

DobotRPC is a free software distributed under the Apache license

Usage
-----

- Users can use the API:
    loggers, RPCClient, DobotlinkAdapter, NetworkError, client, aip
-  Install [Dobotlink](https://cdn.dobotlab.dobot.cc/release/DobotLinkSetup.exe)
-  Right-click the Dobotlink icon and click ``help``, pop up a
   ``Dobotlink help documentation``.
-  You can guide by ``examples``, reference the
   ``Dobotlink help documentation``.
-  Then go ahead and develop your first python script.