#!/usr/bin/env bash
#
# Run locally by the operator. Do not run this script through Codex or CI.
# The app password is prompted for only in memory; it is never written to disk.

set -euo pipefail

# Approved repositories for the PR-alert rollout.
REPOS=(
  "younify-engineering"
  "younify-core"
  "younify-intelligence"
  "younify-infra"
  "natalyx-learn-resources"
)

SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USERNAME="luke@natalyx.health"
MAIL_FROM="github-pr-alerts@natalyx.health"
DEFAULT_RECIPIENTS="luke@natalyx.health,alan@natalyx.health"

dry_run=false
only_recipients=false
recipients="$DEFAULT_RECIPIENTS"

usage() {
  cat <<'USAGE'
Usage:
  ./scripts/set-pr-alert-secrets.sh --dry-run
  ./scripts/set-pr-alert-secrets.sh
  ./scripts/set-pr-alert-secrets.sh --only-recipients \
    --recipients 'luke@natalyx.health,new.person@natalyx.health'

Run this script locally as the operator. It never prints or writes the Google
app password. Use --only-recipients to update PR_ALERT_TO across REPOS without
re-entering the password or changing every repository manually.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      dry_run=true
      ;;
    --only-recipients)
      only_recipients=true
      ;;
    --recipients)
      shift
      recipients="${1:-}"
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) is required." >&2
  exit 1
fi

if ! gh auth status --hostname github.com >/dev/null 2>&1; then
  echo "Authenticate first with: gh auth login --hostname github.com" >&2
  exit 1
fi

if [[ -z "$recipients" ]]; then
  echo "PR recipient list must not be empty." >&2
  exit 1
fi

secret_names=(
  "PR_ALERT_SMTP_HOST"
  "PR_ALERT_SMTP_PORT"
  "PR_ALERT_SMTP_USERNAME"
  "PR_ALERT_SMTP_PASSWORD"
  "PR_ALERT_FROM"
  "PR_ALERT_TO"
)

if [[ "$only_recipients" == true ]]; then
  secret_names=("PR_ALERT_TO")
fi

if [[ "$dry_run" == true ]]; then
  for repo in "${REPOS[@]}"; do
    echo "Would set PR alert secrets for YounifyHealth/$repo"
    for secret_name in "${secret_names[@]}"; do
      echo "  $secret_name"
    done
  done
  exit 0
fi

app_password=""
cleanup() {
  unset app_password
}
trap cleanup EXIT

if [[ "$only_recipients" != true ]]; then
  read -r -s -p "Google app password: " app_password
  echo
  if [[ -z "$app_password" ]]; then
    echo "Google app password must not be empty." >&2
    exit 1
  fi
fi

set_secret() {
  local repo="$1"
  local secret_name="$2"
  local value="$3"

  gh secret set "$secret_name" \
    --repo "YounifyHealth/$repo" \
    --body "$value"
}

for repo in "${REPOS[@]}"; do
  echo "Setting PR alert secrets for YounifyHealth/$repo"

  if [[ "$only_recipients" == true ]]; then
    set_secret "$repo" "PR_ALERT_TO" "$recipients"
  else
    set_secret "$repo" "PR_ALERT_SMTP_HOST" "$SMTP_HOST"
    set_secret "$repo" "PR_ALERT_SMTP_PORT" "$SMTP_PORT"
    set_secret "$repo" "PR_ALERT_SMTP_USERNAME" "$SMTP_USERNAME"

    # Use standard input so the password is not placed in a command argument.
    printf '%s' "$app_password" | gh secret set "PR_ALERT_SMTP_PASSWORD" \
      --repo "YounifyHealth/$repo"

    set_secret "$repo" "PR_ALERT_FROM" "$MAIL_FROM"
    set_secret "$repo" "PR_ALERT_TO" "$recipients"
  fi

  echo "Done"
done
