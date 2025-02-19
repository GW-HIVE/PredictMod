from django.conf import settings

import logging

logger = logging.getLogger()

from ui.models import ReleasedModel


def get_anlaysis_urls():
    try:
        models = ReleasedModel.objects.all()
        model_routing = {m.name: f"http://{m.backend}:4243" for m in models}
        # Shim for the pipeline
        model_routing["pipeline"] = "http://automated-pipeline:4243"
        return model_routing
    except Exception as e:
        logger.critical("=" * 80)
        logger.critical(f"Exception: {e}")
        logger.critical("=" * 80)
        return {"None": "No models found in database"}


ANALYSIS_BACKENDS = get_anlaysis_urls()


def lookup_backend(model_name: str):
    if settings.DJANGO_MODE == "dev":
        return "http://localhost:5000"
    de_modified_model_name = model_name.replace("-", " ")
    logger.debug("-" * 40)
    logger.debug(f"ANALYSIS BACKENDS: {ANALYSIS_BACKENDS}")
    logger.debug(f"Searching for {de_modified_model_name}")
    logger.debug("-" * 40)
    return ANALYSIS_BACKENDS.get(de_modified_model_name, None)
