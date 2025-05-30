# large_scale_final
Large Scale Computations Final Project - Sowder
# large_scale_final

Large Scale Computations Final Project - Sowder

# Genius Lyrics Emotion Analysis

This part of the project explores whether lyrics can be used to reliably predict the emotional content of songs using serverless web scraping (AWS Lambda), distributed processing (Dask), and NLP techniques (BERTa transformer). The pipeline collects lyrics from Genius.com, classifies them with a BERT-based emotion model, and compares the results with tag-based emotion labels.

## Project Structure

```
/genius
├── genius_processing.ipynb
├── genius_lambda_package/
│   ├── lambda_function.py
│   └── ... (dependency packages)
├── genius_lambda.zip
├── final_joined_table.csv
├── genius_local.ipynb
├── lyrics.db
```

### [`genius_processing.ipynb`](https://github.com/mdsowder/large_scale_final/blob/main/genius/genius_processing.ipynb)

This notebook contains the core pipeline for the emotion analysis:

- **[Install requests, set up S3 and bucket](https://github.com/mdsowder/large_scale_final/blob/main/genius/genius_processing.ipynb#Install-requests-and-setup)**
- **[Set up Lambda function and connection](https://github.com/mdsowder/large_scale_final/blob/main/genius/genius_processing.ipynb#Lambda-Setup)**
- **[Set up Lambda environment variables](https://github.com/mdsowder/large_scale_final/blob/main/genius/genius_processing.ipynb#Environment-Variables)**
- **[Use Dask to clean and match data](https://github.com/mdsowder/large_scale_final/blob/main/genius/genius_processing.ipynb#Lyrics-Cleaning)**
- **[Analysis](https://github.com/mdsowder/large_scale_final/blob/main/genius/genius_processing.ipynb#Emotion-Classification-Analysis)**

### `genius_lambda_package/`

This directory contains the Lambda deployment package, including:

- `lambda_function.py`: Scrapes Genius lyrics URLs sent via SQS and stores the result in S3 and DynamoDB
- Required libraries packaged for deployment

### `genius_lambda.zip`

A zipped deployment-ready version of the Lambda function and packages. This was uploaded to AWS Lambda.

### `final_joined_table.csv`

This file contains metadata for each song, including the original emotion labels (`tag_emotion`) derived from BERTa classification of FM song tags. This serves as the ground truth for evaluation.

### `genius_local.ipynb`

A local-only version of the scraping and classification pipeline. This notebook scraped Genius lyrics and ran the full classification pipeline using pandas.

**Note:** Scraping and processing 2,000+ songs locally took over **2 hours**, compared to under **10 minutes** using Lambda + Dask.

### `lyrics.db`

A SQLite database storing the scraped lyrics from the local pipeline (`genius_local.ipynb`). Used for intermediate analysis and validation.

---

## Benefits of Serverless + Distributed Design

**AWS Lambda:**

- Parallel scraping of song lyrics
- Each Lambda function executes in under 1s per song
- Dynamically scalable for thousands of requests

**Dask:**

- Parallel processing of large lyric datasets
- Faster cleaning, classification, and analysis compared to pandas
- Integration with BERTa model using `map_partitions`

Overall, **Lambda + Dask reduced end-to-end runtime by over 90%** compared to a local-only solution.

---

## Emotion Analysis Results

We classified lyrics using a fine-tuned BERTa model (`bhadresh-savani/bert-base-go-emotion`) and compared predictions against tag-based `tag_emotion` labels.

### Key Findings:

- **Accuracy was \~18%**, with highest recall for **"anger"** (0.50) and moderate recall for **"joy"** (0.32).
- Emotions like **"disgust"**, **"surprise"**, and **"fear"** were poorly predicted from lyrics.
- Lyrics-based predictions tend to **overpredict "anger"** and **underpredict "disgust"/"surprise"**.
- **Confusion matrix** showed most confusion between similar affective categories, suggesting emotion boundaries are fuzzy in lyrics.

---

## Interpretation

### Can models predict song emotions from lyrics?

- **Partially.** Lyrics contain emotion signals, especially for high-arousal emotions like _anger_ and _joy_, but subtle or low-arousal emotions are harder to detect reliably.

### Are lyrics or tags better predictors of emotion?

- **Tags (from Spotify metadata) likely reflect listener perception, genre, and mood.**
- **Lyrics reflect narrative or affective content expressed by the artist.**

These two sources capture different facets of emotion:

- **Tags = Audience-level emotion framing**
- **Lyrics = Textual emotion cues**

Combining both may yield the most robust classification.

---

---
