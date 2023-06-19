from loguru import logger

from trubrics.feedback.dataclass import Feedback
from trubrics.trubrics_platform.auth import (
    TrubricsConfig,
    expire_after_n_seconds,
    get_trubrics_auth_token,
)
from trubrics.trubrics_platform.firestore import (
    list_components_in_organisation,
    record_feedback,
)


def save_to_trubrics(trubrics_config: TrubricsConfig, feedback: Feedback) -> dict:
    auth = get_trubrics_auth_token(
        trubrics_config.firebase_api_key,
        trubrics_config.email,
        trubrics_config.password.get_secret_value(),
        rerun=expire_after_n_seconds(),
    )
    components = list_components_in_organisation(firestore_api_url=trubrics_config.firestore_api_url, auth=auth)
    if feedback.component_name not in components:
        logger.error(
            f"Component '{feedback.component_name}' not found in organisation"
            f" '{trubrics_config.firestore_api_url.split('/')[-1]}'. Components currently available: {components}."
        )
        raise ValueError("Component doesn't exist.")
    res = record_feedback(
        auth,
        firestore_api_url=trubrics_config.firestore_api_url,
        document_dict=feedback.dict(),
    )
    if "error" in res:
        logger.error(res["error"])
    else:
        logger.info("Feedback response saved to Trubrics.")

    return res
