For those of you who were in the lab today, and are frustrated with build times for heroku, I have a solution which will speed things up many times. _Note: the first instruction assumes an Anaconda install, if you use a different python distro, use the proper `source` command instead._

0\. In the console, change to your project directory.

1\. Activate your project environment:

```
conda activate <environment>
```

Where `<environment>` is the name of the environment you wish to activate.

2\. Install pipreqs, pressing `\[y\]` when prompted to install dependencies:

```
pip install pipreqs
```

\*\*_**\*IMPORTANT**_\*\*\* **MAKE SURE THE ENVIRONMENT IS <ins>ACTIVE</ins> BEFORE INSTALLING**

3\. Modify your `app.py` file to add the following lines after the last import statement:

```
import gunicorn
import psycopg2
```

![Screen_Shot_2020-07-21_at_4.33.59_PM.png](./Screen_Shot_2020-07-21_at_4.33.59_PM.png)

This will ensure that dependencies required to deploy to Heroku (which are not required for local development) get pulled in.

4\. From the console, change into your project directory containing `requirements.txt` and run pipreqs:

```
pipreqs . --force
```

This will cause pipreqs to overwrite the existing requirements.txt When you're done, it should be quite small:

```
Flask_WTF==0.14.3
SQLAlchemy==1.3.18
WTForms==2.3.1
Flask==1.1.2
psycopg2==2.8.5
Flask_SQLAlchemy==2.4.3
gunicorn==20.0.4
passlib==1.7.2
flask_heroku==0.1.9
python-dotenv==0.14.0
```

The versions listed here may differ from your versions, but that isn't super important at this moment. If you get Heroku app errors (below), fixing them generally just means changing the == to >= for a specific library, or removing the version altogether and allowing Heroku to fix them.

5\. Deploy your app to Heroku normally (login,create an app, set the config, push the database), and finally push:

```
git push heroku master
```

Once you see the 'successfully deployed message' go ahead and attempt to connect to your server. If there is an error, type:

```
heroku logs --tail
```

which will bring up the heroku server logs for your app.

If towards the bottom you see 'app crashed' or 'SIGTERM', scan upwards and see if a package is missing (see screenshot).

![](./Screen_Shot_2020-07-21_at_4.31.16_PM.png)

If that is the case, add that package to step3, and continue from step 4.

To exit the log viewer, type `CTRL-C` in the console.

Hope that was helpful!
