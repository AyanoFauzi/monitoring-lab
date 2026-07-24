from prometheus_client import multiprocess


def child_exit(server, worker):
    # Bersihkan jejak worker yang berhenti agar totalnya tetap akurat.
    multiprocess.mark_process_dead(worker.pid)
