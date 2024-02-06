[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/IVxXQbbN)
# Pset 4: Web Application (Version 2)

### Due Friday Nov 17 11:59 PM NHT (New Haven Time)

## Table of Contents
- [Pset 4: Web Application (Version 2)](#pset-4-web-application-version-2)
    - [Due Friday Nov 17 11:59 PM NHT (New Haven Time)](#due-friday-nov-17-1159-pm-nht-new-haven-time)
  - [Table of Contents](#table-of-contents)
  - [Purpose](#purpose)
  - [Rules](#rules)
  - [Getting Started](#getting-started)
  - [Your Task](#your-task)
  - [The Database](#the-database)
  - [Background](#background)
  - [The Application](#the-application)
  - [Additional Requirements for 519 Students](#additional-requirements-for-519-students)
    - [Additional Features](#additional-features)
  - [A Note About Performance](#a-note-about-performance)
  - [Object-Relational Mappers](#object-relational-mappers)
  - [Specific Endpoints](#specific-endpoints)
  - [Error Handling: Bad Server](#error-handling-bad-server)
  - [Error Handling: Bad Client](#error-handling-bad-client)
    - [Invalid search parameters](#invalid-search-parameters)
    - [Invalid `obj_id`](#invalid-obj_id)
    - [Missing `obj_id`](#missing-obj_id)
    - [Aside: Error Pages](#aside-error-pages)
    - [Other invalid requests](#other-invalid-requests)
  - [Source Code Guide](#source-code-guide)
  - [Submission](#submission)
    - [Late Submissions](#late-submissions)
  - [Grading](#grading)

## Purpose

The purpose of this assignment is to help you learn or review client-side web programming.

---

## Rules

You may work with one teammate on this assignment, and we prefer that you do so.

It must be the case that either you submit all of your team’s files or your teammate submits all of your team’s files.
(It must not be the case that you submit some of your team’s files and your teammate submits some of your team’s files.)
Your `README` file and your source code files must contain your name and your teammate’s name.

---

## Getting Started
> **Note**: this section contains exactly the text on the Canvas assignment, reproduced here only for completeness of this document.
> Since you made it here, you can safely ignore this section.


1. Accept [this GitHub classroom assignment](https://classroom.github.com/a/IVxXQbbN).
    * **Due to several students dropping the course at the midterm deadline, some groups have new members. You will create a new GitHub Classroom Group for this assignment!**
    * GitHub classroom will ask you to create a team, whether you will be working in pairs or individually.
        * **Name this team identically to your Canvas Pset Partner group**, *e.g.* "Pset Partner Group 13".
    * Let your other team member join your team.
    * This step creates a GitHub repository for your team and links your team members' GitHub ids.
        * If you do not have a GitHub account, you are required to create one for this course
    * Use this git repository to track your assignment development.

2. Download the `lux.sqlite` database file from Canvas (or copy it over from your previous assignment) and place it in your new repository folder.
  > **Important**: Do not track `lux.sqlite` in your git repository.
  > It is too large to be hosted on GitHub and recovering from an error telling you that is challenging at best.
  > The included `.gitignore` file in the template repository will help with this, so *do not change or remove* that file.
  > You may keep the database file in the repository folder, but you must be careful not to *track* it.

---

## Your Task

As with Psets 1, 2, and 3, assume you are working for the Yale University Art Galleries (YUAG).
You are given a database containing data about objects and artwork stored in the gallery's collection.
Your task is to compose an application that allows museum visitors and other interested parties to query the database.

This assignment asks you to compose a web application.
On the server side, your application must use the Python Flask framework and the Jinja2 template engine.
If you are interested, you may use SQLAlchemy to manage your database queries, which is an Object Relational Mapper (ORM) for Python.

On the client side, your application must use HTML and JavaScript with AJAX, and may use jQuery (which we recommend).
It must also use CSS, and to keep things easy on yourself you may use Bootstrap.
Your application may not use any other client-side library or framework (such as AngularJS, Vue, React, and so forth).

---
## The Database

The database is identical to the one from Psets 1, 2, and 3.
Refer to the Pset 1 specification for the list of tables and fields in the database.
As with previous psets, the database is in a file named `lux.sqlite` that you should copy into your repository but take care not to track with git.
One possible alternative to keeping the databse file directly in your repository is to keep it in a different folder and store only a [link](https://man7.org/linux/man-pages/man1/ln.1.html) to the "real" database file. Doing so would eliminate the need to copy the very-large file for each of your assignments.

---
## Background

The application you built in Pset 3 is flawed.
The flaw is not in your implementation; instead the flaw (intentionally) is in the specification.

The problem is that an application that conforms to that specification often has inconsistent page states.
For example, consider the following sequence of events:
* The user browses to your website and the browser displays your application's primary page
* The user types "Gogh" into the "Agent" input element, but is distracted before typing the `enter` key or clicking on the `submit` button
* Sometime later the user returns to the page

At that point the page's "Agent" input element contains "Gogh" but the page displays no data.
This is an inconsistent state, and it is a problem that you will fix in this assignment.

---
## The Application

Compose a program named `runserver.py`.
When executed with `-h` as a command-line argument, the program must display the following help message describing the program's behavior:

```
$ python runserver.py -h
usage: runserver.py [-h] port

The YUAG search application

positional arguments:
  port        the port at which the server should listen

optional arguments:
  -h, --help  show this help message and exit
```

> **Note**: The specific verbiage of this help message should be the default for your version of the `argparse` module, which differs slightly between python versions.

Your `runserver.py` must run an instance of the Flask test server on the specified port, which must in turn run your application.

> **Note**: Your application code should *not* be in your `runserver.py` program, which should do nothing but start a Flask server on the provided port number.
> The file containing your application code may be named whatever you want, but we suggest something simple such as `luxapp.py`.

When a client makes an HTTP request to the server, your application must return an HTML webpage appropriate to the request.
Beyond some [specific endpoints](#specific-endpoints) mentioned below, there are several requirements your application must satisfy:

* Your application's **primary web page** (*i.e.*, the webpage returned by a request to the server's root&mdash;*e.g.* `http://yourserver:80/` if your server is listening on port 80) must contain four text input fields labeled "Label", "Classifier", "Agent" and "Date".
    These should, respectively, allow the user to specify an object label, a classifier, the name of an agent, and a date.
  * In contrast to the form from pset 3, your primary page must *not* contain a submit button.
  * The input fields must be filled in with the parameters used to make the most recent query, that is, the values of the input fields as they were upon the most recent query (if a query has never been performed, those fields should be empty)
* Below the input fields, the webpage must display an HTML `table` containing no more than the first 1000 results of the most recent query (or nothing at all if no query has yet been sent)
  * The columns displayed in the table must be&mdash;in order&mdash;the object's label, the object's date, the name of each agent that produced this object and the part they produced (in the format `"{agent-name} ({agent-part})"`), and a list of all classifiers for the object, for each object that matches the specified criteria, or of all objects in the database if the user specifies no criteria.
  The columns must be labeled "Label", "Date", "Agents", and "Classified As", respectively.
    * The lists of things in the "Agents" and "Classified As" columns must be formatted with one item per line
  * The table rows must be _sorted_; the algorithm to sort is the same from Pset 3.
  * A user must be able to click on the `label` for any of the displayed objects to request more information about that object on a different webpage (the "secondary" page) at the url `"/obj/{object-id}"`.
    The requirements for the secondary webpage are below.

    > **Note**: The object's ID must not be displayed in the table.

* The results table on the primary webpage must be updated every time the user types a character in any of the four input fields

    > **Node**: You're required to use JavaScript and AJAX to accomplish this, and we recommend you use jQuery as well to keep your code concise and easy to understand.

* You application must accept requests to the endpoint `/obj/<int:obj_id>` (where `obj_id` is the ID of the clicked-on object).
The webpage returned at this endpoint must satisfy the following requirements:
  * It must display at least the following information about the selected object:
    * A section with header "Summary" containing the following pieces of information in a single-row **HTML table**:
      * The object's accession number, labeled "Accession no."
      * The object's date, labeled "Date"
      * The object's place, labeled "Place"
    * A section with header "Label" containing the object's label
    * A section with header "Produced By", containing an **HTML table** with details of all agents that produced this object.
    The table must have the following column headers and content:
      * "Part", containing the part of the production carried out by each agent
      * "Name", containing the name of each agent
      * "Nationalities", containing all nationalities of each agent, each on its own line
      * "Timespan", containing the *year* of each agent's `begin_date` and the *year* of each agent's `end_date`, separated by a dash or hyphen
        * Some agents are still alive/active; in those cases the Timespan column must contain text such as "1967&ndash;"
        * An agent that has no timespan should have that fact displayed in this column in some reasonable manner
        > **Note**: The table in the "Produced By" section must be sorted in ascending order of agent name, then part, then timespan and finally by nationality.
    * A section with header "Image", containing an image of the object
      * Some objects do not have images. For those objects, this section must *not* be present in the rendered webpage
      * For objects that *do* have images, you should display the image stored at a URL with the pattern:
        ```
        https://media.collections.yale.edu/thumbnail/yuag/obj/{obj-id}
        ```
    * A section with header "Classified As", containing an **unordered list** of all classifiers for the object, sorted in ascending order of the classifier name
      > **Note**: Despite the name "unordered list" given to the HTML `<ul>` element, the list in this case must be sorted in a particular order.
      > In HTML, an unordered list is simply a list in which the items are not numbered.
    * A section with header "Information", containing an **unordered list** of all `references` to the object, with each item in the following format.
      ```html
      <li><strong>{{ reference.type }}:</strong> {{ reference.content }}</li>
      ```
      The list must be sorted first by reference type and then by content.
      > **Note**: Some references contain HTML code verbatim. That HTML must be rendered according to the included elements!

  * Its information must be well-formatted (_e.g._, the headers must be within semantic HTML `<h`*`N`*`>` header elements, and the lists must be within HTML `<ul>` elements)
  * Unlike pset 3, the secondary page must not provide a link back to the primary webpage.
    Instead, the secondary webpage must be displayed by default in a new tab or window.

    > **Note**: Read about the `target="_blank"` attribute of the `a` element

* The default styling of an HTML table is quite ugly.
  Use CSS to spruce up your tables:
   * Add padding of `5px` to all sides of every cell in each table
   * Add a `1px` wide `gray` border between rows of each table
   * When the mouse hovers over a particular row of each table, change that row's background color to `lightgray`
   * You are free to style your application in any other manner that looks good to you (but nothing else is required)
   * Place your CSS into a file named `styles.css` that is loaded by your primary and secondary webpages, but not included directly in those pages

---
## Additional Requirements for 519 Students

If you *or your partner* are enrolled in CPSC 519, your application must satisfy all of the above requirements and you must implement some of the following features.

If at least one member of your team is enrolled in CPSC 519, you are required to implement at least one of the [Additional Features](#additional-features).

Even if you and your partner are in 419 and not 519, you are more than welcome to attempt these activities.
They will not have any bearing on your grade for this assignment, but they will provide valuable experience in adding features to a webpage that may prove useful in developing your final project.

### Additional Features

If you *or your partner* are enrolled in CPSC 519, you must implement the following additional feature.

1. Large result sets are cumbersome for a user to scroll through.
   A standard technique to reduce the burden on users is **pagination**.
   A paginated results table would display only $k$ items at a time, and display a row of buttons that the user could use to go to the next page or previous page (or even a particular page)
   * You are required to implement pagination for your app, which must display no more than `10` items per page, and you must provide a button to go to the next page and a button to go to the previous page
     * Optionally, also display individual page numbers so that the user can jump to a specific page
     * Optionally, also display a "first page" and "last page" button
   * The buttons must be disabled as apprpriate is the user is on the first or last page of results
   * Each page of results must display the column headers
   * Results must still be limited to the first 1000 objects (*i.e.*, 100 pages)

    > **Hint**: You may have to modify somewhat the response from your server to make this feature feasible to implement.
    > In particular, if you return an HTML table from the server in response to a search request, that may be challenging to slice up into pages.
    > However, if you return a JSON list of objects, there are built-in JavaScript functions that will help you pick out chunks of the list.

2. The sorting algorithm required by your program is quite inflexible, and it would be nice if users could sort results however they want.
   * Make (part of) the column header cells clickable, and respond to a click in a column header by sorting the results in ascending order of the values in that column
     * Secondary and tertiary sorting should follow the same algorithm described in Pset 1
     * Sorting by the Agent list must be done by the **name** of the **first** agent in the list
     * Sorting by the Classifier list must be done by the **first** classifier in the list
   * The reordering **must be done locally**, and clicking the header may not send a request to the server
   * Provide some visual indication in the column header when its data is in sorted order. Options include adding an asterisk, changing the color, etc.
    
    > **Hint**: You may have to modify somewhat the response from your server to make this feature feasible to implement.
    > In particular, if you return an HTML table from the server in response to a search request, that will be challenging to reorder.
    > However, if you return a JSON list of objects, there are built-in JavaScript functions that will help you sort things.

---
## A Note About Performance
Despite your best efforts, your queries are likely to be quite slow to return relative to your typing speed.
That's expected, and not something to worry about as far as your grade on this assignment is concerned (to a point...queries that take many seconds to return may earn some additional scrutiny that may result in some penalties for performance or code style, especially if you've received feedback on your queries from previous assignments).
Unfortunately, with a data set as large as `lux.sqlite`&mdash;which isn't very big by today's standards!&mdash;we run into the limitations of SQLite.
We encourage you to explore the capabilities of an industrial-strength DBMS such as [PostgreSQL](https://www.postgresql.org/) or [MySQL](https://www.mysql.com/), both of which are free and open source for individual use.

In exploring these systems, in particular investigate how to use [Materialized Views](https://en.wikipedia.org/wiki/Materialized_view) to improve performance (for example, by materializing join tables rather than creating them from scratch on each query).
SQLite does, in a sense, [support materialization](https://www.sqlite.org/lang_with.html#mathint), but it is not the same as materialized views in an industrial-strength DBMS and in my testing actually make our queries *slower*.

> **Note**: There are nonstandard ways around this limitation of SQLite, including by explicitly creating tables as part of server startup.
> These "cached" tables can then be used to significantly speed up your complex join queries and won't cause data integrity issues because your app doesn't change the data!
> You may find it illustrative to experiment with this, but your time is probably better spent leveraging a more sophisticated DBMS.

---
## Object-Relational Mappers
For this assignment, you may use the [`SQLAlcehemy` ORM](https://www.sqlalchemy.org/) to aid you in your SQL queries.
You are not required to do so, but as with the additional activites for 519 students, doing so may serve as valuable experience if you choose to use SQLAlchemy in your final project or other endeavors.

Some useful materials are included in this template repository to tide you over until we cover it in class (which may be after the deadline for this assignment).

---
## Specific Endpoints

There are three endpoints to which your application must respond (assume your server is listening on port 80):
1. `http://yourserver:80/` must return the primary page
2. `http://yourserver:80/search?...` must return the results of a search using the parameters in the query string
   * Requests to the `/search` endpoint need not be standalone HTML webpages. You might find it easiest to implement the rest of the assignment if this endpoint returns results structured as JSON.
   * The parameters accepted by the `/search` endpoint must be `l` (for the label), `a` (for the agent name), `c` (for the classifiers), and `d` (for the department)
3. `http://yourserver:80/obj/<int:obj_id>` must return the secondary page populated with information about the object with the `id` provided in the query string.

Students completing the [additional 519 activities](#additional-requirements-for-519-students) may add endpoints to accomplish some of those tasks, but the exact names of those endpoints are not specified.

---
## Error Handling: Bad Server

Since you control the machine that is running both the server application and the database, there is not much we will force you to worry about for server-side errors.
There are two errors that your program must handle gracefully.
1. The server is started with a port that is not a positive integer.
If the server is started with a command such as `$ python runserver.py notaport`, it should display a meaningful error message and exit with status code `1`.
1. The database file does not exist.
If the server attempted to open the `lux.sqlite` file but the file does not exist (or otherwise cannot be opened), your program should display a meaningful error message and exit with status code `1`.

---
## Error Handling: Bad Client

It is an unfortunate truth about web applications of this kind that a user can enter anything they want in their request to your server!
For example, anyone can send a request to a URL such as `http://yourserver:80/obj/gobbeldygook`, despite there being no object with id "gobbeldygook" on which they could have clicked.
This means that we will place the same error handling requirements on your software as for Pset 3.
Specifically...

### Invalid search parameters

If the user requests a page at a URL such as `http://yourserver:80/search?foo=bar`&mdash;in which the parameters to a search request are not one of `l`, `a`, `c`, or `d`&mdash;your application must treat those parameters as not existing.
For example, in response to a request to the URL `http://yourserver:80/search?foo=bar&a=gogh`, your server must produce a webpage containing results of a search for objects with agent name containing `gogh`.

### Invalid `obj_id`

If the user requests a page at a URL such as `http://yourserver:80/obj/gobbeldygook`&mdash;in which the object ID value does not appear in the database&mdash;the server must return an appropriate error page as HTML that displays, at a minimum, text that reads "Error: no object with id gobbeldygook exists". (The "gobbeldygook" part should, of course, be replaced with the actual nonexistent id that was queried.)
This page must be returned with status code 404 (not found).

Your application must respond with this error page for *any* missing object id, including numeric and non-numeric ids.

### Missing `obj_id`

If the user requests a page at a URL such as `http://yourserver:80/obj` (that is, missing a `obj_id`), the application must return an appropriate error page as HTML that displays, at a minimum, text that reads "Error: missing object id." and status code 404 (not found).

### Aside: Error Pages

Your error page must have some required content, but it should not live at a special URL.
That is, your application should behave in a similar manner as Google when an invalid page is requested, such as `google.com/notreal`.
The page displayed should clearly indicate an error occurred, but the URL in the browser should remain `google.com/notreal`: it *should not* be some other URL, such as `google.com/404`.

### Other invalid requests

There are many other requests that the user could send that are "wrong", such as:

* `http://yourserver:notyourport/`
* `http://yourserver:80/notyourapp`
* `http://yourserver:80/search?not/well/formed/url`

The only requirement placed on your server in these cases (and similar ones) is that it does not crash when queried with such requests; that is, if the user sends a valid request immediately after an invalid one, the valid request must get the correct result.

---
## Source Code Guide

Here are the **requirements** for the source code of your solution.

* The `runserver.py` program must start a flask server for your application on the port provided as a command-line argument, listening on all IP addresses
* Your application program must communicate with a SQLite database in a file named `lux.sqlite`, organized as described above.
  * If you explore other DBMSes, you may communicate with databases named other things or that are not SQLite databases, but you must document installation instructions in your submitted `README` file so the graders know what is going on.
* Your application program must use SQL prepared statements for every database query.
(This protects the database against SQL injection attacks.)
  * If you use SQLAlchemy, that ORM automatically performs statement preparation and there is nothing special you need to do for this requirement.
* Use cookies to keep track of the application's state
* Your webpage must use Javascript to update only part of the webpage in response to the user typing in the search boxes.
* 

Here are some **recommendations** for the source code of your solution.

* Reuse code from your solution to Pset 3 in this assignment.
* Modularize your application program so that database communication code is cleanly separated from response production code.
    * Use HTML templates to keep your repsonse production code as clear as possible
    * Structure your code according to MVC design principles (the HTML templates are your Views)
* You may use external dependencies, but we advise you not to (with the obvious exception of `flask`).
  This assignment is designed such that everything can be accomplished without too much pain using only packages from the Python standard library.

---
## Submission

Replace the provided `README.md` file (which contains this assignment specification) with your own `README.md` file that conforms to the following requirements.

1. Leave the first line of the file alone (it is the assignment title).

2. Thereafter your `README.md` file must contain:
    * Your name and Yale netid and your teammate’s name and Yale netid (if you worked with a partner)
      * Also indicate here whether you and your teammate are enrolled in 419 or 519
    * A paragraph describing your contribution, and another paragraph describing your teammate’s contribution.
    Please be thorough; we are looking for two substantial paragraphs, not a sentence or two.
    * A description of whatever help (if any) you received from other people while doing the assignment.
    * A description of the sources of information that you used while doing the assignment, that are not direct help from other people.
    * An indication of how much time you spent doing the assignment, rounded to the nearest hour.
    * Your assessment of the assignment:
        * Did it help you to learn?
        * What did it help you to learn?
        * Do you have any suggestions for improvement? *Etc.*
    * (Optionally) Any information that will help us to grade your work in the most favorable light.
        * In particular, describe all known bugs and explain why any `pylint` style warnings you received are unavoidable or why you know better than `pylint` (a convincing argument might negate some `pylint` style penalties you may accrue).
        * You should also describe any installation instructions here if you use a non-SQLite DBMS, including instrcutions on how to retrieve the data

Your `README.md` file must be a plain text file.
**Do not** create your `README.md` file using Microsoft Word or any other word processor, although it may be formatted using [markdown](https://www.markdownguide.org/), like this provided `README.md` file.

Package your assignment files by [creating a release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release) on GitHub in your assignment repository. There must be at least two files with the following (exact) names in that repository when you submit it:
* `README.md`
* `runserver.py`

Ensure that any additional files needed by your program (such as other Python modules, HTML templates, or CSS files) are in the repository snapshot (_i.e._, commit) captured by the release.

> **Note**: If you have installed external packages, you must also include a file named `requirements.txt` containing the dependencies of your project.
> It can be created from your virtual environment by running the following command:
> ```
> $ pip freeze -r requirements.txt
> ```
> 
> Failure to include a `requirements.txt` file if you use third-party packages will result in an automatic 5% penalty and a request that you submit an appropriate `requirements.txt` file to the graders.

Submit your solution to Canvas (in the assignment named "Pset 4: Web Version 2") as [a link to that release](https://docs.github.com/en/repositories/releasing-projects-on-github/linking-to-releases).

As noted above in the [Rules](#rules) section, it must be the case that either you submit all of your team’s files or your teammate submits all of your team’s files.
(It must not be the case that you submit some of your team’s files and your teammate submits some of your team’s files.)
You and your team may submit multiple times; we will grade the latest files that you submit before the deadline unless a particular version is requested as the canonical version.

**Please follow the directions on what to submit and how.**
It will be a big help to us if you get the filenames right and submit exactly what’s asked for.
Thanks.

### Late Submissions

The deadline for this assignment is **11:59 PM NHT (New Haven Time) on Friday Nov 17, 2023**.
There is a strict 30 minute grace period beyond the deadline, to be used in case of technical or administrative difficulties, and not for putting final touches on your solution.

Late submissions will receive a 5% deduction for every 12-hour period (or part thereof) after the deadline.
After 72 hours, the Canvas assignment will close and submissions after that time will not receive any credit.

Except for the 72-hour cutoff, late penalties will be assessed based on the timestamp of the release, not the submission time.
Submissions after 72 hours are not accepted regardless of the timestamp on the release.

---

## Grading

Your grade will be based upon:
* **Correctness**, that is, the correctness of your programs as specified by this document.
* **Style**, that is, the quality of your program style.
This includes not only style as qualitatively assessed by the graders (including modularity, cleanliness, and performance) but also style as reported by the `pylint` tool, using the default settings, and when executed via the command `python -m pylint **/*.py`.

Ten percent of your grade will be based upon the quality of your program style as reported by `pylint`.
Your grader will start with the 10-point score reported by pylint.
Your *pylint style grade* is your pylint score rounded to the nearest integer (minimum 0).
For example, if your pylint score is 9.8, then your *pylint style grade* will be 10; if your pylint score is 7.4, then your *pylint style grade* will be 7.

If your code fails the tests on some particular functionality, your grader will inspect your code manually to try to assign partial credit for that functionality.
Partial credit will be given only if there is an *obvious* "quick fix" (*e.g.*, you have accidentally changed the name of the database file and your solution points to a file with a name that does not match the grader's copy of the database); if no such quick fix exists then no partial credit for that feature will be given.

---

Original copyright &copy;2021 by Robert M. Dondero, Jr.

Modified &copy;2023 by Alan Weide
