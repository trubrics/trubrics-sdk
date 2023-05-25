## Trubrics feedback with Flask

Set environment variables for platform connection:
```bash
export TRUBRICS_CONFIG_EMAIL="guest@trubrics.com"
export TRUBRICS_CONFIG_PASSWORD=
export TRUBRICS_PROJECT_NAME="flask example"
```

Run demo flask app:

```bash
flask --app examples/feedback_apps/flask/app.py --debug run
```
