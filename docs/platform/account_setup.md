## Create an account

To initially start using [Trubrics](https://trubrics.streamlit.app/), navigate to the `Create an account` tab.

If you have forgotten your password, enter your email on the `Forgot password?` tab to send a password reset email.

!!!tip "Team access"
    [Contact us](https://trubrics.com/contact-us/) to gain access for multiple users of an organisation.

## Projects
All data in [Trubrics](https://trubrics.streamlit.app/) is organised into Projects. It is up to you how you group your projects, but we suggest you create different projects per AI use case. Upon account creation, a `default` project is created.

All user prompts are stored directly within the project, i.e. **there is a single table for user prompts per project**. Prompts can be filtered by model config, prompt template, tags, etc.

## Feedback components
Within a project, you may also create feedback components to organise user feedback. Each component collects a unique [type](./user_feedback.md#types-of-feedback) of feedback. Multiple feedback components can be implemented for the same AI use case.

### Create a feedback component
At the top of the `Feedback` page in [Trubrics](https://trubrics.streamlit.app/), you can create a feedback component. To help you determine what type of feedback to use, there is a visual preview of the UI component, along with the generated code snippet for the component to include into your AI application.

A `default` component is created in the `default` project upon account creation, allowing you to directly start saving prompts and 👍 / 👎 user feedback.
