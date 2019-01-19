git diff --cached --stat
staged_count=$(git diff --cached --numstat | wc -l)
zero="0"
if [ $staged_count = $zero ]; then
  echo "nothing is staged on git. exit."
  exit 1
fi
read -p 'commit message please:' commit_msg
python setup.py sdist bdist_wheel
success=$?
if [ $success -ne 0 ]; then
    echo "python setup.py sdist bdist_wheel failed!"
    exit 1
fi
twine upload dist/*
success=$?
rm -rf dist
rm -rf build
project_name=$(ls -1|grep .egg-info)
rm -rf ${project_name}
rm -rf ${project_name%.egg-info}-*.*.*
if [ $success -ne 0 ]; then
    echo "twine upload dist/* failed!"
    exit 1
fi
version=$(cat version.txt)
git reset HEAD version.txt
git add version.txt
git commit -m "version ${version} ${commit_msg}"
git push
