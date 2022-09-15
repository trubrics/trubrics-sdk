```py
from trubrics.context import DataContext
data_context = DataContext(
    testing_data=test_df,  # pandas dataframe of data to test against a model
    target="target_column_name_in_test_df"
)
```
