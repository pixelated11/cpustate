import argparse
import sys
from cpustate import config, apply, status, profiles


def main():
    parser = argparse.ArgumentParser(
        prog="cpustate",
        description="Persist CPU power settings across boot and sleep."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_apply = sub.add_parser("apply", help="Apply settings from config")
    p_apply.add_argument("--profile", "-p", default=None, help="Named profile to apply")

    sub.add_parser("status", help="Show current CPU power state")
    sub.add_parser("edit", help="Open config in $EDITOR")
    sub.add_parser("list-profiles", help="List available profiles")
    sub.add_parser("daemon", help="Internal: called by systemd (same as apply)")

    args = parser.parse_args()

    if args.command in ("apply", "daemon"):
        profile = getattr(args, "profile", None)
        cfg = config.load()
        merged = profiles.merge(cfg, profile)
        apply.apply_all(merged)

    elif args.command == "status":
        status.show()

    elif args.command == "edit":
        config.edit()

    elif args.command == "list-profiles":
        cfg = config.load()
        profiles.list_profiles(cfg)


if __name__ == "__main__":
    main()