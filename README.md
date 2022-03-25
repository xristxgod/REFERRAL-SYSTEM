# Referral system

###### P.S.This mini project was created by me and me personally for general use. I'm still new to programming this project was created after 1 year of commercial work.

####This project is an implemented referral system consisting of 4 levels (you can increase it yourself, my code allows). Written completely asynchronous.

###The levels in the database look like this:
```json
{
  // The user's referral system.
  "user_id": 4,
  "ref_users": {
    // The first level. Users were called directly.
    "lvl_1": [
      {
        // User id who was called
        "user_id": 15,
        // The time of its registration
        "time": 1648069200
      },
      ...
    ],
    // The second level. The user who was called by "user_id": 15
    "lvl_2": [
      {
        "user_id": 19,
        "time": 1648089500
      },
      ...
    ],
    // The third level. The user who was called by "user_id": 19
    "lvl_3": [
      {
        "user_id": 26,
        "time": 1748089500
      },
      ...
    ],
    // The fourth level. The user who was called by "user_id": 26
    "lvl_4": [
      {
        "user_id": 45,
        "time": 1848089500
      },
      ...
    ]
  }
}
```