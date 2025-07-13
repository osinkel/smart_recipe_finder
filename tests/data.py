data_to_add = [
    # valid
    (
        {
            "title": "fried eggs",
            "ingredients": [
                {
                "name": "eggs"
                },
                {
                "name": "salt"
                },
                {
                "name": "oil"
                }
            ],
            "preparation_instructions": "take 5 eggs",
            "cooking_time": 7,
            "difficulty": "easy",
            "cuisine": {
                "name": "international"
            }, 
        },
        200
    ),


    # empty ingredients
    (
        {
            "title": "",
            "ingredients": [],
            "preparation_instructions": "",
            "cooking_time": 0,
            "difficulty": "easy",
            "cuisine": {
                "name": "international"
            }, 
        },
        200
    ),

    # all field empty
    (
        {
            "title": "test",
            "ingredients": [],
            "preparation_instructions": "",
            "cooking_time": 0,
            "difficulty": "",
            "cuisine": {},
        },
        422
    ),

    # empty cuisine
    (
        {
            "title": "test",
            "ingredients": [
                {
                "name": "cabbage"
                }
            ],
            "preparation_instructions": "",
            "cooking_time": 0,
            "difficulty": "hard",
            "cuisine": {},
        },
        422
    ),
    
]

data_to_get = {
    "title": "fried eggs",
    "ingredients": [
        {
        "name": "eggs"
        },
        {
        "name": "salt"
        },
        {
        "name": "oil"
        }
    ],
    "preparation_instructions": "take 5 eggs",
    "cooking_time": 7,
    "difficulty": "easy",
    "cuisine": {
        "name": "international"
    }, 
}

data_to_update = [
    (
        {
            "title": "fried eggs",
            "ingredients": [
                {
                "name": "eggs"
                },
                {
                "name": "salt"
                },
                {
                "name": "oil"
                }
            ],
            "preparation_instructions": "take 5 eggs",
            "cooking_time": 7,
            "difficulty": "easy",
            "cuisine": {
                "name": "international"
            }, 
        },
        {
            "title": "boiled eggs",
            "ingredients": [
                {
                "name": "eggs"
                },
                {
                "name": "salt"
                },
                {
                "name": "water"
                }
            ],
            "preparation_instructions": "take 5 eggs",
            "cooking_time": 8,
            "difficulty": "easy",
            "cuisine": {
                "name": "international"
            }, 
        },
        200
    ),
    (
        {
            "title": "fried eggs",
            "ingredients": [
                {
                "name": "eggs"
                },
                {
                "name": "salt"
                },
                {
                "name": "oil"
                }
            ],
            "preparation_instructions": "take 5 eggs",
            "cooking_time": 7,
            "difficulty": "easy",
            "cuisine": {
                "name": "international"
            }, 
        },
        {
            "title": "test",
            "ingredients": [],
            "preparation_instructions": "",
            "cooking_time": 0,
            "difficulty": "",
            "cuisine": {},
        },
        422
    )
]

data_to_filter = [
    (
        [
            {
                "title": "boiled eggs",
                "ingredients": [
                    {
                    "name": "eggs"
                    },
                    {
                    "name": "salt"
                    },
                    {
                    "name": "water"
                    }
                ],
                "preparation_instructions": "take 5 eggs",
                "cooking_time": 7,
                "difficulty": "easy",
                "cuisine": {
                    "name": "international"
                }, 
            },
            {
                "title": "fried eggs",
                "ingredients": [
                    {
                    "name": "eggs"
                    },
                    {
                    "name": "salt"
                    },
                    {
                    "name": "oil"
                    }
                ],
                "preparation_instructions": "take 5 eggs",
                "cooking_time": 7,
                "difficulty": "easy",
                "cuisine": {
                    "name": "international"
                }, 
            }
        ],
        [
          {'include': ['eggs', 'water'], 'exclude': ['oil'], 'expected_status_code': 200},  # with all filters
          {'include': ['eggs'], 'exclude': [], 'expected_status_code': 200},  # only include
          {'include': [], 'exclude': ['oil'], 'expected_status_code': 200}, # only exclude
        ]
    )
]

data_to_search_similarity = [
    (
        [
            {
                "title": "boiled eggs",
                "ingredients": [
                    {
                    "name": "eggs"
                    },
                    {
                    "name": "salt"
                    },
                    {
                    "name": "water"
                    }
                ],
                "preparation_instructions": "take 5 eggs",
                "cooking_time": 8,
                "difficulty": "easy",
                "cuisine": {
                    "name": "international"
                }, 
            },
            {
                "title": "fried eggs",
                "ingredients": [
                    {
                    "name": "eggs"
                    },
                    {
                    "name": "salt"
                    },
                    {
                    "name": "oil"
                    }
                ],
                "preparation_instructions": "take 5 eggs",
                "cooking_time": 5,
                "difficulty": "easy",
                "cuisine": {
                    "name": "international"
                }, 
            }
        ],
        [
          {'search_text': "recipe with oil", 'limit': 2, 'expected_best_recipe': 'fried eggs',  'expected_status_code': 200},  # valid
          {'search_text': "recipe on 5 minunes", 'limit': 0, 'expected_best_recipe': '', 'expected_status_code': 422}, # bad limit
        ]
    )
]