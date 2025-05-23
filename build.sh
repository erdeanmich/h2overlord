echo 'Building h2overlord!'
echo 'Moving build to build.zip'
rm -rf build
rm -rf build.zip

mkdir build

echo 'Building the webfrontend'
cd web-frontend/h2overlord-frontend
npm install
npm run build 

cd ../..
mv web-frontend/h2overlord-frontend/dist build/web


echo 'Building the backend'
cd h2overlord-python
poetry install 
poetry lock
poetry run python -m nuitka --mode=standalone --include-data-files=src/h2overlord_python/Config/config.json=Config/config.json src/h2overlord_python/main.py
cd ..
mv h2overlord-python/main.dist build/backend

cp run.sh build/run.sh

zip -r build.zip build/
echo 'Finished building h2overlord!'