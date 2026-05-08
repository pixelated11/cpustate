import sys


def merge(config: dict, profile_name: str | None) -> dict:
    """Merge a named profile on top of the base config."""
    if profile_name is None:
        return config

    profiles = config.get("profiles", {})
    if profile_name not in profiles:
        print(f"[cpustate] Profile '{profile_name}' not found in config.")
        print(f"[cpustate] Available: {', '.join(profiles) or 'none'}")
        sys.exit(1)

    overrides = profiles[profile_name]
    merged = {k: v for k, v in config.items() if k != "profiles"}

    for section, values in overrides.items():
        if section in merged and isinstance(merged[section], dict):
            merged[section] = {**merged[section], **values}
        else:
            merged[section] = values

    return merged


def list_profiles(config: dict):
    profiles = config.get("profiles", {})
    if not profiles:
        print("[cpustate] No profiles defined in config.")
        return

    print("Available profiles:")
    for name, values in profiles.items():
        keys = ", ".join(
            f"{k}={v}"
            for section_vals in values.values()
            for k, v in (section_vals.items() if isinstance(section_vals, dict) else {}.items())
        )
        print(f"  {name:<16} {keys}")