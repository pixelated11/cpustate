from pathlib import Path

CPU_BASE = Path("/sys/devices/system/cpu")


def _read(path: Path) -> str:
    try:
        return path.read_text().strip()
    except OSError:
        return "n/a"


def _read_first(glob: str) -> str:
    paths = sorted(CPU_BASE.glob(glob))
    if not paths:
        return "n/a"
    return _read(paths[0])


def show():
    governor = _read_first("cpu0/cpufreq/scaling_governor")
    epp = _read_first("cpu0/cpufreq/energy_performance_preference")
    epp_avail = _read_first("cpu0/cpufreq/energy_performance_available_preferences")
    freq_min = _read_first("cpu0/cpufreq/scaling_min_freq")
    freq_max = _read_first("cpu0/cpufreq/scaling_max_freq")
    freq_cur = _read_first("cpu0/cpufreq/scaling_cur_freq")

    def khz(v: str) -> str:
        try:
            return f"{int(v) // 1000} MHz"
        except ValueError:
            return v

    print("─" * 40)
    print("  cpustate — current CPU power state")
    print("─" * 40)
    print(f"  Governor   : {governor}")
    print(f"  EPP        : {epp}")
    if epp_avail != "n/a":
        print(f"  EPP opts   : {epp_avail}")
    print(f"  Freq (cur) : {khz(freq_cur)}")
    print(f"  Freq range : {khz(freq_min)} – {khz(freq_max)}")

    num_cores = len(list(CPU_BASE.glob("cpu[0-9]*")))
    print(f"  Cores      : {num_cores}")
    print("─" * 40)