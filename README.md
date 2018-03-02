# lobe
To provide for the common defense, and promote the general welfare.

lobe is powered by a few different things.

### messenger platform
Set up messenger.py on heroku or some other platform. Make sure that facebook has subscribed your page to messenger events

### rasa.ai
lobe uses rasa.ai. you can host the model on any given machine this way

###### on the ml endpoint
```sh
bash -c "docker run -p5000:5000 \
-v `pwd`/container_data/data:/app/data \
-v `pwd`/container_data/logs:/app/logs \
-v `pwd`/container_data/proj:/app/projects rasa/rasa_nlu:latest-full"
```


###### on any other machine
Make sure to make a request to the right hosts and the right model.

We'll start by making sure that the docker image is actually up and that it works.
Here's an example from my machine
```
$ curl 'http://localhost:5000/status'
{
  "available_projects": {
    "lobe": {
      "status": "ready",
      "available_models": [
        "model_20180302-192533",
        "model_20180302-170041"
      ]
    },
    "expressions.json": {
      "status": "ready",
      "available_models": [
        "fallback"
      ]
    }
  }
}
```


First pass the model to train it and give the project a name
```sh
cat expressions.json | \
curl --request POST --header 'content-type: application/json' -d@- --url 'localhost:5000/train?project=lobe'
# wait for a bit
{
  "info": "new model trained: model_20180302-192533"
}
```

Then make requests using the name of the model you just created and the name of the project that will use that new model
```sh
curl -X POST localhost:5000/parse \
  -d '{"q":"what is court like?", "model":"model_20180302-170041", "project":"lobe"}'
```

