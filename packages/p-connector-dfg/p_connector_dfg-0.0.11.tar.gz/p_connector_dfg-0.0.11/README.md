## Introduction
This project implements the connector method proposed in the paper [Supporting Confidentiality in Process Mining Using Abstraction and Encryption](https://www.researchgate.net/publication/338432872_Supporting_Confidentiality_in_Process_Mining_Using_Abstraction_and_Encryption) and [Ensuring Confidentiality in Process Mining](https://www.researchgate.net/publication/330042256_Ensuring_Confidentiality_in_Process_Mining).
## Python package
The implementation has been published as a standard Python package. Use the following command to install the corresponding Python package:

```shell
pip install p-connector-dfg
```

## Usage

```python
from p_connector_dfg.privacyPreserving import privacyPreserving

ela_path = ".\intermediate_results\ela_connector.xml"
ela_method = "Connector Method"
ela_desired_analyses = ['directly follows graph', 'process discovery']

activity_activity_matrix_path = r".\intermediate_results\test.csv"

dfg_path = "./DFG.svg"
freq_threshold = 0.0

#Connector structure parameters--------------
relation_depth = True #if you want to have relation depth in the connector structure
trace_length = True # if you want to have trace length in the connector structure
trace_id = True # if you want to have a fake trace id in the connector structure

event_log = "sample_log.xes"
key = 'DEFPASSWORD12345'

pp = privacyPreserving(event_log)
pp.apply_privacyPreserving(key, ela_path, ela_method, ela_desired_analyses, event_log, relation_depth = relation_depth, trace_length = trace_length, trace_id = trace_id)

pp.result_maker_ela(ela_path, True,True, True, freq_threshold, dfg_path, activity_activity_matrix_path = activity_activity_matrix_path,key = key)
```
