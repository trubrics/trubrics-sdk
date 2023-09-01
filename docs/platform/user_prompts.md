## Saving prompts to Trubrics
Analysing user prompts is essential to building AI models that aligns with your users. Upon creating an account with [Trubrics](https://trubrics.streamlit.app/), you can start logging prompts & model generations to the `default` project. Create different projects to organise your prompts (we recommend one project per use case).

Install Trubrics with:

```console
pip install trubrics
```

Set [Trubrics](https://trubrics.streamlit.app/) `email` and `password` as environment variables:

```bash
export TRUBRICS_EMAIL="trubrics_email"
export TRUBRICS_PASSWORD="trubrics_password"
```

and push some user prompts to the `default` project:

```python
import os
from trubrics import Trubrics

trubrics = Trubrics(
    project="default",
    email=os.environ["TRUBRICS_EMAIL"],
    password=os.environ["TRUBRICS_PASSWORD"],
)

prompt = trubrics.log_prompt(
    config_model={{
        "model": "gpt-3.5-turbo",
        "prompt_template": "Tell me a joke about {{animal}}",
        "temperature": 0.7,
    }},
    prompt="Tell me a joke about sharks",
    generation="Why did the shark cross the ocean? To get to the other side."
)
```

!!!note "`trubrics.log_prompt()` arguments"
    :::trubrics.Trubrics.log_prompt

### Saving prompts from Streamlit apps

The `FeedbackCollector` Streamlit integration inherits from the `Trubrics` object, meaning that you can log prompts in the same way directly from the `FeedbackCollector`. For more information on this, see the [Streamlit integration](../integrations/streamlit.md) docs.

## Analyse prompts in Trubrics

Various filters allow AI teams to explore user prompts in Trubrics, and export them to csv.

!!!tip "[Beta] Ask an LLM about your prompts"
    Try asking an LLM a question about the user prompts in your dataset. For example, "What prompts ask for shark jokes?". This feature is in beta, so please give us feedback on the model generations!
