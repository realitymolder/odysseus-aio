#!/bin/sh
set -e

PUID="${PUID:-1000}"
PGID="${PGID:-1000}"
GOSU_BIN="$(command -v gosu)"
PYTHON_BIN="$(command -v python)"

if ! getent group "$PGID" >/dev/null 2>&1; then
    groupadd -g "$PGID" odysseus
fi
if ! getent passwd "$PUID" >/dev/null 2>&1; then
    useradd -u "$PUID" -g "$PGID" -M -s /bin/sh -d /app odysseus
fi

mount_root_for() {
    awk -v target="$1" '$5 == target { print $4; exit }' /proc/self/mountinfo 2>/dev/null || true
}

is_broad_mount_root() {
    case "$1" in
        /|/home|/srv|/var|/usr|/opt|/tmp|/mnt|/media)
            return 0
            ;;
    esac
    return 1
}

repair_tree_ownership() {
    dir="$1"
    if [ -d "$dir" ]; then
        find "$dir" -xdev -not -uid "$PUID" -print0 2>/dev/null \
            | xargs -0 -r chown "$PUID:$PGID" 2>/dev/null || true
    fi
}

repair_app_tree_ownership() {
    if [ -d /app ]; then
        find /app -xdev \
            \( -path /app/data -o -path /app/logs -o -path /app/.ssh -o -path /app/.cache -o -path /app/.local \) -prune \
            -o -not -uid "$PUID" -print0 2>/dev/null \
            | xargs -0 -r chown "$PUID:$PGID" 2>/dev/null || true
    fi
}

repair_bind_mount_ownership() {
    dir="$1"
    if [ ! -d "$dir" ]; then
        return
    fi

    mount_root="$(mount_root_for "$dir")"
    if is_broad_mount_root "$mount_root"; then
        echo "Skipping recursive ownership repair for $dir because it maps to broad host path $mount_root" >&2
        chown "$PUID:$PGID" "$dir" 2>/dev/null || true
        return
    fi

    repair_tree_ownership "$dir"
}

repair_app_tree_ownership
for dir in /app/data /app/logs /app/.ssh /app/.cache/huggingface /app/.local; do
    repair_bind_mount_ownership "$dir"
done

for cu in \
    /app/.local/lib/python*/site-packages/nvidia/cu13 \
    /app/.local/lib/python*/site-packages/nvidia/cu12 \
    /app/.local/lib/python*/site-packages/nvidia/cuda_nvcc; do
    if [ -x "$cu/bin/nvcc" ]; then
        export CUDA_HOME="$cu"
        break
    fi
done
export VLLM_USE_FLASHINFER_SAMPLER="${VLLM_USE_FLASHINFER_SAMPLER:-0}"

export PATH="/app/.local/bin:$PATH"

"$GOSU_BIN" "$PUID:$PGID" "$PYTHON_BIN" /app/setup.py || true

exec "$GOSU_BIN" "$PUID:$PGID" "$@"
