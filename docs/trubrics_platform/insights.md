# 🪄 Insights

The user insights page provides quantitative and qualitative analysis on the feedback collected. This allows AI teams to gain understanding of whether users are satisfied or not with predictions, and compare results between different models.

## Analyse quantitative user feedback

Various filters allow AI teams to:

- Aggregate responses by a frequency (hourly, daily, weekly, monthly)
- View all responses for a given score, model or user
- Compare responses for all scores, models or users

!!!tip
    All quantitative analysis is viewed per feedback component. Each feedback component should have a unique set of scores (i.e a unique [type](../feedback_components/#types-of-feedback)) for analysis to be correctly computed.

## Review user comments

User comments are collected in the `text` field of the [Feedback](../feedback_components/#types-of-feedback) response. All comments are listed in the `Comments` tab, and may be grouped together to create an [issue](issues.md).

## Export all raw data

Export a raw json file of all responses allows AI teams to conduct their own analysis. Use the \`📥 Download all\` button for a full export to json.
