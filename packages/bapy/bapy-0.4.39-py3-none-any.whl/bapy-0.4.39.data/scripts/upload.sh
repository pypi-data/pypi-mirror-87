#!/usr/bin/env bash
# shellcheck disable=SC1090
# shellcheck disable=SC2034
# ${1} - project_path
# ${2} - bump: <major|minor>
# ${3} - twine: <"${GITHUB_USERNAME}"|"${NFERX_GITHUB_USERNAME}"|pypi>
# ${4} - site (default use virtual environment if no defined)
export starting="${BASH_SOURCE[0]}"; debug.sh starting

if ! isuserdarwin.sh || [[ "${USERNAME}" != "${USER}" ]]; then
  error.sh "Can not be done with root and user should be: ${USERNAME}"; exit 1
fi

if [[ "${1-}" ]]; then
  while (( "$#" )); do
    case "${1}" in
      major) bump="${1}" ;;
      minor) bump="${1}" ;;
      patch) bump="${1}" ;;
      "${GITHUB_USERNAME}") twine="${1}" ;;
      "${NFERX_GITHUB_USERNAME}") twine="${1}" ;;
      pypi) twine="${1}" ;;
      git) twine="${1}"; git=git ;;
      site) site="${1}"; export site ;;
      bapy) name="${1}"; project_path="${BAPY}" ;;
      pen) name="${1}"; project_path="${PEN}"; twine=git; git=git ;;
      *) project_path="${PEN}"; name="$( basename "${project_path}" )" ;;
    esac; shift
  done
else
  project_path="${BAPY}"; name="$( basename "${project_path}" )"
fi

[[ "${project_path-}" ]] || { project_path="${BAPY}"; name="$( basename "${project_path}" )"; }
bump="${bump:-patch}"
twine="${twine:-${NFERX_GITHUB_USERNAME}}"
test -n "${twine}" || { error.sh "twine repository" "empty"; exit 1; }
export USERNAME USER GITHUB_USERNAME NFERX_GITHUB_USERNAME BAPY PEN bump twine project_path name site
debug.sh USERNAME USER GITHUB_USERNAME NFERX_GITHUB_USERNAME BAPY PEN bump twine project_path name site

cd "${project_path}" > /dev/null 2>&1 || { error.sh "${project_path}" "invalid"; exit 1; }

if isuserdarwin.sh && [[ "${USERNAME}" == "${USER}" ]]; then
    venv.sh "${name}"
  if [[ ! "${site-}" ]]; then
    virtual="${project_path}/venv/bin/"
    source "${virtual}activate"
    export virtual; debug.sh virtual
  fi
  export VIRTUAL_ENV PYTHONHOME; debug.sh VIRTUAL_ENV PYTHONHOME
  clean.sh "${name}" || exit 1
  find "${project_path}" -type d -name scripts -exec chmod -R +x "{}" \;
	gadd.sh || exit 1
  if error="$( "${virtual}bump2version" --allow-dirty "${bump}" 2>&1 )"; then
    info.sh bump2version "${name}" "${bump}"
  else
    error.sh bump2version "${name} ${bump}" "${error}"; exit 1
  fi
  gpush.sh || exit 1
  unset project_path
  if error="$( "${virtual}python3" setup.py sdist 2>&1 )"; then
    info.sh sdist "${name}"
  else
    error.sh sdist "${name}" "${error}"; exit 1
  fi
  if error="$( "${virtual}python3" setup.py bdist_wheel 2>&1 )"; then
    info.sh wheel "${name}"
  else
    error.sh wheel "${name}" "${error}"; exit 1
  fi
  if [[ "${twine}" = 'git' ]] ; then
    warning.sh twine "${name}" "${twine}"
  else
    if error="$( "${virtual}twine" upload -r "${twine}" dist/* 2>&1 )"; then
      info.sh twine "${name}" "${twine}"
    else
      error.sh twine "${name} ${twine}" "${error}"; exit 1
    fi
  fi
  gmerge.sh || exit 1
  clean.sh "${name}" || exit 1
  unset VIRTUAL_ENV PYTHONHOME
  deactivate > /dev/null 2>&1
  upgrade.sh "${name}" > /dev/null 2>&1
  upgrade.sh "${name}" || exit 1
else
  error.sh "${name}" "Can not be uploaded with root and user should be: ${USERNAME}"; exit 1
fi

cd - > /dev/null || exit 1

unset starting bump twine virtual file error name project_path PYTHONPATH
