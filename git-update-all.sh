find . -name ".git" -type d -execdir pwd \; -execdir git reset --hard origin/master \; -execdir git pull \;
# ls | xargs -I{} git -C {} pull 2> /dev/null
