import click
import isystem.connect as ic


class Config:
    def __init__(self, cmgr, workspace, id):
        self.cmgr = cmgr
        if workspace is not None:
            self.workspace = workspace.name
        else:
            self.workspace = ''
        self.id = str(id)

    def connect(self):
        connection_config = ic.CConnectionConfig()
        connection_config.useIPCDiscovery(True)
        if self.workspace != '':
            click.echo(f"Using workspace: {self.workspace}")
            connection_config.workspace(self.workspace)

        if self.id is not None:
            click.echo(f"Using instance ID: {self.id}")
            connection_config.instanceId(self.id)
        else:
            self.id = ''

        port = self.cmgr.findOrStartInstance(connection_config)
        self.cmgr.connectMRU(self.workspace, self.id)
