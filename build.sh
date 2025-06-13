echo 'Building h2overlord!'
echo 'Moving web to web-build'
rm -rf web-build

echo 'Building the webfrontend'
cd web-frontend/h2overlord-frontend
npm install
npm run build 

cd ../..
mv web-frontend/h2overlord-frontend/dist/ web-build/

echo 'Building the backend'
cd h2overlord-python
eval $(poetry env activate)
poetry install 
poetry lock

echo 'Finished building h2overlord!'