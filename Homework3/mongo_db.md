# Mongo DB Assignment

1. Connect via Mongo Compass and run show DBs:

```javascript
show dbs
```

2. Switch to Database:

```javascript
> use sample_mflix

< sample_airbnb        52.60 MiB
sample_analytics      9.60 MiB
sample_geospatial     1.26 MiB
sample_guides        40.00 KiB
sample_mflix        110.80 MiB
sample_restaurants    6.60 MiB
sample_supplies       1.05 MiB
sample_training      48.85 MiB
sample_weatherdata    3.85 MiB
admin               368.00 KiB
local                 6.97 GiB
```

3. Show collections in current Database:

```javascript
> show collections

< switched to db sample_mflix
```

4. Figure out what the schema of the collection is.

```javascript
> db.movies.find().limit(1)

< {
  _id: ObjectId("573a1390f29313caabcd42e8"),
  plot: 'A group of bandits stage a brazen train hold-up, only to find a determined posse hot on their heels.',
  genres: [
    'Short',
    'Western'
  ],
  runtime: 11,
  cast: [
    'A.C. Abadie',
    "Gilbert M. 'Broncho Billy' Anderson",
    'George Barnes',
    'Justus D. Barnes'
  ],
  poster: 'https://m.media-amazon.com/images/M/MV5BMTU3NjE5NzYtYTYyNS00MDVmLWIwYjgtMmYwYWIxZDYyNzU2XkEyXkFqcGdeQXVyNzQzNzQxNzI@._V1_SY1000_SX677_AL_.jpg',
  title: 'The Great Train Robbery',
  fullplot: "Among the earliest existing films in American cinema - notable as the first film that presented a narrative story to tell - it depicts a group of cowboy outlaws who hold up a train and rob the passengers. They are then pursued by a Sheriff's posse. Several scenes have color included - all hand tinted.",
  languages: [
    'English'
  ],
  released: 1903-12-01T00:00:00.000Z,
  directors: [
    'Edwin S. Porter'
  ],
  rated: 'TV-G',
  awards: {
    wins: 1,
    nominations: 0,
    text: '1 win.'
  },
  lastupdated: '2015-08-13 00:27:59.177000000',
  year: 1903,
  imdb: {
    rating: 7.4,
    votes: 9847,
    id: 439
  },
  countries: [
    'USA'
  ],
  type: 'movie',
  tomatoes: {
    viewer: {
      rating: 3.7,
      numReviews: 2559,
      meter: 75
    },
    fresh: 6,
    critic: {
      rating: 7.6,
      numReviews: 6,
      meter: 100
    },
    rotten: 0,
    lastUpdated: 2015-08-08T19:16:10.000Z
  },
  num_mflix_comments: 0
}
```

5. Query that captures the following requirements:
   1. Movies with `year` between 1975 and 1980.
   2. Display only 3 columns `title`, `year` and `runtime`.
   3. Order by `runtime` (asc or dsc).

```javascript
> db.movies.aggregate([
  {
    $match: {
      year: { $gt: 1975, $lt: 1980 }
    }
  },
  {
    $sort: { runtime: 1 }
  },
  {
    $limit: 5
  },
  {
    $project: {
      title: 1,
      year: 1,
      runtime: 1,
      _id: 0
    }
  },
  {
    $project: {
      title: "$title",
      year: "$year",
      runtime: "$runtime"
    }
  }
])

> {
  title: 'The Secret Life of Plants',
  year: 1978
}
{
  title: 'Un uomo in ginocchio',
  year: 1979
}
{
  title: 'The Burgos Trial',
  year: 1979
}
{
  title: 'Sentimentalnyy roman',
  year: 1977
}
{
  title: 'Powers of Ten',
  year: 1977,
  runtime: 9
}
```

Note that some movies don't have a `runtime`, which is why they're not being displayed.

There's a script called `retrieve_movies.js` that can be run using `node`. Ensure that you create a file called `db_creds.json` before you run the file. The output is given in `movies_query_results.json`, this includes all the movies without any limit.

5. Write an aggregation aggregating year which calculates sum of all runtime for movies where year is between 1975 and 1980 including.
   
```bash
> db.movies.aggregate([
  {
    $match: {
      year: { $gte: 1975, $lte: 1980 }
    }
  },
  {
    $group: {
      _id: "$year",
      sumRuntime: { $sum: "$runtime" }
    }
  },
  {
    $project: {
      _id: 0,
      year: "$_id",
      sumRuntime: "$sumRuntime"
    }
  }
]).sort({ year: 1 })

< {
  year: 1975,
  sumRuntime: 12283
}
{
  year: 1976,
  sumRuntime: 12723
}
{
  year: 1977,
  sumRuntime: 14054
}
{
  year: 1978,
  sumRuntime: 15356
}
{
  year: 1979,
  sumRuntime: 14196
}
{
  year: 1980,
  sumRuntime: 18422
}
```
