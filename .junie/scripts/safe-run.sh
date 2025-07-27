#!/usr/bin/env bash

# safe-run.sh - A simplified non-blocking task runner for Junie
#
# Usage:
#   ./safe-run.sh [options] -- <command> [command-args]

# Defaults
BACKGROUND=false
TIMEOUT=300
NAME=""

# Parse arguments
while (( "$#" )); do
  case "$1" in
    -b|--background)
      BACKGROUND=true
      shift
      ;;
    -t|--timeout)
      TIMEOUT="$2"
      shift 2
      ;;
    -n|--name)
      NAME="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: ./safe-run.sh [options] -- <command> [command-args]"
      echo "Options:"
      echo "  -b, --background     Run command in background (nohup)"
      echo "  -t, --timeout SEC    Set timeout in seconds (default: 300)"
      echo "  -n, --name NAME      Custom name for logs/status (optional)"
      echo "  -h, --help           Show this message"
      echo ""
      echo "Environment:"
      echo "  Logs/status/pids are written to .junie/ directories"
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      break
      ;;
    *)
      break
      ;;
  esac
done

if [[ $# -eq 0 ]]; then
  echo "❌ Error: No command provided"
  exit 1
fi

# Set name from command if not manually set
if [ -z "$NAME" ]; then
  NAME=$(basename "$1" | sed 's/[^a-zA-Z0-9]/_/g' | cut -c1-30)
fi

# Directories
ROOT_DIR="$(pwd)"
JUNIE_DIR="$ROOT_DIR/.junie"
LOGS_DIR="$JUNIE_DIR/logs"
PIDS_DIR="$JUNIE_DIR/pids"
STATUS_DIR="$JUNIE_DIR/status"

mkdir -p "$LOGS_DIR" "$PIDS_DIR" "$STATUS_DIR"

# Files
LOG_FILE="$LOGS_DIR/$NAME.log"
PID_FILE="$PIDS_DIR/$NAME.pid"
STATUS_FILE="$STATUS_DIR/$NAME.status"

# Logging
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

COMMAND_STRING="$*"
log "Running: $COMMAND_STRING"

if [ "$BACKGROUND" = true ]; then
  echo "running" > "$STATUS_FILE"

  nohup bash -c "
    echo \"START: \$(date)\" >> \"$LOG_FILE\"
    $* >> \"$LOG_FILE\" 2>&1
    EXIT_CODE=\$?
    echo \"END: \$(date)\" >> \"$LOG_FILE\"
    echo \$EXIT_CODE > \"$STATUS_FILE\"
    rm -f \"$PID_FILE\"
  " > /dev/null 2>&1 &

  PID=$!
  echo $PID > "$PID_FILE"
  log "Background PID: $PID"
  echo "Use: tail -f $LOG_FILE"
else
  echo "running" > "$STATUS_FILE"
  log "Timeout set to ${TIMEOUT}s"
  timeout $TIMEOUT "$@" >> "$LOG_FILE" 2>&1
  EXIT_CODE=$?

  if [ $EXIT_CODE -eq 124 ]; then
    log "⏰ Timed out after $TIMEOUT seconds"
    echo "timeout" > "$STATUS_FILE"
  else
    log "✅ Exit code: $EXIT_CODE"
    echo "$EXIT_CODE" > "$STATUS_FILE"
  fi

  tail -n 5 "$LOG_FILE"
  echo "→ Full log: $LOG_FILE"
  exit $EXIT_CODE
fi
