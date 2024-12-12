# starpy
Python implementation of the [STAR Voting](https://www.starvoting.org/) system.

## Getting started
Install the required packages

```shell
pip install .
```

## Usage
### Single winner STAR
To run a single winner election create a pandas dataframe of the ballot data and pass it into the STAR function

```python
from starpy.STAR import STAR
import pandas as pd
ballots = pd.DataFrame(columns=['Allie', 'Billy', 'Candace'],
                       data=[*2*[[5,      4,       0]],
                             *1*[[2,      5,       1]],
                             *2*[[0,      4,       5]],])
results = STAR(ballots)
print(results['elected'])
```

### Multi-winner Bloc STAR
To run a multi-winner bloc STAR race, set the input parameter `numwinners`
```python
results = STAR(ballots, numwinners=2)
```

### Multi-winner Proportional STAR
To run proportional STAR
```python
from starpy.Allocated_Score import Allocated_Score 
import pandas as pd
numwinners=2
ballots = pd.DataFrame(columns=['Allie', 'Billy', 'Candace'],
                       data=[*2*[[5,      4,       0]],
                             *1*[[2,      5,       1]],
                             *2*[[0,      4,       5]],])

winner_list = Allocated_Score(5, numwinners, ballots)
print(winner_list)
```
