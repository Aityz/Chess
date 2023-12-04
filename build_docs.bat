@Echo off
echo Aityz_Chess Documentation Build Scripts
pdoc3 aityz_chess --html --force -o ./docs
cd docs
cd aityz_chess
index.html