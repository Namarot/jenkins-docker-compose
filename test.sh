#!/bin/bash

# Check if a port argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <port>"
    exit 1
fi

port="$1"

# Set the total number of requests
total_requests=1000

# Initialize counters for each status code
count_200=0
count_400=0
count_404=0
count_500=0

for ((i=1; i<=total_requests; i++)); do
    # Send the request and capture the response headers
    response_headers=$(curl --include "http://localhost:$port" 2>/dev/null)

    # Extract the HTTP status code from the response headers
    http_status=$(echo "$response_headers" | grep -oP 'HTTP/\d\.\d \K\d{3}')

    # Increment the corresponding counter based on the status code
    case $http_status in
        200) ((count_200++));;
        400) ((count_400++));;
        404) ((count_404++));;
        500) ((count_500++));;
    esac
done

# Calculate the percentage of each status code
percentage_200=$((count_200 * 100 / total_requests))
percentage_400=$((count_400 * 100 / total_requests))
percentage_404=$((count_404 * 100 / total_requests))
percentage_500=$((count_500 * 100 / total_requests))

# Print the percentages
echo "Percentage of 200 OK: $percentage_200%"
echo "Percentage of 400 Bad Request: $percentage_400%"
echo "Percentage of 404 Not Found: $percentage_404%"
echo "Percentage of 500 Internal Server Error: $percentage_500%"
