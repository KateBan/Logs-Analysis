# Logs-Analysis


# Bulding an Internal Reporting Tool

### Overview
This lab cretes Internal reporting tool that uses information from the 'news`
database to discover what kind of articles the site's readers like. For the
task thePostgreSQL database is used. The focus is on building, refining
complex queries and using them to draw business conclusions from data.

### Files
 - newsdata.sql: the data we will be working with can be downloaded form [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
 - lab.py: the Python code for the internal reporting tool
 - report.txt: sample output

 ## Instalation
 For instructions on how to install the install the database software and
 setting it up please look at [Install the database software](https://classroom.udacity.com/nanodegrees/nd016beta/parts/092ebb59-d116-40eb-b19f-0c710e419d1a/modules/cd543def-99c0-455b-b4ab-2ab20091ad23/lessons/262a84d7-86dc-487d-98f9-648aa7ca5a0f/concepts/eaf58af6-a1fa-43a0-b4de-311e04689748#)

### Using the psql command line

To load the data, use the command psql -d news -f newsdata.sql.
Here's what this command does:

 - psql â the PostgreSQL command line program
 - -d news â connect to the database named news which has been set up for you
 - -f newsdata.sql â run the SQL statements in the file newsdata.sql

 ### Creating views

 In order to get the expected results by using the internal reporting tool
 you will need to create a fiew views. Once you have the data loaded into your
 database, connect to your database using `psql -d news`. Then you can use
 the following `CREATE VIEW` commands to create the views:

 **Views needed to get the results from mostPoppularArticles() function**

 - CREATE VIEW most_viewed as
 	SELECT path, COUNT(log.path) as num
 	FROM log
 	WHERE status = '200 OK'
 	GROUP BY path
 	ORDER BY num DESC limit 8 offset 1;

 - CREATE VIEW log_slug_views as
 	SELECT SUBSTRING(path, 10, char_length(path)) as slug, num
 	FROM most_viewed;

  **Views needed to get the results from mostPopularArticleAuthors() function**

 - CREATE VIEW articles_views as
 	SELECT title, num
 	FROM articles,log_slug_views
 	WHERE articles.slug = log_slug_views.slug;

 - CREATE VIEW authors_articles as
 	SELECT title, name
 	FROM articles join authors ON articles.author = authors.id;

 - CREATE VIEW ready_to_sum_author_articles as
 	SELECT name, num
 	FROM authors_articles join articles_views
 	ON authors_articles.title = articles_views.title;

**Views needed to get the results from statusErrors() function**

 - CREATE VIEW statuses as
 	SELECT SUM((status = '200 OK')::int) as good,
    SUM((status != '200 OK')::int) as bad,
    time::date as day
    FROM log
    GROUP BY day;

 - CREATE VIEW percents as
 	SELECT day, CAST(bad as FLOAT) * 100 /good as perc
 	FROM statuses;

**After all of the views have been created navigate to folder `lab` in your VM and run `python lab.py`.**
