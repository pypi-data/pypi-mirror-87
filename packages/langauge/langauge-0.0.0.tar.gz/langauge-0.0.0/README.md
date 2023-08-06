# LanGauge (INTERNAL)
Code here is first "internal" before it is reviewed &amp; upstreamed to the LanGauge mainline, the public release.

# LanGauge
LanGauage: NLP experiment platform. To be open-sourced publicly (Apache 2.0 or similar).

## Architecture
![architecture](images/arc.png)

## What is it?
Natural Language Processing (NLP) is one of the most important fields of research in today’s world. It has many applications such as chatbots, sentiment analysis, and document classification. 

LanGauge is a web application leveraging Natural Language Processing (NLP) to reduce the time spent analyzing medical research papers in an easy-to-use fashion. This free, open-source platform helps researchers in fields such as drug discovery curate their data to secure and scale the development of health solution. An example application would be enhancing COVID-19 research using multiple NLP models on medical datasets.  

We want to use the language processing models to “gauge” the usefulness of open-source medical datasets for the researchers.  

## How to run the project?
 1. Clone the repository.
 ```bash
 git clone -b beam-pipe https://github.com/flapmx/LanGauge-INTERNAL.git
 ```
 2. Ensure you have docker and docker-compose installed. 
 3. Build and Launch the project
 ```bash
 docker-compose up --build
 ```
 
## How to access the application?
 1. http://localhost:8080 for the React front end
 2. http://localhost:5000 for the Flask back end
 
## How to shut down?
```bash
 docker-compose down
 ```
