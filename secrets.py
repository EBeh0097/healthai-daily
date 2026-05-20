import os
from dotenv import load_dotenv

load_dotenv()

def get_secret(secret_name: str, default: str | None = None) -> str | None:
    """
    Loads secrets in this order:
    1. Environment variables / local .env
    2. Streamlit secrets, if running in Streamlit
    3. Google Secret Manager, if GOOGLE_CLOUD_PROJECT_ID is available

    This prevents hardcoding API keys in source code.
    """
    value = os.getenv(secret_name)
    if value:
        return value

    try:
        import streamlit as st
        if secret_name in st.secrets:
            return st.secrets[secret_name]
    except Exception:
        pass

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        try:
            import streamlit as st
            project_id = st.secrets.get("GOOGLE_CLOUD_PROJECT_ID")
        except Exception:
            project_id = None

    if project_id:
        try:
            from google.cloud import secretmanager
            client = secretmanager.SecretManagerServiceClient()
            name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
            response = client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        except Exception:
            return default

    return default
