from wordle_parrallel import *

set_context("*****",
	    "a",
	    ["raise"])
set_words()

def main():
	if __name__ == '__main__':
    		print("hello")
    		from multiprocessing import Pool, cpu_count
    		from time import time

	    	with Pool(cpu_count()) as pool:
        		results = []
        		set_context("*****", "a", ["raise"])
        		set_words()
        		start = time()
        		temp = get_set_of_words()
        		result_objects = [pool.apply_async(compute_score, args=(word,)) for word in temp]
        		results = [r.get() for r in result_objects]
        		results.sort()
        		pool.close()
        		pool.join()
        		print(time() - start)
        		print(results[:10])

main()
