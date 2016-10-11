# StackStorm vADC Pack

This pack is designed to manage vTMs via a Brocade Services Director. 

You can also manage individual vTMs directly, if you don't use Services
Director, but you will need to set brcd\_sd\_proxy to false and supply
appropriate brcd\_vtm\_\* config keys. See Configuration section below.

## Configuration File

You must create a config yaml in:  /opt/stackstorm/configs/vadc.yaml 
```
---
  brcd_sd_proxy: true
  brcd_sd_host: "https://sd1.management.local:8100/"
  brcd_sd_user: "admin"
  brcd_sd_pass: "password"
  brcd_vtm_host: ""
  brcd_vtm_user: ""
  brcd_vtm_pass: ""
```

You only need to provide the brcd\_vtm\_\* values if you plan on calling
the vTMs directly.

The values can be static as above, or dynamic values as below: 
```
  brcd_sd_proxy: "{{system.brcd_sd_proxy}}"
  brcd_sd_host: "{{user.brcd_sd_host}}"
  brcd_sd_pass: "{{user.brcd_sd_pass}}"
```

**Note: You can't use "user" scoped keys with sensors**
Sensors can only access system level keys. So if you want to use the
BSD Status Sensor below, then you'll need to use static keys or
Dynamic Keys in the system scope.

See: https://github.com/StackStorm/st2/issues/2678

## Setting Dynamic Keys

Dynamic user values can be set with (for example):
```
    st2 key set --scope=user brcd_sd_host "https://sd1.brcd.local:8100/"
    st2 key set --scope=user brcd_sd_user "admin"
    st2 key set --scope=user brcd_sd_pass "password" --encrypt
```

## BSD Status Sensor

This pack includes a sensor to monitor errors reported by the Services
Director, and a rule which then reports those errors to ChatOps. 

If you have ChatOps enabled, then take a look at the rule and modify it
to suit your needs. Then enable the rule with:

```
st2 rule enable vadc.bsd_monitor
```

Alternatively you can edit rules/bsd_monitor.yaml and set:
```
  enabled: true
```

## Actions Included

Actions in the pack have required and optional paramaters. To get more
information about a specific action, you can use --help. For example:
```
st2 run vadc.bsd_list_vtms --help
```

The pack includes actions which manipulate or retrieve data from the
Services Director and also actions which configure the vTM itself. A
brief overview of the actions follow, but please use the --help system
for full details of an Action.

_BSD Actions_

  * bsd\_get\_errors
    Retrieve errors from the Services Director.
    Returns a dictionary of failures

  * bsd\_get\_status
    retrieve status from the Services Director. You can optionally
    supply the instanceID/Tag of a specific vTM to get status of only
    that instance.
    Returns a list of Status for all vTMs (or just one).

  * bsd\_license\_vtm
    Create an instance in the Services Director to license a vTM
    You must provide vtm=<tag> and bw=<licensed bandwidth>

  * bsd\ unlicense\_vtm
    Mark a vTM instance as Deleted in the Services Director.
    You must provide a vtm=<tag|ID> parameter.

  * bsd\_list\_vtms 
    Retrieve the licensed vTMs from the Service Director. This returns
    a limited amount of information by default, but can provide more
    with full=true.
 
_vTM Actions_

All of these actions are designed to proxy through the Services
Director, so a vtm parameter is always required. However it isn't used
if brcd\_sd\_proxy is set to false.

  * vtm\_add\_pool
    Create a pool on a vTM. You must provide the vtm, nodes, and name

  * vtm\_add\_tip
    Create a Traffic Ip Group on the vTM. You must provide the vtm,
    name, a list of IP addresses, and a list of vTMs

  * vtm\_add\_vserver
    Create a Virtual Server on the vTM. You must provide the vtm, name,
    pool, and TIP Group.

  * There is also a delete action for all of the add actions above.

  * vtm\_drain\_nodes
    Mark a list of nodes as draining, or undrain the nodes in a pool.
    You must provide the vtm, name, and a list of nodes. By default we
    drain nodes, but you can pass drain=false to undrain them.

  * vtm\_get\_pool\_nodes
    Retrieve a list of nodes from the given pool. You must provide the
    vtm and the name of the pool.

_Chains and workflows_

A couple of example workflows and chains are provided in the pack. They
both create and delete a service comprised of a pool, vserver and tip.

## Aliases Included

Aliases are used to present command aliases to ChatOps, a number are
included for ChatOps integration

__TODO__ List Aliases

