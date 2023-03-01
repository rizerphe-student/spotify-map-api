# A very minimal API that generates a map based on spotify data
For a given artist, it shows an artist's most popular song for each country.

# Deployment
Clone the repo and install the requirements:
```sh
git clone git@github.com:rizerphe-student/spotify-map-api.git
cd spotify-map-api
pip insall -r requirements.txt
```
Make sure the `countries.json` file is in the working directory of your deployment. You will also need to specify the environment variables for your deployment: `CLIENT_ID` and `CLIENT_SECRET`. The project can read them from a `.env` file located in the working directory.
Run it with uvicorn:
```sh
uvicorn api:app
```
