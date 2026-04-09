#!/bin/bash

# Fetches data from 5 repos with more than 10000 stars, (page 20 in this case). New data fetched on server start
curl -L   -H "Accept: application/vnd.github+json"   -H "Authorization: Bearer YOUR_TOKEN_HERE"   -H "X-GitHub-Api-Version: 2022-11-28" "https://api.github.com/search/repositories?q=stars:>10000&per_page=5&page=20" | jq -r '.items[] | {forks_count, size, watchers_count, open_issues_count, stargazers_count} | [.forks_count, .size, .watchers_count, .open_issues_count, .stargazers_count] | @csv' > repos.csv