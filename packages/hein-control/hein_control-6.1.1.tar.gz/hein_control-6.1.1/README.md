# Hein Experiment Control

`hein_control` is a collection of code for automating and scheduling tasks related to experiment monitoring. The 
Experiment Scheduler module (`hein_control.scheduler`) contains code for scheduling actions at given time spacing 
with a focus on reaction monitoring.  

## Experiment Scheduler 

This repository contains code for "Experiment Schedulers" which will perform "actions" (Python functions) at user-defined 
time points. This package has no dependencies beyond the Python standard library. 

For example, performing the function `perform_sampling_sequence` 5 times at 60 second intervals then 10 
times at 300 second intervals. At the moment, action functions are user-defined, but a planned feature is to have built-in
methods for standard operations like direct-inject sequences. An example script has been provided to illustrate basic 
usage (please see `example_scheduler_script.py`). 

### Current workflow: 
1) The user defines action function(s) to perform
2) The `SamplingScheduler` is instantiated, providing those functions in the order they are to be executed 
3) Time points are added with one of: 

    a) `.insert_time_point`: inserts a single time point
    b) `.insert_time_point_list`: inserts a list of time points
    c) or `.insert_time_point_list_pairs`: inserts a sequence of time point list pairs (e.g. 6 times 60 seconds, then 
       10 times 120 seconds, etc.)
    
4) The `SamplingScheduler` sequence is started with `SamplingScheduler.start_sequence()`

### Notes
- A running `SamplingScheduler` instance may be paused with `SamplingScheduler.pause_sequence()`
- A `SamplingScheduler` instance may be manually triggered at any time (a time point is automatically created with its 
  associated metadata)
- When executing in a script, `SamplingScheduler.join()` should be placed at the end of the script to prevent 
    premature exit. 

### Modules and Classes

#### Actions

The `action.SchedulerAction` class represents callable functions with default arguments and keyword arugments for calling. 
"Action" methods (any callable) are registered with `SchedulerAction.register_action(callable)` and may then be associated with any 
Scheduler instance. 

The `action.TrackedAction` class wraps the above class to handle execution and storage of runtime metadata: 
 - `.time_started`: time when the action was started
 - `.time_completed`: time when the action was completed
 - `.started_timestamp`: `datetime.datetime` timestamp for when the action was started
 - `.action_duration`: duration of the action
 - `.name`: action name
 - `.status`: string status of the action execution
 - `.method_return`: any return from the method upon completion 

#### Time Points

There are two classes in the `.timepoint` module: `TimePoint` and `ActionTimePoint`. The former is for denoting that an 
action occurred at a given time, and the latter is for managing a sequence of actions at a given time. Any number of 
actions may be associated with an `ActionTimePoint` instance and they will be performed in the order provided. A variety 
of properties are available for retrieving metadata associated with the actions of a time point.  

Time points are triggered by either calling the class instance or by calling `.trigger()`. Keyword argument 
passthrough is supported, but has some restrictions as the keywords must be provided as dictionaries keyed by their 
respective function names. 

## Automation

The aim of the Automation class is to create a class that makes it easier to put together an automation sequence.

An `Automation` instance is callable. When called, it will run the first `Step`, get the `next_step` from that first
 step, and loop through running and retrieving the next Step to run, until there are no more `Steps` to run.

The possible Steps that can be used are: `CustomStep` and `IfStep`. For the `IfStep` to work, you need to make
`ConditionCheck` instances.

### Current workflow

The way that an Automation and the Steps for an Automation need to be scripted up is specific to ensure everything
works.

There is an [example_automation_script](example_automation_script.py) for reference of how to use the `Automation`
 module.

These are the main rules:
* An `Automation` instantiation MUST include a dictionary of arguments and initial values to be used by the Steps
    in the `Automation`, unless no variables need to be passed between/used by multiple `Steps`
* The parameter names for all the functions of `CustomSteps` must be identical to the keys, in the `kwargs`
    dictionary that get passed into an Automation instance on instantiation
* The return value of any `CustomStep` must be a dictionary, with the keys being identical to the keys in the
    `kwargs` dictionary of the `Automation` instance, and the values are the updated values
* All these functions for the `CustomSteps` must also have a `**kwargs parameter`, to catch arguments that get passed
    through that are not actually required by the functions.
* An Automation instance must know what the first step to run is

### Modules and classes

#### Automation

The `Automation` class is important, because all the arguments for all the `Steps` must be passed into the
    `Automation` on instantiation, and these arguments may potentially be updated by the `Steps`. All these arguments for
    the `CustomSteps` must be passed into an `Automation` sequence as a dictionary, where the keys are the argument names
    and the values are the initial values for these arguments. These arguments get stored as `self.kwargs` in the
    Automation instance, and `self.kwargs` gets used as the arguments to run the `CustomSteps`. If the `CustomStep` run
    function has a return value, it MUST be a dictionary, where the keys are argument names (that must correspond to
    a key in the `self.kwargs` dictionary of the `Automation` instance), and the values are the new values for the
    arguments; and in this way the arguments for the `Automation` instance can be updated.

#### Step

A step in an automation sequence. An instance of a `Step` should not be created, instead one of the subclasses
    should be instantiated.

A `Step` can be bypassed (skipped over).

A `Step` will have a `next_step`, which is another `Step` or `None`; in this way,
steps in an `Automation` can be linked, and different work flows can be created.

A `Step` is also callable. The details of this will depend on the specific subclass.

##### CustomStep

A `Step` that could have a return value after the callable has been executed; the return type must be a dictionary
where keys are argument names (identical to the arguments of the parameters of the callable and therefore also identical
 to the keys in the dictionary used when an `Automation` is instantiated), and the values are the new value they
 should take. See the `Automation` class as to
why this is important.

##### IfStep

A `Step` in an automation sequence that has multiple possible next steps, which is decided based on a list of
`ConditionChecks`. If the return of the first `ConditionCheck` is `True`, then the next step of the `IfStep` is
 the `next_step` of the `ConditionCheck`. If the bool is `False`, then iterate through the list of `ConditionChecks`
  until a condition returns `True`. If none of them return `True`, then the last `ConditionCheck` in the list is
   assumed to be `True` (essentially it is like the `else` in an `if-elif-...-else` block).

##### ConditionCheck

A `Step` that, when executed, returns a `bool`. It is used by the `IfStep` to know what the `next_step` in an
`Automation` instance should be.
