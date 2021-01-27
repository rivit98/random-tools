git filter-branch -f --commit-filter 'if [ "$GIT_COMMITTER_EMAIL" = "email" ];
  then git commit-tree -S "$@";
  else git commit-tree "$@";
  fi' HEAD --all
