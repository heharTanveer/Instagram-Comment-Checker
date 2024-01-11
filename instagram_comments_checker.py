import requests
import openai
from instascrape import Post
import csv

def get_comments(url):
    post_comments = Post(url)
    post_comments.scrape()
    return post_comments.get_recent_comments()

def rate_inappropriateness(comment):
    openai.api_key = '///'
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=comment,
        max_tokens=50  # Adjust as needed
    )

    # Analyze the generated response for inappropriate content
    generated_text = response['choices'][0]['text']
    
    keywords = ['explicit', 'offensive', 'inappropriate']
    rating = sum(keyword in generated_text.lower() for keyword in keywords)

    # Normalize the rating to a scale of 1 to 5
    normalized_rating = min(5, max(1, rating))

    return normalized_rating

def save_comments_and_ratings(url, output_folder):
    comments = get_comments(url)

    # Create CSV file for comments
    comments_csv_filename = f'{output_folder}/comments_data.csv'
    with open(comments_csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['username', 'text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for comment in comments:
            writer.writerow({'username': comment['username'], 'text': comment['text']})

    # Create CSV file for ratings
    ratings_csv_filename = f'{output_folder}/ratings_data.csv'
    with open(ratings_csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['username', 'rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for comment in comments:
            rating = rate_inappropriateness(comment['text'])
            writer.writerow({'username': comment['username'], 'rating': rating})

def main():
    openai.api_key = 'your_openai_api_key'
    url = "https://www.instagram.com/p/CLnSbP7hOjh/"
    output_folder = 'output_folder'

    save_comments_and_ratings(url, output_folder)

if __name__ == "__main__":
    main()
