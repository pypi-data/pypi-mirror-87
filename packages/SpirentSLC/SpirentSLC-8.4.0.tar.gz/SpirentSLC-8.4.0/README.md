# Spirent Session Control Library

The Spirent Session Control Library is used to control iTest sessions to enable quick and easy interaction with devices from a Python script. These target devices/APIs may be defined either on the fly, or via session profiles defined in iTest projects.

## How to run

The simplest way is as follows:

* Download the latest Velocity Agent

* Run it like this
    ./velocity-agent --agentVelocityHost localhost --sfAgentServerPort 9005 --listeningMode --sfAgentDisableSslValidation

* Write python scripts using SLC
   Example script could be found and executed here:
    `python example.py`

## Documentation

### Modes of Operation

The Python Session Control Library is used to control iTest sessions to enable quick and easy interaction with devices from a Python script. These target devices/APIs may be defined either on the fly, or via session profiles defined in iTest projects.

The library may operate in either one of these modes:

* Standalone on a workstation
* Connected to an iTest GUI instance

#### Initialization

##### Standalone

Ensure that the following environment variables are set on the workstation that the library is installed on and that the script will run on:

```bash
  SPIRENT_SLC_HOST=local
  ITAR_PATH=path #to folder where iTars are placed
```

It is also legal to not have the `SPIRENT_SLC_HOST` environment variable, in which case local is assumed.

`ITAR_PATH` is set on the local environment to point to a folder where iTars and exploded project folders are placed, so that the local execution agent can find projects. It is not necessary to set this when connecting to a running instance of iTest GUI or Velocity.

```python
from SpirentSLC import SLC
slc = SLC.init()
```

Once the library is imported, calling `SLC.init()` will initialize the underlying execution agent as a background process which the library will communicate with. An object is returned which is the entry point for further communication with the library. In this release only one `init()` call may be made within one Python interpreter context.

An exception will be thrown if unable to initialize the library.

##### iTest GUI

Ensure that the following environment variables are set on the workstation that the library is installed on and that the script will run on:

```bash
SPIRENT_SLC_HOST=localhost:port  # must be host and port of the configured instance of iTest GUI
SPIRENT_SLC_PASSWORD=xxxx
```

An instance of iTest must be running on the specified host and must be configured to accept connections at the desired port. A password may be optionally configured to restrict access to that instance, in which case the `SPIRENT_SLC_PASSWORD` environment variable must be specified, or provided in the init() call.

```python
from SpirentSLC import SLC
slc = SLC.init() # will take all values from environment variables
```

alternatively values may be provided in the init() call:

```python
slc = SLC.init(host='localhost:3030', password='xxx')
```

An exception will be thrown if the library is unable to connect to the iTest GUI instance.

##### Automatic Agent launching

By specification `SPIRENT_SLC_AGENT_PATH` environment variable pointing to iTest Agent folder it is possible to configure SLC to automatically start instance of new agent.

```bash
SPIRENT_SLC_AGENT_PATH=path #to agent folder
ITAR_PATH=path #to folder where iTars are placed
````

```python
from SpirentSLC import SLC
slc = SLC.init()
```

##### Working With Projects

Once initialized, the library will have access to all available iTest Projects.
Each project contains a number of entities that can be addressed via code.
These include Session Profiles, and Topologies.

###### Listing Projects

```python
slc.list()
==> ['topologies', 'session_profiles']
```

All spaces in the name of a project or any other characters that are not legal in a Python identifier will be replaced by underscores in the returned values.

###### Importing Projects

Projects need to be imported first before being used. Since "import" is a reserved word in Python we will call it "open". This can be done via the following code:

```python
proj = slc.open('project_name')
```

Multiple projects can be imported if needed

```python
sessions = slc.open('my_sessions')
response_maps = slc.open('response_maps')
```

###### Querying a Project

* list all the usable topologies and session profiles in the project
  ```python
  proj.list()
  ==> ['dut1_ffsp', 'lab1_setup_tbml']
  ```
* list other types of assets, such as parameter files and response maps
  ```python
  proj.list(parameter_file=True, response_map=True)
  ==> ['dut1_ffsp', 'lab1_setup_tbml', 'main_setup_ffpt', 'response_map1_ffrm']
  ```
* show all QuickCalls available on a given session profile
  ```python
  proj.dut1_ffsp.list()
  ==> {
    'init_routes': {
      'all': 'True if all routes should be initialized'
    },
    'do_something_cool': {
      'param': 'Description of parameter'
    }
  }
  ```
* access help on QuickCalls on a session attached to a resource in a topology
  ```python
  proj.lab1_setup_tbml.router1.ssh.list()
  ==> { ... same as above }
  ```

* access the list of parameters for a specific QuickCall
  ```python
  proj.dut1_ffsp.list('init_routes')
  ==> { 'all': 'True if all routes should be initialized' }
  ```
  Built in session actions are not listed, only QuickCalls if a QuickCall library is attached to the session profile.

  If the user is accessing a built-in session type such as Telnet or SSH, they may still invoke the actions, but they will not be listed by the list() call.

  It should be noted that all displayed QuickCall names will by transformed into snake-case to conform to Python naming conventions.
  Working With Sessions

  ###### Opening a Session

  Sessions are opened either directly on a session profile or local topology.
* open session on a session profile
  ```python
  s1 = proj.dut1_ffsp.open()
  ```

* open session, giving required parameters
  ```python
  s1 = proj.rest_session_ffsp.open(url='https://my_site.my_domain.com', accept_all_cookies=True)
  ```
* open session, using parameter file
  ```python
  s1 = proj.rest_session_ffsp.open(parameter_file=proj.main_setup_ffpt)
  ```
* open session, specify a response map to use
  ```python
  s1 = proj.rest_session_ffsp.open(response_map=proj.response_map1_ffrm)
  ```
* open session, specify a reponse map library to use
  ```python
  s1 = proj.rest_session_ffsp.open(response_map_lib=resp_lib)
  ```
* open session, specifying additional session properties
  ```python
  s1 = proj.rest_session_ffsp.open(properties={'authentication.authentication': 'Basic', 'authentication.user': 'me', 'authentication.password': 'totes_secret!'})
  ```
* open session on a resource in a local topology
  ```python
  s1 = proj.lab1_setup_tbml.router1.ssh.open(...) # may use any combination of parameters, parameter_file, agent_requirements, properties
  ```

###### Opening a Native Session Type Directly (Not supported in 6.2)

It is possible to open a session directly without having a underlying session profile or topology file to start with.

* open the native ssh session type directly, supplying required session profile information
  ```python
  s1 = slc.sessions.ssh.open(ip_address='10.20.30.40')
  ```
  Session Information
  Once a session is opened it is possible to find out some basic information about where the session is being handled. This is done via the agent property of a session object.
  ```python
  s1.agent
  ==> {
    'agent_type': 'local', # may be local, iTestGUI, or Velocity
    'name': 'agent_identifier',
    'capabilities': {...} # set of agent capabilities
  }
  ```

##### Invoking Actions on Session

An active session has a number of actions defined on it, which may be either built-in actions or QuickCalls defined on that session type. Any of those can be invoked on the session.

* invoke the init_routes QuickCall with one parameter
  ```python
  response = s1.init_routes(all=True)
  ```
* invoke a built-in action with a specific response map (which may override what was set for the session as a whole)
  ```python
  response = my_ssh_session.command('ls', response_map=proj.response_map_ls_ffrm)
  ```
  Response
  The resulting response object can be used to query details about the action execution as well as the response itself:
* duration of execution and any error status
  ```python
  response.duration
  ==> 3 # number of seconds
  response.result
  ==> 'success' # may be success, failed, timeout
  ```

* textual rendering of the response
  ```python
  response.text
  ==> 'textual response data'
  ```

* if the response is json, it is easier to grab the json directly as a dictionary
  ```python
  response.json
  ==> instance of dictionary # null if not available as json
  ```

* likewise if the response is xml it can be accessed directly as XML
  ```python
  response.xml
  ==> instance of xml.etree.ElementTree # null if not available as XML

  response.data
  ==> { dictionary of elements that exist in step structured data }
  ```

##### Queries

The response object may also have queries defined on it - methods that query the structured data and return values. Queries may be auto-generated in iTest or be defined in response maps.

* list the set of queries that exist for the response
  ```python
  response.queries()
  ==> [ 'is_empty()', 'counter_by_row(row)' ]
  ```

* invoke query
  ```python
  response.counter_by_row(3)
  ==> 35
  ```
  Query names are always converted to snake case.

##### Closing a Session

Sessions should be closed when no longer needed, as they consume resources on the agent (and on Velocity if being used.) It is especially important to close sessions if sessions are being opened within a loop.

* close session and free resources
  ```python
  s1.close()
  ```

##### Shutdown

Proper shutdown of the library is important to ensure timely release of resources.

* release all resources used by the library
  ```python
  slc.close()
  ```
  Resources released include all remaining open sessions, all reservations initiated by the script, and (if local) the underlying execution agent.
