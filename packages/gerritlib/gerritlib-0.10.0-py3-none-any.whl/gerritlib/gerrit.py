# Copyright 2011 OpenStack, LLC.
# Copyright 2012 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json
import logging
import platform
import pprint
import select
import six.moves
import threading
import time

import paramiko

CONNECTED = 'connected'
CONNECTING = 'connecting'
CONSUMING = 'consuming'
DEAD = 'dead'
DISCONNECTED = 'disconnected'
IDLE = 'idle'
UPDATE_ALLOWED_KEYS = ['description', 'submit-type',
                       'contributor-agreements', 'signed-off-by',
                       'content-merge', 'change-id',
                       'project-state',
                       'max-object-size-limit']
IS_LINUX = platform.system() == "Linux"


class GerritConnection(object):
    log = logging.getLogger("gerrit.GerritConnection")

    def __init__(self, username=None, hostname=None, port=29418,
                 keyfile=None, keep_alive=0, connection_attempts=-1,
                 retry_delay=5):

        assert retry_delay >= 0, "Retry delay must be >= 0"
        self.username = username
        self.hostname = hostname
        self.port = port
        self.keyfile = keyfile
        self.connection_attempts = int(connection_attempts)
        self.retry_delay = float(retry_delay)
        self.keep_alive = keep_alive

    def connect(self):
        """Attempts to connect and returns the connected client."""

        def _make_client():
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.WarningPolicy())
            return client

        def _attempt_gen(connection_attempts, retry_delay):
            if connection_attempts <= 0:
                attempt = 1
                while True:
                    yield (attempt, retry_delay)
                    attempt += 1
            else:
                for attempt in range(1, connection_attempts + 1):
                    if attempt < connection_attempts:
                        yield (attempt, retry_delay)
                    else:
                        # No more attempts left after this one, (signal this by
                        # not returning a valid retry_delay).
                        yield (attempt, None)

        for (attempt, retry_delay) in _attempt_gen(self.connection_attempts,
                                                   self.retry_delay):
            self.log.debug("Connection attempt %s to %s:%s (retry_delay=%s)",
                           attempt, self.hostname, self.port, retry_delay)
            client = None
            try:
                client = _make_client()
                client.connect(self.hostname,
                               username=self.username,
                               port=self.port,
                               key_filename=self.keyfile)
                if self.keep_alive:
                    client.get_transport().set_keepalive(self.keep_alive)
                return client
            except (IOError, paramiko.SSHException) as e:
                self.log.exception("Exception connecting to %s:%s",
                                   self.hostname, self.port)
                if client:
                    try:
                        client.close()
                    except (IOError, paramiko.SSHException):
                        self.log.exception("Failure closing broken client")
                if retry_delay is not None:
                    if retry_delay > 0:
                        self.log.info("Trying again in %s seconds",
                                      retry_delay)
                        time.sleep(retry_delay)
                else:
                    raise e


class GerritWatcher(threading.Thread):
    log = logging.getLogger("gerrit.GerritWatcher")

    def __init__(
            self, gerrit, username=None, hostname=None, port=None,
            keyfile=None, keep_alive=0, connection_attempts=-1, retry_delay=5):
        """Create a GerritWatcher.

        :param gerrit: A GerritConnection instance to pass events to.

        All other parameters are optional and if not supplied are sourced from
        the gerrit instance.
        """
        super(GerritWatcher, self).__init__()
        self.connection = GerritConnection(
            username or gerrit.connection.username,
            hostname or gerrit.connection.hostname,
            port or gerrit.connection.port,
            keyfile or gerrit.connection.keyfile,
            keep_alive or gerrit.connection.keep_alive,
            connection_attempts,
            retry_delay
        )
        self.gerrit = gerrit
        self.retry_delay = float(retry_delay)
        self.state = IDLE

    def _read(self, fd):
        line = fd.readline()
        if line:
            try:
                data = json.loads(line)
                self.log.debug("Received data from Gerrit event stream: \n%s" %
                               pprint.pformat(data))
                self.gerrit.addEvent(data)
            except json.decoder.JSONDecodeError:
                self.log.debug("Can not parse data from Gerrit event stream: \n%s" %
                               pprint.pformat(line))
        else:
            # blank read indicates EOF and the connection closed
            self.state = DISCONNECTED

    def _listen(self, stdout, stderr):
        poll = select.poll()
        poll.register(stdout.channel)
        while True:
            if self.state == DISCONNECTED:
                return
            ret = poll.poll()
            for (fd, event) in ret:
                if fd == stdout.channel.fileno():
                    # event is a bitmask
                    # On Darwin non-critical OOB messages can be received
                    if (IS_LINUX and event == select.POLLIN) or \
                            (not IS_LINUX and event & select.POLLIN):
                        self._read(stdout)
                    else:
                        raise Exception("event %s on ssh connection" % event)

    def _consume(self, client):
        """Consumes events using the given client."""
        stdin, stdout, stderr = client.exec_command("gerrit stream-events")

        self.state = CONSUMING
        self._listen(stdout, stderr)

        ret = stdout.channel.recv_exit_status()
        self.log.debug("SSH exit status: %s" % ret)

        if ret:
            raise Exception("Gerrit error executing stream-events:"
                            " return code %s" % ret)

    def _run(self):
        self.state = CONNECTING
        client = self.connection.connect()
        self.state = CONNECTED
        try:
            self._consume(client)
        except Exception:
            # NOTE(harlowja): allow consuming failures to *always* be retryable
            self.log.exception("Exception consuming ssh event stream:")
            if client:
                try:
                    client.close()
                except (IOError, paramiko.SSHException):
                    self.log.exception("Failure closing broken client")
            self.state = DISCONNECTED
            if self.retry_delay > 0:
                self.log.info("Delaying consumption retry for %s seconds",
                              self.retry_delay)
                time.sleep(self.retry_delay)

    def run(self):
        try:
            while True:
                self.state = DISCONNECTED
                self._run()
        finally:
            self.state = DEAD


class Gerrit(object):
    log = logging.getLogger("gerrit.Gerrit")

    def __init__(
            self, hostname, username, port=29418, keyfile=None,
            keep_alive_interval=0,
            connection_attempts=-1,
            retry_delay=5):
        self.connection = GerritConnection(
            username, hostname, port, keyfile,
            keep_alive=keep_alive_interval,
            connection_attempts=connection_attempts,
            retry_delay=retry_delay)
        self.client = None
        self.watcher_thread = None
        self.event_queue = None
        self.installed_plugins = None

    def startWatching(self, connection_attempts=-1, retry_delay=5):
        self.event_queue = six.moves.queue.Queue()
        watcher = GerritWatcher(self,
                                connection_attempts=connection_attempts,
                                retry_delay=retry_delay)
        self.watcher_thread = watcher
        self.watcher_thread.daemon = True
        self.watcher_thread.start()

    def addEvent(self, data):
        return self.event_queue.put(data)

    def getEvent(self):
        return self.event_queue.get()

    def createGroup(self, group, visible_to_all=True, owner=None):
        cmd = 'gerrit create-group'
        if visible_to_all:
            cmd = '%s --visible-to-all' % cmd
        if owner:
            cmd = '%s --owner %s' % (cmd, owner)
        cmd = '%s "%s"' % (cmd, group)
        out, err = self._ssh(cmd)
        return err

    def listMembers(self, group, recursive=False):
        cmd = 'gerrit ls-members'
        if recursive:
            cmd = '%s --recursive' % cmd
        cmd = '%s "%s"' % (cmd, group)
        out, err = self._ssh(cmd)
        ret = []
        rows = out.split('\n')
        if len(rows) > 1:
            keys = rows[0].split('\t')
            for row in rows[1:]:
                ret.append(dict(zip(keys, row.split('\t'))))
        return ret

    def _setMember(self, verb, group, member):
        cmd = 'gerrit set-members'
        if verb == 'add':
            cmd = '%s --add "%s"' % (cmd, member)
        elif verb == 'remove':
            cmd = '%s --remove "%s"' % (cmd, member)
        cmd = '%s "%s"' % (cmd, group)
        out, err = self._ssh(cmd)
        return err

    def addMember(self, group, member):
        self._setMember('add', group, member)

    def removeMember(self, group, member):
        self._setMember('remove', group, member)

    def createProject(self, project, require_change_id=True, empty_repo=False,
                      description=None, branches=None):
        cmd = 'gerrit create-project'
        if require_change_id:
            cmd = '%s --require-change-id' % cmd
        if empty_repo:
            cmd = '%s --empty-commit' % cmd
        if description:
            cmd = "%s --description \"%s\"" % \
                  (cmd, description.replace('"', r'\"'))
        if branches:
            # Branches should be a list. The first entry will be repo HEAD.
            for branch in branches:
                cmd = "%s --branch \"%s\"" % (cmd, branch)
        version = None
        try:
            version = self.parseGerritVersion(self.getVersion())
        except Exception:
            # If no version then we know version is old and should use --name
            pass
        if not version or version < (2, 12):
            cmd = '%s --name "%s"' % (cmd, project)
        else:
            cmd = '%s "%s"' % (cmd, project)
        out, err = self._ssh(cmd)
        return err

    def updateProject(self, project, update_key, update_value):
        # check for valid keys
        if update_key not in UPDATE_ALLOWED_KEYS:
            raise Exception("Trying to update a non-valid key %s" % update_key)

        cmd = 'gerrit set-project %s ' % project
        if update_key == 'description':
            cmd += "--%s \"%s\"" % (update_key,
                                    update_value.replace('"', r'\"'))
        else:
            cmd += '--%s %s' % (update_key, update_value)
        out, err = self._ssh(cmd)
        return err

    def listProjects(self, show_description=False):
        cmd = 'gerrit ls-projects'
        if show_description:
            # display projects alongs with descriptions
            # separated by ' - ' sequence
            cmd += ' --description'
        out, err = self._ssh(cmd)
        return list(filter(None, out.split('\n')))

    def listGroups(self, verbose=False):
        if verbose:
            cmd = 'gerrit ls-groups -v'
        else:
            cmd = 'gerrit ls-groups'
        out, err = self._ssh(cmd)
        return list(filter(None, out.split('\n')))

    def listGroup(self, group, verbose=False):
        if verbose:
            cmd = 'gerrit ls-groups -v'
        else:
            cmd = 'gerrit ls-groups'
        version = None
        try:
            version = self.parseGerritVersion(self.getVersion())
        except Exception:
            # If no version then we know version is old and should use -q
            pass
        if not version or version < (2, 14):
            query_flag = '-q'
        else:
            query_flag = '-g'
        # ensure group names with spaces are escaped and quoted
        group = "\"%s\"" % group.replace(' ', r'\ ')
        out, err = self._ssh(' '.join([cmd, query_flag, group]))
        return list(filter(None, out.split('\n')))

    def listPlugins(self):
        plugins = self.getPlugins()
        plugin_names = plugins.keys()
        return plugin_names

    # get installed plugins info returned is (name, version, status, file)
    def getPlugins(self):
        # command only available on gerrit verion >= 2.5
        cmd = 'gerrit plugin ls --format json'
        out, err = self._ssh(cmd)
        return json.loads(out)

    def getVersion(self):
        # command only available on gerrit verion >= 2.6
        cmd = 'gerrit version'
        out, err = self._ssh(cmd)
        out = out.split(' ')[2]
        return out.strip('\n')

    def parseGerritVersion(self, version):
        # Adapted from gertty setRemoteVersion()
        base = version.split('-')[0]
        parts = base.split('.')
        major = minor = micro = 0
        if len(parts) > 0:
            major = int(parts[0])
        if len(parts) > 1:
            minor = int(parts[1])
        if len(parts) > 2:
            micro = int(parts[2])
        return (major, minor, micro)

    def replicate(self, project='--all'):
        cmd = 'replication start %s' % project
        if self.installed_plugins is None:
            try:
                self.installed_plugins = self.listPlugins()
            except Exception:
                cmd = 'gerrit replicate %s' % project
        out, err = self._ssh(cmd)
        return out.split('\n')

    def review(self, project, change, message, action={}):
        cmd = 'gerrit review %s --project %s' % (change, project)
        if message:
            cmd += ' --message "%s"' % message
        for k, v in action.items():
            if v is True:
                cmd += ' --%s' % k
            else:
                cmd += ' --%s %s' % (k, v)
        out, err = self._ssh(cmd)
        return err

    def query(self, change, commit_msg=False, comments=False):
        if commit_msg:
            if comments:
                cmd = ('gerrit query --format json --commit-message --comments'
                       ' %s"' % change)
            else:
                cmd = 'gerrit query --format json --commit-message %s"' % (
                    change)
        else:
            if comments:
                cmd = 'gerrit query --format json --comments %s"' % (change)
            else:
                cmd = 'gerrit query --format json %s"' % (change)
        out, err = self._ssh(cmd)
        if not out:
            return False
        lines = out.split('\n')
        if not lines:
            return False
        data = json.loads(lines[0])
        if not data:
            return False
        self.log.debug("Received data from Gerrit query: \n%s" % (
            pprint.pformat(data)))
        return data

    def bulk_query(self, query):
        cmd = 'gerrit query --format json %s"' % (
            query)
        out, err = self._ssh(cmd)
        if not out:
            return False
        lines = out.split('\n')
        if not lines:
            return False

        data = []
        for line in lines:
            if line:
                data.append(json.loads(line))
        if not data:
            return False
        self.log.debug("Received data from Gerrit query: \n%s" % (
            pprint.pformat(data)))
        return data

    def _ssh(self, command):

        try:
            if self.client is None:
                self.client = self.connection.connect()

            self.log.debug("SSH command:\n%s" % command)
            stdin, stdout, stderr = self.client.exec_command(command)

            out = stdout.read().decode('utf8')
            self.log.debug("SSH received stdout:\n%s" % out)

            ret = stdout.channel.recv_exit_status()
            self.log.debug("SSH exit status: %s" % ret)

            err = stderr.read().decode('utf8')
            self.log.debug("SSH received stderr:\n%s" % err)
            if ret:
                raise Exception("Gerrit error executing %s" % command)
            return (out, err)

        except Exception:
            if self.client:
                self.client.close()
                self.client = None
            raise
