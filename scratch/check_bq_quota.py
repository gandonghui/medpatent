from google.cloud import bigquery
import os

def check_quota():
    project_id = 'my-project-gemini-test-485607'
    client = bigquery.Client(project=project_id)
    
    ids = [
        'US-2024350121-A1', 'US-2022414914-A1', 'US-12205315-B2', 
        'US-2020022769-A1', 'US-11304771-B2', 'US-2017181798-A1', 
        'US-10334227-B2', 'US-2017181808-A1', 'US-2017180704-A1', 
        'US-10555788-B2'
    ]
    
    id_list = ", ".join([f"'{i}'" for i in ids])
    
    # Selecting only necessary large columns
    sql = f"""
        SELECT 
            publication_number, 
            description_localized[SAFE_OFFSET(0)].text as description
        FROM 
            `patents-public-data.patents.publications`
        WHERE 
            publication_number IN ({id_list})
    """
    
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
    query_job = client.query(sql, job_config=job_config)
    
    total_gb = query_job.total_bytes_processed / (1024**3)
    print(f"Estimated scan for unified query: {total_gb:.2f} GB")
    
    # Individual scans (what we did before)
    print(f"Total scan if done individually (10 separate queries): {total_gb * 10:.2f} GB")

if __name__ == "__main__":
    check_quota()
