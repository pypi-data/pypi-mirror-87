#!/usr/bin/env bash
# shellcheck disable=SC1090
# shellcheck disable=SC2034
# ${1} - project_path
# ${2} - bump: <major|minor>
# ${3} - twine: <"${GITHUB_USERNAME}"|"${GITHUB_ORGANIZATION_ID}"|pypi>
export starting="${BASH_SOURCE[0]}"; debug.sh starting

if ! isuserdarwin.sh || [[ "${USERNAME}" != "${USER}" ]]; then
  error.sh "Can not be done with root and user should be: ${USERNAME}"; exit 1
fi

if [[ "${1-}" ]]; then
  while (( "$#" )); do
    case "${1}" in
      bapy) name="${1}"; project_path="${BAPY}" ;;
      pen) name="${1}"; project_path="${PEN}" ;;
      site) site="${1}" ;;
      *) project_path="${PEN}"; name="$( basename "${project_path}" )" ;;
    esac; shift
  done
else
  project_path="${BAPY}"; name="$( basename "${project_path}" )"
fi

[[ "${project_path-}" ]] || { project_path="${BAPY}"; name="$( basename "${project_path}" )"; }
export BAPY PEN project_path name; debug.sh BAPY PEN project_path name

cd "${project_path}" > /dev/null 2>&1 || { error.sh "${project_path}" "invalid"; exit 1; }

virtual="${project_path}/venv/bin/"
export virtual; debug.sh virtual

if isuserdarwin.sh && [[ "${USERNAME}" == "${USER}" ]]; then
  # shellcheck disable=SC2154
  #  export site in project-upload.sh (default use virtual environment if no defined)
  if [[ ! "${site-}" ]]; then
    if ! test -d "${virtual}"; then
      if error="$( python3.8 -m venv "${project_path}/venv" 2>&1 )"; then
        info.sh venv "${name}" "${site}"
      else
        error.sh venv "${name} ${site}" "${error}"; exit 1
      fi
    fi
    source "${virtual}/activate"
  else
    warning.sh venv "${name}" "${site}"
  fi
  while read -r file; do
    export file; debug.sh file
    if error="$( "${virtual}python3" -m pip install --upgrade pip wheel setuptools && \
                 "${virtual}python3" -m pip install --upgrade -r "${file}" 2>&1 )"; then
      info.sh requirements "${name} ${site}" "${file}"
    else
      error.sh requirements "${name} ${site} ${file}" "${error}"; exit 1
    fi
  done < <( find "${project_path}" -mindepth 1 -maxdepth 2 -type f -name "requirements*".txt )
else
  error.sh "${BASHRC}" "Can not be uploaded with root and user should be: ${USERNAME}"; exit 1
fi

cd - > /dev/null || exit 1

unset starting virtual file error name project_path site
