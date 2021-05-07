# MSiA423 Steam Recommender

Author: Junpeng Jiang

QA: Hao Xu

<!-- toc -->
- [Project Charter](#project_charter)
- [Directory structure](#directory-structure)
- [Midterm Check Point Tutorial](#Midterm-Check-Point-Tutorial)  
  * [0. Connect to Northwestern vpn](#0-Connect-to-Northwestern-vpn)
  * [1. Build the image](#1-build-the-image)
  * [2. Uploading Raw Data to S3 Bucket](#2-uploading-raw-data-to-s3-bucket)
  * [3. Create RDS](#3-create-rds)  

<!-- tocstop -->

## Project Charter: Steam Recommender

### Vision

Steam is a digital video game library for users to purchase, download and play games on PC/labtops. It started in September 2003 as software platform to update games for valve (steam's parent company) but gradually expanded to include a variaty of games from third-party game producers. As of the end of 2020, there are more than 10,000 games released on steam world wide and certainly it has become the most prevalent game hub for game enthusiasts on PC.
In steam, each user possesses a game library profile that records of all the games purchased, time played, achievements acquired and etc. Whether you are a experienced video gamer or just new to steam, you would always wonder what game to play next and how long you will spend in the next game on steam . Hopefully, this web app recommender can help you find and enjoy your next favorite game on steam.

### Mission

The primary data source for this project should contain a complete list of games on steams and their related features. The dataset I am currently considering is from kaggle(https://www.kaggle.com/nikdavis/steam-store-games). However, since this is not the mosted updated game library, I might also consider scrap data from steam using API services such as [StorefrontAPI](https://wiki.teamfortress.com/wiki/User:RJackson/StorefrontAPI/) or [SteamSpy](https://steamspy.com/about/).

The users will enter their game profile on steam or game preference if they have not acquired a profile to start. These inputs should include the name of the games purchase, time played, date of purchase, price paid, and interest in looking for the next game to play. The recommender will return a list of games (and steam urls) based on an evaluation of the input information and records in the game library dataset. Additionally, the recommender will output estimates of  the time users will play in these games.


### Success Criteria

#### Machine Learning Metric

The primary method for this recommender will be content based filtering/clustering, and the wep app should take different similary metrics into consideration when making recommendations. Before the wep app goes live, we should look at F-statistic/Silhouette-statitics if implementing clustering methods. Since we will not have users' data, we will be able to cross validate the recommendations. However, after the app launches, it is possible to trach the click through rate and conversion rate as an estimate of whether a users likes the recommendations. Based on these estimates, we can calculate the precision/recall/ROC/mRR(mean reciprocal rank) to evalutation the recommender.

#### Business Metric

From a business perspective, their are mainly two metrics to evaluate the performance of the webapp, the click throught rate and the conversion rate. Specifically, we can measure the number of times a user would click the recommended games' urls and track if they consider these recommendations as viable options. Similarly, it's also important to track if these recommendations actually make a user to purchase the games. These metric will be strong indications of the effectiveness of the recommendations and they are directly related to steam's revenue and user acquisition.

## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│   ├── steamdata/                    <- Newly added raw data
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│   ├── s3.py                         <- Module used to upload file to s3.
│   ├── create_dy.py                  <- Module used to create local/RDS databases.
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
├── Dockerfile                        <- Dockerfile used to build docker


```


## Midterm Check Point Tutorial

### 0. Connect to Northwestern vpn

### 1. Build the image 

`cd` into the top level of this project's repository

```bash
 docker build -t steam .
```

This command builds the Docker image, with the tag `steam`, based on the instructions in `Dockerfile` and the files existing in this directory.
 
### 2. Uploading Raw Data to S3 Bucket

#### 2.1 Raw Data Aquirement and Setup
For this project, I am using datasets from https://www.kaggle.com/nikdavis/steam-store-games. You can use this link to access the original data source and manually download it using the download button on the upper right corner.

After downloading the compressed file, you shuold un-zip it and store the 6 raw steam_xxx.csv files to your local directory.

Before start uploading, you should configure your environment variables as follows: 

```bash
export AWS_ACCESS_KEY_ID=<Your Access Key ID>

export AWS_SECRET_ACCESS_KEY=<Your Secret Key ID>
```

Alternatively, you can create a `.awsconfig` file at your local repository and store your `AWS_ACCESS_KEY_ID` and your `AWS_SECRET_ACCESS_KEY`. You can `source .awsconfig` when you want to use AWS related services.

#### 2.2 Uploading Files to S3 Bucket Using run.py
```bash
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY steam run.py upload --s3path='s3://2021-msia423-lastname-firstname/to/path' --local_path='local/path'
```

Example:
```bash
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY steam run.py upload --s3path='s3://2021-msia423-jiang-junpeng/raw/steamspy_tag_data.csv' --local_path='data/steamdata/steamspy_tag_data.csv'
```
### 3. Create RDS 

#### 3.1 Introduction and Setup

At this time I have created one table named `steam`. This table combines information from all 6 raw data files. I may add more relational tables as the project progresses.

You should set up your database connect configurations before the next steps. You can type the following in the console:
```bash
export MYSQL_USER="Your_username"
export MYSQL_PASSWORD="Your_password"
export MYSQL_HOST="nw-msia423-jjp3451.czalnmqkpupo.us-east-1.rds.amazonaws.com"
export MYSQL_PORT="3306"
export DATABASE_NAME="msia423_db"
```

Alternatively, you can create a `.mysqlconfig` file at your local repository and store your configs. You can `source .mysqlconfig` when you want to use AWS related services.
 
#### 3.2 Create RDS Table `steam` using run.py

#### To run on RDS:

If you have `MYSQL_HOST` in your environment variable, this will create a table named steam on your AWS RDS.
```bash
docker run -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_PORT -e DATABASE_NAME -e MYSQL_HOST steam run.py create_db
```

If you don't have specified `MYSQL_HOST` environment variable in your repository, or this variable is set to `None`, you can run the command follows. This will create a local .db file to the default path `sqlite:///data/steam.db`

```bash
docker run -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_PORT -e DATABASE_NAME -e MYSQL_HOST steam run.py create_db
```

You can also specify a path to store the created .db file by using the --engine_string argument:

```bash
docker run -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_PORT -e DATABASE_NAME -e MYSQL_HOST steam run.py create_db --engine_string="sqlite:///randomfolder/steam.db"
```
