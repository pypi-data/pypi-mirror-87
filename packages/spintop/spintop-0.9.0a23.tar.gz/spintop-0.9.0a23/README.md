# Attach a Data Analysis Pipeline

A data analysis pipeline is a function that takes a message as argument and returns nothing.

```python

from spintop import Spintop
from spintop.messages import PersistenceRecordsUpdateMessage

def my_pipeline(message: PersistenceRecordsUpdateMessage):
    env = message.env

spintop = Spintop()
spintop.records.update_message.subscribe(my_pipeline)

```

## Integration with Spintop Data Analysis pipeline

```python
from spintop_da.pipelines import dut_states_pipeline

spintop.records.update_message.subscribe(dut_states_pipeline())


```

## Integration with Spintop-OpenHTF (sync)

```python

from spintop_openhtf import TestPlan

plan = TestPlan()

spintop = plan.enable_spintop(spintop=None)
spintop.records.update_message.subscribe(dut_states_pipeline())

```

## Integration with Spintop-OpenHTF (async)

```python

from spintop_openhtf import SpintopUpdater

updater = SpintopUpdater(spintop=None)
updater.update_from_results(folder=None) # Use normal storage location

```