# ML System Design One-Page Revision

## The 8-Step ML System Design Framework
1. **Requirements & Framing:** What is the business goal? Is this classification, regression, or recommendation? What are the latency requirements (batch vs real-time)?
2. **Data Pipeline:** Where does the data come from? How is it ingested? Deal with missing values, class imbalance, and data leakage.
3. **Features:** Feature engineering. Categorical encoding (One-hot vs Embedding). Normalization. Feature Store (offline for training, online for fast inference retrieval).
4. **Model Selection:** Start simple (Logistic Regression / XGBoost). Only move to Deep Learning if unstructured data (text/images) or massive scale justifies it.
5. **Evaluation:** Offline metrics (F1, AUC-ROC) vs Online metrics (Click-through rate, Revenue).
6. **Deployment & Serving:** 
   - *Batch Prediction:* Run nightly, store in DB. (High throughput, high latency).
   - *Online Prediction:* Run behind API. (Low latency, requires fast feature store).
7. **Monitoring & Drift:** 
   - *Data Drift:* Input distribution changes over time.
   - *Concept Drift:* The relationship between input and output changes (e.g., inflation changes housing prices).
8. **Retraining Pipeline:** Triggered based on time (weekly) or performance drop.

## Latency vs Throughput
- **Latency:** Time taken to process ONE request. (Important for real-time APIs).
- **Throughput:** Number of requests processed per second. (Important for Batch jobs).
- *Tradeoff:* Batching inputs before passing to GPU heavily increases throughput but increases latency for the first request in the batch.

## Recommender Systems (Classic Architecture)
1. **Candidate Generation (Retrieval):** Fast, coarse model. Filters 10 million items down to 1,000. (e.g., Matrix Factorization, Two-Tower Embeddings with FAISS).
2. **Scoring (Reranking):** Heavy, precise model. Scores the 1,000 items and ranks them. (e.g., Deep Neural Networks using user context, item features, cross-features).

## Interview Traps
- *Proposing a massive deep learning model first.* Always establish a simple baseline (XGBoost) before proposing DL. Systems interviewers care about end-to-end engineering, not just the model architecture.
- *Ignoring Data Leakage.* Using future information during training that won't be available at inference time (e.g., using "time spent on page" to predict "will user click ad").
