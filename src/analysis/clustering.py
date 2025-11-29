from sklearn.cluster import KMeans
import numpy as np

def cluster_embeddings(embedded_data: list, num_clusters: int = 5):
    """
    Clusters embedded news chunks using KMeans.
    
    embedded_data: list of { "text": str, "embedding": list, "metadata": dict }
    
    Returns:
    {
        cluster_id: {
            "texts": [...],
            "metadatas": [...],
            "centroid": [...],
        }
    }
    """
    if not embedded_data:
        return {}

   
    embeddings = np.array([item["embedding"] for item in embedded_data])

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)

    clusters = {}

    for idx, label in enumerate(labels):
        if label not in clusters:
            clusters[label] = {
                "texts": [],
                "metadatas": [],
                "centroid": kmeans.cluster_centers_[label].tolist()
            }

        clusters[label]["texts"].append(embedded_data[idx]["text"])
        clusters[label]["metadatas"].append(embedded_data[idx]["metadata"])

    return clusters
