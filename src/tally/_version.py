# This file is auto-generated during build. Do not edit manually.
VERSION = "0.1.0"
GIT_SHA = "unknown"
REPO_URL = "https://github.com/davidfowl/tally"


def check_for_updates(timeout: float = 2.0) -> dict | None:
    """Check GitHub for a newer version.

    Returns dict with 'latest_version' and 'update_available' keys,
    or None if check fails or current version is unknown.
    """
    import urllib.request
    import json

    # Don't check if we're running a dev/unknown version
    if VERSION in ("unknown", "dev", "0.1.0"):
        return None

    try:
        # Extract owner/repo from REPO_URL
        # Expected format: https://github.com/owner/repo
        parts = REPO_URL.rstrip('/').split('/')
        if len(parts) < 2:
            return None
        owner, repo = parts[-2], parts[-1]

        api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

        req = urllib.request.Request(
            api_url,
            headers={
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': f'tally/{VERSION}'
            }
        )

        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode('utf-8'))
            latest_tag = data.get('tag_name', '')

            # Remove 'v' prefix if present
            latest_version = latest_tag.lstrip('v')

            # Compare versions (simple string comparison works for our format: 0.1.X)
            update_available = _version_greater(latest_version, VERSION)

            return {
                'latest_version': latest_version,
                'current_version': VERSION,
                'update_available': update_available,
                'release_url': data.get('html_url', f'{REPO_URL}/releases/latest')
            }
    except Exception:
        # Network error, timeout, or API error - fail silently
        return None


def _version_greater(v1: str, v2: str) -> bool:
    """Return True if v1 > v2 using semantic versioning comparison."""
    try:
        def parse_version(v: str) -> tuple:
            parts = v.split('.')
            return tuple(int(p) for p in parts[:3])

        return parse_version(v1) > parse_version(v2)
    except (ValueError, IndexError):
        return False
