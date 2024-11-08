 .. _posts:

Posts
======================================================================

You can find the posts app documentation here.

For not letting the users to abuse the system, we have generally a throttling system in place.
This could be changed by our needs, but for now, we have a limit of 50 requests per day per user.

For calculating the rating of a post, we have a simple algorithm in place.
We have a materialized view in the database that calculates the rating of a post.
And how we calculated that we remove the top 10% and bottom 10% of the ratings and calculate the average of the rest,
so that hyped ratings or bad ratings do not affect the rating of a post.

Also, we have a task that refreshes the materialized view every 1 minute concurrently.
The task is called `refresh_materialized_view` and it is in the `posts.tasks` module.
For 1 million records, it takes around 700 milliseconds to refresh the materialized view, we can say it's actually performing very well,
since we don't actually care that users see the ratings with a few minutes delay.

On the other hand, we have a command called `detect_fraudulent_ratings` that finds suspicious activities and ratings.
We can run this command whenever we need it to get valuable data and change our policies and system.

It's also worth mentioning that the posts list view uses pagination and also caching the result for 1 minute to respond quickly.

Commands
----------------------------------------------------------------------
.. automodule:: bitpin.posts.management.commands.create_random_posts
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: bitpin.posts.management.commands.create_random_ratings
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: bitpin.posts.management.commands.detect_fraudulent_ratings
   :members:
   :undoc-members:
   :show-inheritance:

Tasks
----------------------------------------------------------------------
.. automodule:: bitpin.posts.tasks
   :members:

Serializers
----------------------------------------------------------------------
.. automodule:: bitpin.posts.api.serializers
   :members:
   :noindex:

Views
----------------------------------------------------------------------
.. automodule:: bitpin.posts.api.views
   :members:
   :noindex:

Models
----------------------------------------------------------------------
.. automodule:: bitpin.posts.models
   :members:
   :noindex:
