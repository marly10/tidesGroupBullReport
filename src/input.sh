#!/bin/bash

read -p "Enter a word: " user_value

user_value_word="this_is_a_random_string_to_test_something"

if [[ $user_value_word =~ $user_value ]]; then
    echo "You Found The Winner"
else
    echo "You DID NOT Found The Winner"
fi

read -p "Shall I continue anyway? (y/N) " proceed
if [ $(echo "$proceed" | grep -ic ^y) = 0 ]; then
    echo "We will exit"
    exit 0
else
    echo "We will continue"
fi

#printf 'string\ny\nno\nmaybe\n' | ./input.sh
# https://docs.github.com/en/actions/using-jobs/defining-outputs-for-jobs