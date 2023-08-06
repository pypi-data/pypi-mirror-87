'''
Cache Wrapper Method to store temporary results.
'''
import os
import json
import time
import tempfile
from functools import wraps
from howcani.utility import run_on_thread

def cache_results(get_result_func, max_size=5, name='default'):

    path = os.path.join(tempfile.gettempdir(), "howcani-{}.json".format(name))

    def clear_cache(cache):
        # Clear Cache if full
        if len(cache.keys()) >= max_size:
            query_to_delete = ""
            least_recently_used_timestamp = -1
            for i, query in enumerate(cache):
                if least_recently_used_timestamp == -1:
                    query_to_delete = query
                    least_recently_used_timestamp = cache[query]['timestamp']
                    continue
                if least_recently_used_timestamp > cache[query]['timestamp']:
                    least_recently_used_timestamp = cache[query]['timestamp']
                    query_to_delete = query
            del cache[query_to_delete]
        return cache

    def store_cache_result(cache, query, results):
        cache = clear_cache(cache)

        cache[query] = {
            "result": results,
            "timestamp": time.time()
        }

        json.dump(cache, open(path, 'w'))

    @wraps(get_result_func)
    def wrapper(*args, **kwargs): 
        # Check if cache has results
        try:
            fp = open(path, 'r')
            cache = json.load(fp)
            fp.close()
        except Exception:
            cache = {}

        query = kwargs['query']

        # Cache Hit
        if query in cache:
            # Update Cache Timestamp for Query
            results = cache[query]['result']
            
            run_on_thread(store_cache_result, cache, query, results)

            return results

        # Cache Miss
        results = get_result_func(*args, **kwargs)
        
        run_on_thread(store_cache_result, cache, query, results)
        
        return results
  
    return wrapper 
  



