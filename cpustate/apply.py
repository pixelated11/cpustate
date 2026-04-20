import shutil
import subprocess
import logging
from pathlib import Path

log = logging.getLogger("cpustate")
logging.basicConfig(format="[cpustate] %(message)s", level=logging.INFO)

CPU_BASE = Path("/sys/devices/system/cpu")


def is_ryzen_mobile() -> bool:
    try:
        info = Path("/proc/cpuinfo").read_text()
        return "AuthenticAMD" in info and "Ryzen" in info
    except OSError:
        return False


def apply_governor(config: dict):
    governor = config.get("cpu", {}).get("governor")
    if not governor:
        return

    paths = list(CPU_BASE.glob("cpu[0-9]*/cpufreq/scaling_governor"))
    if not paths:
        log.warning("scaling_governor sysfs not found — governor skipped")
        return

    failed = 0
    for path in paths:
        try:
            path.write_text(governor)
        except OSError as e:
            log.warning(f"Could not write governor to {path}: {e}")
            failed += 1

    if failed == 0:
        log.info(f"Governor set to '{governor}' on {len(paths)} cores")
    else:
        log.warning(f"Governor: {len(paths) - failed}/{len(paths)} cores updated")


def apply_epp(config: dict):
    epp = config.get("cpu", {}).get("epp")
    if not epp:
        return

    paths = list(CPU_BASE.glob("cpu[0-9]*/cpufreq/energy_performance_preference"))
    if not paths:
        log.info("EPP not supported on this CPU — skipping")
        return

    failed = 0
    for path in paths:
        try:
            path.write_text(epp)
        except OSError as e:
            log.warning(f"Could not write EPP to {path}: {e}")
            failed += 1

    if failed == 0:
        log.info(f"EPP set to '{epp}' on {len(paths)} cores")
    else:
        log.warning(f"EPP: {len(paths) - failed}/{len(paths)} cores updated")


def apply_ryzenadj(config: dict):
    rz = config.get("ryzenadj", {})
    if not rz:
        return

    if not shutil.which("ryzenadj"):
        log.warning("ryzenadj not found in PATH — TDP limits skipped")
        log.warning("Install 'ryzenadj' (AUR: ryzenadj-git) to enable this feature")
        return

    args = ["ryzenadj"] + [f"--{k}={v}" for k, v in rz.items()]
    log.info(f"Running: {' '.join(args)}")

    try:
        result = subprocess.run(args, check=True, capture_output=True, text=True)
        log.info("ryzenadj applied successfully")
        if result.stdout.strip():
            log.info(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        log.error(f"ryzenadj failed (exit {e.returncode})")
        if e.stderr:
            log.error(e.stderr.strip())


def apply_all(config: dict):
    log.info("Applying CPU state...")
    apply_governor(config)
    apply_epp(config)

    if is_ryzen_mobile():
        apply_ryzenadj(config)
    elif config.get("ryzenadj"):
        log.info("ryzenadj section found but CPU is not Ryzen mobile — skipping")

    log.info("Done.")